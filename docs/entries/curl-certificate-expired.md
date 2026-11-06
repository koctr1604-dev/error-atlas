# curl: (60) SSL certificate problem: certificate has expired

**curl 7.x / 8.x（OpenSSL 后端）** · TLS / 证书 · `curl-certificate-expired`

验证链中某张证书的 notAfter 早于客户端当前时间。先确认是哪张证书与本机时间，再决定续签、更新证书链或修正时钟。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `CERT_HAS_EXPIRED`
- `certificate has expired`
- `curl error 60 expired`

## 确认原因，再修复

### 1. 本机时间正确，错误指向站点或中间证书

**原因：** 站点证书或服务器提供的中间证书已经过期，也可能是续签后服务仍加载旧文件。

**确认：** 查看验证输出的 depth，并检查实际部署证书的起止时间；不要只看续签任务的成功日志。

**修复：** 续签对应证书或换用有效链，按服务软件要求重载证书，再检查对外监听端口实际返回的证书。

### 2. 同一服务只有一台设备报过期

**原因：** 客户端时间可能错误；证书有效期检查依赖当前时间。

**确认：** 核对 UTC 时间、时区显示及系统时间同步状态，与可信时间源比较。

**修复：** 按系统管理流程恢复正确的时间同步；若时钟正确，继续检查该客户端的信任库和所走代理。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 先核对客户端 UTC 时间

此命令只显示时间；显示正确不等于已验证时间同步来源。

```bash
date -u
```

### 诊断 · 定位线上证书链中失败的层级

需 OpenSSL 3.0；将 service.example 换成实际域名。关注 depth、subject、issuer 和过期错误；此命令不会续签证书。

```bash
openssl s_client -connect service.example:443 -servername service.example -showcerts -verify_hostname service.example -verify_return_error </dev/null
```

### 诊断 · 检查已取得的 PEM 证书有效期

替换 PEM 文件路径。只检查输入中的第一张证书；链中的其他证书需分别检查。成功读取证书时，-checkend 0 的非零状态表示已到期；另需留意读取或解析错误。

```bash
openssl x509 -in '/path/to/certificate.pem' -noout -subject -issuer -dates -checkend 0
```

## 边界与注意事项

- 过期对象可能是中间证书，不一定是站点证书。
- 不要倒调系统时钟或关闭校验来掩盖真实过期。
- 本地证书文件更新后，仍需检查负载均衡器、CDN 和每个对外节点的实际证书。

## 官方依据

- [OpenSSL 3.0 — X509 verification errors](https://docs.openssl.org/3.0/man3/X509_STORE_CTX_get_error/)
- [OpenSSL 3.0 — openssl-x509 dates and checkend](https://docs.openssl.org/3.0/man1/openssl-x509/)
- [curl — TLS Certificate Verification](https://curl.se/docs/sslcerts.html)

[返回分类索引](../INDEX.md)
