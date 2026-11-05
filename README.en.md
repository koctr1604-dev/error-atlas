# Error Atlas

**Cryptic error → likely cause → verification → scoped fix.**

A Chinese-first, source-backed reference for CI, TLS, permissions and package-manager errors. The initial catalog has 32 entries. Each includes the original error, aliases, a brief explanation, conditional causes, checks, fixes, caveats and primary sources.

[Browse the index](docs/INDEX.md) · [中文](README.md) · [Contribute](CONTRIBUTING.md)

## Use

Open `docs/index.html` in a browser for offline search. No server, account, API key, analytics or log uploads. Search data and scripts are embedded. Source links open external websites only when clicked. Content is currently in Chinese; error strings remain in their original language.

Or use Python 3.10+ with no third-party packages:

```bash
python3 scripts/catalog.py search "ERESOLVE"
python3 scripts/catalog.py search "certificate" --category tls
```

This is literal/keyword search, not an AI diagnosis engine. If a full log does not match, use the core error phrase. An error message alone does not establish a unique root cause.

## Verification and maintenance

Initial entries are `docs-reviewed`, not claimed to have been reproduced on every platform. Each has its own review date and references. `data/*.json` is the source of truth; generated Markdown and HTML must be committed with content changes.

```bash
python3 scripts/catalog.py build
python3 -m unittest discover -s tests -v
node --test tests/search.test.js
python3 scripts/catalog.py check
```

Node.js 22+ is only needed for search tests. CI validates data and generated output, not the correctness of every remediation. See [release notes](CHANGELOG.md) and [contribution policy](CONTRIBUTING.md).

Original code and explanatory content: [MIT](LICENSE). Referenced works retain their own licenses.
