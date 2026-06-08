import json, os

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR    = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(ROOT_DIR, "config.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# 把 site 改成 sites
data["sites"] = data.pop("site")

# 把 search: true/false 改成 1/0
for s in data["sites"]:
    if s.get("search") is True:
        s["search"] = 1
    elif s.get("search") is False:
        s["search"] = 0

# 把 type 12 的改成 type 3（T3 Python 模式，ZYFun 支持）
fixed_count = 0
for s in data["sites"]:
    if s.get("type") == 12:
        s["type"] = 3
        fixed_count += 1

print(f"修复完成: site->sites, search布尔转数字, type12->type3 ({fixed_count}个)")
print(f"sites数量: {len(data['sites'])}")

with open(CONFIG_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("已保存")
