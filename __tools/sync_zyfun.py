import json, shutil, os

base = r"D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source"

with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
    cfg = json.load(f)

ts = "20260608_204040"
shutil.copy("zyfun_config.json", f"__backup/zyfun_backup_{ts}.json")

with open("zyfun_config.json", "r", encoding="utf-8") as f:
    zyfun = json.load(f)

print("原 zyfun site 数:", len(zyfun["site"]))
print("合并后 sites 数:", len(cfg["sites"]))

zyfun["site"] = cfg["sites"]

with open("zyfun_config.json", "w", encoding="utf-8") as f:
    json.dump(zyfun, f, ensure_ascii=False, indent=2)

with open("zyfun_config.json", "r", encoding="utf-8") as f:
    v = json.load(f)
print("同步后 zyfun site 数:", len(v["site"]))
print("其他字段保留:", [k for k in v if k != "site"])
print("done")
