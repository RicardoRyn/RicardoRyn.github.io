# RicardoRyn 的个人博客

用 [Hugo](https://gohugo.io) 生成静态网站，托管在 GitHub Pages 上。

站点地址：https://ricardoryn.github.io/

## 目录说明

| 路径 | 作用 |
| --- | --- |
| `hugo.toml` | 站点配置：站名、地址、菜单、简介、社交链接 |
| `content/posts/` | 文章，一篇一个目录（`index.md`，图片放同目录） |
| `content/pages/` | 独立页面（关于、联系） |
| `assets/sass/` | 配色覆盖（Catppuccin Latte / Mocha） |
| `assets/code-highlight.css` | 代码高亮的 token 配色，由脚本生成 |
| `scripts/gen-code-highlight.py` | 生成上面那个文件的脚本 |
| `archetypes/default.md` | 新建文章的模板 |
| `themes/hugo-blog-awesome/` | 主题，**不要直接修改** |
| `.github/workflows/hugo.yml` | 推送到 `main` 时自动构建并发布 |

## 主题来源

- 上游项目：<https://github.com/hugo-sid/hugo-blog-awesome>（MIT 许可证，见 `themes/hugo-blog-awesome/LICENSE`）
- 固定提交：`6fcfddf960a41309a6a376d513ff661ed422119a`
- 处理方式：下载该提交的源码归档后解压，删除了 `.github/`、`.devcontainer/`、`exampleSite/`、`images/` 等与本博客无关的开发文件，其余内容与上游一致。

升级主题时：下载新提交的归档，用同样的排除规则替换整个 `themes/hugo-blog-awesome/` 目录，然后更新本节记录的提交号。自己的样式都在 `assets/` 里，不会被覆盖。

## 代码高亮配色

`assets/code-highlight.css` 不要手改，用脚本重新生成：

```bash
python3 scripts/gen-code-highlight.py
```

脚本用 `hugo gen chromastyles` 取 Catppuccin Latte 和 Mocha 两套配色，然后做三件上游没做的事：

1. 暗色规则只作用在 `html.dark` 和 `prefers-color-scheme: dark` 下，不会污染亮色模式。
2. 补上 Catppuccin 主题缺失的 token（标点 `.p`、空白 `.w`、关键字值 `.kv`、杂项数字 `.mx`）。主题自带一套 Gruvbox 规则，会把这些 token 染成 `#fbf1c7`，在浅色背景下对比度只有 1.07:1，等于看不见。
3. 把对比度低于 4.5:1 的 token 沿原色相调暗或调亮，色相和饱和度保持 Catppuccin 原值。

想恢复 Catppuccin 的原始色值（会有很多 token 在浅色模式下偏淡），把脚本里的 `MIN_CONTRAST` 改成 `1` 再跑一次即可。

## 本地预览

```bash
hugo server -D
```

然后打开 <http://localhost:1313/>。`-D` 表示连草稿一起显示；保存 Markdown 后浏览器会自动刷新。按 `Ctrl+C` 停止。

检查正式构建有没有报错：

```bash
hugo build --gc --minify
```

生成结果在 `public/`（已被 .gitignore 忽略，不需要提交）。

## 写一篇新文章

```bash
hugo new content posts/my-next-post/index.md
```

打开生成的文件，把 `draft: true` 改成 `false` 才会发布。文章头部的字段：

```yaml
---
title: '文章标题'
date: 2026-11-22T12:00:00+08:00
draft: true
description: '一句话摘要，会出现在列表和 RSS 里'
toc: true
---
```

## 发布

本站用 Jujutsu（`jj`）管理版本：

```bash
jj status                     # 看改了哪些文件
jj describe -m "写一篇新文章"   # 给当前修改写说明
jj bookmark set main -r @     # 把 main 指到这次修改上
jj git push --bookmark main   # 推送到 GitHub
```

推送后 GitHub Actions 会自动构建并发布，约 1 分钟后线上更新。在仓库的 **Actions** 页可以看到每次构建的状态。

首次部署前需要在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
