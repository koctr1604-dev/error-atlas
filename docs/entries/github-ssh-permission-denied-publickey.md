# git@github.com: Permission denied (publickey).

**Git / OpenSSH / GitHub** · 权限 / 身份 · `github-ssh-permission-denied-publickey`

GitHub 的 SSH 认证没有接受本次连接提供的密钥。先确认连接身份和被提供的公钥，不要只凭此信息判断仓库不存在。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `Permission denied (publickey)`
- `fatal: Could not read from remote repository.`

## 确认原因，再修复

### 1. remote 写成个人用户名@github.com，或连到了错误主机

**原因：** GitHub 的 SSH Git 连接使用 git 用户；登录名不是 GitHub 个人用户名。

**确认：** 核对 clone URL、SSH Host 别名和实际连接目标。

**修复：** 从目标仓库页面复制正确 SSH URL，修正 remote 或 SSH 配置。

### 2. 没有提供正确密钥，或密钥尚未关联目标账户

**原因：** agent 未加载预期密钥、客户端选错 identity，或 GitHub 账户没有对应公钥。

**确认：** 查看 agent 的公钥指纹及 SSH 诊断中的 Offering public key，并与 GitHub 账户中的公钥指纹核对。

**修复：** 加载或显式选择正确私钥；仅将对应公钥添加到有访问权的账户。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 检查 agent 已加载的公钥指纹

只显示指纹，不显示私钥；提示没有 agent 与没有密钥是不同状态。

```bash
ssh-add -l -E sha256
```

### 诊断 · 检查向 GitHub 提供的身份

主机若尚未受信任，应先核对 GitHub 官方主机指纹。分享诊断日志前隐藏用户名、路径和地址。

```bash
ssh -vT git@github.com
```

## 边界与注意事项

- 不要用 sudo git 改变运行身份来试图修复；它可能选用另一套密钥。
- 不要上传私钥，也不要关闭 SSH 主机校验。
- 成功认证只证明账户身份；仓库授权还需单独检查。GitHub 不提供 shell，成功测试也可能返回非零退出码。

## 官方依据

- [GitHub Docs — Error: Permission denied (publickey)](https://docs.github.com/en/authentication/troubleshooting-ssh/error-permission-denied-publickey)
- [GitHub Docs — Testing your SSH connection](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)

[返回分类索引](../INDEX.md)
