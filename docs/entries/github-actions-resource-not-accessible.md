# Resource not accessible by integration

**GitHub Actions / REST API** · CI / 持续集成 · `github-actions-resource-not-accessible`

GitHub 拒绝了当前令牌对该 API 资源的操作。先确认实际使用的令牌、目标仓库和端点所需权限，再调整最小授权。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `Resource not accessible by personal access token`
- `GitHub Actions HTTP 403 权限不足`

## 确认原因，再修复

### 1. 使用 GITHUB_TOKEN 操作当前仓库的 API

**原因：** 作业的有效权限不包含端点所需的读写权限；显式设置某项 permissions 后，未列出的权限会变为 none。

**确认：** 查看失败端点的官方权限要求、作业 Set up job 中的 GITHUB_TOKEN Permissions，以及响应中的 X-Accepted-GitHub-Permissions（如有）。

**修复：** 只在需要的作业上声明端点要求的权限，例如创建 issue 才授予 issues: write。

### 2. 目标属于另一个仓库或组织

**原因：** GITHUB_TOKEN 的资源范围只覆盖运行工作流的仓库，增加当前仓库 permissions 无法跨越这一范围。

**确认：** 比对请求 URL 中的资源归属与 github.repository；检查实际令牌对应的 App 安装范围或 PAT 仓库选择。

**修复：** 使用限定到目标仓库、权限最小的 GitHub App 安装令牌，或适当的细粒度 PAT，并通过 secret 提供。

### 3. 失败只出现在 fork 的 pull_request 运行中

**原因：** 这类运行的写权限通常会降为只读，声明 write 不一定能获得写令牌。

**确认：** 检查触发事件、PR 来源与该次运行的实际权限，不以仓库默认设置代替运行证据。

**修复：** 让不可信 PR 仅执行只读检查；确需写操作时，设计独立且受信任的审批或发布流程。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 修复 · 为创建 issue 的作业声明最小权限

这是特定端点示例；其他 API 需要按其文档替换权限。片段本身不会创建 issue。

```yaml
# 放入确实需要创建 issue 的 jobs.<job_id> 下
permissions:
  contents: read
  issues: write
```

## 边界与注意事项

- 403 也可能来自限流或其他策略；只有匹配本条信息时才按令牌权限排查。
- 不要为解决此错误开放所有写权限，或把运行不可信 PR 代码的事件直接改为 pull_request_target。
- 不要打印令牌或完整认证请求头。

## 官方依据

- [GitHub Docs — Troubleshooting the REST API](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api#resource-not-accessible)
- [GitHub Docs — Workflow syntax / permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions)
- [GitHub Docs — Use GITHUB_TOKEN for authentication](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)

[返回分类索引](../INDEX.md)
