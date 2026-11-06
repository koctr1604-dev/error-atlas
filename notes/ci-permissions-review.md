# CI 与权限条目核查

核查日期：2026-11-05。`data/ci-permissions.json` 含 8 条 `ci`、8 条 `permissions`。全部标注 `docs-reviewed`；没有在真实 GitHub runner、用户仓库或 Docker 主机上复现，不代表命令已在用户环境实测。

所有来源均通过网页工具实际打开并查看相关段落。以下只记录支持关系，不复制长段官方原文。GitHub/Git/OpenSSH 的官方源码属于一手实现依据；它们可确认错误字符串，仍应按用户实际版本核对。

| 条目 ID | 已检查的一手来源 | 支持关系 / 边界 |
| --- | --- | --- |
| `github-actions-resource-not-accessible` | [REST troubleshooting](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api#resource-not-accessible)、[workflow permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions)、[GITHUB_TOKEN tutorial](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token) | 资源不足、端点权限响应头、仓库范围、显式权限的 none 行为及 fork 降权。未提供跨仓库令牌的过宽示例。 |
| `github-actions-process-exit-code-one` | [exit codes](https://docs.github.com/en/actions/how-tos/create-and-publish-actions/set-exit-codes)、[run logs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs)、[shell semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#exit-codes-and-error-action-preference) | 非零结果只说明步骤失败；通过失败步骤日志诊断，Bash 内置 shell 的 `-e` / `pipefail` 差异。明确保留此条作为诊断导航，不声称有统一修复。 |
| `github-actions-secrets-in-if` | [secrets example](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#example-using-secrets)、[context availability](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#context-availability) | steps.if 不可直接引用 secrets，官方建议 job.env 再判断 step.if；jobs.if 的上下文列表不含 env/secrets。错误全文的行号和位置随表达式变化。 |
| `github-actions-local-action-metadata-missing` | [runner ActionManager.cs](https://github.com/actions/runner/blob/main/src/Runner.Worker/ActionManager.cs)、[local actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions#adding-an-action-from-the-same-repository)、[reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows#calling-a-reusable-workflow) | 源码含完整缺失元数据错误；`./` 取工作区路径；可复用 workflow 应在 job 层调用。本条刻意限定 `./`，未把新出现的 `$/` 引用行为混入。 |
| `setup-node-cache-lockfile-not-found` | [setup-node README](https://github.com/actions/setup-node#caching-global-packages-data)、[cache-restore.ts](https://github.com/actions/setup-node/blob/main/src/cache-restore.ts) | 源码分别给出无匹配 hash 和根目录无锁文件两种消息；README 说明根目录默认、cache-dependency-path、自动 npm 缓存和不缓存 node_modules。不是正常 cache miss。 |
| `upload-artifact-name-conflict` | [upload-artifact README](https://github.com/actions/upload-artifact#not-uploading-to-the-same-artifact) | 同 run 唯一 artifact 名、默认名冲突、矩阵命名和不可变行为；README 明确 overwrite 会先删除。409 的具体包装措辞可能随 toolkit/service 版本变化，因此采用已出现的常见形式，并以“名称已存在”作 aliases。 |
| `github-actions-artifact-v3-retired` | [GitHub Changelog](https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/)、[upload-artifact README](https://github.com/actions/upload-artifact) | 官方 changelog 确认 v3 退役后会失败，tag 不删除，GHES 不同。README 当前仍有旧的 2024-11-30 退役提示，changelog 则为 2025-01-30；数据不写日期，以免延续冲突。Missing download info 是可能变体，明确不能仅凭它推断退役。 |
| `github-actions-required-input-missing` | [toolkit core.ts](https://github.com/actions/toolkit/blob/main/packages/core/src/core.ts)、[use secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets) | core.getInput(required) 在空输入时报错；未定义 secret 为空、fork 以及复用传递限制。也检查了 [raw 源码](https://raw.githubusercontent.com/actions/toolkit/main/packages/core/src/core.ts)，避免 GitHub 页面只显示文件壳。 |
| `github-ssh-permission-denied-publickey` | [publickey troubleshooting](https://docs.github.com/en/authentication/troubleshooting-ssh/error-permission-denied-publickey)、[SSH test](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection) | git 用户、agent 指纹、实际密钥选择、关联账户、避免 sudo。SSH test 页面支持先核对主机指纹，以及 GitHub 成功认证也应退出 1。 |
| `ssh-private-key-permissions-too-open` | [OpenSSH ssh manual](https://man.openbsd.org/ssh#FILES)、[OpenSSH authfile.c](https://github.com/openssh/openssh-portable/blob/master/authfile.c) | 官方实现确认过宽文件会被忽略，manual 说明私钥不能由他人访问。仅给自己拥有的单个私钥 `chmod 600`，不递归、不覆盖 Windows ACL 语义。 |
| `github-repository-not-found` | [cloning errors](https://docs.github.com/en/repositories/creating-and-managing-repositories/troubleshooting-cloning-errors#error-repository-not-found)、[authentication](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github#authorizing-for-saml-single-sign-on) | 目标不存在或无权限、remote 拼写、实际 SSH 身份以及组织 SSO。明确浏览器与 Git 身份可能不同；公开仓库匿名读取不能证明写权限。 |
| `github-https-authentication-failed` | [HTTPS authentication](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github#https)、[HTTPS cloning](https://docs.github.com/en/repositories/creating-and-managing-repositories/troubleshooting-cloning-errors#https-cloning-errors) | GitHub.com Git 不接受账户密码、PAT/GCM/CLI 方式、缓存错误凭据，以及组织授权。没有把 token 拼入命令。 |
| `git-dubious-ownership` | [Git safe.directory](https://git-scm.com/docs/git-config#Documentation/git-config.txt-safedirectory) | 他人所有仓库的配置/钩子风险、protected configuration、精确目录例外、`*` 关闭检查。数值 UID 的排查属于由所有者检查推导的诊断建议；没有建议递归 chown。 |
| `docker-daemon-socket-permission-denied` | [Linux postinstall](https://docs.docker.com/engine/install/linux-postinstall/)、[contexts](https://docs.docker.com/engine/manage-resources/contexts/)、[context inspect CLI](https://docs.docker.com/reference/cli/docker/context/inspect/) | rootful socket 的组访问、重新登录、docker 组 root 级能力、Rootless 替代，以及 context / DOCKER_HOST 覆盖。没有把加 docker 组当成无条件复制修复。 |
| `linux-script-execution-permission-denied` | [Linux execve(2)](https://man7.org/linux/man-pages/man2/execve.2.html) | EACCES 包含路径搜索权限、文件/解释器执行位和 noexec。仅对 owner 脚本 `chmod u+x`；ACL/LSM 是超出常见原因后应继续调查的边界提示。 |
| `docker-read-only-filesystem` | [bind mount](https://docs.docker.com/engine/storage/bind-mounts/#use-a-read-only-bind-mount)、[docker run --read-only](https://docs.docker.com/reference/cli/docker/container/run/#mount-volume-read-only---read-only)、[Linux open(2)](https://man7.org/linux/man-pages/man2/open.2.html)、[container inspect](https://docs.docker.com/reference/cli/docker/container/inspect/) | EROFS 是请求写只读文件系统；区分 Mounts.RW 与 ReadonlyRootfs；保留只读根并配置必要可写 volume/tmpfs。诊断只提取字段，防止完整 inspect 暴露环境凭据。 |

## 本地验证

- JSON 已用 Python `json.loads` 解析。
- 验证 16 个唯一 kebab-case ID、分类恰好 8+8、所有 schema 字段存在且没有额外字段。
- 验证 causes 数量 1–3、commands 数量 1–3，各子字段和 language/kind 枚举正确。
- 每条日期均为 `2026-11-05`，状态均为 `docs-reviewed`。
- 未执行条目中的修复命令，也未真实触发 CI、认证或容器权限错误。

## 交付边界

示例中的仓库、RUN_ID、INPUT_NAME、密钥路径、容器名及项目目录均为明确占位符。YAML 片段的插入层级写在命令说明中，不作为完整 workflow 提供。各来源当前主分支可能继续变化；生产使用应按实际 action/runner/Git/OpenSSH/Docker 版本复核。
