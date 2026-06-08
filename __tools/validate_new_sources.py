import json, subprocess, re, time, os, datetime

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR    = os.path.dirname(SCRIPT_DIR)
SOURCES_MD  = os.path.join(ROOT_DIR, "__sources", "多仓地址簿.md")
FOUND_FILE  = os.path.join(ROOT_DIR, "__temp", "新发现多仓_20260608.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# 黑名单
BLACKLIST = [
    r"example\.com",
    r"github\.com/.*/blob/", r"github\.com/.*/tree/",
    r"pan\.quark\.cn", r"pan\.wpcoder\.cn",
    r"api\.btstu\.cn", r"饭\.eu\.org",
    r"www\.kf666888\.cn",
    r"agit\.ai/.*/TVBox/.*raw",
    r"tvbox\.clbug\.com",
    r"tv\.nxog\.top/m/111\.php",
    r"tv\.nxog\.top/m$",
    r"tvbox\.xn--.*\.top$",
    r"tv\.999888987\.xyz",
    r"xn--sdds-rp5imh\.v\.nxog\.top",
    r"iyouhun\.com",
    r"bizhangjie/CatVodSpider",
    r"fenghuang\.m3u", r"HerbertHe/iptv-sources",
    r"q215613905/TVBoxOS", r"takagen99/Box",
    r"FongMi/TV", r"ssili126/tv",
    r"juwanhezi\.com",
    r"raw\.gitcode\.com", r"raw\.gitmirror\.com",
    r"饭太硬\.top", r"王二小放牛娃",
    r"raw\.lanyunsec\.top",
    r"tv\.203511\.xyz",
    r"cwezhd/TVList",
    r"饭.eu.org",
]

def blacklisted(url):
    for p in BLACKLIST:
        if re.search(p, url, re.I):
            return True
    return False

def fetch_json(url):
    cmd = ["curl", "-sL", "-A", UA, "--tlsv1.2", "-m", "20", "--compressed", url]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=25)
        text = r.stdout
        if isinstance(text, bytes):
            text = text.decode("utf-8", errors="replace")
        text = text.replace("\r", "").strip()
        text = re.sub(r"^\ufeff", "", text)
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)
        if text.startswith("<!") or text.startswith("<html"):
            return None
        try:
            return json.loads(text)
        except:
            # 尝试提取 JSON
            for m in re.finditer(r"\{[\s\S]{50,}\}|\[[\s\S]{50,}\]", text):
                try:
                    obj = json.loads(m.group())
                    if isinstance(obj, (dict, list)) and len(m.group()) > 100:
                        return obj
                except:
                    continue
            return None
    except:
        return None

def count_sites(data):
    """返回 (站点数, 说明)"""
    if isinstance(data, dict):
        for k in ["sites", "urls", "data"]:
            if k in data and isinstance(data[k], list):
                return len(data[k]), f"字段:{k}"
        # 递归找
        def walk(obj, depth=0):
            if depth > 5: return []
            if isinstance(obj, dict):
                for v in obj.values():
                    r = walk(v, depth+1)
                    if r: return r
            elif isinstance(obj, list) and len(obj) > 5:
                return obj
            return []
        sites = walk(data)
        if sites:
            return len(sites), "递归找到"
    return 0, "无sites"

# 加载已有地址
existing = set()
with open(SOURCES_MD, encoding="utf-8") as f:
    md = f.read()
for line in md.split("\n"):
    parts = [p.strip().strip("`").strip() for p in line.split("|")]
    for p in parts:
        if p.startswith("http"):
            existing.add(p.rstrip("/"))

with open(FOUND_FILE, encoding="utf-8") as f:
    data = json.load(f)

today = datetime.date.today().strftime("%Y-%m-%d")
valid = []

for url in data["来源"]:
    if blacklisted(url):
        print(f"  [SKIP] {url[:60]}")
        continue
    if url in existing:
        print(f"  [EXIST] {url[:60]}")
        continue

    print(f"  检测: {url[:70]}", end="", flush=True)
    d = fetch_json(url)
    if d is None:
        print(" -> 非JSON")
        continue

    cnt, note = count_sites(d)
    if cnt == 0:
        print(f" -> JSON有效但无sites({note})")
    else:
        valid.append((url, cnt, note))
        print(f" -> 有效 {cnt}站点({note})")
    time.sleep(0.3)

print(f"\n有效新多仓: {len(valid)} 个")
for url, cnt, note in valid:
    name = url.split("//")[-1].split("/")[0].replace("www.", "").split(".")[0]
    print(f"  + [{name}] {url} ({cnt}站)")

if valid:
    with open(SOURCES_MD, encoding="utf-8") as f:
        md = f.read()

    rows = []
    for url, cnt, note in valid:
        name = url.split("//")[-1].split("/")[0].replace("www.", "").split(".")[0]
        rows.append(f"| {name} | `{url}` | 🔄 | 自动发现 | {cnt} | {today} |")

    new_section = (
        f"\n\n## 自动发现新多仓（{today}）\n\n"
        + "| 名称 | 地址 | 状态 | 来源 | 站点数 | 备注 |\n"
        + "|:---|:---|:---:|:---|---:|:---|\n"
        + "\n".join(rows)
    )
    m = re.search(r"\*\*最后更新\*\*: \d{4}-\d{2}-\d{2}", md)
    if m:
        md = md[:m.end()] + new_section + md[m.end():]
    with open(SOURCES_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"\n已更新: {SOURCES_MD}")
