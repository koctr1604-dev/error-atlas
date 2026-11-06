# ERR_PNPM_NO_MATCHING_VERSION_INSIDE_WORKSPACE

**pnpm 10.x workspace: 协议** · 包管理 / 依赖 · `pnpm-workspace-version-missing`

workspace: 依赖要求本地存在匹配版本的 workspace 包，pnpm 不会回退到 registry。此条针对同名本地包的版本不满足要求，应核对依赖范围与实际清单版本。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `no matching version found inside the workspace`
- `workspace dependency version mismatch`

## 确认原因，再修复

### 1. 内部包升级版本后，依赖它的项目安装失败

**原因：** 依赖仍要求旧的 workspace 版本，而本地仅有不满足范围的新版本。

**确认：** 对比依赖声明中的 workspace: 范围与目标包 package.json 的 name、version，同时核对当前 checkout 与 workspace 项目列表。

**修复：** 按真实兼容性更新依赖范围或恢复应使用的包版本，再同步锁文件；不应为装成功随意扩大范围。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 列出 pnpm 识别的 workspace 项目

在含 pnpm-workspace.yaml 的仓库根目录执行；该深度列出项目本身，用于核对名称与版本。

```bash
pnpm -r list --depth -1
```

### 诊断 · 检查 workspace 配置与相关清单

packages/consumer 与 packages/internal-package 都是占位目录，应换成报错中的依赖方与提供方路径。

```bash
cat pnpm-workspace.yaml
cat packages/consumer/package.json
cat packages/internal-package/package.json
```

### 修复 · 修正清单后同步并审查锁文件

先手动确认正确的包名与兼容范围；此命令会更新锁文件及可能的清单，不写 node_modules。

```bash
pnpm install --lockfile-only
git diff -- pnpm-lock.yaml ':(glob)**/package.json'
```

## 边界与注意事项

- 此错误专指 workspace 内部匹配，不等同于 registry 上没有某个版本。
- 不要为回避报错直接移除 workspace:；这可能让内部依赖解析成 registry 上的同名包。
- workspace:* 有明确语义，应在项目确实接受本地任意版本时才使用。

## 官方依据

- [pnpm 10.x — workspace version error](https://pnpm.io/10.x/errors#err_pnpm_no_matching_version_inside_workspace)
- [pnpm 10.x — Workspace protocol](https://pnpm.io/10.x/workspaces)
- [pnpm 10.x — list depth and recursive options](https://pnpm.io/10.x/cli/list)

[返回分类索引](../INDEX.md)
