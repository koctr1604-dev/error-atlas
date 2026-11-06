# WARNING: UNPROTECTED PRIVATE KEY FILE!

**OpenSSH on Linux / macOS** · 权限 / 身份 · `ssh-private-key-permissions-too-open`

OpenSSH 发现私钥可被其他用户访问，因而拒绝使用它。应收紧具体私钥文件的访问权限，并确认它归当前用户所有。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `Permissions 0644 for 'KEY_FILE' are too open.`
- `This private key will be ignored.`
- `Load key: bad permissions`

## 确认原因，再修复

### 1. 私钥由复制、解压或共享目录导入后报错

**原因：** 文件保留了组用户或其他用户可访问的权限位。

**确认：** 查看报错中的具体私钥路径、所有者和权限；不要把 .pub 公钥当成私钥处理。

**修复：** 对自己拥有的该私钥设置仅自己可读写的权限，然后重新认证。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 查看具体私钥文件的权限

只查看元数据，不要 cat 私钥。

```bash
# /absolute/path/to/KEY_FILE 是需替换的私钥路径
ls -l -- /absolute/path/to/KEY_FILE
```

### 修复 · 限制自己拥有的单个私钥文件

仅限当前用户拥有的私钥；不递归修改目录，不处理 Windows 原生 ACL。

```bash
# 确认路径、所有者和文件系统支持 Unix 权限后执行
chmod 600 -- /absolute/path/to/KEY_FILE
```

## 边界与注意事项

- 不要给整个 .ssh 目录递归套用 600；目录需要搜索权限。
- 私钥若已经泄露给他人，收紧权限无法撤销泄露，应撤销并轮换密钥。
- Windows 原生 OpenSSH 的 ACL 排查不同，本条 chmod 示例仅适用于 Unix 权限环境。

## 官方依据

- [OpenBSD OpenSSH manual — ssh FILES](https://man.openbsd.org/ssh#FILES)
- [OpenSSH portable — authfile.c permission check](https://github.com/openssh/openssh-portable/blob/master/authfile.c)

[返回分类索引](../INDEX.md)
