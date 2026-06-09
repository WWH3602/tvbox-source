#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xuanqiong_to_tvbox.py
将 xuanqiong_single.json 的站点同步到 config.json 和 zyfun_config.json

用法: python xuanqiong_to_tvbox.py
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


def to_tvbox_site(site: dict) -> dict:
    """xuanqiong 格式 → TVBox sites 格式"""
    key = site["key"]
    name = site["name"]
    api = site["api"]
    stype = site.get("type", 1)

    # 根据类型确定 group
    if "音乐" in name or "听" in name:
        group = "音乐"
    elif "动漫" in name:
        group = "动漫"
    elif "直播" in name or "体育" in name or "看球" in name:
        group = "直播"
    elif "影视" in name or "资源" in name or "影院" in name or "电影" in name:
        group = "影视"
    elif "夸克" in name:
        group = "夸克"
    else:
        group = "采集"

    result = {
        "key": key,
        "name": name,
        "type": stype,
        "api": api,
        "group": group,
        "searchable": site.get("searchable", 1),
        "quickSearch": site.get("quickSearch", 1),
        "filterable": site.get("filterable", 1),
        "changeable": site.get("changeable", 1),
    }

    # playerType
    pt = site.get("playerType", -1)
    if pt != -1:
        result["playerType"] = pt

    # ext 字段
    if site.get("ext"):
        result["ext"] = site["ext"]

    return result


def to_zyfun_site(site: dict) -> dict:
    """xuanqiong 格式 → ZYFun site 格式"""
    key = site["key"]
    name = site["name"]
    api = site["api"]
    stype = site.get("type", 1)
    searchable = site.get("searchable", 1)

    # 根据类型确定 group
    if "音乐" in name or "听" in name:
        group = "音乐"
    elif "动漫" in name:
        group = "动漫"
    elif "直播" in name or "体育" in name or "看球" in name:
        group = "直播"
    elif "影视" in name or "资源" in name or "影院" in name or "电影" in name:
        group = "影视"
    elif "夸克" in name:
        group = "夸克"
    else:
        group = "tvbox"

    result = {
        "id": str(uuid.uuid4()),
        "key": key,
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

    return result


def merge_sites_tvbox(config: dict, new_sites: list) -> dict:
    """合并 TVBox sites（去重，基于 key）"""
    existing_keys = {s["key"] for s in config.get("sites", [])}
    to_add = [s for s in new_sites if s["key"] not in existing_keys]

    if "sites" not in config:
        config["sites"] = []

    config["sites"].extend(to_add)
    return config, len(to_add)


def merge_sites_zyfun(config: dict, new_sites: list) -> dict:
    """合并 ZYFun site（去重，基于 key）"""
    existing_keys = {s["key"] for s in config.get("site", [])}
    to_add = [s for s in new_sites if s["key"] not in existing_keys]

    if "site" not in config:
        config["site"] = []

    config["site"].extend(to_add)
    return config, len(to_add)


def main():
    print("=" * 60)
    print("xuanqiong → TVBox/ZYFun 配置同步工具")
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

    # 2. 转换为两种格式
    print("\n[2] 转换格式...")
    tvbox_sites = [to_tvbox_site(s) for s in src_sites]
    zyfun_sites = [to_zyfun_site(s) for s in src_sites]
    print(f"    TVBox 格式: {len(tvbox_sites)} 个")
    print(f"    ZYFun 格式: {len(zyfun_sites)} 个")

    # 3. 读取并更新 config.json
    print(f"\n[3] 更新 config.json...")
    config = load_json(CONFIG_FILE)
    old_count = len(config.get("sites", []))
    config, added = merge_sites_tvbox(config, tvbox_sites)
    new_count = len(config.get("sites", []))
    print(f"    原站点数: {old_count}, 新增: {added}, 总计: {new_count}")
    save_json(CONFIG_FILE, config)

    # 4. 读取并更新 zyfun_config.json
    print(f"\n[4] 更新 zyfun_config.json...")
    zyfun = load_json(ZYFUN_FILE)
    old_count = len(zyfun.get("site", []))
    zyfun, added = merge_sites_zyfun(zyfun, zyfun_sites)
    new_count = len(zyfun.get("site", []))
    print(f"    原站点数: {old_count}, 新增: {added}, 总计: {new_count}")
    save_json(ZYFUN_FILE, zyfun)

    print("\n" + "=" * 60)
    print("同步完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
