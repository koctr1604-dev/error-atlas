# 检查范围

核心检查无需第三方依赖：

```bash
python3 -m unittest discover -s tests -v
node --test tests/search.test.js
python3 scripts/catalog.py check
```

检查唯一 ID、数据结构、必要证据、明显危险命令模式、生成文件一致性、索引内部链接、HTML JSON 注入边界，以及原文/别名检索和类别过滤。静态检查不等于执行所有修复命令，也不替代技术审核。

可选浏览器 smoke test：在具备 `playwright` 包和 Chromium 的环境运行 `node tests/browser-smoke.cjs`。它检查离线启动、搜索、筛选、空状态、详情、Escape 关闭、深链接、移动端溢出、页面异常和自动联网请求，并更新 `docs/preview.png`。浏览器工具不是使用索引或日常贡献的前置依赖。

GitHub Actions 只运行核心检查；浏览器检查是发布前额外验证。第三方来源的远端可用性与命令实际兼容性不属于这些测试的证明范围。
