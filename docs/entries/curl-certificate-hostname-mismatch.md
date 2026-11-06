# curl: (60) SSL: no alternative certificate subject name matches target hostname

**curl 7.x / 8.x（错误措辞随 TLS 后端变化）** · TLS / 证书 · `curl-certificate-hostname-mismatch`

URL 中的主机名与服务器证书允许的名称不匹配。常见于直接用 IP 访问、域名写错，或 SNI、反向代理与证书部署不一致。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `certificate subject name does not match target host name`
- `HOSTNAME_MISMATCH`
- `no alternative certificate subject name matches`

## 确认原因，再修复

### 1. 将域名改成 IP 后报错

**原因：** 证书覆盖域名，但通常不包含这个 IP 的 subjectAltName。HTTP Host 请求头不能代替 TLS 主机名验证。

**确认：** 比较 URL 主机名与证书的 subjectAltName；如果目的是测试指定后端，确认应保留哪个正式域名。

**修复：** 使用证书覆盖的正式域名；测试指定 IP 时使用 curl --resolve 保留 URL 主机名与 SNI。

### 2. 域名正确，但返回了别的站点证书

**原因：** DNS、负载均衡器或基于 SNI 的虚拟主机可能选中了错误证书。

**确认：** 带正确 -servername 和 -verify_hostname 检查连接，逐一对照域名、解析目标和证书 SAN。

**修复：** 修正 DNS、SNI 路由或证书绑定；需要新名称时申请覆盖该名称的证书。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 带正式主机名验证线上连接

需 OpenSSL 3.0；替换全部 service.example。仅设置 -servername 不等于启用主机名校验。

```bash
openssl s_client -connect service.example:443 -servername service.example -verify_hostname service.example -verify_return_error </dev/null
```

### 诊断 · 检查本地证书的 SAN 与名称匹配

替换文件路径和域名；此处只检查名称，不代替完整证书链、用途与有效期验证。

```bash
openssl x509 -in '/path/to/certificate.pem' -noout -ext subjectAltName -checkhost service.example
```

### 修复 · 测试指定 IP，同时保留域名校验

service.example 与 192.0.2.10 都是占位值；换成经确认的域名和后端 IP。该参数只影响这次 curl 请求，不修改系统 DNS。

```bash
curl --resolve service.example:443:192.0.2.10 -I https://service.example/
```

## 边界与注意事项

- 不要通过关闭校验来接受名称不符的证书。
- 通配符证书不覆盖任意层级域名，必须依据实际匹配结果判断。
- --resolve 用于明确目标的连接测试，生产修复仍应处理错误的 DNS 或证书绑定。

## 官方依据

- [curl — man page, resolve and certificate verification](https://curl.se/docs/manpage.html#--resolve)
- [OpenSSL 3.0 — hostname verification options](https://docs.openssl.org/3.0/man1/openssl-verification-options/)
- [OpenSSL 3.0 — openssl-x509 checkhost](https://docs.openssl.org/3.0/man1/openssl-x509/)

[返回分类索引](../INDEX.md)
