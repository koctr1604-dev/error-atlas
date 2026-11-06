# fatal: Authentication failed for 'https://github.com/OWNER/REPO.git/'

**Git HTTPS / GitHub.com** · 权限 / 身份 · `github-https-authentication-failed`

GitHub.com 没有接受本次 HTTPS Git 凭据。账户密码已不能用于 Git 认证，还应核对缓存凭据和令牌授权。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `Support for password authentication was removed`
- `Invalid username or token`
- `GitHub HTTPS authentication failed`

## 确认原因，再修复

### 1. 在 Git 的 Password 提示中输入了 GitHub 账户密码

**原因：** GitHub.com 的 HTTPS Git 操作需要令牌或受支持的凭据管理器登录。

**确认：** 确认 remote 使用 HTTPS，且输入的是账户密码还是令牌；不要把网页登录成功当作 Git 认证成功。

**修复：** 使用 Git Credential Manager、GitHub CLI 的受支持登录方式，或在密码提示中输入权限最小的 PAT。

### 2. 已经使用令牌，但仍失败或一直复用旧账户

**原因：** credential helper 可能缓存旧凭据；也可能令牌已失效、仓库范围或组织授权不满足要求。

**确认：** 检查系统凭据管理器中的 GitHub 账户，以及令牌有效期、目标仓库范围、所需权限和 SSO 状态。

**修复：** 通过所用凭据管理器更新对应账户的条目；必要时换用有效且仅授权目标仓库的令牌。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 使用正常凭据流程只读验证 HTTPS 访问

可能使用缓存凭据；若验证了错误账户，应先在对应凭据管理器中修正。

```bash
# 替换 OWNER/REPO；不要在 URL 中拼接用户名或 token
git ls-remote https://github.com/OWNER/REPO.git HEAD
```

## 边界与注意事项

- 不要把 PAT 写入 remote URL、脚本、终端历史或截图。
- 本条适用于 GitHub.com HTTPS；其他 Git 服务的认证策略不同。
- 认证错误、仓库读取权限和分支写入规则是不同层次的问题；更换令牌不保证能推送。

## 官方依据

- [GitHub Docs — About authentication / HTTPS](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github#https)
- [GitHub Docs — Troubleshooting HTTPS cloning errors](https://docs.github.com/en/repositories/creating-and-managing-repositories/troubleshooting-cloning-errors#https-cloning-errors)

[返回分类索引](../INDEX.md)
