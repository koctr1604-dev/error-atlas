# remote: Repository not found.

**Git / GitHub** · 权限 / 身份 · `github-repository-not-found`

目标仓库可能不存在，也可能是当前 Git 身份无权访问。私有仓库的认证问题同样会表现为找不到仓库。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `ERROR: Repository not found.`
- `fatal: repository 'https://github.com/OWNER/REPO.git/' not found`

## 确认原因，再修复

### 1. 刚设置 remote、仓库已改名或转移

**原因：** owner、仓库名或服务器地址不正确。

**确认：** 用有权访问的账户打开仓库页面，比对页面提供的 clone URL 与本地 remote。

**修复：** 修正 remote 的地址；新仓库需确认已真正创建。

### 2. 浏览器可见私有仓库，但 Git 无法读取

**原因：** 浏览器身份不一定等于 Git 身份；SSH 密钥、缓存凭据或令牌所代表的账户可能不同。

**确认：** 按 HTTPS/SSH 分别检查实际账户、令牌仓库范围和仓库成员权限；组织资源还要核查 SSO 授权。

**修复：** 使用有仓库访问权的身份，并为正确的凭据完成所需授权。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 用当前 Git 凭据只读验证目标仓库

不修改仓库；可能调用已配置的 credential helper 或交互式认证。不要把 token 写入 URL。

```bash
# 替换 OWNER/REPO；需要 SSH 时改用仓库页面提供的 SSH URL
git ls-remote https://github.com/OWNER/REPO.git HEAD
```

## 边界与注意事项

- 公开仓库可匿名读取；读取成功不能证明你拥有推送权限。
- 不要因为找不到私有仓库就修改其可见性；先核对身份与授权。
- 复制或分享 remote URL 前检查其中是否嵌入凭据。

## 官方依据

- [GitHub Docs — Troubleshooting cloning errors](https://docs.github.com/en/repositories/creating-and-managing-repositories/troubleshooting-cloning-errors#error-repository-not-found)
- [GitHub Docs — About authentication to GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github#authorizing-for-saml-single-sign-on)

[返回分类索引](../INDEX.md)
