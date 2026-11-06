# Can't find 'action.yml', 'action.yaml' or 'Dockerfile' under 'PATH'. Did you forget to run actions/checkout before running your local action?

**GitHub Actions runner** · CI / 持续集成 · `github-actions-local-action-metadata-missing`

runner 在指定的本地 action 目录中没有找到可加载的定义。提示中的 checkout 只是常见原因，还要检查路径、大小写以及是否把 workflow 当成 action 调用。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `local action action.yml not found`
- `本地 action 找不到元数据文件`

## 确认原因，再修复

### 1. steps.uses 使用 ./ 路径，前面没有检出仓库

**原因：** ./ 引用依赖 runner 工作区中的实际文件，而工作区尚未包含 action 源码。

**确认：** 查看步骤顺序和 checkout 的 path 输入，确认目标目录实际位于工作区中的何处。

**修复：** 先检出包含 action 的仓库，再让 uses 指向实际检出目录下的 action 文件夹。

### 2. 已经 checkout 但仍报错

**原因：** 目录拼写或大小写不符、元数据未提交，或者路径指向的是 .github/workflows 中的可复用工作流。

**确认：** 检查报错给出的完整目录，以及当前提交中是否有 action.yml、action.yaml 或 Dockerfile。

**修复：** 修正目录或提交 action 定义；若目标是可复用工作流，改在 jobs.<job_id>.uses 中按 workflow 语法调用。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 检查当前提交包含的 action 定义

my-action 是占位目录名。uses 指向目录，不是 action.yml 文件本身。

```bash
# 在已 checkout 的工作区运行；替换示例目录
git ls-files -- .github/actions/my-action
ls -la -- .github/actions/my-action
```

## 边界与注意事项

- 本条限定 ./ 本地路径引用；远程 action 下载失败要另外检查仓库访问和 ref。
- 不要靠复制任意 Dockerfile 到目录中来绕过错误；它必须是该 action 的有效定义。

## 官方依据

- [actions/runner — ActionManager.cs](https://github.com/actions/runner/blob/main/src/Runner.Worker/ActionManager.cs)
- [GitHub Docs — Find and customize actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions#adding-an-action-from-the-same-repository)
- [GitHub Docs — Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows#calling-a-reusable-workflow)

[返回分类索引](../INDEX.md)
