# 报错索引

共 32 条。按报错原文、错误码或工具搜索；原因需要结合环境确认。

此文件由 `python3 scripts/catalog.py build` 生成，请修改 `data/*.json`。

## CI / 持续集成（8）

| 报错 | 工具 | 一句话解释 |
| --- | --- | --- |
| [This request has been automatically failed because it uses a deprecated version of actions/upload-artifact: v3](entries/github-actions-artifact-v3-retired.md) | GitHub.com Actions artifact actions | GitHub.com 已停止接受旧版 artifact action，仓库中的旧 tag 仍存在也不代表还能运行。需要按迁移说明更新上传端与下载端。 |
| [Can't find 'action.yml', 'action.yaml' or 'Dockerfile' under 'PATH'. Did you forget to run actions/checkout before running your local action?](entries/github-actions-local-action-metadata-missing.md) | GitHub Actions runner | runner 在指定的本地 action 目录中没有找到可加载的定义。提示中的 checkout 只是常见原因，还要检查路径、大小写以及是否把 workflow 当成 action 调用。 |
| [Process completed with exit code 1.](entries/github-actions-process-exit-code-one.md) | GitHub Actions | 这只是步骤返回失败状态的摘要，不能据此判断是依赖、测试、权限还是脚本错误。真正的线索通常在同一步骤更早的日志里。 |
| [Input required and not supplied: INPUT_NAME](entries/github-actions-required-input-missing.md) | GitHub Actions / @actions/core | action 读取某个必填输入时拿到了空值。先看冒号后的实际输入名，以及该 action 对应版本的定义。 |
| [Resource not accessible by integration](entries/github-actions-resource-not-accessible.md) | GitHub Actions / REST API | GitHub 拒绝了当前令牌对该 API 资源的操作。先确认实际使用的令牌、目标仓库和端点所需权限，再调整最小授权。 |
| [Unrecognized named-value: 'secrets'. Located at position 1 within expression](entries/github-actions-secrets-in-if.md) | GitHub Actions expressions | 在 if 条件中直接引用 secrets 会遇到上下文限制。若要按 secret 是否存在来决定步骤是否运行，可先把它映射到作业环境变量。 |
| [Some specified paths were not resolved, unable to cache dependencies.](entries/setup-node-cache-lockfile-not-found.md) | actions/setup-node | setup-node 无法从锁文件生成依赖缓存键。这通常与检出顺序或 cache-dependency-path 有关，和首次运行时正常的 cache miss 不同。 |
| [Failed to CreateArtifact: Received non-retryable error: Failed request: (409) Conflict: an artifact with this name already exists on the workflow run](entries/upload-artifact-name-conflict.md) | actions/upload-artifact v4+ | 同一次 workflow run 中重复创建了同名 artifact。v4 及其后的实现不支持把不同上传步骤当作对同一 artifact 的追加写入。 |

## TLS / 证书（8）

| 报错 | 工具 | 一句话解释 |
| --- | --- | --- |
| [curl: (77) error setting certificate file](entries/curl-ca-certificate-badfile.md) | curl 7.x / 8.x（文件型 CA 信任库；后端行为不同） | curl 无法读取或加载配置的 CA 证书文件。先检查实际路径、格式与进程读取权限；这是本地信任材料加载失败，和远端证书不受信任的错误码 60 有区别。 |
| [curl: (60) SSL certificate problem: certificate has expired](entries/curl-certificate-expired.md) | curl 7.x / 8.x（OpenSSL 后端） | 验证链中某张证书的 notAfter 早于客户端当前时间。先确认是哪张证书与本机时间，再决定续签、更新证书链或修正时钟。 |
| [curl: (60) SSL: no alternative certificate subject name matches target hostname](entries/curl-certificate-hostname-mismatch.md) | curl 7.x / 8.x（错误措辞随 TLS 后端变化） | URL 中的主机名与服务器证书允许的名称不匹配。常见于直接用 IP 访问、域名写错，或 SNI、反向代理与证书部署不一致。 |
| [curl: (60) SSL certificate problem: unable to get local issuer certificate](entries/curl-unable-to-get-local-issuer.md) | curl 7.x / 8.x（OpenSSL 后端；其他后端措辞可能不同） | 客户端无法把收到的证书接到受信任的 CA。既可能是服务器漏发中间证书，也可能是本机缺少应信任的根证书，需要分别检查。 |
| [SELF_SIGNED_CERT_IN_CHAIN](entries/node-self-signed-cert-in-chain.md) | Node.js 22 / 24；NODE_EXTRA_CA_CERTS 自 v7.3.0 提供 | Node.js 无法把当前连接的证书链连接到受信任的签发者。企业代理或内部 CA 是常见场景，但先要确认签发者身份，不能见到自签名就自动信任。 |
| [UNABLE_TO_VERIFY_LEAF_SIGNATURE](entries/node-unable-to-verify-leaf-signature.md) | Node.js 22 / 24 的 TLS 与 HTTPS 客户端 | 当前可用于验证的链不足以验证首张非自签名证书，常见于缺少中间证书。应先确认服务端发送的链和 Node 的 ca 配置，再判断是服务端还是客户端需要修复。 |
| [SSL routines:wrong version number](entries/openssl-wrong-version-number.md) | OpenSSL 3.x；curl 的 OpenSSL 后端也可能透传此信息 | TLS 记录解析失败，不能仅凭这句话断定 TLS 版本太旧。应先核对目标端口、是否需要 STARTTLS，以及代理自身使用的协议。 |
| [ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate](entries/python-ssl-certificate-verify-failed.md) | Python 3.13 标准库 ssl；第三方 HTTP 库可能另有信任配置 | Python 的证书验证失败；这里重点排查无法找到签发者的子信息。应读取 verify_code 和 verify_message，不能把所有 CERTIFICATE_VERIFY_FAILED 都当成本机缺 CA。 |

## 权限 / 身份（8）

| 报错 | 工具 | 一句话解释 |
| --- | --- | --- |
| [permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock](entries/docker-daemon-socket-permission-denied.md) | Docker Engine on Linux | 当前进程没有访问所选 Docker Unix socket 的权限。本条主要针对 Linux 的传统 rootful Engine；Rootless 和 Docker Desktop 的 socket 位置及授权方式可能不同。 |
| [Read-only file system](entries/docker-read-only-filesystem.md) | Docker / Linux filesystem | 应用试图写入只读文件系统；普通 chmod 或更换文件所有者不能让只读挂载变成可写。Docker 中应先分辨是单个挂载只读，还是容器根文件系统只读。 |
| [fatal: detected dubious ownership in repository at 'PATH'](entries/git-dubious-ownership.md) | Git | Git 发现仓库所有者与当前运行用户不一致，因此阻止读取配置和执行钩子。先确认仓库来源、实际 UID 与所有权，再决定是否信任这一具体目录。 |
| [fatal: Authentication failed for 'https://github.com/OWNER/REPO.git/'](entries/github-https-authentication-failed.md) | Git HTTPS / GitHub.com | GitHub.com 没有接受本次 HTTPS Git 凭据。账户密码已不能用于 Git 认证，还应核对缓存凭据和令牌授权。 |
| [remote: Repository not found.](entries/github-repository-not-found.md) | Git / GitHub | 目标仓库可能不存在，也可能是当前 Git 身份无权访问。私有仓库的认证问题同样会表现为找不到仓库。 |
| [git@github.com: Permission denied (publickey).](entries/github-ssh-permission-denied-publickey.md) | Git / OpenSSH / GitHub | GitHub 的 SSH 认证没有接受本次连接提供的密钥。先确认连接身份和被提供的公钥，不要只凭此信息判断仓库不存在。 |
| [bash: ./scripts/build.sh: Permission denied](entries/linux-script-execution-permission-denied.md) | Linux shell / execve | Linux 拒绝执行该路径。常见原因包括缺少执行位、父目录不可搜索或挂载了 noexec，不能统一用提高权限解决。 |
| [WARNING: UNPROTECTED PRIVATE KEY FILE!](entries/ssh-private-key-permissions-too-open.md) | OpenSSH on Linux / macOS | OpenSSH 发现私钥可被其他用户访问，因而拒绝使用它。应收紧具体私钥文件的访问权限，并确认它归当前用户所有。 |

## 包管理 / 依赖（8）

| 报错 | 工具 | 一句话解释 |
| --- | --- | --- |
| [The following signatures couldn't be verified because the public key is not available: NO_PUBKEY](entries/apt-no-pubkey.md) | Debian 12 / APT 2.6；其他发行版应查对应版本的 keyring 指引 | APT 无法使用当前允许的密钥验证仓库的 Release 签名。应确认仓库身份、发行版代号与 Signed-By 指向的 keyring，再从可信渠道恢复正确密钥。 |
| [npm error `npm ci` can only install packages when your package.json and package-lock.json or npm-shrinkwrap.json are in sync](entries/npm-ci-lockfile-mismatch.md) | npm ci；规则按 npm 11 文档审核 | npm ci 要求清单与现有锁文件一致，发现差异时会退出而不会替你更新锁文件。应先确认遗漏的锁文件变更或本地与 CI 的安装配置差异。 |
| [npm error ERESOLVE unable to resolve dependency tree](entries/npm-eresolve-peer-dependency.md) | npm 7+；配置与命令按 npm 11 文档审核 | npm 无法组合出满足当前约束的依赖树，常见原因是插件要求的 peerDependencies 与宿主版本冲突。先读 Found 与 Could not resolve dependency，找出冲突双方及允许范围。 |
| [npm error code EACCES](entries/npm-global-eacces.md) | npm 全局安装；下列 prefix 修复适用于 Unix / macOS，不适用于 Windows | 当前用户无权访问安装所需的路径。这里限定 npm install -g 的全局目录场景，先看报错 path，其他 EACCES 应按其具体路径单独排查。 |
| [error: externally-managed-environment](entries/pip-externally-managed-environment.md) | 支持 PEP 668 的 pip 与带 EXTERNALLY-MANAGED 标记的 Python；示例使用 Python 3 venv | 当前 Python 的基础环境由系统或发行方管理，pip 被要求避免直接改动其中的软件包。通常应为项目创建虚拟环境，或为系统用途使用发行版包管理器。 |
| [ERROR: No matching distribution found for PACKAGE](entries/pip-no-matching-distribution.md) | Python 3 + pip；诊断命令按 pip stable 文档审核 | pip 在当前索引和兼容性条件下没有找到满足要求的发行文件。这不等于包一定不存在：版本约束、Python 版本、平台标签、索引配置及前面的网络错误都可能影响候选集。 |
| [ERR_PNPM_OUTDATED_LOCKFILE](entries/pnpm-outdated-lockfile.md) | pnpm 10.x；CI 有锁文件时默认 frozen-lockfile | 本次安装需要更新 pnpm-lock.yaml，但 frozen-lockfile 禁止更新。CI 中常见于清单已修改、锁文件未同步或相关 workspace 清单没有一起提交。 |
| [ERR_PNPM_NO_MATCHING_VERSION_INSIDE_WORKSPACE](entries/pnpm-workspace-version-missing.md) | pnpm 10.x workspace: 协议 | workspace: 依赖要求本地存在匹配版本的 workspace 包，pnpm 不会回退到 registry。此条针对同名本地包的版本不满足要求，应核对依赖范围与实际清单版本。 |
