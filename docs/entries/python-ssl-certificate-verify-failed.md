# ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate

**Python 3.13 标准库 ssl；第三方 HTTP 库可能另有信任配置** · TLS / 证书 · `python-ssl-certificate-verify-failed`

Python 的证书验证失败；这里重点排查无法找到签发者的子信息。应读取 verify_code 和 verify_message，不能把所有 CERTIFICATE_VERIFY_FAILED 都当成本机缺 CA。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `SSLCertVerificationError`
- `CERTIFICATE_VERIFY_FAILED`
- `ssl.CertificateError`

## 确认原因，再修复

### 1. 新建 Python 环境或容器失败，其他环境正常

**原因：** 该解释器的 OpenSSL 默认 CA 文件或目录可能缺失、被错误环境变量覆盖，或未包含组织 CA。

**确认：** 在出错解释器中打印 OpenSSL 版本、默认验证路径与实际异常的 verify_message。

**修复：** 按解释器或系统发行方说明修复 CA 安装；内部 CA 已核验时，可在默认 context 基础上用 load_verify_locations 添加。

### 2. 多个客户端都在同一站点失败

**原因：** 服务端可能缺少必要的中间证书，而非 Python 安装损坏。

**确认：** 检查服务端发送的链，与 CA 提供的中间证书链对照。

**修复：** 由服务端维护者部署正确中间链；不要以更换客户端信任库代替服务端修复。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 确认实际解释器和默认验证路径

python 应替换为实际运行应用的解释器；路径为 None 是线索，不单独证明全部系统信任库不可用。

```bash
python -c "import sys, ssl; print(sys.executable); print(ssl.OPENSSL_VERSION); print(ssl.get_default_verify_paths())"
```

### 诊断 · 使用默认安全 context 读取精确验证错误

将 service.example 替换为实际域名。此探测直连目标，不自动复用应用的 HTTP 代理或第三方库配置。

```bash
python - <<'PY'
import socket, ssl
host = 'service.example'
try:
    with socket.create_connection((host, 443), timeout=10) as raw:
        with ssl.create_default_context().wrap_socket(raw, server_hostname=host) as tls:
            print(tls.version())
except ssl.SSLCertVerificationError as exc:
    print(exc.verify_code, exc.verify_message)
    raise SystemExit(1)
PY
```

### 修复 · 在默认信任基础上添加已核验 CA 的代码模板

这是 Python 代码模板，不是 shell 命令；替换 CA 文件路径并按客户端 API 接入。保留默认主机名及证书验证。

```text
import ssl
context = ssl.create_default_context()
context.load_verify_locations(cafile='/path/to/verified-company-ca.pem')
# 将 context 传给应用所用客户端支持的 SSLContext 参数。
```

## 边界与注意事项

- Requests、pip 等工具可能使用独立 CA 设置，标准库的路径不能直接代表它们。
- 同类异常也可由名称不符、过期或证书格式策略导致，应以 verify_message 分流。
- Python 3.13 默认验证更严格；不要默认降低验证标志，应修复不合规证书。

## 官方依据

- [Python 3.13 — ssl exceptions, contexts and verification paths](https://docs.python.org/3.13/library/ssl.html)
- [OpenSSL 3.0 — issuer certificate verification errors](https://docs.openssl.org/3.0/man3/X509_STORE_CTX_get_error/)
- [pip — HTTPS Certificates and distinct CA configuration](https://pip.pypa.io/en/stable/topics/https-certificates/)

[返回分类索引](../INDEX.md)
