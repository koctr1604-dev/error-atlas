# Input required and not supplied: INPUT_NAME

**GitHub Actions / @actions/core** · CI / 持续集成 · `github-actions-required-input-missing`

action 读取某个必填输入时拿到了空值。先看冒号后的实际输入名，以及该 action 对应版本的定义。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `Input required and not supplied: token`
- `Input required and not supplied: github-token`
- `action 必填输入为空`

## 确认原因，再修复

### 1. with 缺少参数，或参数名与 action 文档不符

**原因：** 所需输入未被传给 action；相似名称的参数不能互相替代。

**确认：** 比对实际引用 ref 的 README、action.yml 和报错中的输入名，确认 with 缩进归属于正确步骤。

**修复：** 按该版本的输入名补齐 with 值；普通配置可直接传值，凭据应从 secret 引用。

### 2. with 已引用 secret，但运行时仍为空

**原因：** secret 未配置、当前环境或仓库无权使用，或触发事件不提供该 secret；可复用工作流也不会自动收到调用方 secrets。

**确认：** 检查 secret 名称、仓库/环境/组织可用范围、触发来源和显式传递关系，只检查存在性。

**修复：** 修正 secret 的可用范围或显式传递；不可信 PR 中缺失凭据时跳过特权步骤。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 只验证输入凭据是否非空

不打印 secret。检查非空不能证明其有效或拥有所需权限。

```yaml
# 放在使用该 secret 的 action 前；替换 EXAMPLE_TOKEN
- name: Check required credential
  shell: bash
  env:
    REQUIRED_INPUT: ${{ secrets.EXAMPLE_TOKEN }}
  run: |
    if [ -z "$REQUIRED_INPUT" ]; then
      echo 'Required credential is unavailable for this run.' >&2
      exit 1
    fi
```

## 边界与注意事项

- INPUT_NAME 是占位符，必须以实际错误里的名字为准。
- 不要为让输入变成非空而填入随意字符串，也不要在日志中回显凭据。
- 同样的提示可能由 action 自己生成，具体必填规则仍以其实现为准。

## 官方依据

- [actions/toolkit — core.getInput implementation](https://github.com/actions/toolkit/blob/main/packages/core/src/core.ts)
- [GitHub Docs — Using secrets in GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)

[返回分类索引](../INDEX.md)
