# __tools/ 工具目录

> 存放影视源维护相关的脚本工具。

---

## auto_update.py（主控脚本）

自动从多仓拉取 → 对比 config.json 去重 → 输出待测试 JSON

```bash
python __tools/auto_update.py              # 拉取 + 对比 + 输出测试文件
python __tools/auto_update.py --testonly  # 仅对比已有测试文件
python __tools/auto_update.py --push     # 额外提交 config.json 变更并推送
```

输出文件：`__temp/待测试_YYYYMMDD.json`

---

## add_sites.py（批量添站脚本）

把站点 api 直接追加进 config.json（自动去重）

```bash
python __tools/add_sites.py
```

修改 `add_sites.py` 里的 `new_sites` 列表即可添加。

---

## merge_and_test.py（合并测试脚本）

合并多个来源的站点数据，并进行可用性测试

```bash
python __tools/merge_and_test.py
```

---

## 一键更新.bat

Windows 批处理：检查 git 变更 → 提交 → 推送到 GitHub

```bash
双击运行 一键更新.bat
```

---

**最后更新**: 2026-06-08
