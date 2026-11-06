# Process completed with exit code 1.

**GitHub Actions** · CI / 持续集成 · `github-actions-process-exit-code-one`

这只是步骤返回失败状态的摘要，不能据此判断是依赖、测试、权限还是脚本错误。真正的线索通常在同一步骤更早的日志里。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `The process exited with code 1`
- `GitHub Actions exit code 1`

## 确认原因，再修复

### 1. 测试、构建或第三方 action 运行后失败

**原因：** 底层工具返回了非零状态；退出码 1 没有跨工具通用的根因含义。

**确认：** 展开首个失败步骤，向上寻找第一条具体错误，记录命令、工具版本和工作目录。

**修复：** 按底层错误修复，再用相同版本和参数验证；把有多条命令的步骤拆分，便于定位。

### 2. Bash 多行脚本或管道在中途停止

**原因：** 内置 shell 的失败处理会终止脚本；显式 shell: bash 还会启用 pipefail，管道中较早的命令失败也会使步骤失败。

**确认：** 检查实际 shell、最后执行到的命令及管道各部分的预期退出码。

**修复：** 对确实允许的非零结果显式处理；意外失败则修复命令本身，保留可靠的失败传播。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 读取某次运行的失败步骤日志

仅查询已有日志。分享输出前检查是否含项目敏感信息。

```bash
# 替换 OWNER/REPO 和 RUN_ID；需已安装并认证 GitHub CLI
gh run view RUN_ID --repo OWNER/REPO --log-failed
```

## 边界与注意事项

- 不要用 continue-on-error 或在命令末尾追加 || true 掩盖尚未解释的失败。
- 不要直接对包含凭据的脚本启用 set -x，也不要输出整个环境变量集合。

## 官方依据

- [GitHub Docs — Setting exit codes for actions](https://docs.github.com/en/actions/how-tos/create-and-publish-actions/set-exit-codes)
- [GitHub Docs — Using workflow run logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs)
- [GitHub Docs — Workflow syntax / shell exit codes](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#exit-codes-and-error-action-preference)

[返回分类索引](../INDEX.md)
