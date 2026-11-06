# ERR_PNPM_OUTDATED_LOCKFILE

**pnpm 10.x；CI 有锁文件时默认 frozen-lockfile** · 包管理 / 依赖 · `pnpm-outdated-lockfile`

本次安装需要更新 pnpm-lock.yaml，但 frozen-lockfile 禁止更新。CI 中常见于清单已修改、锁文件未同步或相关 workspace 清单没有一起提交。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `Cannot install with frozen-lockfile`
- `pnpm-lock.yaml is not up to date`
- `pnpm outdated lockfile`

## 确认原因，再修复

### 1. CI 失败，本地安装后可正常运行

**原因：** 依赖清单与锁文件不一致；本地允许更新锁文件，CI 默认冻结现有锁文件。

**确认：** 核对 pnpm 版本、根项目与 workspace 清单的改动，以及锁文件是否实际提交。

**修复：** 在开发环境使用团队约定版本同步锁文件，审查后提交，再保持 CI 的冻结安装。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 比较清单和锁文件改动

在仓库根目录执行；检查 CI 的 checkout 提交与 packageManager 约定。Git pathspec 需保留引号。

```bash
pnpm --version
git diff -- package.json pnpm-workspace.yaml pnpm-lock.yaml ':(glob)**/package.json'
```

### 修复 · 在开发工作区同步锁文件

pnpm 10.x：此选项更新锁文件与可能相关的 package.json，不写 node_modules。执行前检查清单，执行后审查差异并提交。

```bash
pnpm install --lockfile-only
git diff -- pnpm-lock.yaml package.json ':(glob)**/package.json'
```

### 修复 · 修复后在可重建工作区复验冻结安装

会安装依赖且可能触发生命周期脚本；用于修复后的复验，不是只读校验。

```bash
pnpm install --frozen-lockfile
```

## 边界与注意事项

- 不要把永久关闭 frozen-lockfile 当作默认 CI 修复。
- 不要默认删除 pnpm-lock.yaml；先保存并审查原有解析记录。
- 锁文件格式不兼容等其他错误需另行处理，不能一概归为清单没同步。

## 官方依据

- [pnpm 10.x — ERR_PNPM_OUTDATED_LOCKFILE](https://pnpm.io/10.x/errors#err_pnpm_outdated_lockfile)
- [pnpm 10.x — install, lockfile-only and frozen-lockfile](https://pnpm.io/10.x/cli/install)

[返回分类索引](../INDEX.md)
