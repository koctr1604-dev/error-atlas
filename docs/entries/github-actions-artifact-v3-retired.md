# This request has been automatically failed because it uses a deprecated version of actions/upload-artifact: v3

**GitHub.com Actions artifact actions** · CI / 持续集成 · `github-actions-artifact-v3-retired`

GitHub.com 已停止接受旧版 artifact action，仓库中的旧 tag 仍存在也不代表还能运行。需要按迁移说明更新上传端与下载端。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `Missing download info for actions/upload-artifact@v3`
- `actions/download-artifact@v3 deprecated`
- `artifact v3 已退役`

## 确认原因，再修复

### 1. 工作流显式使用 upload-artifact@v3 或 download-artifact@v3

**原因：** 运行引用了服务端已经退役的 artifact action 版本。

**确认：** 搜索本仓库 workflow、复合 action 和被调用的工作流，确认是哪一层仍引用 v3。

**修复：** 在 GitHub.com 上迁移到受支持的 v4 或更高版本，并检查名称、不可变 artifact 和下载兼容性变化。

### 2. 本仓库已升级，但第三方 action 或复用工作流仍触发错误

**原因：** 间接依赖内部还在使用旧 artifact action。

**确认：** 从 Prepare actions 日志定位实际引用，再检查依赖仓库对应 ref 的定义。

**修复：** 选用已完成迁移的依赖版本；没有兼容版本时提交上游修复或采用经过审查的替代实现。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 查找本仓库显式的旧版 artifact 引用

只检查已跟踪的本仓库 YAML；不能发现远程依赖内部的引用。无匹配时 git grep 返回 1。

```bash
git grep -n -E 'actions/(upload|download)-artifact@v[123]([[:space:]]|$)' -- '*.yml' '*.yaml'
```

## 边界与注意事项

- 本条退役结论针对 GitHub.com。GitHub Enterprise Server 的兼容矩阵不同，不能直接照搬 v4+。
- Missing download info 也可能有其他原因；只有确认引用退役版本时才用本条处理。
- 仅替换版本号不代表迁移完成，需核对上传与下载行为及 runner 兼容要求。

## 官方依据

- [GitHub Changelog — Deprecation notice: v3 of the artifact actions](https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/)
- [actions/upload-artifact — Documentation and GHES support](https://github.com/actions/upload-artifact)

[返回分类索引](../INDEX.md)
