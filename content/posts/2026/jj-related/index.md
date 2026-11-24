---
title: "学习使用 jj"
date: 2026-11-22T12:00:00+08:00
draft: true
description: "jujutsu 的配置、日常操作、变基、拆分、回滚和冲突处理"
toc: true
tocOpen: false
tags: ["jj"]
---

我要成为 `jj` 糕手。

## 配置

先看一下配置文件在哪：

```bash
jj config path --user
```

基本配置：

```bash
# 用户名和邮箱
jj config set --user user.name "Example User"
jj config set --user user.email "user@example.com"

# 默认编辑器（值要用 TOML 字符串，所以带引号）
jj config set --user core.editor '"nvim"'

# 改了用户名或邮箱之后，用它更新已有提交的作者信息
jj metaedit --update-author
```

推送相关的配置：

```bash
# 新书签直接推送，不必额外加参数
jj config set --user git.push-new-bookmarks true
```

GPG 签名。默认用和 `user.email` 关联的那把密钥：

```bash
jj config set --user signing.behavior '"own"'
jj config set --user signing.backend '"gpg"'
```

## 常规操作

### 初始化仓库

```bash
jj git init 仓库名 --colocate # --colocate 表示 jj 和 git 共用同一个 .git 目录
jj git remote add origin git@github.com:用户名/仓库名.git
jj git remote list
```

也可以直接克隆：

```bash
jj git clone git@github.com:用户名/仓库名.git
```

### 查看提交

```bash
jj log
jj log -r ::          # 所有提交组成的链
jj log -r "heads(::)" # 各条提交线的头部

jj show @ # 当前工作副本
jj show main@origin

jj evolog # 当前 change 下经历过的所有 commit
```

### 查看操作日志

jj 会记录每一次操作，出问题可以沿着它往回找。

```bash
jj op log
jj op log --limit 2           # 最近 2 次操作
jj op log --limit 2 --summary # 每次操作对仓库的改动摘要
jj op log --limit 2 --patch   # 每次操作具体的文件改动

jj op show 操作名 # 单次操作引起的变化
jj op show 操作名 --summary
jj op show 操作名 --patch
```

### 提交

```bash
jj commit
jj commit -m "feat: 初始化仓库"
```

`jj commit` 相当于先 `jj describe` 给当前提交写描述，再 `jj new` 开一个新提交。

### 书签

书签是 jj 里对 commit 的具名引用。它对应 Git 里的分支，但两者行为不完全一样。

```bash
jj bookmark create 书签名 -r 修订名
```

推送新书签，不需要额外参数：

```bash
jj git push --bookmark 书签名
```

> 旧版本要加 `-N` / `--allow-new`，jj 0.47 起新书签默认允许推送。

推送已有的书签时，**先移动书签，再推送**：

```bash
jj bookmark move 书签名 -t 修订名 # 这里是 -t 不是 -r
jj git push
```

也可以让 jj 自动在远端建书签：

```bash
jj git push -c 修订名
```

`-c` 表示 `--change`，会在远端创建名为 `push-<修订号>` 的书签。

从远端获取更新：

```bash
jj git fetch
```

### 放弃修订

```bash
jj abandon 修订名
jj abandon 'description("Experiment")' # 只放弃描述里带 Experiment 的 change
```

如果这个修订上有书签，书签会一起被放弃。

本地删掉的书签，用这条命令同步到远端：

```bash
jj git push --deleted
```

### 合并与变基

把两条提交线合并成一个新的提交：

```bash
jj new 修订1 修订2
```

变基把一段提交从一个基点搬到另一个基点：

```bash
jj rebase -d 修订名 # -d 是 --destination
jj rebase -A 修订名 # --insert-after：插到目标修订之后
jj rebase -B 修订名 # --insert-before：插到目标修订之前
```

### 停止追踪文件

```bash
echo "rm_rjx.txt" >>.gitignore
jj file untrack rm_rjx.txt
```

> 顺序不能反。先让 Git 忽略这个文件，`jj file untrack` 才会生效。否则下一条 jj 命令会把文件重新加回来。

