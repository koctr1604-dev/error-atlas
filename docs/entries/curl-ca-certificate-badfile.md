# curl: (77) error setting certificate file

**curl 7.x / 8.x（文件型 CA 信任库；后端行为不同）** · TLS / 证书 · `curl-ca-certificate-badfile`

curl 无法读取或加载配置的 CA 证书文件。先检查实际路径、格式与进程读取权限；这是本地信任材料加载失败，和远端证书不受信任的错误码 60 有区别。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `CURLE_SSL_CACERT_BADFILE`
- `error setting certificate verify locations`
- `curl error 77`

## 确认原因，再修复

### 1. 移动环境、容器或证书文件后出现

**原因：** --cacert、CURL_CA_BUNDLE、SSL_CERT_FILE 或构建默认路径指向不存在或不可读的文件。

**确认：** 用 curl -v 确认当前路径，并以运行 curl 的同一用户检查文件是否存在、是否可读。

**修复：** 修正为该环境真实可读的 CA 文件路径；需要修复访问权时，仅对必要文件与目录采用组织批准的最小权限。

### 2. 文件存在但仍无法加载

**原因：** 传入的可能是 DER、HTML 错误页、私钥或损坏的文件，而不是所需 PEM CA 证书。

**确认：** 使用 OpenSSL 解析证书，确认 BEGIN CERTIFICATE 格式和可信来源；多证书 bundle 要检查全部内容。

**修复：** 从可信的系统或组织渠道恢复正确 PEM CA bundle，再明确指定该文件。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 确认 curl 后端与报错路径

将域名替换为实际目标；CA 路径取决于 curl 编译后端。分享输出前脱敏。

```bash
curl -V
curl -vI https://service.example/
```

### 诊断 · 检查读取权限及第一张证书能否解析

替换全部路径，并在出错进程的同一用户环境执行。test -r 以退出码表示结果；x509 只验证 bundle 第一张证书能否解析。

```bash
ls -l '/path/to/ca-bundle.pem'
test -r '/path/to/ca-bundle.pem'
openssl x509 -in '/path/to/ca-bundle.pem' -noout -subject -issuer
```

### 修复 · 使用已修复且经核验的 CA 文件重试

替换路径与域名；适用于支持 --cacert 的后端。文件可读后若改报 60，应继续排查链、名称和有效期。

```bash
curl --cacert '/path/to/verified-ca-bundle.pem' -I https://service.example/
```

## 边界与注意事项

- CA 文件与客户端证书、客户端私钥用途不同，不要混用。
- 不要为解决读取问题递归放宽系统目录权限。
- Windows Schannel 与其他原生信任库后端的默认路径和加载行为不同，先确认 curl -V。

## 官方依据

- [libcurl — CURLE_SSL_CACERT_BADFILE (77)](https://curl.se/libcurl/c/libcurl-errors.html)
- [curl — CA trust stores and environment variables](https://curl.se/docs/sslcerts.html)
- [OpenSSL 3.0 — openssl-x509 input](https://docs.openssl.org/3.0/man1/openssl-x509/)

[返回分类索引](../INDEX.md)
