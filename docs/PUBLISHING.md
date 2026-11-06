# 发布到 GitHub

当前交付是完整源码与生成文档。尚未创建或推送远程仓库。

## 首次发布

1. 在你的 GitHub 账户创建空仓库，建议名 `error-atlas`。描述可用：`Cryptic errors explained: causes, checks & fixes. CI / TLS / permissions / package managers. 中文优先。`
2. 不要勾选自动创建 README、license 或 `.gitignore`，本项目已包含这些文件。
3. 在本地解压并进入项目目录，用你自己的 Git 身份提交。以下 `YOUR_USERNAME` 是占位符，替换成你的 GitHub 用户名。

```bash
git init -b main
git add .
git commit -m "Initial release: source-backed error catalog"
git remote add origin https://github.com/YOUR_USERNAME/error-atlas.git
git push -u origin main
```

首次公开前，查看 README、许可与条目内容；推送后等待仓库内 `Validate catalog` 检查完成。此文档不表示工作流已在 GitHub 实际运行。

## 可选：开启 GitHub Pages

仓库 Settings → Pages → Build and deployment，选择 **Deploy from a branch**，分支 `main`，目录 `/docs`。入口是已生成的 `docs/index.html`；`docs/.nojekyll` 禁用不需要的 Jekyll 处理。

来源：[GitHub Pages 发布源说明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。Pages 的可用性与访问范围取决于账户和仓库设置。

页面离线也可以使用。GitHub 仓库主页打开 HTML 源码不等于运行页面；在线访问应使用 Pages 提供的 URL。

建议 topics：`troubleshooting`、`error-messages`、`devops`、`github-actions`、`tls`、`developer-tools`、`chinese`。

## 维护节奏

- 新条目先核对证据，再合并；先修错，再扩量。
- 记录实际核对日期，不承诺无人执行的自动持续更新。
- 工具重大版本变更后复查相关条目；无证据时标明待核查，不伪造“已测试”。
- 首次实机复现优先选安全、可隔离的 npm 依赖冲突和 CI 最小示例。
