---
title: "如何搭建博客"
date: 2026-11-22T12:00:00+08:00
draft: false
description: "用 Hugo + hugo-blog-awesome 主题 + GitHub Pages 搭一个静态博客"
toc: true
tocOpen: false
tags: []
---

几年前，我就动过搭建博客的念头。
但技术不行，意愿也不够，这事始终只停在脑子里。

如今借着 AI 的帮助，总算迈出了第一步。
当务之急，是把 AI 的知识，装进自己的脑子里。

## 三要素

整个博客只有三样东西在工作：

1. **Hugo**：把 `content/` 里的 Markdown 文件变成网页。
2. **themes**：决定网页长什么样。本站用的是 `hugo-blog-awesome`。
3. **GitHub Actions 和 Pages**：`push` 之后，Github 自动跑 Hugo，把结果发布上线。

```bash
brew install hugo

brew tap dart-lang/dart
brew install sass/sass/sass
```

没有数据库，服务器依赖 Github。

## 开启新篇章

```bash
hugo new content posts/my-next-post/index.md
hugo server -D
```

也可以手动创建 markdown 文件。

第二条命令会在本地启动预览服务，打开 <http://localhost:1313/> 预览，修改保存后自动刷新。

## Markdown 就好

主题自带样式，直接写 Markdown 即可。

无序列表

- 条目 1
- 条目 2
  - 嵌套条目

有序列表:

1. 第一条
2. 第二条
3. 第三条

引用块：

> 多行引用块
>
> > 嵌套引用

特殊引用块：

> [!INFO]
> 信息
>
> > [!WARNING]
> > 警告

```diff
--- config.txt
+++ config.txt
@@ -1,5 +1,5 @@
 User=admin
-Password=oldpass
+Password=newpass
 Host=localhost
 Port=8080
```

```python
def hello():
    print("hello world")
```

| 标题 1 | 标题 2 | 标题 3 |
| ------ | ------ | ------ |
| 行 2   | 数据   | 数据   |
| 行 1   | 数据   | 数据   |

---

- [x] 已完成的任务
- [ ] 未完成的任务
