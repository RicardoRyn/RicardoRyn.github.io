---
title: "Neovim 插件——Catppuccin"
date: 2026-11-23T18:45:00+08:00
draft: false
description: "Catppuccin 是一套柔和协调的粉彩配色主题，为 Neovim、终端及众多开发工具提供统一的视觉风格。"
tocOpen: false
toc: true
tags: ["nvim"]
---

有了博客，就想写点什么。
既然喜欢折腾 nvim，不如记录我正在使用或者曾经使用过的各种 nvim 插件，
权当消遣。

排在我 `pack.lua` 列表的第一个是 —— [catppuccin/nvim](https://github.com/catppuccin/nvim)。

## 介绍

![](https://user-images.githubusercontent.com/56817415/213472445-091e54fb-091f-4448-a631-fa6b2ba7d8a5.png)

**Catppuccin（猫布奇）**，简单来说，是一套配色主题。
复杂点说，是一套统一的颜色规范，已经被移植到大量应用程序、编辑器、终端和桌面环境中。

> 几乎就没有不支持猫布奇主题的程序了吧？点名批评 rex。

名字来源于咖啡。
Cappuccino，卡布奇诺？又多了一个不得不用的理由。
它的四套配色也采用了咖啡的名字：

- Latte 拿铁（浅色系）
- Frappé 法拉沛（深色系）
- Macchiato 玛奇朵（深色系）
- Mocha 摩卡（深色系）

本站的浅色主题就是 Latte，深色主题就是 Mocha。

## 配置

```lua
-- lua/config/pack.lua

{ src = "https://github.com/catppuccin/nvim", name = "catppuccin" },

```

仓库默认名字是 `nvim`，还是改成 `catppuccin` 做区分吧。

```lua
-- plugin/catppuccin.lua

if vim.g.vscode then
  return
end

require("mini.misc").safely("now", function()
  require("catppuccin").setup({
    flavour = "auto", -- latte, frappe, macchiato, mocha, auto
    background = {
      light = "latte",
      dark = "mocha",
    },
    transparent_background = false,
    auto_integrations = true,
  })

  vim.cmd.colorscheme("catppuccin")
  if vim.o.background == "light" then
    vim.api.nvim_set_hl(0, "CursorLine", { bg = "#dddddd" })
  end
end)
```

该插件可以根据系统环境自动切换深浅色主题。比如我的设定为：

- 浅色为 Latte
- 深色为 Mocha（还可以换成 Frappe 或者 Macchiato）

可以设置透明背景，但我觉得透明背景看的时间长了比较累，还是禁用了。

catppuccin/nvim 为大量 nvim 插件提供了集成功能。
涉及的插件列表：[lua/catppuccin/groups/integrations/](https://github.com/catppuccin/nvim/tree/main/lua/catppuccin/groups/integrations)

作为整个 nvim 最基础的核心插件之一，我没有为它设置懒加载选项。
保证它优先加载，也为其他插件的配色稳定提供基础。

Latte 配色下，当前行的高亮效果较差，与背景色的对比度不足，有时难以辨认。
为提高当前行的可见性，我将其高亮颜色自定义为 `#dddddd`。
