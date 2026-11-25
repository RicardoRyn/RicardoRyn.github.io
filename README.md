# RicardoRyn 的个人博客

用 [Hugo](https://gohugo.io) 生成静态网站，托管在 GitHub Pages 上。

站点地址：https://ricardoryn.github.io/

## 目录说明

| 路径                                                            | 作用                                           |
| --------------------------------------------------------------- | ---------------------------------------------- |
| `hugo.toml`                                                     | 站点配置：站名、地址、菜单、简介、社交链接     |
| `content/posts/`                                                | 文章，一篇一个目录（`index.md`，图片放同目录） |
| `content/pages/`                                                | 独立页面（关于、联系）                         |
| `archetypes/default.md`                                         | 新建文章的模板                                 |
| `assets/sass/`、`assets/code-highlight.css`                     | 站点配色、代码块样式和语法高亮                 |
| `assets/icons/theme/`                                           | 主题切换按钮的三个 SVG 图标                    |
| `assets/js/theme.js`、`layouts/_partials/scriptsBodyStart.html` | 切换逻辑，以及加载图标和脚本的模板             |
| `themes/hugo-blog-awesome/`                                     | 主题，**不要直接修改**                         |
| `.github/workflows/hugo.yml`                                    | 推送到 `main` 时自动构建并发布                 |

## 主题

- upstream：<https://github.com/hugo-sid/hugo-blog-awesome>（MIT 许可证，见 `themes/hugo-blog-awesome/LICENSE`）
- commit：`6fcfddf960a41309a6a376d513ff661ed422119a`
- vendor：下载该提交的源码归档后解压，删除了 `.github/`、`.devcontainer/`、`exampleSite/`、`images/` 等与本博客无关的开发文件，其余内容与上游一致。

更新主题时：下载新提交的归档，用同样的排除规则替换整个 `themes/hugo-blog-awesome/` 目录，然后更新 commit。
站点保留该版本主题的布局。
禁止直接修改上游主题文件。

## 深浅色切换

浅色使用 Catppuccin Latte，深色使用 Catppuccin Mocha。代码高亮使用 Hugo Chroma 的对应配色。

点击导航栏的主题按钮，按「跟随系统 → 浅色 → 深色」循环。
跟随系统时，系统外观变化会立即生效，不用刷新。
手动选择浅色或深色后，浏览器会记住该选择。

三个图标分别是 `sun-moon.svg`（跟随系统）、`sun.svg`（浅色）和 `moon.svg`（深色），均位于 `assets/icons/theme/`，不依赖 Nerd Fonts。

## 本地预览

```bash
hugo server -D
```

预览：<http://localhost:1313/>

检查正式构建有没有报错：

```bash
hugo build --gc --minify
```

## 新建post

```bash
hugo new content posts/my-next-post/index.md
```

文章头部的字段：

```yaml
---
title: "文章标题"
date: 2026-11-22T12:00:00+08:00
draft: true
description: "一句话摘要，会出现在列表和 RSS 里"
toc: true
---
```

`draft: true` 改成 `false` 才会发布。

## 带颜色的终端输出

要保留 `jj log` 等命令的颜色，把输出存成文章目录里的 `.ansi` 文件。

```bash
jj log --color=always >content/posts/2026/my-post/log.ansi
python3 scripts/ansi-to-html.py content/posts/2026/my-post/log.ansi
rm content/posts/2026/my-post/log.ansi
```

然后在该文章里引用（无需 `.htmlfrag` 后缀）：

```text
{{< ansi "log.ansi" >}}
```

会处理 `content/` 下的所有 `.ansi` 文件，
jj 只需追踪 `*.ansi.htmlfrag` 文件。

终端颜色会映射到 Catppuccin Latte / Mocha，跟随站点深浅色切换。
超出 16 色的颜色会取最接近的色位。

## 数学公式

```yaml
---
title: '文章标题'
math: true
---
```

支持的分隔符：`$...$` 是行内公式，`$$...$$` 是块级公式。

正文里的美元符号（比如价格）要用 `\$` 转义，否则会被当成公式开头。

## 发布

推送后 GitHub Actions 会自动构建并发布。

首次部署前需要在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
