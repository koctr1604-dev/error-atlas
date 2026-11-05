# 贡献指南

欢迎纠错，优先于扩充数量。每条记录应让使用者在一分钟内判断“是不是我的场景”。

## 收录标准

1. 保留可检索的真实报错，说明工具、环境或版本边界。含动态路径、包名、主机名时注明占位值。
2. `summary` 为 1–2 句中文；不能把常见原因写成唯一原因。
3. 至少一组 `when → reason → check → fix`。确认步骤应能区分原因，修复应只改变必要的范围。
4. 至少一个实际查阅过的官方文档、官方仓库源码、官方维护者记录或规范链接。链接能访问不等于支持结论。
5. 不复制博客全文。不提交凭证、私钥、带认证参数的 URL 或未脱敏日志。
6. 不以关闭 TLS 校验、全局放开权限、删除锁文件、重装系统等作为默认修复。
7. 有管理权限要求、平台差异、兼容性或配置副作用时写明。可变 major action 标签不视为不可变供应链锁定。

## 数据格式

在 `data/` 的相应 JSON 数组新增条目。顶层字段必须完整：

| 字段 | 要求 |
| --- | --- |
| `id` | 全局唯一、稳定的 kebab-case；发布后避免随意改名 |
| `category` | `ci`、`tls`、`permissions`、`packages` |
| `tool` / `error` / `summary` | 工具与适用范围、原始报错、1–2 句解释 |
| `aliases` / `tags` | 字符串数组；别名应是同类报错或真实检索词 |
| `causes` | 非空数组，每项包含 `when`、`reason`、`check`、`fix` |
| `commands` | 数组，可为空；每项包含 `label`、`language`、`code`、`kind`、`note` |
| `commands.language` | `bash`、`yaml`、`text` |
| `commands.kind` | `diagnostic` 或 `fix`；副作用在 `note` 说明 |
| `cautions` | 字符串数组，写边界和风险 |
| `sources` | 非空数组，每项为 `title` + HTTPS `url` |
| `verified_on` | 实际资料核对日期，`YYYY-MM-DD`；不能只批量刷新日期 |
| `verification` | `docs-reviewed` 或 `reproduced` |

可复制一个已有条目作为结构模板，但必须重新核实内容。

## 验证级别

- `docs-reviewed`：逐条查阅来源，确认它支持错误含义或修复方法。不是实机验证。
- `reproduced`：除来源外，在 `notes/reproductions/<id>.md` 提交 OS、工具版本、最小环境、触发步骤、脱敏输出、修复后结果与验证日期。缺少该记录时不得升级状态。

首版利用 AI 协助整理，并进行文档核对。AI 输出、搜索摘要或用户评论本身不能替代证据。欢迎通过可复现的 PR 修正遗漏。

## 本地检查

```bash
python3 scripts/catalog.py validate
python3 scripts/catalog.py build
python3 -m unittest discover -s tests -v
node --test tests/search.test.js
python3 scripts/catalog.py check
```

需要 Python 3.10+、Node.js 22+；不必安装 npm/pip 依赖。一起提交 `data/` 与生成的 `docs/` 改动。`web/` 是检索界面源码，`scripts/catalog.py` 是构建器。不要手动修改生成条目。

浏览器端 smoke test 为可选附加检查，说明见 `tests/README.md`。不必为了提交一条文档安装浏览器自动化工具。

## PR 内容

说明报错出现的环境、原解释哪里不足、查阅来源及检查结果。修复建议有争议时保留多个条件分支，不用“一定”“直接执行即可”等措辞代替论证。
