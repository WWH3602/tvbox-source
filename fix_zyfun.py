import json

f = open(r'D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source\config.json', 'r', encoding='utf-8')
data = json.load(f)
f.close()

# 把 site 改成 sites
data['sites'] = data.pop('site')

# 把 search: true/false 改成 1/0
for s in data['sites']:
    if s.get('search') == True:
        s['search'] = 1
    elif s.get('search') == False:
        s['search'] = 0

# 把 type 12 的改成 type 3（T3 Python模式，ZYFun支持）
fixed_count = 0
for s in data['sites']:
    if s.get('type') == 12:
        s['type'] = 3
        fixed_count += 1

print(f'修复完成: site->sites, search布尔转数字, type12->type3 ({fixed_count}个)')
site_count = len(data['sites'])
print(f'sites数量: {site_count}')

# 保存
with open(r'D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source\config.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('已保存')
