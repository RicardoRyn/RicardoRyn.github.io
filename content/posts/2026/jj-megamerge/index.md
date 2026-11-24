---
title: "jj 的 megamerge 章鱼合并工作流"
date: 2026-11-24T08:45:00+08:00
draft: false
description: "翻译自 Isaac Corbrey：用一个 octopus merge 把所有在做的分支合到一起，减少冲突，降低切换任务的成本"
toc: true
tocOpen: false
tags: ["jj"]
---

megamerge 是 jj 的一种工作流。
我是从 **Isaac Corbrey** 的这篇博客中了解到的。

**原文地址：[Jujutsu megamerges for fun and profit](https://isaaccorbrey.com/notes/jujutsu-megamerges-for-fun-and-profit/)。**

本博客描述我对该工作流的理解，以及一些实际操作。

> 感谢 [c妹](https://github.com/Star0x00) 分享 Isaac 的帖子，让我朝 jj 糕手的方向又前进一步，我就说水群能学到新东西。

## 多分支场景

megamerge 只适用于多分支场景。

假设你在一个项目中，同时进行 3 件事情：

- 开发新特性
- 修复某个 bug
- 审查某个 PR

为了区分这些工作场景，我们往往会新建 3 个分支（jj 意义上的分支，并不一定需要设置 bookmark）来各司其职。例如：

{{< ansi "log/log1.ansi" >}}

这样做的痛点有：

- 做不同的工作时，需要频繁在多个分支间切换。
- 可能积累大量冲突并需要在最终合并时全部解决。
- 一些临时工作也需要额外管理。

所以 megamerge 从另一个角度来解决这些痛点。

## 章鱼合并

三个或更多父提交的 merge commit，我们称为 octopus merge（章鱼合并）。

> 非正式称呼。

如上述的三分支工作，可以通过 `jj new k z v` 进行章鱼合并，合并得到的空 change 我们可以手动添加名为“megamerge”的描述。例如：

{{< ansi "log/log2.ansi" >}}

在这个合并过程中，可能会发生冲突。
如果我们一开始就是在各个分支上进行了大量的工作，每个分支可能有更多的 change，那这种冲突可能更加难以解决。例如：

{{< ansi "log/log3.ansi" >}}

而 megamerge 的核心思想，**应该**就是利用 octopus merge 将多个独立工作分支的 tip 汇集到一个共同的 merge change 中，并始终在这个 megamerge 上方的 working copy 中进行开发。

当产生新的修改时，再根据修改所属的任务，将其整理回对应的工作分支。这样既能在一个统一的工作环境中协同开发，又能保持各个任务的提交历史相互独立。

> 为什么要加“应该”呢？因为这是我的个人观点。:)

## megamerge

还是上面三分支的例子，我们知道未来有不同的工作（新特性、修 bug 和审查 PR）。

但是我们还没有动手开始做，于是我们可以事先创建一个章鱼合并的 change，写上描述，只是并不实际改动文件。例如：

{{< ansi "log/log4.ansi" >}}

然后我们只需要在 megamerge change 之后，也就是当前名为 `zw` 的 change 上做我们的修改。

如果我先开始修 bug，并完成了部分任务，于是想将这些修改合并到 `v` 这个 change 中。
只需要执行：`jj squash -t v`。当前修改就 squash 进了 `v` 这个 change 中。

{{< ansi "log/log5.ansi" >}}

然后我又想执行一些开发新特性的工作，并想将这些更改合并到 `k` 这个 change 中。
同样的，执行：`jj squash -t k`。

{{< ansi "log/log6.ansi" >}}

冲突了！很合理。

megamerge 工作流不会消灭冲突，但是它不会将一大堆的冲突累积起来，留给你最后将各个分支合并的时候一次性解决。
我们知道我们刚刚改动了哪些内容，小型冲突解决起来一定会更加容易。

> 当然只要你愿意，也可以不管，jj 中冲突是一等公民。你完全可以把它晾在一边，心情好的时候再解决。:)

解决一下，恢复正常，又可以愉快地开发了。

{{< ansi "log/log7.ansi" >}}

再做个审查相关的动作。完成后执行：`jj squash -t z`

{{< ansi "log/log8.ansi" >}}

至此，3 条分支上都完成了各自的部分工作，但是我们：

