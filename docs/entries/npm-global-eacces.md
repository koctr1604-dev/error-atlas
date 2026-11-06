# npm error code EACCES

**npm 全局安装；下列 prefix 修复适用于 Unix / macOS，不适用于 Windows** · 包管理 / 依赖 · `npm-global-eacces`

当前用户无权访问安装所需的路径。这里限定 npm install -g 的全局目录场景，先看报错 path，其他 EACCES 应按其具体路径单独排查。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `npm ERR! code EACCES`
- `EACCES: permission denied`
- `npm global permission denied`

## 确认原因，再修复

### 1. npm install -g 报错，path 位于系统全局 prefix 下

**原因：** 全局目录由系统或其他用户管理，当前用户没有写入权。

**确认：** 读取 npm 全局 prefix，并将其与报错 path、当前用户和目录归属对应。

**修复：** 优先按 npm 官方指南使用 Node 版本管理器；另一个选择是把全局 prefix 配到用户自己的目录，并配置 PATH。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 检查全局安装目录与当前身份

对照错误中的 path；如果出错的是缓存、项目目录或网络挂载，本条的 prefix 修复不一定适用。

```bash
npm config get prefix
id
```

### 修复 · 选择用户目录作为全局 prefix

Unix / macOS 示例；仅在选择手动 prefix 方案并确认不与现有版本管理器冲突后执行。会修改当前用户 npm 配置。

```bash
npm config set prefix ~/.local
```

### 修复 · 让当前 shell 找到用户全局命令

仅影响当前 shell；持久化时按实际 shell 将相应 PATH 设置加入用户启动文件，并先检查是否已存在。

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## 边界与注意事项

- 不要用管理员权限安装所有 npm 包来回避目录设计问题。
- 不要对 /usr、全局目录或整个项目递归开放写权限。
- 若使用版本管理器，优先依照其安装与 prefix 约定；不要叠加互相冲突的配置。

## 官方依据

- [npm — Resolving EACCES permissions errors when installing packages globally](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally/)
- [npm — Downloading and installing packages globally](https://docs.npmjs.com/downloading-and-installing-packages-globally/)

[返回分类索引](../INDEX.md)
