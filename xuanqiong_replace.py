#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xuanqiong_replace.py
将 xuanqiong_single.json 作为唯一来源，重新生成 config.json 和 zyfun_config.json

用法: python xuanqiong_replace.py
"""

import json
import uuid
import time
from pathlib import Path

# 时间戳
TS = int(time.time() * 1000)

BASE_DIR = Path(__file__).parent
XUANQIONG_FILE = BASE_DIR / "_warehouse" / "xuanqiong_single.json"
CONFIG_FILE = BASE_DIR / "config.json"
ZYFUN_FILE = BASE_DIR / "zyfun_config.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  已写入: {path}")


def to_tvbox_config(sites: list) -> dict:
    """xuanqiong 格式 → TVBox config 格式"""
    tvbox_sites = []
    for site in sites:
        name = site["name"]
        api = site["api"]
        stype = site.get("type", 1)
        searchable = site.get("searchable", 1)

        # 根据名称确定 group
        if "音乐" in name or "听" in name:
            group = "音乐"
        elif "动漫" in name:
            group = "动漫"
        elif "直播" in name or "体育" in name or "看球" in name:
            group = "直播"
        elif "夸克" in name:
            group = "夸克"
        elif "影视" in name or "资源" in name or "影院" in name or "电影" in name:
            group = "影视"
        else:
            group = "采集"

        item = {
            "key": site["key"],
            "name": name,
            "type": stype,
            "api": api,
            "group": group,
            "searchable": searchable,
            "quickSearch": searchable,
            "filterable": site.get("filterable", 1),
            "changeable": site.get("changeable", 1),
        }

        pt = site.get("playerType", -1)
        if pt != -1:
            item["playerType"] = pt

        if site.get("ext"):
            item["ext"] = site["ext"]

        tvbox_sites.append(item)

    return {"sites": tvbox_sites}


def to_zyfun_config(sites: list) -> dict:
    """xuanqiong 格式 → ZYFun site 格式"""
    zyfun_sites = []
    for site in sites:
        name = site["name"]
        api = site["api"]
        stype = site.get("type", 1)
        searchable = site.get("searchable", 1)

        # 根据名称确定 group
        if "音乐" in name or "听" in name:
            group = "音乐"
        elif "动漫" in name:
            group = "动漫"
        elif "直播" in name or "体育" in name or "看球" in name:
            group = "直播"
        elif "夸克" in name:
            group = "夸克"
        elif "影视" in name or "资源" in name or "影院" in name or "电影" in name:
            group = "影视"
        else:
            group = "tvbox"

        item = {
            "id": str(uuid.uuid4()),
            "key": site["key"],
            "name": name,
            "api": api,
            "playUrl": "",
            "search": bool(searchable),
            "group": group,
            "type": stype,
            "ext": site.get("ext", ""),
            "categories": "",
            "isActive": True,
            "createdAt": TS,
            "updatedAt": TS,
        }

        zyfun_sites.append(item)

    return {"site": zyfun_sites}


def main():
    print("=" * 60)
    print("xuanqiong → 重新生成 TVBox/ZYFun 配置")
    print("=" * 60)

    # 1. 读取源文件
    print(f"\n[1] 读取源文件: {XUANQIONG_FILE}")
    xuanqiong = load_json(XUANQIONG_FILE)
    src_sites = xuanqiong.get("sites", [])
    print(f"    共 {len(src_sites)} 个站点")

    # 打印源站列表
    print("\n    源站列表:")
    for s in src_sites:
        tname = {1: "JSON", 3: "Python", 7: "DRPY/JS"}.get(s.get("type", 1), "Unknown")
        print(f"      [{tname}] {s['name']} ({s.get('key', '')})")

    # 2. 生成新配置
    print(f"\n[2] 生成新配置...")
    new_config = to_tvbox_config(src_sites)
    new_zyfun = to_zyfun_config(src_sites)
    print(f"    TVBox: {len(new_config['sites'])} 个站点")
    print(f"    ZYFun: {len(new_zyfun['site'])} 个站点")

    # 3. 写入 config.json
    print(f"\n[3] 写入 config.json...")
    save_json(CONFIG_FILE, new_config)

    # 4. 写入 zyfun_config.json
    print(f"\n[4] 写入 zyfun_config.json...")
    save_json(ZYFUN_FILE, new_zyfun)

    print("\n" + "=" * 60)
    print("重新生成完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
