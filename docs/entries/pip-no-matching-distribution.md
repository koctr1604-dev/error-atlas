# ERROR: No matching distribution found for PACKAGE

**Python 3 + pip；诊断命令按 pip stable 文档审核** · 包管理 / 依赖 · `pip-no-matching-distribution`

pip 在当前索引和兼容性条件下没有找到满足要求的发行文件。这不等于包一定不存在：版本约束、Python 版本、平台标签、索引配置及前面的网络错误都可能影响候选集。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `Could not find a version that satisfies the requirement`
- `from versions: none`
- `Ignored the following versions that require a different python version`

## 确认原因，再修复

### 1. 日志提示 Requires-Python 或跳过不兼容 wheel

**原因：** 目标版本不支持当前 Python、解释器实现、ABI 或操作系统架构，且没有可用源码发行文件满足本次条件。

**确认：** 核对实际 Python 与 pip，读取详细日志中的跳过理由，并查看兼容标签。

**修复：** 选择项目明确支持的 Python 与包版本组合；若需源码构建，先确认上游支持及所需构建依赖。

### 2. 公开存在的包或内部包却显示无可用版本

**原因：** 包名或版本写错，或当前索引、认证、网络与 TLS 失败使 pip 没有获得候选文件。

**确认：** 用 pip index 查询当前索引，并查看错误前的连接、认证或证书信息；核对组织批准的包源与名称。

**修复：** 修正包名、版本约束或已批准索引的配置；网络与证书故障应修复其根因后再查询。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 确认实际解释器及兼容标签

python 替换为实际解释器；debug 输出格式是临时诊断接口，分享前删除本地敏感路径和配置。

```bash
python -m pip --version
python -m pip debug --verbose
```

### 诊断 · 查询当前索引中的兼容候选版本

PACKAGE 是占位包名，应替换；查询会使用当前 pip 配置与网络，私有索引日志可能含敏感地址。

```bash
python -m pip index versions 'PACKAGE' -v
```

### 诊断 · 详细检查指定约束的解析过程

替换 PACKAGE 与 VERSION，在项目虚拟环境执行。不会最终安装，但可能下载文件并调用构建后端生成元数据，因此仅检查可信包。

```bash
python -m pip install --dry-run --ignore-installed -v 'PACKAGE==VERSION'
```

## 边界与注意事项

- 不要默认忽略 Requires-Python 或强装不兼容 wheel。
- 不要为找包随意添加额外索引，尤其是内部包，以免选中其他来源的同名包。
- 日志中的 TLS 或认证错误可能比最后一行 No matching distribution 更接近根因。

## 官方依据

- [pip — install compatibility and dry-run options](https://pip.pypa.io/en/stable/cli/pip_install/)
- [pip — index versions](https://pip.pypa.io/en/stable/cli/pip_index/)
- [pip — debug compatible tags](https://pip.pypa.io/en/stable/cli/pip_debug/)
- [PyPI — Troubleshooting No matching distribution and TLS errors](https://docs.pypi.org/using-pypi/troubleshooting/)

[返回分类索引](../INDEX.md)
