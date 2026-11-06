# SSL routines:wrong version number

**OpenSSL 3.x；curl 的 OpenSSL 后端也可能透传此信息** · TLS / 证书 · `openssl-wrong-version-number`

TLS 记录解析失败，不能仅凭这句话断定 TLS 版本太旧。应先核对目标端口、是否需要 STARTTLS，以及代理自身使用的协议。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `SSL routines::wrong version number`
- `tls_validate_record_header:wrong version number`
- `ssl3_get_record:wrong version number`

## 确认原因，再修复

### 1. 连到 HTTP 后端、其他明文服务，或 TLS 终止代理之后的端口

**原因：** 客户端期待 TLS 记录，收到的却可能是其他协议的数据；不同 OpenSSL 版本与返回内容可能报其他记录层错误。

**确认：** 对照服务的监听配置与端口说明，查看 curl -v 的实际目标及代理步骤。

**修复：** 连接服务提供的正确 TLS 入口；若原本要求加密，不应直接把目标 URL 降级为 HTTP。

### 2. SMTP 587 等通过协议命令升级 TLS 的服务

**原因：** 把 STARTTLS 端口当作连接后立即握手的隐式 TLS 端口。

**确认：** 检查服务文档明确要求 STARTTLS 还是隐式 TLS，并用对应的 -starttls 参数诊断。

**修复：** 在应用中启用该协议的 STARTTLS 流程，或使用服务明确提供的隐式 TLS 端口。

### 3. 通过代理时才出现

**原因：** 把仅支持 HTTP CONNECT 的代理地址写成 https://，使客户端对代理本身发起了不受支持的 TLS。

**确认：** 核对代理供应方提供的协议与端口；HTTPS_PROXY 表示为 HTTPS 目标选择代理，不代表代理本身一定使用 TLS。

**修复：** 按经确认的代理协议填写地址；目标站点仍保持 HTTPS 和证书校验。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 查看 TLS 连接经过的端点与代理步骤

替换域名与实际 TLS 端口；日志可能包含凭据和内部信息，分享前脱敏。

```bash
curl -vI https://service.example:443/
```

### 诊断 · 按 SMTP STARTTLS 方式诊断 587 端口

需 OpenSSL 3.0；mail.example 是占位域名。仅在服务说明要求 SMTP STARTTLS 时使用；其他协议需相应的 -starttls 值。

```bash
openssl s_client -connect mail.example:587 -starttls smtp -servername mail.example -verify_hostname mail.example -verify_return_error </dev/null
```

### 修复 · 仅在已确认 HTTP CONNECT 代理后修正代理协议

替换为组织允许的代理和目标。此命令不降低目标 HTTPS 的验证要求；如果代理要求 HTTPS，应保留其正确协议并排查别处。

```bash
curl --proxy http://proxy.example:8080 -I https://service.example/
```

## 边界与注意事项

- 报错函数名和错误号随 OpenSSL 版本变化，全文匹配可能漏检。
- 不要一见 version 就强制启用旧 TLS 或降低加密等级。
- 非 TLS 数据只是候选原因，须结合实际监听与代理配置证实。

## 官方依据

- [OpenSSL upstream issue #27293 — non-TLS server record errors](https://github.com/openssl/openssl/issues/27293)
- [OpenSSL 3.0 — openssl-s_client starttls](https://docs.openssl.org/3.0/man1/openssl-s_client/)
- [curl — proxy protocol and HTTPS_PROXY](https://curl.se/docs/manpage.html#--proxy)

[返回分类索引](../INDEX.md)
