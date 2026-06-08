import json

with open(r"D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source\test_聚玩盒子.json", "r", encoding="utf-8") as f:
    data = json.load(f)

sites = data.get("sites", [])
print(f"原始站点数: {len(sites)}")

# 按 key 去重，保留第一个
seen = {}
unique = []
dup_count = 0
for site in sites:
    key = site.get("key", "")
    if key not in seen:
        seen[key] = True
        unique.append(site)
    else:
        dup_count += 1

print(f"去重后站点数: {len(unique)}")
print(f"重复key数量: {dup_count}")

# 按 key 名排序（方便查看）
unique.sort(key=lambda x: x.get("key", ""))

# 保存
out_path = r"D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source\test_聚玩盒子_去重.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"sites": unique}, f, ensure_ascii=False, indent=2)

print(f"\n已保存: {out_path}")
print(f"文件大小: {len(open(out_path, 'rb').read()) // 1024} KB")

# 分析 ZYFun 可能的过滤原因
print("\n--- 分析 ZYFun 显示 777 的可能原因 ---")
empty_type = sum(1 for s in unique if not s.get("type"))
empty_api = sum(1 for s in unique if not s.get("api"))
unknown_type = sum(1 for s in unique if s.get("type", 0) not in (0, 1, 2, 3, 4))
print(f"type 为空的: {empty_type}")
print(f"api 为空的: {empty_api}")
print(f"type 不是 0-4 的: {unknown_type}")

# 统计 type 分布
from collections import Counter
type_dist = Counter(s.get("type", -1) for s in unique)
print(f"\ntype 分布: {dict(sorted(type_dist.items()))}")
