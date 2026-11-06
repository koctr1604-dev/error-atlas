# permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock

**Docker Engine on Linux** · 权限 / 身份 · `docker-daemon-socket-permission-denied`

当前进程没有访问所选 Docker Unix socket 的权限。本条主要针对 Linux 的传统 rootful Engine；Rootless 和 Docker Desktop 的 socket 位置及授权方式可能不同。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `dial unix /var/run/docker.sock: connect: permission denied`
- `Docker socket EACCES`

## 确认原因，再修复

### 1. CLI 指向本机 rootful Engine 的 /var/run/docker.sock

**原因：** 当前用户未获得 socket 所属组的访问授权，或刚变更组成员关系但会话尚未更新。

**确认：** 比对 socket 的所有者、所属组与当前进程的 id 输出；确认管理员是否已授权 Docker 使用。

**修复：** 按主机策略由管理员配置所需组授权并重新登录，或采用 Docker 官方 Rootless 方案。

### 2. 预期使用 Rootless、Desktop 或远程 Engine，却连接到 rootful socket

**原因：** Docker context 或环境选择指向了错误端点。

**确认：** 检查当前 context 及其 Docker Host，并核对 DOCKER_HOST/DOCKER_CONTEXT 是否另有覆盖。

**修复：** 选择预期且已获授权的 context，修正不需要的环境覆盖；不要通过放宽错误 socket 的权限来解决。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 检查本机 socket 与当前进程组

仅适用于错误明确指向此路径的 Linux 主机；不存在时应先核对端点，而非创建文件。

```bash
id
ls -l -- /var/run/docker.sock
```

### 诊断 · 确认当前 Docker context 的端点

环境覆盖也会影响连接；只核对相关变量，不要输出整个环境。

```bash
docker context show
docker context inspect --format '{{.Endpoints.docker.Host}}'
```

## 边界与注意事项

- docker 组通常具有主机 root 级能力，加入该组是授权决定，不是普通的无害权限修补。
- 不要 chmod 666/777 Docker socket，不要为了连通而开放未认证的 daemon TCP 端口。
- Cannot connect to the Docker daemon 也可能是服务未启动；与明确的 permission denied 分开排查。

## 官方依据

- [Docker Docs — Linux post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/)
- [Docker Docs — Docker contexts](https://docs.docker.com/engine/manage-resources/contexts/)

[返回分类索引](../INDEX.md)
