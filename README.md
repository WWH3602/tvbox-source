# 影视源库 - TVBox / ZYFun 配置管理

> **版本**: v3.0 | 2026-06-09
> **定位**: 泫穹影视仓 —— 人工验证可用站点，GitHub Pages 托管。

---

## 泫穹系列配置

### 点播仓

| 名称 | 地址 |
|:---|:---|
| **泫穹单仓**（36站，人工验证） | `https://wwh3602.github.io/tvbox-source/_warehouse/xuanqiong_single.json` |
| **泫穹聚合仓**（13源，多仓切换） | `https://wwh3602.github.io/tvbox-source/_warehouse/xuanqiong_agg.json` |

### 直播仓

| 名称 | 地址 |
|:---|:---|
| **泫穹直播仓**（10源，EPG+台标） | `https://wwh3602.github.io/tvbox-source/_warehouse/xuanqiong_zb.json` |

---

## 聚合仓包含的源

| # | 仓库 | 说明 |
|:---|:---|:---|
| 1 | 王二小放牛娃 | `http://tv.999888987.xyz` |
| 2 | 泫穹单仓 | 自建 36 站 |
| 3 | 王小二 | `https://9280.kstore.vip/newwex.json` |
| 4 | 影视仓 | `http://影视仓.com/` |
| 5 | 二月红接口 | `https://700sjro44343.vicp.fun/eggp/0211/tv.json` |
| 6 | 俊哥接口 | `http://home.jundie.top:81/top98.json` |
| 7 | 宝盒接口 | `http://宝盒接口.top` |
| 8 | 荐片 | `https://tv.203511.xyz/0821.json` |
| 9 | Clun在线 | `https://clun.top/box.json` |
| 10 | 心魔在线 | GitHub 代理 |
| 11 | 真心在线 | cnb.cool |
| 12 | 七星影仓 | kstore |
| 13 | 饭太硬 | ⚠️ 禁用（内存耗尽） |

---

## 直播仓包含的源

| # | 名称 | 说明 |
|:---|:---|:---|
| 1 | 综合直播 | vbskycn/iptv 每6小时自动更新 |
| 2 | YanG综合 | tv.iill.top 综合频道 |
| 3 | 体育直播 | tv.iill.top 体育赛事 |
| 4 | 范明明IPv6 | fanmingming IPv6 源 |
| 5 | MemoryC综合 | MemoryCollection/IPTV |
| 6 | 肥猫综合 | 肥猫经典直播源 |
| 7 | Global直播 | fanmingming 全球频道 |
| 8 | IPTV(IPv6) | fanmingming IPv6 |
| 9 | Radio电台 | fanmingming 收音机 |
| 10 | 电台FM | GitHub 代理收音机 |

---

## 目录结构

```
tvbox-source/
├── _warehouse/                   ← 泫穹系列配置
│   ├── xuanqiong_single.json     ← 单仓（36站，人工验证）
│   ├── xuanqiong_agg.json        ← 聚合仓（13源，多仓切换）
│   └── xuanqiong_zb.json         ← 直播仓（10源，EPG+台标）
│
├── __sources/                    ← API 文档
│   ├── 可用线路api.md             ← 人工验证可用 API 记录
│   └── 可用线路api_正式.md        ← 正式版
│
├── __tools/                      ← 脚本工具
│   └── test_zyfun_sites.py       ← 站点可用性测试脚本
│
├── config.json                   ← 原始完整配置
├── zyfun_config.json             ← ZYFun 专用配置
├── .nojekyll                     ← GitHub Pages 下划线目录支持
└── README.md                     ← 本文件
```

---

## 使用方法

### TVBox / ZYFun

1. 打开 app → 设置 → 配置地址
2. 填入对应地址：
   - **单仓**（只要泫穹站点）→ 填单仓地址
   - **聚合仓**（多仓切换）→ 填聚合仓地址
3. 等待加载完成

---

## 维护记录

| 日期 | 操作 |
|:---|:---|
| 2026-06-09 | v3.0 泫穹系列：单仓36站 + 聚合仓13源 + 直播仓10源 |
| 2026-06-09 | 人工验证41条可用线路，创建正式文档 |
| 2026-06-09 | 修复测试脚本3个bug（中文URL/XML/JSONP），可用站65→80 |
| 2026-06-08 | v2.0 重构目录结构 |
| 2026-06-08 | 首批 17 个 T1 采集源测试入库 |

---

**最后更新**: 2026-06-09
