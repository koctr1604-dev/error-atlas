# npm error ERESOLVE unable to resolve dependency tree

**npm 7+；配置与命令按 npm 11 文档审核** · 包管理 / 依赖 · `npm-eresolve-peer-dependency`

npm 无法组合出满足当前约束的依赖树，常见原因是插件要求的 peerDependencies 与宿主版本冲突。先读 Found 与 Could not resolve dependency，找出冲突双方及允许范围。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `npm ERR! ERESOLVE`
- `ERESOLVE could not resolve`
- `unable to resolve dependency tree`

## 确认原因，再修复

### 1. 升级框架或添加插件后失败

**原因：** 插件声明的 peer 范围不包含当前宿主版本；npm 7 起默认安装并处理 peer dependencies。

**确认：** 对照错误中的包版本与 peer 范围，再查看目标插件版本的官方元数据。

**修复：** 选择相互兼容的插件与宿主版本，或等待上游正式支持；更新清单后生成并审查锁文件。

### 2. 同一清单在不同机器表现不同

**原因：** npm 版本、锁文件或 strict-peer-deps 等项目配置不同，可能改变解析结果或是否把冲突作为失败。

**确认：** 核对 npm 版本、项目 .npmrc 与锁文件提交，确认 CI 和本地使用相同约定。

**修复：** 统一团队约定的 npm 版本与项目配置，再按已确认的兼容关系更新依赖。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 核对 npm 版本和 peer 严格度

在项目根目录执行；配置输出只是线索，仍需阅读完整冲突报告。

```bash
npm --version
npm config get strict-peer-deps
npm config get legacy-peer-deps
```

### 诊断 · 查询目标插件的 peer 约束

将 PLUGIN 和 VERSION 替换为错误中的真实包名与版本；作用域包名应保留 @scope/name。查询会访问当前配置的 registry。

```bash
npm view 'PLUGIN@VERSION' peerDependencies --json
```

### 诊断 · 查看已安装包为何进入当前项目

将 PACKAGE 替换为冲突包；需要已有对应的已安装依赖，首次安装失败且无 node_modules 时应直接看解析报告与清单。

```bash
npm explain 'PACKAGE'
```

## 边界与注意事项

- 不要把 --force 或忽略 peer 约束作为默认修复；安装成功并不证明运行兼容。
- ERESOLVE 不是唯一指向 peer 冲突的保证，应根据完整报告判断。
- 不要默认删除 package-lock.json；它记录了团队实际解析结果。

## 官方依据

- [npm 11 — package.json peerDependencies](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/#peerdependencies)
- [npm 11 — strict-peer-deps and legacy-peer-deps](https://docs.npmjs.com/cli/v11/using-npm/config/)
- [npm 11 — npm view](https://docs.npmjs.com/cli/v11/commands/npm-view/)
- [npm 11 — npm explain](https://docs.npmjs.com/cli/v11/commands/npm-explain/)

[返回分类索引](../INDEX.md)
