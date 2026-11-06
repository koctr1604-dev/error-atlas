# curl: (60) SSL certificate problem: unable to get local issuer certificate

**curl 7.x / 8.x（OpenSSL 后端；其他后端措辞可能不同）** · TLS / 证书 · `curl-unable-to-get-local-issuer`

客户端无法把收到的证书接到受信任的 CA。既可能是服务器漏发中间证书，也可能是本机缺少应信任的根证书，需要分别检查。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `CURLE_PEER_FAILED_VERIFICATION`
- `unable to get local issuer certificate`
- `curl error 60 issuer`

## 确认原因，再修复

### 1. 浏览器可访问，curl 或新容器失败

**原因：** 服务器可能只发送站点证书，缺少构建证书链需要的中间证书；浏览器成功不能证明链完整。

**确认：** 查看 s_client 的 Certificate chain、issuer 和验证错误对应的 depth，并与 CA 提供的链对照。

**修复：** 由服务端维护者部署站点证书及正确的中间证书链，再用独立客户端验证；不要把抓到的站点证书直接当根 CA。

### 2. 内部服务或经授权的企业 TLS 代理才失败

**原因：** 签发该连接证书的组织 CA 未包含在 curl 实际使用的信任库。

**确认：** 从 curl -v 输出确认 CAfile / CApath 和实际签发者，再通过组织的可信渠道核对 CA 指纹。

**修复：** 使用经核验的组织 CA 文件做本次连接，或按操作系统与 curl 后端的说明维护信任库。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 确认 TLS 后端与信任路径

将 service.example 换成实际域名；分享 verbose 输出前删除凭据、Cookie 和内部地址。HEAD 不受支持的 HTTP 状态与 TLS 验证失败应分开看。

```bash
curl -V
curl -vI https://service.example/
```

### 诊断 · 查看服务器发送的证书链并严格验证

需 OpenSSL 3.0；替换全部 service.example。OpenSSL 的默认信任库可能与 curl 不同，输出中的证书不因此获得信任。

```bash
openssl s_client -connect service.example:443 -servername service.example -showcerts -verify_hostname service.example -verify_return_error </dev/null
```

### 修复 · 仅在已核验组织 CA 后指定信任文件

替换域名和 PEM 文件路径；该文件必须能构建目标证书的可信链。此选项会改变本次连接的信任来源。

```bash
curl --cacert '/path/to/verified-ca-bundle.pem' -I https://service.example/
```

## 边界与注意事项

- 错误码 60 还包括主机名和有效期等验证失败，应以完整错误文本判断。
- 不要关闭证书校验，也不要从失败连接中下载证书后直接加入信任。
- HTTPS 代理自身与目标站点的证书验证分开，代理 CA 配置不能盲目套用于目标服务。

## 官方依据

- [curl — TLS Certificate Verification](https://curl.se/docs/sslcerts.html)
- [curl FAQ — Why do I get certificate verify failed?](https://curl.se/docs/faq.html)
- [OpenSSL 3.0 — openssl-s_client](https://docs.openssl.org/3.0/man1/openssl-s_client/)

[返回分类索引](../INDEX.md)
