#!/usr/bin/env python3
"""
ZYFun 配置维护脚本
用法:
  python make_zyfun_config.py          # 生成 zyfun_config.json
  python make_zyfun_config.py --push   # 生成 + git commit + push
"""
import json
import sys
import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.dirname(SCRIPT_DIR)           # tvbox-source/
CONFIG_PATH = os.path.join(ROOT_DIR, "config.json")
ZYFUN_PATH = os.path.join(ROOT_DIR, "zyfun_config.json")

def build_zyfun_config():
    """从 config.json 生成 zyfun_config.json"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    zyfun = {}

    # site (影视) - 字段名必须是 site，search 改成布尔
    zyfun["site"] = []
    for s in data["sites"]:
        item = dict(s)
        item["search"] = bool(item.get("search", 0))
        zyfun["site"].append(item)

    # analyze / iptv / channel 原样复制
    zyfun["analyze"] = data["analyze"]
    zyfun["iptv"]    = data["iptv"]
    zyfun["channel"] = data["channel"]

    with open(ZYFUN_PATH, "w", encoding="utf-8") as f:
        json.dump(zyfun, f, ensure_ascii=False, indent=2)

    return {
        "site":     len(zyfun["site"]),
        "analyze":  len(zyfun["analyze"]),
        "iptv":     len(zyfun["iptv"]),
        "channel":  len(zyfun["channel"]),
    }

def git_push():
    """git add + commit + push"""
    subprocess.run(["git", "-C", SCRIPT_DIR, "add", "zyfun_config.json"], check=True)
    result = subprocess.run(
        ["git", "-C", SCRIPT_DIR, "commit", "-m", "更新: zyfun_config.json (自动派生)"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        if "nothing to commit" in result.stderr:
            print("  [git] 无变更，跳过提交")
            return
        raise RuntimeError(result.stderr)
    subprocess.run(["git", "-C", SCRIPT_DIR, "push"], check=True)
    print("  [git] 已推送")

if __name__ == "__main__":
    counts = build_zyfun_config()
    print(f"生成完成  site={counts['site']}  analyze={counts['analyze']}  iptv={counts['iptv']}  channel={counts['channel']}")

    if "--push" in sys.argv:
        print("提交到 GitHub ...")
        git_push()
