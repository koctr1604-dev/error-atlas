# fatal: detected dubious ownership in repository at 'PATH'

**Git** · 权限 / 身份 · `git-dubious-ownership`

Git 发现仓库所有者与当前运行用户不一致，因此阻止读取配置和执行钩子。先确认仓库来源、实际 UID 与所有权，再决定是否信任这一具体目录。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `detected dubious ownership`
- `unsafe repository is owned by someone else`
- `safe.directory`

## 确认原因，再修复

### 1. 仓库来自其他账户、共享目录或容器挂载

**原因：** 仓库所有者与当前 Git 进程身份不同，触发了安全检查。

**确认：** 查看当前用户、仓库及 .git 的所有者；容器内外需比对数值 UID/GID，而不只看用户名。

**修复：** 优先使用仓库预期的运行身份；确属可信且有意共享的仓库，才将其精确绝对路径加入当前用户的 safe.directory。

### 2. 平时正常，换用 sudo 或另一账户后报错

**原因：** Git 的运行身份和读取到的受保护配置发生了变化。

**确认：** 确认本次运行用户和 safe.directory 的配置来源；不要假设一个账户的 global 配置会被其他账户读取。

**修复：** 恢复正确的普通用户执行方式；若所有权意外改变，先由目录维护者确认范围再处理。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 检查身份、所有者与已配置的例外

没有配置项时 git config 可能返回非零；.git 也可能是指向实际 gitdir 的文件，需按实际布局继续核查。

```bash
# 在 Linux 上运行；替换为实际仓库绝对路径
id
ls -ldn -- /absolute/path/to/repo /absolute/path/to/repo/.git
git config --global --show-origin --get-all safe.directory
```

### 修复 · 仅信任已核实的具体共享仓库

绝对路径是占位符；此配置是信任例外，不会修改目录所有权或补齐文件访问权限。

```bash
# 仅在已核实来源、内容及共享意图后执行
git config --global --add safe.directory /absolute/path/to/repo
```

## 边界与注意事项

- 不要设置 safe.directory '*' 或宽泛目录通配符来关闭所有仓库的检查。
- 不要对工作区、主目录或挂载盘整体执行递归 chown。
- 不可信仓库不应因为本条提示就获得信任；先由可信用户核查来源与配置。

## 官方依据

- [Git documentation — safe.directory](https://git-scm.com/docs/git-config#Documentation/git-config.txt-safedirectory)

[返回分类索引](../INDEX.md)
