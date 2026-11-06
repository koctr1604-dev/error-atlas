# npm error `npm ci` can only install packages when your package.json and package-lock.json or npm-shrinkwrap.json are in sync

**npm ci；规则按 npm 11 文档审核** · 包管理 / 依赖 · `npm-ci-lockfile-mismatch`

npm ci 要求清单与现有锁文件一致，发现差异时会退出而不会替你更新锁文件。应先确认遗漏的锁文件变更或本地与 CI 的安装配置差异。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `npm ci EUSAGE`
- `Missing from lock file`
- `Invalid: lock file`
- `npm ci lockfile out of sync`

## 确认原因，再修复

### 1. 修改 package.json 后 CI 才失败

**原因：** 未更新或未提交对应的 package-lock.json；也可能根本没有提交 ci 需要的锁文件。

**确认：** 查看清单与锁文件的 Git 差异，以及 npm ci 输出的 Missing 或 Invalid 项。

**修复：** 在开发环境用团队约定的 npm 版本执行 npm install，审查并提交清单与锁文件后再运行 CI。

### 2. 锁文件存在，但本地能装、CI 不能装

**原因：** 创建锁文件时使用了影响树形状的选项，而 CI 的 npm ci 未使用同样配置。

**确认：** 比较 npm 版本和项目 .npmrc，特别是 install-links、legacy-peer-deps 等历史配置。

**修复：** 统一已评估的项目配置并提交必要配置；若历史上忽略了 peer 约束，评估真实兼容性后修正依赖。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 查看依赖文件变更和 npm 版本

在项目根目录执行；没有工作区 diff 不代表提交历史或 CI checkout 一定正确。

```bash
npm --version
git diff -- package.json package-lock.json npm-shrinkwrap.json .npmrc
```

### 修复 · 在开发环境同步并审查依赖锁

会更新依赖文件并可能执行依赖生命周期脚本；先确认清单改动与包来源。使用团队约定的 npm 版本和配置。

```bash
npm install
git diff -- package.json package-lock.json npm-shrinkwrap.json
```

### 修复 · 修复后在可重建工作区复验 CI 安装

会删除已有 node_modules 并重新安装，还可能执行生命周期脚本；用于修复完成后的可重建工作区，不是只读检查。

```bash
npm ci
```

## 边界与注意事项

- 不要默认删除锁文件或把 CI 改成 npm install；这会改变可重复安装的约束。
- EUSAGE 也用于其他用法错误，只有完整信息符合本条时才按锁文件同步处理。
- npm ci 会移除 node_modules，但不会修改 package.json 或锁文件。

## 官方依据

- [npm 11 — npm ci description and lockfile requirements](https://docs.npmjs.com/cli/v11/commands/npm-ci/)

[返回分类索引](../INDEX.md)
