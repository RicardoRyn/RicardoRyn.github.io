# RicardoRyn 的个人博客

用 [Hugo](https://gohugo.io) 生成静态网站，托管在 GitHub Pages 上。

站点地址：https://ricardoryn.github.io/

## 目录说明

| 路径 | 作用 |
| --- | --- |
| `hugo.toml` | 站点配置：站名、地址、菜单、简介、社交链接 |
| `content/posts/` | 文章，一篇一个目录（`index.md`，图片放同目录） |
| `content/pages/` | 独立页面（关于、联系） |
| `archetypes/default.md` | 新建文章的模板 |
| `assets/sass/`、`assets/code-highlight.css` | 站点配色、代码块样式和语法高亮 |
| `assets/icons/theme/` | 主题切换按钮的三个 SVG 图标 |
| `assets/js/theme.js`、`layouts/_partials/scriptsBodyStart.html` | 切换逻辑，以及加载图标和脚本的模板 |
| `themes/hugo-blog-awesome/` | 主题，**不要直接修改** |
| `.github/workflows/hugo.yml` | 推送到 `main` 时自动构建并发布 |

## 主题来源

- 上游项目：<https://github.com/hugo-sid/hugo-blog-awesome>（MIT 许可证，见 `themes/hugo-blog-awesome/LICENSE`）
- 固定提交：`6fcfddf960a41309a6a376d513ff661ed422119a`
- 处理方式：下载该提交的源码归档后解压，删除了 `.github/`、`.devcontainer/`、`exampleSite/`、`images/` 等与本博客无关的开发文件，其余内容与上游一致。

升级主题时：下载新提交的归档，用同样的排除规则替换整个 `themes/hugo-blog-awesome/` 目录，然后更新本节记录的提交号。站点保留该版本主题的布局。自定义配色和切换功能不直接修改上游主题文件。

## 深浅色切换

浅色使用 Catppuccin Latte，深色使用 Catppuccin Mocha。代码高亮使用 Hugo Chroma 的对应配色。

点击导航栏的主题按钮，按「跟随系统 → 浅色 → 深色」循环。跟随系统时，系统外观变化会立即生效，不用刷新。手动选择浅色或深色后，浏览器会记住该选择。

三个图标分别是 `sun-moon.svg`（跟随系统）、`sun.svg`（浅色）和 `moon.svg`（深色），均位于 `assets/icons/theme/`，不依赖 Nerd Fonts。

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

推送后 GitHub Actions 会自动构建并发布。可在仓库的 **Actions** 页查看进度。

首次部署前需要在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
