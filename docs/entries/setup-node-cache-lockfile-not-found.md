# Some specified paths were not resolved, unable to cache dependencies.

**actions/setup-node** · CI / 持续集成 · `setup-node-cache-lockfile-not-found`

setup-node 无法从锁文件生成依赖缓存键。这通常与检出顺序或 cache-dependency-path 有关，和首次运行时正常的 cache miss 不同。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `Dependencies lock file is not found`
- `setup-node cache-dependency-path 找不到锁文件`

## 确认原因，再修复

### 1. 开启缓存后，在 checkout 之前执行 setup-node

**原因：** 生成缓存键时锁文件还不在工作区中。

**确认：** 确认 checkout 是否成功，且先于启用缓存的 setup-node 步骤执行。

**修复：** 把 checkout 放到该步骤前；若源码由其他步骤生成，确保锁文件先存在。

### 2. 项目在子目录，或显式配置了 cache-dependency-path

**原因：** 默认查找仓库根目录的锁文件；自定义路径或通配符没有匹配到工作区中的文件。

**确认：** 对照已提交文件、路径大小写和 checkout 的 path；run 步骤的 working-directory 不会重定义 action 输入路径。

**修复：** 把 cache-dependency-path 指向工作区内真实的锁文件；在本地按项目包管理器生成并提交应有的锁文件。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 确认检出的锁文件位置

只列已被 Git 跟踪的锁文件；未提交或动态生成的文件需另查。

```bash
# 在 checkout 后运行
pwd
git ls-files '*package-lock.json' '*npm-shrinkwrap.json' '*yarn.lock' '*pnpm-lock.yaml'
```

### 修复 · 修正 setup-node 的子目录锁文件输入

需先 checkout，且该文件确实存在；包管理器和锁文件应与项目一致。

```yaml
# 合并到已有 setup-node 步骤的 with 中；web 为占位子目录
with:
  cache: npm
  cache-dependency-path: web/package-lock.json
```

## 边界与注意事项

- 不要为消除此错误删除项目锁文件或临时伪造空锁文件。
- setup-node 缓存的是包管理器数据，并不缓存 node_modules，也不替代依赖安装。
- 较新版本可能自动开启 npm 缓存；应检查实际 action 版本和输入。

## 官方依据

- [actions/setup-node — Caching global packages data](https://github.com/actions/setup-node#caching-global-packages-data)
- [actions/setup-node — cache-restore.ts](https://github.com/actions/setup-node/blob/main/src/cache-restore.ts)

[返回分类索引](../INDEX.md)
