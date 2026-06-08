# 影视源库 - TVBox 配置管理

> **版本**: v2.1 | 2026-06-08
> **定位**: 统一管理 TVBox 影视播放器的配置文件，GitHub Pages 托管，支持自动更新。

---

## 快速使用

在 **TVBox** 中填入订阅地址：

```
https://wwh3602.github.io/tvbox-source/config.json
```

备用地址（国内访问更快）：

```
https://cdn.jsdelivr.net/gh/wwh3602/tvbox-source@main/config.json
```

---

## 内容概览

- **影视站点**: `1095 个`（2026-06-08 最新）
- **线路解析**: `90 个`（jx.xyflv / jx.xmflv / 夜幕 / 冰豆 等）
- **电视直播**: `38 个` 直播源（APTV / 4k8k / 秋天直播等）
- **直播频道**: `307 个`（央视 / 卫视 / 地方台 / 海外）

---

## 目录结构

```
tvbox-source/
├── config.json              ← TVBox 主配置（直接编辑此文件）
│
├── __tools/                 ← 脚本工具
│   ├── README.md            ← 工具说明
│   ├── auto_update.py       ← 主控脚本：拉取多仓→去重→输出测试文件
│   ├── add_sites.py         ← 批量添加站点
│   ├── merge_and_test.py    ← 合并测试脚本
│   ├── 一键更新.bat         ← Windows 一键提交推送
│   └── ...
│
├── __sources/               ← 多仓地址簿
│   └── 多仓地址簿.md        ← 记录所有多仓来源及状态
│
└── README.md                ← 本文件
```

---

## 更新流程

```
发现新多仓 / 博主推荐 →  加到 __sources/多仓地址簿.md
                                    ↓
                        python __tools/auto_update.py
                                    ↓
              ┌─ __temp/待测试_YYYYMMDD.json（新增站点）
              │        ↓
              │  你在 TVBox 测试 → 哪些可用？
              │        ↓
              │  告诉 AI 测试结果
              │        ↓
              └→ AI 把可用的合并进 config.json
                            ↓
                  GitHub Pages 1-3 分钟生效
```

---

## 多仓接口原理

| 类型 | 特点 | 能否 curl 抓取 |
|:---|:---|:---|
| **直接 JSON** | URL 返回 `.json` 文件 | ✅ 可以 |
| **多仓（UA 路由）** | 浏览器打开是网页，App 打开返回 JSON | ⚠️ 部分可以 |
| **中文域名** | 肥猫.com / 饭太硬.com 国内 DNS 污染 | ❌ 不可行 |
| **加密数据** | 返回 hex+二进制加密，需 App 解密 | ❌ 不可行 |
| **GitHub Raw** | GitHub raw 被墙，需代理 | ⚠️ 需用 ghproxy |

详见 `__sources/多仓地址簿.md`

---

## 站点分类说明

| 分组 | 类型 | 特点 |
|:---|:---|:---|
| `采集` | T1_JSON CMS 采集 | 直连影视资源站 API，数量多、更新快 |
| `默认` | T1_JSON | 标准资源站 |
| `影视` | T1_JSON | 综合影视站 |
| `官采` | T1_JSON | 官方授权采集 |
| DRPY/JS 类 | 脚本驱动 | 爬取网页，资源覆盖广 |

---

## 维护记录

| 日期 | 操作 |
|:---|:---|
| 2026-06-08 | 清理 zyfun 相关文件，专注 config.json |
| 2026-06-08 | v2.0 重构目录结构：分离 __tools/ __sources/ __temp/ |
| 2026-06-08 | 首批 17 个 T1 采集源测试入库 |

---

**最后更新**: 2026-06-08
