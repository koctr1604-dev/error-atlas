# Read-only file system

**Docker / Linux filesystem** · 权限 / 身份 · `docker-read-only-filesystem`

应用试图写入只读文件系统；普通 chmod 或更换文件所有者不能让只读挂载变成可写。Docker 中应先分辨是单个挂载只读，还是容器根文件系统只读。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `EROFS: read-only file system`
- `touch: cannot touch: Read-only file system`
- `容器写入只读文件系统`

## 确认原因，再修复

### 1. 失败路径位于 bind mount 中

**原因：** 该挂载可能设置了 readonly/:ro，应用却把配置或输出写入其中。

**确认：** 在 docker inspect 的 Mounts 中匹配实际 Destination，并检查 RW 是否为 false。

**修复：** 优先把输出改到专门的可写目录；确实需要写回主机且已授权时，仅调整该挂载的只读配置并按部署流程应用。

### 2. 多个根文件系统路径都无法写入

**原因：** 容器可能通过 --read-only 或等价配置启用了只读根文件系统。

**确认：** 检查 HostConfig.ReadonlyRootfs 和部署定义，并确认失败路径没有独立可写挂载。

**修复：** 保留只读根文件系统，为必要的持久数据配置 volume，为临时数据配置适合的 tmpfs，并修改应用写入位置。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 检查容器挂载与根文件系统模式

只选择所需字段，避免完整 inspect 输出环境中的凭据；比较挂载目标与实际失败路径。

```bash
# CONTAINER_NAME 是需替换的容器名或 ID
docker inspect --format '{{json .Mounts}}' CONTAINER_NAME
docker inspect --format '{{.HostConfig.ReadonlyRootfs}}' CONTAINER_NAME
```

## 边界与注意事项

- 不要为了让应用启动就移除所有只读保护；写权限应限定到必要路径。
- tmpfs 中的数据不持久化，不适合需要保留的数据。
- 若 Docker 配置显示可写，仍需检查主机底层文件系统是否只读；主机因故障转为只读时不要盲目强制重新挂载。
- 本条针对 EROFS；Permission denied/EACCES 应按身份、文件权限和安全策略另行诊断。

## 官方依据

- [Docker Docs — Bind mounts / Read-only bind mount](https://docs.docker.com/engine/storage/bind-mounts/#use-a-read-only-bind-mount)
- [Docker Docs — docker run / --read-only](https://docs.docker.com/reference/cli/docker/container/run/#mount-volume-read-only---read-only)
- [Linux man-pages — open(2) EROFS](https://man7.org/linux/man-pages/man2/open.2.html)

[返回分类索引](../INDEX.md)
