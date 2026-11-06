"""Dependency-free catalog validation, generation and local search."""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {"ci": "CI / 持续集成", "tls": "TLS / 证书", "permissions": "权限 / 身份", "packages": "包管理 / 依赖"}
REQUIRED = {"id", "category", "tool", "error", "aliases", "summary", "causes", "commands", "cautions", "sources", "verified_on", "verification", "tags"}


def validate(entries):
    if not isinstance(entries, list) or not entries:
        raise ValueError("catalog must be a non-empty array")
    ids = set()
    for e in entries:
        if not isinstance(e, dict) or set(e) != REQUIRED:
            raise ValueError(f"entry keys must match schema: {getattr(e, 'get', lambda _: '?')('id')}")
        ident = e["id"]
        if not isinstance(ident, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", ident) or ident in ids:
            raise ValueError(f"invalid/duplicate id: {ident}")
        ids.add(ident)
        if e["category"] not in CATEGORIES:
            raise ValueError(f"unknown category: {ident}")
        for key in ("tool", "error", "summary"):
            if not isinstance(e[key], str) or not e[key].strip():
                raise ValueError(f"empty {key}: {ident}")
        if e["verification"] not in {"docs-reviewed", "reproduced"}:
            raise ValueError(f"invalid verification: {ident}")
        date = dt.date.fromisoformat(e["verified_on"])
        if date > dt.datetime.now(dt.timezone.utc).date():
            raise ValueError(f"future review date: {ident}")
        for key in ("aliases", "cautions", "tags"):
            if not isinstance(e[key], list) or any(not isinstance(s, str) or not s.strip() for s in e[key]):
                raise ValueError(f"invalid {key}: {ident}")
        if not e["tags"] or not e["causes"] or not e["sources"]:
            raise ValueError(f"missing tags/causes/sources: {ident}")
        for cause in e["causes"]:
            if set(cause) != {"when", "reason", "check", "fix"} or any(not isinstance(s, str) or not s.strip() for s in cause.values()):
                raise ValueError(f"incomplete cause: {ident}")
        if not isinstance(e["commands"], list):
            raise ValueError(f"invalid commands: {ident}")
        for cmd in e["commands"]:
            if set(cmd) != {"label", "language", "code", "kind", "note"}:
                raise ValueError(f"invalid command: {ident}")
            if cmd["kind"] not in {"diagnostic", "fix"} or cmd["language"] not in {"bash", "yaml", "text"}:
                raise ValueError(f"invalid command metadata: {ident}")
            if any(not isinstance(s, str) or not s.strip() for s in cmd.values()):
                raise ValueError(f"empty command field: {ident}")
            if re.search(r"chmod\s+(?:-[A-Za-z]+\s+)*777|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*0|strict-ssl\s+false|curl\s+-k\b|safe\.directory\s+[\"']?\*", cmd["code"]):
                raise ValueError(f"unsafe blanket fix: {ident}")
        for source in e["sources"]:
            if set(source) != {"title", "url"} or not source["title"].strip():
                raise ValueError(f"invalid source: {ident}")
            url = urlparse(source["url"])
            if url.scheme != "https" or not url.netloc or url.username or url.password:
                raise ValueError(f"source must be public HTTPS: {ident}")
    return entries


def load_entries():
    entries = []
    for path in sorted((ROOT / "data").glob("*.json")):
        entries.extend(json.loads(path.read_text(encoding="utf-8")))
    return sorted(validate(entries), key=lambda e: (list(CATEGORIES).index(e["category"]), e["id"]))


def normalize(value):
    return re.sub(r"\s+", " ", str(value).lower().replace("’", "'").replace("‘", "'").replace('“', '"').replace('”', '"')).strip()


def score(entry, query):
    q = normalize(query)
    if not q:
        return 1
    needles = [normalize(entry["error"]), *(normalize(x) for x in entry["aliases"])]
    if any(q == n for n in needles):
        return 100
    if any(len(n) >= 8 and n in q for n in needles):
        return 90
    if any(q in n for n in needles):
        return 80
    corpus = normalize(json.dumps(entry, ensure_ascii=False))
    if q in corpus:
        return 50
    words = q.split()
    return 20 if words and all(w in corpus for w in words) else 0


def markdown(entry):
    e = entry
    lines = [f"# {e['error']}", "", f"**{e['tool']}** · {CATEGORIES[e['category']]} · `{e['id']}`", "", e['summary'], "", f"核对日期：{e['verified_on']} · 验证：{'文档核对，未声称实机复现' if e['verification'] == 'docs-reviewed' else '已复现（见贡献记录）'}", ""]
    if e['aliases']:
        lines += ["## 同类报错 / 搜索词", "", *[f"- `{s}`" for s in e['aliases']], ""]
    lines += ["## 确认原因，再修复", ""]
    for i, cause in enumerate(e['causes'], 1):
        lines += [f"### {i}. {cause['when']}", "", f"**原因：** {cause['reason']}", "", f"**确认：** {cause['check']}", "", f"**修复：** {cause['fix']}", ""]
    if e['commands']:
        lines += ["## 命令 / 配置示例", "", "请先阅读对应场景和注释，替换示例路径、域名与标识符。", ""]
        for cmd in e['commands']:
            lines += [f"### {'诊断' if cmd['kind'] == 'diagnostic' else '修复'} · {cmd['label']}", "", cmd['note'], "", f"```{cmd['language']}", cmd['code'], "```", ""]
    if e['cautions']:
        lines += ["## 边界与注意事项", "", *[f"- {s}" for s in e['cautions']], ""]
    lines += ["## 官方依据", "", *[f"- [{s['title']}]({s['url']})" for s in e['sources']], "", "[返回分类索引](../INDEX.md)", ""]
    return "\n".join(lines)


def products(entries):
    outputs = {ROOT / 'docs' / 'entries' / f"{e['id']}.md": markdown(e) for e in entries}
    lines = ["# 报错索引", "", f"共 {len(entries)} 条。按报错原文、错误码或工具搜索；原因需要结合环境确认。", "", "此文件由 `python3 scripts/catalog.py build` 生成，请修改 `data/*.json`。", ""]
    for category, title in CATEGORIES.items():
        group = [e for e in entries if e['category'] == category]
        lines += [f"## {title}（{len(group)}）", "", "| 报错 | 工具 | 一句话解释 |", "| --- | --- | --- |"]
        for e in group:
            escape = lambda s: s.replace('|', '\\|').replace('\n', ' ')
            lines += [f"| [{escape(e['error'])}](entries/{e['id']}.md) | {escape(e['tool'])} | {escape(e['summary'])} |"]
        lines += ['']
    outputs[ROOT / 'docs' / 'INDEX.md'] = '\n'.join(lines)
    template = (ROOT / 'web' / 'template.html').read_text(encoding='utf-8')
    payload = json.dumps(entries, ensure_ascii=False).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    outputs[ROOT / 'docs' / 'index.html'] = template.replace('/*__SEARCH_JS__*/', (ROOT / 'web' / 'search.js').read_text()).replace('/*__APP_JS__*/', (ROOT / 'web' / 'app.js').read_text()).replace('__CATALOG_JSON__', payload)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['validate', 'build', 'check', 'search'])
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--category', choices=CATEGORIES)
    parser.add_argument('--limit', type=int, default=8)
    args = parser.parse_args()
    entries = load_entries()
    if args.action == 'search':
        found = sorted(((score(e, args.query), e) for e in entries if not args.category or e['category'] == args.category), key=lambda pair: (-pair[0], pair[1]['id']))
        for rank, e in [(r, e) for r, e in found if r][:max(0, args.limit)]:
            print(f"[{e['id']}] {e['error']}\n  {e['summary']}\n  docs/entries/{e['id']}.md\n")
        if not any(r for r, _ in found):
            print('没有匹配条目。尝试只保留错误码或报错核心短语。')
        return
    if args.action in {'build', 'check'}:
        outputs = products(entries)
        obsolete = set((ROOT / 'docs' / 'entries').glob('*.md')) - outputs.keys()
        if args.action == 'check':
            stale = [str(p.relative_to(ROOT)) for p, content in outputs.items() if not p.exists() or p.read_text(encoding='utf-8') != content]
            stale.extend(str(p.relative_to(ROOT)) for p in obsolete)
            if stale:
                raise ValueError('generated files out of date: ' + ', '.join(stale))
        else:
            for path, content in outputs.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding='utf-8')
            for path in obsolete:
                path.unlink()
    print(f'OK: {len(entries)} entries; {args.action}')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
