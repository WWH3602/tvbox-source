import json, uuid

with open(r'D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source\config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

new_sites = [
    {'name': '量子资源',   'api': 'http://www.lzzy.tv/api.php/provide/vod/'},
    {'name': '淘片资源',   'api': 'https://taopianapi.com/cjapi/mc10/vod/json.html'},
    {'name': '新浪资源',   'api': 'https://api.xinlangapi.com/xinlangapi.php/provide/vod/'},
    {'name': '光速资源',   'api': 'https://api.guangsuapi.com/api.php/provide/vod/'},
    {'name': '金鹰资源',   'api': 'https://jyzyapi.com/provide/vod/'},
    {'name': '非凡资源',   'api': 'http://cj.ffzyapi.com/api.php/provide/vod/from/ffm3u8/'},
    {'name': 'iKun资源',  'api': 'https://ikunzyapi.com/api.php/provide/vod'},
    {'name': '1080zyku',  'api': 'http://api.1080zyku.com/inc/api_mac10.php'},
    {'name': 'U酷资源',    'api': 'https://api.ukuapi.com/api.php/provide/vod/'},
    {'name': '无尽资源',   'api': 'https://api.wujinapi.me/api.php/provide/vod/'},
    {'name': '红牛资源',   'api': 'https://www.hongniuzy2.com/api.php/provide/vod/'},
    {'name': '最大资源',   'api': 'https://api.zuidapi.com/api.php/provide/vod/'},
    {'name': '极速资源',   'api': 'https://jszyapi.com/api.php/provide/vod/'},
    {'name': '优质资源网', 'api': 'https://api.1080zyku.com/inc/apijson.php'},
    {'name': '豪华资源',   'api': 'https://hhzyapi.com/api.php/provide/vod'},
    {'name': '速播资源',   'api': 'http://suboziyuan.net/api.php/provide/vod/'},
    {'name': '魔都动漫',   'api': 'https://caiji.moduapi.cc/api.php/provide/vod/'},
]

existing_apis = {s['api'].strip() for s in data['sites']}
added = 0
for ns in new_sites:
    api = ns['api'].strip()
    if api in existing_apis:
        print(f'  已存在，跳过: {ns["name"]}')
        continue
    site = {
        'id': str(uuid.uuid4()),
        'key': str(uuid.uuid4()),
        'name': ns['name'],
        'api': api,
        'playUrl': '',
        'search': 1,
        'group': '采集',
        'isActive': True,
        'type': 1,
        'ext': '',
        'categories': '',
        'createdAt': 1780033646806,
        'updatedAt': 1780033646806,
    }
    data['sites'].append(site)
    print(f'  + 新增: {ns["name"]}')
    added += 1

print(f'\n共新增 {added} 个站点，当前共 {len(data["sites"])} 个')

with open(r'D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source\config.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('config.json 已保存')
