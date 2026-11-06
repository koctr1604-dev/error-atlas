# The following signatures couldn't be verified because the public key is not available: NO_PUBKEY

**Debian 12 / APT 2.6；其他发行版应查对应版本的 keyring 指引** · 包管理 / 依赖 · `apt-no-pubkey`

APT 无法使用当前允许的密钥验证仓库的 Release 签名。应确认仓库身份、发行版代号与 Signed-By 指向的 keyring，再从可信渠道恢复正确密钥。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `NO_PUBKEY`
- `GPG error: public key is not available`
- `The repository is not signed`

## 确认原因，再修复

### 1. 新增第三方仓库后 update 失败

**原因：** 未安装该仓库的官方签名 keyring，或 Signed-By 指向错误、不可被 _apt 读取的文件。

**确认：** 核对源配置的 URL、suite、Signed-By 路径和 keyring 指纹，与仓库官方安装说明比较。

**修复：** 按仓库针对当前发行版的官方步骤安装并核验 keyring，只将该仓库关联到所需密钥。

### 2. 旧系统或仓库轮换签名密钥后失败

**原因：** 本地 keyring 可能过旧，或源被错误切换到了另一个发行版或仓库。

**确认：** 核对系统 VERSION_CODENAME、源 suite 与官方密钥轮换公告；不能只依赖错误中的短 key ID。

**修复：** 通过已受信任的发行版更新或官方恢复流程更新 keyring；若源配置错误，先修正源。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 检查系统代号与源配置

只读取配置；缺少某文件时可忽略该路径错误。若没有 rg，用系统文本查看器读取 .list 与 .sources；分享前删除仓库 URL 中的凭据。

```bash
cat /etc/os-release
rg -n '^(deb |Types:|URIs:|Suites:|Signed-By:)' /etc/apt/sources.list /etc/apt/sources.list.d
```

### 诊断 · 检查指定仓库 keyring 的完整指纹

路径是占位示例，应替换为实际 Signed-By 文件；需要 GnuPG。将完整指纹与独立取得的官方公布值核对，显示出密钥不等于密钥可信。

```bash
gpg --show-keys --with-fingerprint '/etc/apt/keyrings/vendor-archive-keyring.gpg'
```

### 修复 · 修复密钥或源后更新并复验索引

会更新本地软件包索引并可能获取仓库数据；在已修复且已核验来源后执行，不安装或升级软件包。

```bash
sudo apt-get update
```

## 边界与注意事项

- 不要默认关闭仓库认证或把仓库标记为无条件可信。
- 不要只凭 NO_PUBKEY 后面的 ID 从任意 keyserver 导入密钥；必须验证仓库身份与完整指纹。
- The repository is not signed 还可能源于确实没有 Release 签名，本条只覆盖同时出现 NO_PUBKEY 的场景。
- 密钥文件需要 _apt 可读，但不应因此递归放宽系统目录权限。

## 官方依据

- [Debian bookworm — apt-secure(8)](https://manpages.debian.org/bookworm/apt/apt-secure.8.en.html)
- [Debian bookworm — sources.list(5), Signed-By](https://manpages.debian.org/bookworm/apt/sources.list.5.en.html)
- [Debian Wiki — SecureApt and NO_PUBKEY](https://wiki.debian.org/SecureApt)

[返回分类索引](../INDEX.md)