### 跳到某个修订

```bash
jj new 修订名
```

这条命令在指定修订之后创建一个空的子修订。你可以查看当时的状态，也可以在上面改东西。

> 如果什么都不改就离开，jj 会自动删掉这个空的子修订。

### 书签的追踪状态

书签有两种状态：

- **已追踪**：显示为 `书签名`
- **未追踪**：只显示 `书签名@origin`

已追踪的书签会在 `jj git fetch` 时自动和远端同步。新建书签并推送之后，它会自动变成已追踪。

克隆仓库或初始化 Git 仓库时，有些书签（Git 语境下的分支）默认不被追踪，需要手动打开：

```bash
jj bookmark track 书签名@origin
```

## 高级操作

### split

`jj split` 把一个修订拆成两个，会打开差异编辑器。

默认逻辑是：你选中的内容先成为一个提交，可以给它写完整描述。剩下的内容进入一个新的空描述子修订。

差异编辑器里的按键：

| 按键      | 作用           |
| --------- | -------------- |
| `F`       | 展开或折叠文件 |
| `h` / `l` | 展开或折叠区域 |
| `j` / `k` | 上下移动       |
| `<space>` | 选中区域       |
| `c`       | 保存并退出     |
| `q`       | 不保存退出     |

### squash

```bash
jj squash -i
```

`-i` 表示 `--interactive`，打开差异编辑器，把当前修订的内容合并进上一个修订。

1. 选中的区域合并到父修订中。
2. 如果全部内容都合并了，描述也会一起合并过去，并自动创建一个新的空修订。

### 恢复与回滚

```bash
jj undo # 回滚最近一次操作
jj undo # 再执行一次，继续往前回滚
```

`jj undo` 不接受操作名，它只往上退一步，多执行几次就继续往前退。

几点注意：

1. `jj undo` 回滚的是仓库状态，操作日志里的记录不会消失。
2. `jj undo` 自己也会被记进操作日志。
3. 可以连续执行，但只有第一次有意义的情况很多，后面几次只是多写日志。

要精确回滚到某一次操作，用 `jj op restore`：

```bash
jj op restore 操作名
```

它会创建一个新操作，把仓库恢复到那次操作时的状态。如果指定的是 `x`，那么 `x` 之后的所有操作都会被撤销。

> 注意区分两个命令：
> `jj undo` 回滚最近一次操作。
> `jj op restore 操作名` 回滚指定操作之后的所有操作。
> 只想撤销某一次操作、不影响其它操作，用 `jj op revert 操作名`。

回滚之前建议先看一眼当时的仓库状态：

```bash
jj log --at-op 操作名 --patch
```

### 撤销对文件的修改

```bash
jj restore README.md # 撤销单个文件的修改
jj restore           # 撤销所有文件的修改

# 把文件恢复到指定 change 的状态
jj restore -f 'description("Fix loop syntax")' hello.py # -f 表示 --from
```

## 冲突

```bash
jj new main @-
```

冲突文件里会显示这样的标记：

```text
<<<<<<< Conflict 1 of 1
%%%%%%% Changes from base to side #1
 print("Hello, world!")
+print("Hallo, Welt!")
+print("Bonjour, le monde!")
+++++++ Contents of side #2
for _ in range(10):
    print("Hello, world!")
>>>>>>> Conflict 1 of 1 ends
```

怎么读这段标记：

- `<<<<<<< Conflict 1 of 1` 是冲突开始，`>>>>>>> Conflict 1 of 1 ends` 是冲突结束。
- `%%%%%%% Changes from base to side #1` 表示下面列出的是相对 base 的改动，来自第 1 边。
- `base` 指两条分支开始分叉的那个提交。
- `side #1` 指 `jj new main @-` 里的第 1 个 change，即 `main`。
- `side #2` 指第 2 个 change，即 `@-`。
- 每一行都以 `空格`、`-`、`+` 中的一种开头，分别表示未变、删除、新增。
