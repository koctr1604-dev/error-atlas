# UNABLE_TO_VERIFY_LEAF_SIGNATURE

**Node.js 22 / 24 的 TLS 与 HTTPS 客户端** · TLS / 证书 · `node-unable-to-verify-leaf-signature`

当前可用于验证的链不足以验证首张非自签名证书，常见于缺少中间证书。应先确认服务端发送的链和 Node 的 ca 配置，再判断是服务端还是客户端需要修复。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `unable to verify the first certificate`
- `unable to verify leaf signature`

## 确认原因，再修复

### 1. 多个干净环境的 Node 请求都失败

**原因：** 服务端可能仅发送叶子证书，未提供所需中间证书。

**确认：** 检查 s_client -showcerts 的证书数量和 issuer 衔接；只有一张非自签名证书是重要线索，但仍需对照正确链。

**修复：** 在 TLS 终止服务部署 CA 提供的完整中间链；重新验证对外入口。

### 2. 只有指定自定义 HTTPS Agent 的应用失败

**原因：** 显式 ca 配置可能不完整，且它会取代该连接的默认与 NODE_EXTRA_CA_CERTS 信任来源。

**确认：** 比较标准 Node 请求与应用请求，审查 Agent 或 TLS 连接的 ca 参数。

**修复：** 修正应用所使用的可信 CA 集；如无需自定义 ca，按应用设计恢复默认信任配置。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 检查服务端发送的链

需 OpenSSL 3.0；替换域名。OpenSSL 与 Node 的信任来源可能不同，不能用其中一个成功代替另一个。

```bash
openssl s_client -connect service.example:443 -servername service.example -showcerts -verify_hostname service.example -verify_return_error </dev/null
```

### 诊断 · 用默认 Node HTTPS 客户端对比

将 service.example 换成目标域名；不带应用的自定义 Agent、认证头或自建代理逻辑。连通路径不同也会影响对比。

```bash
node -e "const r = require('node:https').request('https://service.example/', {method:'HEAD'}, s => { console.log(s.statusCode); s.resume(); }); r.on('error', e => { console.error(e.code, e.message); process.exitCode = 1; }); r.end();"
```

## 边界与注意事项

- 不要把错误直接归为 npm registry 故障；此代码来自底层 TLS，许多 Node 工具都会显示。
- 把叶子证书塞进可信 CA 文件会掩盖部署问题，应优先修复链或准确的根 CA 信任。
- 未在此环境运行真实服务复现；此条依据官方错误定义与配置文档审核。

## 官方依据

- [Node.js v24.20.0 — UNABLE_TO_VERIFY_LEAF_SIGNATURE](https://nodejs.org/download/release/v24.20.0/docs/api/errors.html#unable_to_verify_leaf_signature)
- [Node.js TLS — X509 certificate error codes](https://nodejs.org/download/release/latest-jod/docs/api/tls.html#x509-certificate-error-codes)
- [Node.js v24.20.0 — explicit ca and extra CA behavior](https://nodejs.org/download/release/v24.20.0/docs/api/cli.html#node_extra_ca_certsfile)
- [OpenSSL 3.0 — openssl-s_client](https://docs.openssl.org/3.0/man1/openssl-s_client/)

[返回分类索引](../INDEX.md)
