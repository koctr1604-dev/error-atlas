# bash: ./scripts/build.sh: Permission denied

**Linux shell / execve** · 权限 / 身份 · `linux-script-execution-permission-denied`

Linux 拒绝执行该路径。常见原因包括缺少执行位、父目录不可搜索或挂载了 noexec，不能统一用提高权限解决。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `./script.sh: Permission denied`
- `exec: permission denied`
- `execve EACCES`

## 确认原因，再修复

### 1. 文件存在且可读，但对应身份没有执行权限

**原因：** 脚本缺少适用于当前用户的执行位。

**确认：** 查看当前身份和 ls -l 中的文件权限，确认该脚本确实应当被执行且由自己维护。

**修复：** 只给自己拥有的目标脚本增加必要执行位，并按项目方式保留该权限变更。

### 2. 文件有执行位，仍无法执行

**原因：** 路径某级目录缺少搜索权限，或脚本解释器自身不可访问/执行。

**确认：** 逐级检查路径权限与 shebang 指向的解释器。

**修复：** 由目录维护者补齐必要的目录搜索/解释器访问权限，或选择已授权的运行路径。

### 3. 同一文件换到某个挂载目录后才失败

**原因：** 文件系统使用 noexec 挂载选项，执行位不能覆盖此限制。

**确认：** 查看目标路径所在挂载点的实际选项。

**修复：** 在组织允许执行代码的位置构建和运行；如确需变更挂载策略，由管理员按用途调整。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 检查执行身份与脚本权限

适用于 Linux；先确认文件内容和来源可信。

```bash
# scripts/build.sh 为需替换的示例路径
id
ls -l -- ./scripts/build.sh
```

### 诊断 · 检查父目录权限和挂载选项

需系统提供 namei 和 findmnt；注意逐级目录的 x/search 权限与 noexec。

```bash
namei -l -- ./scripts/build.sh
findmnt -T ./scripts/build.sh -o TARGET,OPTIONS
```

### 修复 · 仅为自己维护的脚本补执行位

只解决该文件的 owner 执行位；不解决 noexec、目录权限、ACL 或安全模块拒绝。

```bash
# 仅当已确认缺少 owner 执行位，且自己拥有此脚本时
chmod u+x -- ./scripts/build.sh
```

## 边界与注意事项

- 不要 chmod -R 777、递归改变所有者，或默认改用 sudo 运行未知脚本。
- 显式 bash script.sh 仍会执行脚本内容，不应当用作绕过组织 noexec 策略的建议。
- 若普通权限和挂载选项均正常，继续查 ACL、SELinux/AppArmor 等策略日志；本条不穷尽所有 EACCES 来源。

## 官方依据

- [Linux man-pages — execve(2) EACCES](https://man7.org/linux/man-pages/man2/execve.2.html)

[返回分类索引](../INDEX.md)
