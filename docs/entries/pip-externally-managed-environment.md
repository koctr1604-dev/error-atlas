# error: externally-managed-environment

**支持 PEP 668 的 pip 与带 EXTERNALLY-MANAGED 标记的 Python；示例使用 Python 3 venv** · 包管理 / 依赖 · `pip-externally-managed-environment`

当前 Python 的基础环境由系统或发行方管理，pip 被要求避免直接改动其中的软件包。通常应为项目创建虚拟环境，或为系统用途使用发行版包管理器。

核对日期：2026-11-05 · 验证：文档核对，未声称实机复现

## 同类报错 / 搜索词

- `This environment is externally managed`
- `EXTERNALLY-MANAGED`
- `PEP 668`

## 确认原因，再修复

### 1. 在系统 Python 中直接执行 pip install

**原因：** 解释器不在虚拟环境中，且标准库目录存在发行方的 EXTERNALLY-MANAGED 标记。

**确认：** 确认 sys.executable、sys.prefix / sys.base_prefix 与标记文件位置；读取发行方给出的错误指引。

**修复：** 在项目目录创建 .venv，使用其 Python 安装项目依赖；系统组件则采用发行版支持的安装方式。

### 2. 以为已启用虚拟环境，仍然遇到该错误

**原因：** 实际执行的 pip 可能来自系统环境，或脚本明确调用了系统 Python。

**确认：** 对照 python -m pip --version 与 sys.executable；确认应用启动脚本实际使用哪个解释器。

**修复：** 直接使用 .venv 的解释器调用 -m pip 和运行项目，避免 shell PATH 歧义。

## 命令 / 配置示例

请先阅读对应场景和注释，替换示例路径、域名与标识符。

### 诊断 · 确认解释器、虚拟环境状态与标记

替换为出错时实际使用的解释器。marker 存在与是否位于虚拟环境要一起判断。

```bash
python3 - <<'PY'
import pathlib, sys, sysconfig
marker = pathlib.Path(sysconfig.get_path('stdlib')) / 'EXTERNALLY-MANAGED'
print('executable:', sys.executable)
print('in_venv:', sys.prefix != sys.base_prefix)
print('marker:', marker, 'exists:', marker.exists())
PY
python3 -m pip --version
```

### 修复 · 为当前项目建立独立环境并安装依赖

POSIX shell 示例；在项目根目录执行，requirements.txt 必须是已审核的依赖文件。Windows 使用 .venv\Scripts\python.exe；若 venv 组件缺失，按发行版指引安装。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## 边界与注意事项

- 不要删除 EXTERNALLY-MANAGED 标记或默认使用覆盖系统保护的参数。
- 不要使用管理员权限运行 pip 来绕过系统包管理。
- 项目虚拟环境不要提交到 Git，应保存依赖声明与所需 Python 版本。

## 官方依据

- [Python Packaging — Externally Managed Environments specification](https://packaging.python.org/en/latest/specifications/externally-managed-environments/)
- [Python 3.13 — venv](https://docs.python.org/3.13/library/venv.html)

[返回分类索引](../INDEX.md)
