#!/usr/bin/env python3
"""
多仓地址管理 & 自动更新主控脚本

工作流程:
  1. 从 __sources/多仓地址簿.md 读取多仓 URL 列表
  2. 尝试用 curl 拉取每个多仓的 JSON
  3. 与 config.json 去重，输出 __temp/待测试_YYYYMMDD.json
  4. 如果 config.json 有更新，自动派生 zyfun_config.json

用法:
  python auto_update.py              # 拉取 + 对比 + 输出测试文件
  python auto_update.py --push      # 上述 + 提交 config.json 变更 + 推送
  python auto_update.py --force     # 强制重新拉取（跳过缓存）
  python auto_update.py --testonly  # 仅对比已有 __temp/ 下的文件
"""
import json, os, sys, re, uuid, datetime, subprocess
import shutil

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")
SOURCES_MD  = os.path.join(SCRIPT_DIR, "__sources", "多仓地址簿.md")
TEMP_DIR    = os.path.join(SCRIPT_DIR, "__temp")
TOOLS_DIR   = os.path.join(SCRIPT_DIR, "__tools")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(os.path.join(SCRIPT_DIR, "__sources"), exist_ok=True)


# ── 1. 读取多仓地址簿 ────────────────────────────────────────────
def load_source_registry():
    if not os.path.exists(SOURCES_MD):
        print(f"[WARN] 地址簿不存在: {SOURCES_MD}")
        print(f"       已自动创建空地址簿，请编辑添加多仓地址")
        with open(SOURCES_MD, "w", encoding="utf-8") as f:
            f.write("# 多仓地址簿\n\n> 记录所有多仓来源地址，auto_update.py 会从这里读取并拉取。\n\n"
                    "## 活跃多仓\n\n"
                    "| 名称 | 地址 | 状态 | 来源 | 备注 |\n"
                    "|:---|:---|:---:|:---|:---|\n")
        return []
    with open(SOURCES_MD, encoding="utf-8") as f:
        content = f.read()
    sources = []
    for line in content.split("\n"):
        line = line.strip()
        if not line.startswith("|") or "名称" in line or "---" in line or not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3 and parts[1]:
            sources.append({
                "name":   parts[1],
                "url":    parts[2],
                "status": parts[3] if len(parts) > 3 else "?",
                "note":   parts[4] if len(parts) > 4 else "",
            })
    return sources


# ── 2. 拉取单个多仓 ────────────────────────────────────────────
def fetch_url(url, name):
    """用 curl 拉取 URL，返回 (原始文本, 错误信息)"""
    if not url or url.startswith("#"):
        return None, "空地址"
    cmd = [
        "curl", "-sL", "-A", UA,
        "--tlsv1.2", "--tls-max", "1.2",
        "-m", "25",
        url
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", timeout=30)
        if r.returncode != 0 or not r.stdout:
            return None, f"exit={r.returncode}"
        return r.stdout, None
    except Exception as e:
        return None, str(e)


# ── 3. 解析 JSON ───────────────────────────────────────────────
def try_parse_json(text):
    if not text:
        return None
    text = text.strip()
    # 去 BOM / markdown
    text = re.sub(r"^\ufeff", "", text)
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)
    # 直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # 找最大的 JSON 对象/数组
    best = None
    for pat in [r"\{[\s\S]*?\}", r"\[[\s\S]*?\]"]:
        for m in re.finditer(pat, text):
            try:
                obj = json.loads(m.group())
                if len(m.group()) > (len(best) if best else 0):
                    best = m.group()
            except json.JSONDecodeError:
                continue
    if best:
        return json.loads(best)
    return None


# ── 4. 提取站点 ────────────────────────────────────────────────
def extract_sites(data, source_name):
    sites = []
    raw = []
    if isinstance(data, dict):
        for k in ("sites", "urls", "rules", "channels", "data", "list"):
            if k in data and isinstance(data[k], list):
                raw.extend(data[k])
        if not raw:
            def walk(obj):
                found = []
                if isinstance(obj, dict):
                    for v in obj.values():
                        found.extend(walk(v))
                    if "sites" in obj and isinstance(obj["sites"], list):
                        found.extend(obj["sites"])
                    if "urls" in obj and isinstance(obj["urls"], list):
                        found.extend(obj["urls"])
                elif isinstance(obj, list):
                    for i in obj:
                        found.extend(walk(i))
                return found
            raw = walk(data)
    elif isinstance(data, list):
        raw = data
    for s in raw:
        if not isinstance(s, dict):
            continue
        name_v = s.get("name") or s.get("n") or s.get("title") or ""
        api_v  = s.get("api")  or s.get("url") or s.get("i")   or ""
        key_v  = s.get("key")  or s.get("id")  or ""
        srh_v  = s.get("search", 1)
        ext_v  = s.get("ext")   or s.get("player") or ""
        pl_v   = s.get("playUrl") or s.get("p")  or ""
        if not name_v or not api_v:
            continue
        sites.append({
            "id":         str(uuid.uuid4()),
            "key":        key_v if key_v else str(uuid.uuid4()),
            "name":       f"[{source_name}] {name_v.strip()}",
            "api":        api_v.strip(),
            "playUrl":    pl_v,
            "search":     srh_v,
            "ext":        ext_v,
            "group":      source_name,
            "isActive":   True,
            "type":       1,
            "categories": "",
            "createdAt":  1780033646806,
            "updatedAt":  1780033646806,
        })
    return sites


