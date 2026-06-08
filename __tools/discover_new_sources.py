#!/usr/bin/env python3
"""
发现新多仓地址

从已知的聚合页/入口页抓取所有子仓 URL，
结果追加到 __sources/多仓地址簿.md
"""
import json, os, sys, re, subprocess, datetime

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR    = os.path.dirname(SCRIPT_DIR)
SOURCES_MD  = os.path.join(ROOT_DIR, "__sources", "多仓地址簿.md")
TEMP_DIR    = os.path.join(ROOT_DIR, "__temp")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

os.makedirs(TEMP_DIR, exist_ok=True)

# ── curl 拉取 ────────────────────────────────────────────────
def curl(url, referer=None):
    cmd = [
        "curl", "-sL", "-A", UA,
        "--tlsv1.2", "--tls-max", "1.2", "-m", "30",
    ]
    if referer:
        cmd += ["-H", f"Referer: {referer}"]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, timeout=35)
    if r.returncode != 0:
        return None
    try:
        return r.stdout.decode("utf-8", errors="replace")
    except Exception:
        return None

# ── 从多仓地址簿读取已有 URL ───────────────────────────────
def load_existing_urls():
    urls = set()
    if not os.path.exists(SOURCES_MD):
        return urls
    with open(SOURCES_MD, encoding="utf-8") as f:
        content = f.read()
    for line in content.split("\n"):
        line = line.strip()
        if not line.startswith("|") or "---" in line or "名称" in line or not line:
            continue
        parts = [p.strip().strip("`").strip() for p in line.split("|")]
        for p in parts:
            if p.startswith("http://") or p.startswith("https://"):
                urls.add(p.strip().rstrip("/"))
    return urls

# ── URL 去重标记 ────────────────────────────────────────────
def is_new_url(url, existing):
    url = url.strip().rstrip("/")
    if not url or len(url) < 10:
        return False
    skip_exts = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".css", ".js",
                 ".mp4", ".mp3", ".pdf", ".zip", ".rar"}
    skip_keywords = ["github.com/raw", "jihulab.com", "gitlab.com", "gitee.com"]
    for ext in skip_exts:
        if url.endswith(ext):
            return False
    for kw in skip_keywords:
        if kw in url.lower():
            return False
    return url not in existing

# ── 模式匹配子仓 URL ────────────────────────────────────────
def extract_urls_from_text(text, page_url):
    found = []
    if not text:
        return found
    # JSON 数组/对象内的 api/url 字段
    json_urls = re.findall(
        r'["\']?(?:api|url|json_url|apiUrl)["\']?\s*[:＝]\s*["\'](https?://[^"\']+)["\']',
        text, re.IGNORECASE
    )
    found.extend(json_urls)
    # Markdown 链接
    md_links = re.findall(r'\[.*?\]\((https?://[^)\s]+)\)', text)
    found.extend(md_links)
    # 裸 URL（周围有 tv/box/json/api 等关键词）
    for m in re.finditer(r'(?:tv|box|json|api|源|仓|接口)[^\s]*?[:＝]?\s*(https?://[^\s\'"<>]+)', text, re.IGNORECASE):
        found.append(m.group(1))
    # 简单裸 URL（只取以 /tv、/box、/json、/api 等结尾的）
    raw_urls = re.findall(r'https?://[^\s\'"`<>]+', text)
    for u in raw_urls:
        u = u.rstrip("/").rstrip("\\").rstrip(",").rstrip(";").rstrip(")")
        if any(x in u.lower() for x in ["/tv", "/box", "/json", "/api", "tvbox", "source", "box/", "api."]):
            if len(u) > 15 and not u.endswith(".js") and not u.endswith(".css"):
                found.append(u)
    return list(set(found))