- 并没有频繁地切换 change / 分支。
- 每次一点小改动产生的冲突都会被报告，因此我们可以更容易地解决冲突。

**megamerge 的基本理念已经实现。**

## 额外操作

一条分支上不能只有一个 change，如果我们想在某条分支上增加新的 change，依旧很简单。

和之前一样，我们依然在当前 working copy 上完成任务（例如我们开发了新特性 2）。

{{< ansi "log/log9.ansi" >}}

当务之急，就是将 `w` 这个 change 插入到 `k` 和 `x` 之间，也就是作为开发新特性这条分支上的第 2 个 change。

只需要执行：`jj rebase -r w -B x -A k`。其中 `-B` 表示在指定的 change 之前，`-A` 表示在指定的 change 之后。

{{< ansi "log/log10.ansi" >}}

更多的新特性呢？

{{< ansi "log/log11.ansi" >}}

只消：`jj rebase -r n::y -B x -A w`

{{< ansi "log/log12.ansi" >}}

如果我有一些临时任务，想开启一个新的分支呢？

{{< ansi "log/log13.ansi" >}}

只消：`jj rebase -r n -B x -A lw`

{{< ansi "log/log14.ansi" >}}

## 自定义命令

对于新建分支，Isaac 创建了实用的自定义命令，而无需手敲大量参数：

- `jj stack`：将指定的 change 或提交栈 rebase 到 trunk 与 megamerge 之间，使其纳入 megamerge 的集成环境。
- `jj stage`：自动选取 megamerge 上方的所有非空 change，并将它们纳入 megamerge。
- `jj restack`：将所有相关的可修改提交重新 rebase 到最新的 trunk 上，同时简化冗余的 parent 关系。

在你的 jj 配置文件中加入：

```toml
[revset-aliases]
"closest_merge(to)" = "heads(::to & merges())"

[aliases]
# `jj stack <revset>` to include specific revs
stack = ["rebase", "--after", "trunk()", "--before", "closest_merge(@)", "--revision"]

# `jj stage` to include the whole stack after the megamerge
stage = ["stack", "closest_merge(@)+:: ~ empty()"]

# `jj restack` to rebase your changes onto `trunk()`
restack = ["rebase", "--onto", "trunk()", "--source", "roots(trunk()..) & mutable()", "--simplify-parents"]
```

### 自定义函数 `closest_merge`

```toml
[revset-aliases]
"closest_merge(to)" = "heads(::to & merges())"
```

定义一个名为 `closest_merge` 的 revset 函数，接收一个参数 `to`。

- `::to` 选择 to 及其所有祖先。
- `merges()` 选择所有具有多个 parent 的 merge commits。
- `&` 取交集。
- `heads()` 从结果中选出没有其他结果作为后代的提交。

总结：找到指定 change 的祖先中最近的 merge commit，通常就是 megamerge。

### stack

```toml
stack = [
    "rebase",
    "--after", "trunk()",
    "--before", "closest_merge(@)",
    "--revision"
]
```

- `--revision` 指定需要 rebase 的 change
- `--after trunk()` 将其放在 trunk 之后
- `--before closest_merge(@)` 将其放在 megamerge 之前

总结：将指定的 change 或提交栈重新安排到 trunk 与 megamerge 之间，使其成为 megamerge 的组成部分。

### stage

```toml
stage = [
    "stack",
    "closest_merge(@)+:: ~ empty()"
]
```

- `closest_merge(@)+` 找到当前 megamerge 的子提交
- `::` 选择这些子提交及其所有后代
- `~ empty()` 排除空提交

总结：选取 megamerge 上方的所有非空提交，然后将它们重新安排到 trunk 与 megamerge 之间。

### restack

```toml
restack = [
    "rebase",
    "--onto", "trunk()",
    "--source", "roots(trunk()..) & mutable()",
    "--simplify-parents"
]
```

- `--onto trunk()` 指定新的 rebase 基底为 trunk，也就是最新的主分支。
- `trunk()..` 选择不属于 trunk 及其祖先链的提交。
- `roots()` 从这些提交中选出最靠近 trunk 的根提交。
- `mutable()` 只保留允许修改的提交。
- `--simplify-parents` 简化 rebase 后的 parent 关系，去除冗余的 parent，避免提交图中保留不必要的依赖关系。

总结：将自己的可修改提交栈重新 rebase 到最新 trunk 上，并简化 parent 关系。
