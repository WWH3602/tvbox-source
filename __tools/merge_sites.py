import json, os, shutil

base = r"D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source"

with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
    config = json.load(f)

with open(os.path.join(base, "test_聚玩盒子_去重.json"), "r", encoding="utf-8") as f:
    dedup = json.load(f)

print("=" * 50)
print("=== 合并前检查 ===")
print(f"config.json 原有站点: {len(config['sites'])}")
print(f"去重版站点: {len(dedup['sites'])}")

# 构建已见过的 key 集合（按插入顺序）
merged_keys = {}
merged = []

# 先加 config.json 的（优先级高）
for site in config["sites"]:
    k = site["key"]
    if k not in merged_keys:
        merged_keys[k] = site
        merged.append(site)

# 再加入去重版独有的
added = 0
skipped = 0
for site in dedup["sites"]:
    k = site["key"]
    if k not in merged_keys:
        merged_keys[k] = site
        merged.append(site)
        added += 1
    else:
        skipped += 1

print(f"\n=== 合并结果 ===")
print(f"去重版新增: {added} 个")
print(f"去重版跳过(与config重复): {skipped} 个")
print(f"合并后总计: {len(merged)} 个站点")

# 备份原始 config.json 里的字段结构（保留除 sites 外的其他字段）
print(f"\nconfig.json 其他字段: {[k for k in config.keys() if k != 'sites']}")

# 写入 config.json
with open(os.path.join(base, "config.json"), "w", encoding="utf-8") as f:
    json.dump({"sites": merged}, f, ensure_ascii=False, indent=2)

# 验证写入
with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
    final = json.load(f)
print(f"\n=== 写入验证 ===")
print(f"config.json 现站点数: {len(final['sites'])}")

# 验证无重复 key
keys = [s["key"] for s in final["sites"]]
unique_keys = set(keys)
print(f"唯一key数: {len(unique_keys)}")
print(f"是否有重复key: {len(keys) != len(unique_keys)}")

print("\n合并完成!")
