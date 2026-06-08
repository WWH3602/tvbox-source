"""
从可用数据源提取所有站点，合并去重后生成测试 JSON
输入：__temp/聚玩盒子_可用品.json（爬取脚本产出）
输出：__temp/聚玩盒子_合并测试.json
"""
import requests, json, re, warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
warnings.filterwarnings('ignore')

s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0'

# 加载可用源列表
meta_path = r"D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source\__temp\聚玩盒子_可用品.json"
with open(meta_path, 'r', encoding='utf-8') as f:
    meta = json.load(f)

sources = meta['sources']
print(f"共 {len(sources)} 个可用数据源，开始提取站点...\n")

# 去重用的 key
def site_key(site):
    return (site.get('key', ''), site.get('name', ''), site.get('api', ''))

seen_keys = set()
all_sites = []

def fetch_source(src):
    url = src['url']
    name_hint = url.split('/')[-1].split('.')[0]
    try:
        r = s.get(url, timeout=20, verify=False)
        raw = r.content
        text = raw.decode('utf-8', errors='replace').replace('\r', '')

        # 去注释
        cleaned = re.sub(r'//[^\n]*', '', text)
        cleaned2 = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)

        for trial in [text, cleaned2, cleaned]:
            try:
                data = json.loads(trial.strip())
                break
            except:
                continue
        else:
            return name_hint, [], 0, "PARSE_ERR"

        # 如果是 urls 多仓，展开子仓再取
        urls_list = data.get('urls', [])
        if isinstance(urls_list, list) and len(urls_list) > 0:
            # 递归抓子仓
            sub_sites = []
            for item in urls_list:
                sub_url = item.get('url', '') if isinstance(item, dict) else item
                sub_name = item.get('name', '') if isinstance(item, dict) else ''
                if sub_url:
                    sub = fetch_single(sub_url, sub_name)
                    sub_sites.extend(sub)
            return name_hint, sub_sites, len(sub_sites), "MULTI"

        # 普通站点列表
        sites = data.get('sites', [])
        if isinstance(sites, list):
            return name_hint, sites, len(sites), "OK"

        return name_hint, [], 0, f"UNEXPECTED_KEYS={list(data.keys())[:3]}"

    except Exception as e:
        return name_hint, [], 0, f"ERR={str(e)[:40]}"

def fetch_single(url, hint=""):
    """单独抓一个 URL，返回站点列表"""
    try:
        r = s.get(url, timeout=15, verify=False)
        if r.status_code != 200:
            return []
        text = r.content.decode('utf-8', errors='replace').replace('\r', '')
        cleaned = re.sub(r'//[^\n]*', '', text)
        try:
            data = json.loads(cleaned.strip())
            return data.get('sites', []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        except:
            return []
    except:
        return []

# 并行抓所有源
source_results = []
with ThreadPoolExecutor(max_workers=6) as pool:
    futures = {pool.submit(fetch_source, src): src for src in sources}
    for fut in as_completed(futures):
        name_hint, sites, count, status = fut.result()
        source_results.append((name_hint, sites, count, status))
        icon = "✅" if status == "OK" or status == "MULTI" else "❌"
        print(f"  {icon} {name_hint}: {status} | 提取 {count} 个站点")

# 合并去重
print(f"\n开始合并去重...")
key_set = set()
unique_sites = []

for hint, sites, count, status in source_results:
    if status not in ("OK", "MULTI"):
        continue
    for site in sites:
        key = f"{site.get('key','')}|{site.get('api','')}|{site.get('name','')}"
        if key and key not in key_set:
            key_set.add(key)
            unique_sites.append(site)

print(f"  合并去重后共 {len(unique_sites)} 个独立站点")

# 生成 ZYFun 格式的测试 JSON
# ZYFun 格式: { "sites": [...] }
output_path = r"D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source\__temp\聚玩盒子_合并测试.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({"sites": unique_sites}, f, ensure_ascii=False, indent=2)

print(f"\n已保存: {output_path}")

# 统计信息
api_counts = {}
for site in unique_sites:
    api = site.get('api', 'unknown')
    api_counts[api] = api_counts.get(api, 0) + 1

print(f"\nAPI 类型分布（前15）：")
for api, cnt in sorted(api_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  {cnt:3d} | {api}")

# 来源仓统计
print(f"\n各数据仓贡献：")
for hint, sites, count, status in source_results:
    if status in ("OK", "MULTI"):
        print(f"  {hint}: {count} 个站点")

print(f"\n\n文件大小: {len(open(output_path,'rb').read())//1024} KB")
print("下一步：导入 ZYFun 测试，或运行 sync_to_config.py 同步到 config.json")
