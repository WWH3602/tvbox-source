# 可用线路 API 记录

> 经过自动化测试筛选，确认可用的站点。一行一条，直接可用。
> **测试日期**: 2026-06-09 | **测试源**: zy_config_20260609.json（762 站 → 65 可用）

---

## T1 采集站（直连 API，最稳定）

| 名称 | API |
|:---|:---|
| 最大资源 | `https://api.zuidapi.com/api.php/provide/vod/` |
| 暴风资源 | `https://bfzyapi.com/api.php/provide/vod/` |
| 闪电资源 | `https://sdzyapi.com/api.php/provide/vod/` |
| 无尽资源 | `https://api.wujinapi.me/api.php/provide/vod/` |
| 如意采集 | `https://cj.rycjapi.com/api.php/provide/vod/` |
| iKun资源 | `https://ikunzyapi.com/api.php/provide/vod/` |
| 1080zyku | `http://api.1080zyku.com/inc/api_mac10.php` |
| 淘片资源 | `https://taopianapi.com/cjapi/mc10/vod/json.html` |
| U酷资源 | `https://api.ukuapi.com/api.php/provide/vod/` |
| 魔都动漫 | `https://caiji.moduapi.cc/api.php/provide/vod/` |
| 樱花采集 | `https://m3u8.apiyhzy.com/api.php/provide/vod/` |
| 天堂采集 | `http://caiji.dyttzyapi.com/api.php/provide/vod/` |
| 索尼采集 | `https://suoniapi.com/api.php/provide/vod/` |
| 艾旦采集 | `https://www.lovedan.net/api.php/provide/vod/` |

## DRPY/JS 脚本（需 app 内置 drpy 引擎）

| 名称 | API（drpy 引擎） | EXT（实际脚本） |
|:---|:---|:---|
| 豆瓣 | `https://www.agit.ai/fantaiying/dr_py/raw/branch/main/libs/drpy2.min.js` | `https://www.agit.ai/fantaiying/dr_py/raw/branch/main/js/drpy.js` |
| 360影视 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/360影视.js` |
| 优酷 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/优酷.js` |
| 爱奇艺 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/奇珍异兽.js` |
| 腾讯 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/腾云驾雾.js` |
| 芒果 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/百忙无果.js` |
| 搜狗 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/菜狗.js` |
| 兔小贝 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/兔小贝.js` |
| 童趣 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/童趣.js` |
| 有声绘本 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/有声绘本网.js` |
| 310直播 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/310直播.js` |
| 88看球 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/88看球.js` |
| 抓饭体育 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/抓饭体育.js` |
| JRKAN直播 | `gh-proxy + drpy2.min.js` | `gh-proxy + /js/JRKAN直播.js` |
| 两个BT | `agit.ai + drpy2.min.js` | `agit.ai + /js/两个BT.js` |
| 低端影视 | `agit.ai + drpy2.min.js` | `agit.ai + /js/ddys.js` |
| 厂长资源 | `agit.ai + drpy2.min.js` | `agit.ai + /js/厂长资源.js` |
| 子子影视 | `agit.ai + drpy2.min.js` | `agit.ai + /js/子子影视.js` |
| 怡萱动漫 | `agit.ai + drpy2.min.js` | `agit.ai + /js/怡萱动漫.js` |
| 哔哩合集 | `agit.ai + drpy2.min.js` | `agit.ai + /js/我的哔哩.js` |
| 爱看 | `agit.ai + drpy2.min.js` | `agit.ai + /js/爱看.js` |
| 短剧网 | `agit.ai + drpy2.min.js` | `github.io + /js/短剧网.js` |
| 人人电影 | `bitbucket + drpy2.min.js` | `bitbucket + /js/人人电影.js` |
| 努努影院 | `bitbucket + drpy2.min.js` | `bitbucket + /js/努努影院.js` |
| 泥泥视频 | `bitbucket + drpy2.min.js` | `bitbucket + /js/泥泥视频.js` |
| 夸克影视 | `bitbucket + drpy2.min.js` | `bitbucket + /js/夸克影视.js` |
| 爱看资源网 | `bitbucket + drpy2.min.js` | `bitbucket + /js/爱看资源网.js` |
| 电视直播 | `bitbucket + live2vod.js` | `bitbucket + /json/feimaolive.json` |
| 爱上听书 | `bitbucket + drpy2.min.js` | `bitbucket + /js/爱上听书.js` |
| 稀饭动漫 | `bitbucket + drpy2.min.js` | `bitbucket + /js/稀饭动漫.js` |
| 哔哩直播 | `agit.ai + drpy2.min.js` | `agit.ai + /js/哔哩直播.js` |
| 斗鱼直播 | `agit.ai + drpy2.min.js` | `agit.ai + /js/斗鱼直播.js` |
| 虎牙直播 | `agit.ai + drpy2.min.js` | `agit.ai + /js/虎牙直播.js` |

## PY 脚本（需 app 内置 Python 引擎）

| 名称 | API |
|:---|:---|
| 皮虾4K | `https://gh-proxy.com/https://raw.githubusercontent.com/IY-CPU/IY/main/lib/ppx.py` |
| 星芽短剧 | `https://qist.wyfc.qzz.io/xiaosa/py/星芽短剧.py` |
| 网络直播 | `https://qist.wyfc.qzz.io/xiaosa/py/网络直播.py` |
| 爱听音乐 | `https://qist.wyfc.qzz.io/xiaosa/py/爱听音乐.py` |
| 哔哩直播 | `https://qist.wyfc.qzz.io/xiaosa/py/哔哩直播.py` |

> ⚠️ PY 脚本仅测试 URL 可达，实际能否运行取决于 app 的 Python 引擎版本

## 推送工具

| 名称 | API |
|:---|:---|
| 123推送 | `https://so.yinpai.xyz/api.php?type=123` |
| UC推送 | `https://so.yinpai.xyz/api.php?type=uc` |
| 夸克推送 | `https://so.yinpai.xyz/api.php?type=quark` |
| 天翼推送 | `https://so.yinpai.xyz/api.php?type=tianyi` |
| 移动推送 | `https://so.yinpai.xyz/api.php?type=mobile` |
| 百度推送 | `https://so.yinpai.xyz/api.php?type=baidu` |
| 采集集合 | `http://zhangqun1818.serv00.net/cj/cjjh.php` |

---

## 失败原因统计（762 → 697 失败）

| 原因 | 数量 | 说明 |
|:---|---:|:---|
| HTTP 404 | 626 | JS/PY 脚本文件已删除或链接失效 |
| NOT_JSON | 20 | 返回内容不是有效 JSON |
| SSL 错误 | 30 | 证书问题或握手失败 |
| 超时 | 6 | 连接超时 |
| 编码错误 | 9 | URL 含中文字符，编码问题 |
| 其他 | 6 | 连接被拒/HTTP 525/403 |

**按类型可用率**: T1采集 35.7% · 推送 35.0% · DRPY/JS 5.0% · PY脚本 16.7%（仅可达）

**统计**: 65 条可用线路（去重后约 58 条独立源）| 2026-06-09
