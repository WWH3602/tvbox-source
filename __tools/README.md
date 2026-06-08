# __tools/ 工具目录

> 存放影视源维护相关的脚本工具。

---

## test_all_sites.py（站点可用性测试）

遍历 `zyfun_config.json` 里每个站点的 `api` URL，测试是否可达并返回 JSON 格式。

```bash
python __tools/test_all_sites.py                           # 测全部 1349 站（并发30，超时6s）
python __tools/test_all_sites.py --workers 10 --timeout 10  # 低并发，更稳定
python __tools/test_all_sites.py --save results.json        # 保存完整结果
python __tools/test_all_sites.py --active-only              # 只测 isActive=true 的站
python __tools/test_all_sites.py --type 1                   # 只测 type=1 的采集站
```

**测试完成后输出**：
- `✓ 可用` / `✗ 失败` / `○ 无API` 三类统计
- 失败分类（连接错误 / 非JSON / TIMEOUT / HTTP-4xx）
- 失败详情列表（含 API URL）
- `test_results.json` 保存完整结果供后续使用

---

## remove_failed_sites.py（失败站点清理）

根据 `test_results.json` 清理配置中的问题站点。

```bash
python __tools/remove_failed_sites.py --dry-run              # 预览，不写入
python __tools/remove_failed_sites.py --backup              # 备份后生成 _clean.json
python __tools/remove_failed_sites.py --inplace             # 直接覆盖原文件（危险）
```

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
