# SELF_SIGNED_CERT_IN_CHAIN

**Node.js 22 / 24；NODE_EXTRA_CA_CERTS 自 v7.3.0 提供** · TLS / 证书 · `node-self-signed-cert-in-chain`

Node.js 无法把当前连接的证书链连接到受信任的签发者。企业代理或内部 CA 是常见场景，但先要确认签发者身份，不能见到自签名就自动信任。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `self signed certificate in certificate chain`
- `Node self signed certificate chain`

## 确认原因，再修复

### 1. 浏览器正常，Node 内部 HTTPS 请求失败

**原因：** Node 的信任来源与浏览器或系统可能不同，组织根 CA 未被当前 Node 进程采用。

**确认：** 记录 Node 版本，检查实际证书签发者及应用的 ca 配置，并向组织核对 CA 指纹。

**修复：** 为新启动的进程设置 NODE_EXTRA_CA_CERTS 指向经核验的 PEM CA；在支持的版本也可按官方文档使用系统信任库。

### 2. 已设置额外 CA，应用仍失败

**原因：** 变量可能在进程启动后才修改，或者应用显式 ca 选项取代了默认与额外 CA。

**确认：** 检查启动脚本、容器环境和 HTTPS Agent 的 ca 选项；确认 PEM 文件存在且可读。

**修复：** 在进程启动前设置变量并重启；若应用使用显式 ca，按应用设计提供正确且经核验的 CA 集。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 确认运行时版本

在实际运行应用的容器或终端执行，避免检查到另一套 Node。

```bash
node -p "process.version + ' / OpenSSL ' + process.versions.openssl"
```

### 诊断 · 检查链与签发者

需 OpenSSL 3.0；替换域名。此工具使用的信任库不一定与 Node 相同，输出可用于检查链和签发者。

```bash
openssl s_client -connect service.example:443 -servername service.example -showcerts -verify_hostname service.example -verify_return_error </dev/null
```

### 修复 · 为单次应用启动添加已核验的组织 CA

POSIX shell 示例；替换 CA 文件与实际应用入口。文件可含多张可信 PEM 证书；必须在 Node 启动前设置。

```bash
NODE_EXTRA_CA_CERTS='/path/to/verified-company-ca.pem' node app.js
```

## 边界与注意事项

- 不要关闭 Node 的 TLS 证书验证。
- NODE_EXTRA_CA_CERTS 对显式设置 ca 的连接不起作用；setuid 或带 Linux file capabilities 的 Node 还有额外限制。
- 错误名称不足以证明当前证书来自合法企业代理，应先通过可信渠道核对。

## 官方依据

- [Node.js v24.20.0 — OpenSSL error codes](https://nodejs.org/download/release/v24.20.0/docs/api/errors.html#openssl-error-codes)
- [Node.js v24.20.0 — NODE_EXTRA_CA_CERTS](https://nodejs.org/download/release/v24.20.0/docs/api/cli.html#node_extra_ca_certsfile)
- [Node.js Learn — Enterprise Network Configuration](https://nodejs.org/learn/http/enterprise-network-configuration)

[返回分类索引](../INDEX.md)