# ── 主程序 ─────────────────────────────────────────────────
def main():
    today = datetime.date.today().strftime("%Y-%m-%d")
    existing = load_existing_urls()
    print(f"地址簿已有 {len(existing)} 个 URL\n")

    # 三个主要发现来源：聚玩盒子、硬核指南、clbug
    pages = [
        ("聚玩盒子",  "http://www.jhapp.com/box",  None),
        ("硬核指南",  "http://tvbox.cnhei.cn",       None),
        ("Clbug",    "https://tvbox.clbug.com/user.php", None),
    ]

    all_found = {}  # name -> url

    for page_name, page_url, referer in pages:
        print(f"\n{'='*60}")
        print(f"抓取: [{page_name}] {page_url}")
        text = curl(page_url, referer)
        if not text:
            print(f"  [FAIL] 无法获取页面")
            continue

        urls = extract_urls_from_text(text, page_url)
        print(f"  提取到 {len(urls)} 个候选 URL")

        new_count = 0
        for url in urls:
            if is_new_url(url, existing):
                # 尝试给 URL 起个名字
                slug = re.sub(r'^https?://', '', url).split("/")[0]
                name = re.sub(r'\.(com|top|xyz|cc|fun|net|cn|org|io|info|biz|vip|wiki|cc|cf|love|ren|live|art|me|cc)/.*', '', slug)
                name = name.replace("www.", "").replace("-", "").replace("_", "")
                if not name:
                    name = url[:30]
                all_found[url] = name
                existing.add(url)  # 避免同一页面重复发现
                new_count += 1
                print(f"    + [{name}] {url[:70]}")

        print(f"  新增 {new_count} 个未知 URL")

    # 也从 GitHub raw JSON 中找子仓
    print(f"\n{'='*60}")
    print("扫描 GitHub 已知仓库中的子仓引用...")
    github_manifests = [
        ("https://raw.githubusercontent.com/noimank/tvbox/main/README.md", "小马线路"),
        ("https://raw.githubusercontent.com/gaotianliuyun/gao/master/README.md", "高天流云"),
    ]
    for gh_url, src in github_manifests:
        text = curl(gh_url)
        if not text:
            continue
        urls = extract_urls_from_text(text, gh_url)
        for url in urls:
            if is_new_url(url, existing):
                slug = re.sub(r'^https?://', '', url).split("/")[0]
                name = f"{src}_子仓"
                all_found[url] = name
                existing.add(url)
                print(f"    + [{name}] {url[:70]}")

    print(f"\n{'='*60}")
    print(f"共发现 {len(all_found)} 个新多仓地址")

    if not all_found:
        print("没有发现新的多仓地址，地址簿已是最新。")
        return

    # 打印汇总
    print("\n新发现的多仓地址:")
    for url, name in sorted(all_found.items()):
        print(f"  [{name}] {url}")

    # 更新地址簿 - 追加到「活跃多仓」表格
    with open(SOURCES_MD, encoding="utf-8") as f:
        md_content = f.read()

    # 在最后更新时间后面追加
    new_rows = []
    for url, name in sorted(all_found.items()):
        new_rows.append(f"| {name} | `{url}` | 🔄 | 自动发现 | ? | {today} 自动发现 |")

    new_section = "\n\n## 自动发现新多仓（" + today + "）\n\n" + \
                  "| 名称 | 地址 | 状态 | 来源 | 站点数 | 备注 |\n" + \
                  "|:---|:---|:---:|:---|---:|:---|\n" + \
                  "\n".join(new_rows)

    # 插入到「最后更新时间」行之后
    marker = f"**最后更新**: {today.split()[0]}"
    if marker in md_content:
        md_content = md_content.replace(marker, marker + new_section)
    else:
        md_content += new_section

    with open(SOURCES_MD, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\n已更新地址簿: {SOURCES_MD}")
    print("请手动验证后把 🔄 改为 ✅ 或 ❌")

    # 保存发现列表
    out_path = os.path.join(TEMP_DIR, f"新发现多仓_{datetime.date.today().strftime('%Y%m%d')}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"发现时间": today, "来源": list(all_found.keys())}, f, ensure_ascii=False, indent=2)
    print(f"已保存发现列表: {out_path}")

if __name__ == "__main__":
    main()
