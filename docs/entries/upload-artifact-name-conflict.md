# Failed to CreateArtifact: Received non-retryable error: Failed request: (409) Conflict: an artifact with this name already exists on the workflow run

**actions/upload-artifact v4+** · CI / 持续集成 · `upload-artifact-name-conflict`

同一次 workflow run 中重复创建了同名 artifact。v4 及其后的实现不支持把不同上传步骤当作对同一 artifact 的追加写入。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `artifact with this name already exists`
- `upload-artifact 409 Conflict`

## 确认原因，再修复

### 1. 多个步骤或作业都上传且没有设置 name

**原因：** 它们默认都使用 artifact 这个名称；即使上传的文件名不同也会冲突。

**确认：** 检查同次运行中所有上传步骤的 name，以及先前已成功创建的 artifact。

**修复：** 合并文件后仅上传一次，或给每次上传分配不同且稳定的名称。

### 2. matrix 中每个组合都用同一个 name

**原因：** 各矩阵作业并行创建了相同的 artifact 名。

**确认：** 展开矩阵维度，确认每个有效组合是否能得到唯一名称。

**修复：** 把区分组合的 matrix 维度加入 name；下载端同步使用新名称。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 修复 · 给矩阵上传设置唯一名称

这是片段；请替换矩阵键与产物路径，并确保其他维度也不会产生重名。

```yaml
# 合并到已有 upload-artifact 步骤的 with；要求矩阵含 os 和 node
with:
  name: build-${{ matrix.os }}-node-${{ matrix.node }}
  path: dist/
```

## 边界与注意事项

- 不要把 overwrite: true 当成并行合并方案；它会删除并替换已有 artifact。
- 本条示例适用于默认归档上传；archive: false 等模式应查实际版本的名称规则。

## 官方依据

- [actions/upload-artifact — (Not) Uploading to the same artifact](https://github.com/actions/upload-artifact#not-uploading-to-the-same-artifact)

[返回分类索引](../INDEX.md)
