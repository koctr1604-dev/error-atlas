# Unrecognized named-value: 'secrets'. Located at position 1 within expression

**GitHub Actions expressions** · CI / 持续集成 · `github-actions-secrets-in-if`

在 if 条件中直接引用 secrets 会遇到上下文限制。若要按 secret 是否存在来决定步骤是否运行，可先把它映射到作业环境变量。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `Invalid workflow file secrets if`
- `secrets cannot be directly referenced in if`

## 确认原因，再修复

### 1. 步骤 if 写成 secrets.DEPLOY_TOKEN != ''

**原因：** secrets 上下文不能直接用于 if 条件。

**确认：** 定位报错的 YAML 行，确认这是步骤级 if，而非 action 的 with 或 env。

**修复：** 在该作业 env 中映射 secret，然后在步骤 if 中判断 env 对应项。

### 2. 将同样的判断移到了 jobs.<job_id>.if 后仍无效

**原因：** 作业级 if 与步骤级 if 可用的上下文不同；作业环境变量的方案不能直接搬到作业级判断。

**确认：** 按 Contexts reference 对照该 YAML 键允许的上下文。

**修复：** 将 secret 存在性判断放到步骤级；作业调度条件使用该层支持的 inputs、vars 等非敏感配置。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 修复 · 在步骤级条件中判断 secret 是否可用

只输出是否执行到此步骤，不输出凭据值。实际部署步骤仍需自行接入。

```yaml
# 放入已有 jobs.<job_id>；DEPLOY_TOKEN 是需自行配置的 secret 名
env:
  DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
steps:
  - name: Check deploy eligibility
    if: ${{ env.DEPLOY_TOKEN != '' }}
    run: echo 'Credential is available for this step.'
```

## 边界与注意事项

- 本条针对报错中明确命名 secrets 的情形；其他 named-value 需要分别检查上下文和拼写。
- 语法修好后 secret 仍可能因 fork、环境或组织策略不可用；空字符串不等于密码错误。

## 官方依据

- [GitHub Docs — Workflow syntax / Using secrets](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#example-using-secrets)
- [GitHub Docs — Contexts reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#context-availability)

[返回分类索引](../INDEX.md)
