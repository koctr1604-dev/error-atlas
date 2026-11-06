# TLS 与软件包条目审核记录

审核日期：2026-11-05。范围：`data/tls-packages.json` 的 16 条，TLS 8 条、packages 8 条。所有条目的 `verification` 均为 `docs-reviewed`，表示审阅来源和静态内容，**不表示已在对应软件版本、操作系统或真实网络中复现成功**。

## 来源支持关系

以下链接已通过联网检索或打开页面检查。条目内保留具体参考链接；此处记录来源支持的关键关系，便于复核，未复制长段原文。

| 条目 ID | 已检查的主要一手来源 | 审核要点 |
| --- | --- | --- |
| `curl-unable-to-get-local-issuer` | [curl TLS verification](https://curl.se/docs/sslcerts.html)、[curl FAQ](https://curl.se/docs/faq.html)、[OpenSSL 3.0 s_client](https://docs.openssl.org/3.0/man1/openssl-s_client/) | curl 信任库与服务器完整中间链是两个不同方向；浏览器成功不足以证明服务器链完整；指定 CA 前须确认其来源。 |
| `curl-certificate-expired` | [OpenSSL verification errors](https://docs.openssl.org/3.0/man3/X509_STORE_CTX_get_error/)、[OpenSSL x509](https://docs.openssl.org/3.0/man1/openssl-x509/) | notAfter 相对当前时间；检查失败 depth；`-dates`、`-checkend` 的用途，且单次 x509 只检查一张证书。 |
| `curl-certificate-hostname-mismatch` | [curl --resolve](https://curl.se/docs/manpage.html#--resolve)、[OpenSSL verification options](https://docs.openssl.org/3.0/man1/openssl-verification-options/)、[x509](https://docs.openssl.org/3.0/man1/openssl-x509/) | URL 名称、SAN、SNI 应区分；设置 SNI 不能代替 hostname verification；--resolve 保留 URL 域名进行指定 IP 测试。 |
| `openssl-wrong-version-number` | [OpenSSL issue #27293](https://github.com/openssl/openssl/issues/27293)、[s_client STARTTLS](https://docs.openssl.org/3.0/man1/openssl-s_client/)、[curl proxy](https://curl.se/docs/manpage.html#--proxy) | upstream issue 给出非 TLS 数据触发记录层错误的具体报告；文档证实 STARTTLS 和代理协议语义。将监听端口、STARTTLS、HTTP CONNECT 代理列为待证实候选，不宣称是唯一根因。 |
| `node-self-signed-cert-in-chain` | [Node v24.20.0 errors](https://nodejs.org/download/release/v24.20.0/docs/api/errors.html)、[Node CLI extra CA](https://nodejs.org/download/release/v24.20.0/docs/api/cli.html)、[Node enterprise networking](https://nodejs.org/learn/http/enterprise-network-configuration) | 缺少可信签发者与企业 CA；额外 CA 仅启动时读取；显式 ca 会取代默认/额外 CA；未将系统信任选项当作所有 Node 版本都有的功能。 |
| `node-unable-to-verify-leaf-signature` | [Node errors](https://nodejs.org/download/release/v24.20.0/docs/api/errors.html)、[Node 22 TLS X509 errors](https://nodejs.org/download/release/latest-jod/docs/api/tls.html#x509-certificate-error-codes)、[Node CLI](https://nodejs.org/download/release/v24.20.0/docs/api/cli.html)、[s_client](https://docs.openssl.org/3.0/man1/openssl-s_client/) | 叶证书无法验证与链不完整；另检查应用显式 ca 配置。优先修复服务器中间链，不把导入站点叶证书当通用修复。 |
| `python-ssl-certificate-verify-failed` | [Python 3.13 ssl](https://docs.python.org/3.13/library/ssl.html)、[OpenSSL errors](https://docs.openssl.org/3.0/man3/X509_STORE_CTX_get_error/)、[pip HTTPS trust](https://pip.pypa.io/en/stable/topics/https-certificates/) | ssl 异常的 verify_code / verify_message、默认路径与默认安全 context；追加 CA 保留默认验证；区分标准库与第三方信任配置。 |
| `curl-ca-certificate-badfile` | [libcurl error 77](https://curl.se/libcurl/c/libcurl-errors.html)、[curl CA stores](https://curl.se/docs/sslcerts.html)、[x509 input](https://docs.openssl.org/3.0/man1/openssl-x509/) | 77 是本地 CA 读取/加载问题；60 是远端验证失败，不能混为一类；检查路径、可读性、PEM 格式。 |
| `npm-eresolve-peer-dependency` | [npm11 peerDependencies](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/#peerdependencies)、[npm11 config](https://docs.npmjs.com/cli/v11/using-npm/config/)、[view](https://docs.npmjs.com/cli/v11/commands/npm-view/)、[explain](https://docs.npmjs.com/cli/v11/commands/npm-explain/) | npm7+ peer 安装行为，strict-peer-deps；忽略 peer 不保证兼容。view 查发布元数据，explain 仅解释已安装树。 |
| `npm-global-eacces` | [npm EACCES guide](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally/)、[global installation](https://docs.npmjs.com/downloading-and-installing-packages-globally/) | 限全局 prefix 权限场景；官方推荐版本管理器，另有用户 prefix 方案；手动 prefix 示例不适用于 Windows。 |
| `npm-ci-lockfile-mismatch` | [npm11 ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/) | 清单与锁文件必须一致；树形配置应一致；ci 删除 node_modules 但不更新清单和锁文件。复验命令标为 fix 并说明会安装和执行脚本。 |
| `pnpm-outdated-lockfile` | [pnpm10 errors](https://pnpm.io/10.x/errors#err_pnpm_outdated_lockfile)、[pnpm10 install](https://pnpm.io/10.x/cli/install) | 有锁文件时 CI 默认冻结；开发环境同步并审查；`--lockfile-only` 可能更新 package.json，明确提示副作用。 |
| `pnpm-workspace-version-missing` | [pnpm10 errors](https://pnpm.io/10.x/errors#err_pnpm_no_matching_version_inside_workspace)、[workspace protocol](https://pnpm.io/10.x/workspaces)、[list](https://pnpm.io/10.x/cli/list) | workspace: 必须解析本地匹配版本，不能回退 registry；深度 -1 用于列项目。范围限定为同名本地包版本不匹配，不把完全缺包的另一个错误码混入。 |
| `pip-externally-managed-environment` | [Packaging specification](https://packaging.python.org/en/latest/specifications/externally-managed-environments/)、[Python venv](https://docs.python.org/3.13/library/venv.html) | 标记文件和不在 venv 两条件共同触发；项目用 venv，系统软件依发行版方式；不推荐删除标记或覆盖保护。 |
| `pip-no-matching-distribution` | [pip install](https://pip.pypa.io/en/stable/cli/pip_install/)、[index](https://pip.pypa.io/en/stable/cli/pip_index/)、[debug](https://pip.pypa.io/en/stable/cli/pip_debug/)、[PyPI troubleshooting](https://docs.pypi.org/using-pypi/troubleshooting/) | 候选由版本约束、Requires-Python、实现/ABI/平台标签与索引共同决定；前置网络/TLS 失败会让最终信息误导；dry-run 仍可能调用元数据构建后端。 |
| `apt-no-pubkey` | [Debian12 apt-secure](https://manpages.debian.org/bookworm/apt/apt-secure.8.en.html)、[sources.list](https://manpages.debian.org/bookworm/apt/sources.list.5.en.html)、[Debian SecureApt](https://wiki.debian.org/SecureApt) | 限 Debian12/APT2.6；验证 Release 签名；Signed-By 将信任限制到仓库；operator keyring 与包管理的 keyring 目录不同；需要核对完整指纹。 |

## 限制与版本边界

- TLS 的完整英文信息会随 curl 后端、OpenSSL 版本与库封装变化。aliases 是检索辅助，不表示其中所有信息具有同一个根因；主机名、有效期、链和本地文件加载按不同层级处理。
- `s_client` 是测试工具，默认可能在验证错误后继续。因此所有连接诊断示例显式使用 `-verify_return_error`，主机名检查另加 `-verify_hostname`；不会把建立连接当成校验通过。
- `wrong version number` 的候选原因由官方 upstream issue 的具体观察和官方连接参数语义综合得出，属于排查推断；issue 不是保证该错误与某一个根因一一对应的规范。未使用原报告中的提议错误文案冒充已发布行为。
- Node 源码文档选定 v24.20.0，并辅以 Node22 TLS 文档与官方企业网络指南；未声称其为所有环境的当前版本。`NODE_EXTRA_CA_CERTS` 的启动时读取、显式 ca、setuid/file-capabilities 限制均已保留。系统 CA 功能存在版本门槛，正文没有把它作为跨版本默认命令。
- Python 标准库条目限定 3.13。`ssl.get_default_verify_paths()` 不等于 Requests 或 pip 的实际 CA 配置。Python3.13 更严格的默认策略作为限制提示，未建议关闭验证标志。
- pip 页面 `/stable/` 在检索时标题为 26.3；条目只依赖已说明的命令与兼容性规则，不宣称在本环境运行了该版本。`pip debug` 输出是官方声明的临时诊断接口。
- apt 没有提供通用导入 key 命令，因为第三方仓库的分发方式、密钥轮换和发行版支持不同。给出的恢复流程依赖仓库官方指引和独立核验指纹；不采用任意 keyserver、关闭认证或全局信任。
- `npm ci`、`pnpm install --frozen-lockfile` 与 `apt-get update` 会改变工作区或本地索引，已标为 fix 并注明副作用。`pip --dry-run` 不最终安装，但下载与元数据构建不是纯离线只读操作，已明确写出。
- 所有示例域名、文档 IP、包名大写标记与 `/path/to/...` 都在 note 中要求替换。命令为 POSIX/Bash 示例；Windows 的 venv 路径单独说明，npm prefix 的系统边界明确。

## 静态验证记录

已对 JSON 执行解析、16 个 ID 唯一性、类别数量 8+8、完整字段集合、日期与审核枚举、1–3 原因、1–3 命令、首命令为诊断、子对象字段和 HTTPS 来源地址检查；所有 Bash 示例经 `bash -n` 语法检查。未安装包、改动系统 CA、访问示例目标、导入密钥或运行故障复现，未宣称运行测试通过。

自动静态检查不能证明每个环境下的修复有效；正文把根因作为带条件的候选，并保留诊断、最小修改和副作用说明。