# ── 5. 对比 config.json，输出差异 ─────────────────────────────
def diff_with_config(new_sites, config_sites):
    existing_apis = {s["api"].strip().rstrip("/") for s in config_sites}
    to_add = []
    dup    = []
    for s in new_sites:
        key = s["api"].strip().rstrip("/")
        if key in existing_apis:
            dup.append(s)
        else:
            to_add.append(s)
    return to_add, dup


# ── 6. 派生 zyfun_config.json ──────────────────────────────────
def build_zyfun():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        data = json.load(f)
    zyfun = {}
    zyfun["site"] = []
    for s in data["sites"]:
        item = dict(s)
        item["search"] = bool(item.get("search", 0))
        zyfun["site"].append(item)
    zyfun["analyze"] = data.get("analyze", [])
    zyfun["iptv"]    = data.get("iptv", [])
    zyfun["channel"] = data.get("channel", [])
    out = os.path.join(SCRIPT_DIR, "zyfun_config.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(zyfun, f, ensure_ascii=False, indent=2)
    return len(zyfun["site"])


# ── 主程序 ─────────────────────────────────────────────────────
def main():
    force    = "--force"   in sys.argv
    do_push  = "--push"    in sys.argv
    testonly = "--testonly" in sys.argv

    today = datetime.date.today().strftime("%Y%m%d")
    temp_file = os.path.join(TEMP_DIR, f"待测试_{today}.json")

    print("=" * 60)
    print("  TVBox 多仓自动更新工具")
    print("=" * 60)

    # 加载 config.json
    if not os.path.exists(CONFIG_PATH):
        print(f"[ERROR] config.json 不存在: {CONFIG_PATH}")
        return
    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = json.load(f)
    config_sites = config.get("sites", [])
    existing_apis = {s["api"].strip().rstrip("/") for s in config_sites}
    print(f"当前 config.json: {len(config_sites)} 个站点")

    if testonly:
        # 仅对比 __temp 下已有的文件
        import glob
        files = sorted(glob.glob(os.path.join(TEMP_DIR, "待测试_*.json")))
        if not files:
            print("[INFO] __temp 目录无测试文件")
        for fpath in files:
            with open(fpath, encoding="utf-8") as f:
                tdata = json.load(f)
            ts = tdata.get("sites", [])
            to_add, dup = diff_with_config(ts, config_sites)
            print(f"  {os.path.basename(f)}: 新增{len(to_add)} 已重复{len(dup)}")
        return

    # 读取多仓地址簿
    sources = load_source_registry()
    if not sources:
        print("[INFO] 地址簿为空或无活跃多仓，退出")
        return
    print(f"地址簿共 {len(sources)} 条")

    # 拉取
    all_new = []
    fail_list = []
    for src in sources:
        name = src["name"]
        url  = src["url"]
        if src["status"] in ("❌", "×", "已失效", "disabled"):
            print(f"  [-] {name} 已标记失效，跳过")
            continue
        print(f"\n  [{name}] {url[:60]}")
        text, err = fetch_url(url, name)
        if err:
            print(f"     [FAIL] {err}")
            fail_list.append((name, url, err))
            continue
        data = try_parse_json(text)
        if not data:
            print(f"     [WARN] 无法解析 JSON")
            fail_list.append((name, url, "无法解析JSON"))
            continue
        sites = extract_sites(data, name)
        print(f"     [OK] 提取 {len(sites)} 个站点")
        all_new.extend(sites)

    print(f"\n共拉取 {len(all_new)} 个站点（含重复）")

    # 去重（同源内）
    seen_api = set()
    deduped  = []
    for s in all_new:
        k = s["api"].strip().rstrip("/")
        if k not in seen_api:
            seen_api.add(k)
            deduped.append(s)
    print(f"同源去重后 {len(deduped)} 个")

    # 与 config.json 对比
    to_add, dup = diff_with_config(deduped, config_sites)

    if not to_add:
        print("\n[OK] 无新增站点，与 config.json 完全重复")
    else:
        print(f"\n[NEW] 新增 {len(to_add)} 个站点，待测试:")
        for s in to_add[:20]:
            print(f"     + {s['name']}: {s['api'][:55]}")
        if len(to_add) > 20:
            print(f"     ... 还有 {len(to_add)-20} 个")

    # 保存测试文件
    test_data = {"spider": "", "lives": [], "sites": to_add, "analyze": []}
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    print(f"\n已保存到: __temp/待测试_{today}.json")

    # 失败汇总
    if fail_list:
        print(f"\n[FAIL] {len(fail_list)} 个多仓拉取失败:")
        for n, u, e in fail_list:
            print(f"     - [{n}] {u[:50]}  → {e}")

    # 推送
    if do_push:
        print("\n提交 config.json 变更...")
        r = subprocess.run(["git", "-C", SCRIPT_DIR, "status", "--short"],
                          capture_output=True, text=True)
        if not r.stdout.strip():
            print("  无变更，跳过")
        else:
            subprocess.run(["git", "-C", SCRIPT_DIR, "add", "config.json", "zyfun_config.json"],
                          check=True)
            msg = f"更新影视源 {datetime.date.today()} 增{len(to_add)}站"
            r = subprocess.run(["git", "-C", SCRIPT_DIR, "commit", "-m", msg],
                              capture_output=True, text=True)
            if "nothing to commit" not in r.stderr and r.returncode == 0:
                subprocess.run(["git", "-C", SCRIPT_DIR, "push"], check=True)
                print(f"  [OK] 已推送: {msg}")
            else:
                print(f"  无变更或提交失败")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
