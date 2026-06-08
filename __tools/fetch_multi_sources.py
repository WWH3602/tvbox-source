import requests, json, re, os, uuid

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "",
})

SOURCES = [
    ("肥猫",     "http://xn--fiqs8s.xn--fiqs8s/"),
    ("饭太硬",   "http://xn--4gqvb6h.xn--fiqs8s/tv"),
    ("小米",     "https://mpanso.me/DEMO.json"),
    ("王二小",   "http://xn--4kq62z5rby2qupq9ub.top/"),
    ("南风",     "https://ghproxy.net/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json"),
    ("菜妮丝",   "https://tvbox.cainisi.cc"),
    ("摆烂",     "https://raw.gitmirror.com/Yidinglong/TVBox/master/tv.json"),
    ("小香肠",   "https://raw.gitmirror.com/172321461/TVBox/main/TVBox.json"),
    ("超人说",   "https://raw.gitmirror.com/w1218115434/TVBox/main/tv.json"),
    ("vmgbb",    "https://raw.gitmirror.com/guot55/TVBox/main/v.json"),
    ("荷城茶秀", "https://raw.gitmirror.com/wwm6/TVBox/main/tv.txt"),
]

def fetch(url, name):
    print(f"\n[{name}] {url}")
    try:
        r = session.get(url, timeout=20, allow_redirects=True, verify=False)
        r.encoding = 'utf-8'
        text = r.text
        print(f"  status={r.status_code} len={len(text)}")
        return text
    except Exception as e:
        print(f"  [FAIL] {e}")
        return None

def parse_json(text, source):
    if not text:
        return None
    text = text.strip()
    # 去 markdown
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text, flags=re.MULTILINE)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # 找最大的 JSON 对象
        best = None
        for m in re.finditer(r'\{[\s\S]*\}', text):
            try:
                obj = json.loads(m.group())
                if isinstance(obj, (dict, list)) and len(m.group()) > (len(best) if best else 0):
                    best = m.group()
            except:
                continue
        if best:
            return json.loads(best)
        for m in re.finditer(r'\[[\s\S]*\]', text):
            try:
                arr = json.loads(m.group())
                if isinstance(arr, list) and len(arr) > (len(best) if best else 0):
                    best = m.group()
            except:
                continue
        if best:
            return json.loads(best)
        return None

def extract_sites(data, source_name):
    sites = []
    raw = []
    if isinstance(data, dict):
        for k, v in data.items():
            if k in ("sites", "urls", "rules", "channels", "data", "list") and isinstance(v, list):
                raw.extend(v)
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
        pl_v   = s.get("playUrl") or s.get("p") or ""
        if not name_v or not api_v:
            continue
        sites.append({
            "id": str(uuid.uuid4()),
            "key": key_v if key_v else str(uuid.uuid4()),
            "name": f"[{source_name}] {name_v.strip()}",
            "api": api_v.strip(),
            "playUrl": pl_v,
            "search": srh_v,
            "ext": ext_v,
            "group": source_name,
            "isActive": True,
            "type": 1,
            "categories": "",
            "createdAt": 1780033646806,
            "updatedAt": 1780033646806,
        })
    return sites

# === 主程序 ===
os.environ['PYTHONIOENCODING'] = 'utf-8'
all_sites = []
seen = {}

for name, url in SOURCES:
    text = fetch(url, name)
    if text:
        data = parse_json(text, name)
        if data:
            sites = extract_sites(data, name)
            print(f"  -> 提取 {len(sites)} 个")
            for s in sites:
                api = s["api"]
                if api in seen:
                    continue
                seen[api] = name
                all_sites.append(s)
                print(f"     + {s['name']}: {api[:55]}")
        else:
            snippet = text[:200].replace('\n',' ')
            print(f"  [WARN] 无法解析: {snippet}")

print(f"\n总计 {len(all_sites)} 个站点（去重后）")

out = os.path.join(os.path.dirname(__file__), "zyfun_multi_test.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump({"spider":"","lives":[],"sites":all_sites,"analyze":[]}, f, ensure_ascii=False, indent=2)
print(f"已保存: {out}")
