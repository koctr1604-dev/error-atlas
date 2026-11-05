# Error Atlas · 报错译本

**报错原文 → 可能原因 → 确认方法 → 最小修复。**

面向已经在写代码、配 CI、部署服务，却被一句模糊报错卡住的人。每条先用 1–2 句话解释问题，再列出适用条件、诊断与修复。无需账户、API Key 或付费模型。

**[浏览完整索引](docs/INDEX.md)** · [贡献条目](CONTRIBUTING.md) · [发布到 GitHub](docs/PUBLISHING.md) · [验证记录](notes/RELEASE_REVIEW.md) · [English](README.en.md)

## 先查这些问题

| 你看到的报错 | 进入分类 |
| --- | --- |
| `Resource not accessible by integration`、找不到本地 action | [CI / 持续集成](docs/INDEX.md) |
| `certificate verify failed`、`wrong version number` | [TLS / 证书](docs/INDEX.md) |
| `Permission denied (publickey)`、`dubious ownership` | [权限 / 身份](docs/INDEX.md) |
| `ERESOLVE`、`externally-managed-environment` | [包管理 / 依赖](docs/INDEX.md) |

## 使用

- **在 GitHub 阅读：** 打开 [分类索引](docs/INDEX.md)，使用浏览器查找或仓库搜索。
- **离线检索：** 下载仓库后，直接用浏览器打开 `docs/index.html`。数据与脚本内嵌，不需要服务器，也不上传或保存输入的日志。外部来源链接只有点击时才访问。
- **命令行：** Python 3.10+，无第三方依赖。

```bash
python3 scripts/catalog.py search "ERESOLVE"
python3 scripts/catalog.py search "certificate" --category tls
python3 scripts/catalog.py search "Permission denied (publickey)"
```

检索支持原文、别名、工具名、中文关键词和分类筛选。完整日志包含已收录的核心短语时可命中；不做语义推断，也不保证识别所有动态变量或拼写错误。无结果时缩短为错误码或核心短语。

## 为什么保留“确认方法”

同一条错误信息可能对应多个原因。`exit code 1` 只能说明命令失败，证书校验失败也不能直接推出“服务器证书过期”。本项目把环境条件和排查动作放在修复之前，避免用一条命令掩盖问题。

每条记录包括：

- 原始报错及可检索的变体；
- 1–2 句直白解释；
- 按触发条件区分的原因、确认方法和修复；
- 标注“诊断”或“修复”的命令，以及适用范围；
- 官方来源、核对日期与验证级别。

首版 **32 条 / 4 类**，状态均为 `docs-reviewed`：查阅官方资料后编写，**不等于已在每个工具和版本中复现**。工具版本与环境限制见每条正文。后续实机验证记录需包含版本、环境、复现过程和结果，见 [贡献要求](CONTRIBUTING.md)。

## 维护与生成

`data/*.json` 是唯一内容源。Markdown 索引、独立条目和离线 HTML 从同一份数据生成，避免手动维护多个版本。

```bash
python3 scripts/catalog.py validate
python3 scripts/catalog.py build
python3 -m unittest discover -s tests -v
node --test tests/search.test.js
python3 scripts/catalog.py check
```

Python 负责校验和生成；Node.js 22+ 仅用于检索逻辑测试。GitHub Actions 配置会在 push / pull request 时运行这些检查，不执行条目里的修复命令。检查能发现格式、重复 ID、缺少来源、过期生成文件等问题；不能自动证明技术解释正确或来源页面仍然有效。

## 第一版范围

聚焦 GitHub Actions、Git/SSH、Linux/Docker 权限、TLS、npm/pnpm/pip/apt。暂不收录缺乏证据的“万能修复”、仅给出重装建议的条目或大批未经审核的 AI 生成答案。

优先欢迎：可复现的纠错、官方依据更准确的补充、同一报错的不同根因。先看 [贡献规范](CONTRIBUTING.md)，再提交 Issue 或 PR。

## 许可与来源

本仓库原创代码、数据组织及原创解释采用 [MIT License](LICENSE)。外部文档、商标与链接内容保留各自权利；收录链接不表示对方背书。报错原文保留用于检索，正文使用原创概括。
