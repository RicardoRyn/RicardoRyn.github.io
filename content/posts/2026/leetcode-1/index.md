---
title: "力扣第 1 题 —— 交替合并字符串"
date: 2026-11-25T08:45:00+08:00
draft: true
description: "力扣刷题记录：交替合并字符串"
toc: true
tocOpen: false
tags: ["leetcode"]
math: true
---

## 题目描述

给你两个字符串 `word1` 和 `word2`。请你从 `word1` 开始，通过交替添加字母来合并字符串。如果一个字符串比另一个字符串长，就将多出来的字母追加到合并后字符串的末尾。

返回合并后的字符串。

**示例 1：**

> 输入：`word1 = "abc", word2 = "pqr"`
>
> 输出：`"apbqcr"`

**示例 2：**

> 输入：`word1 = "ab", word2 = "pqrs"`
>
> 输出：`"apbqrs"`

**示例 3：**

> 输入：`word1 = "abcd", word2 = "pq"`
>
> 输出：`"apbqcd"`

**提示：**

- `1 <= word1.length, word2.length <= 100`
- `word1` 和 `word2` 由小写英文字母组成

## 我的答案

```python
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        len_short = min(len(word1), len(word2))
        len_long = max(len(word1), len(word2))

        if len(word1) > len(word2):
            long_word = word1
        else:
            long_word = word2

        res = ""
        for i in range(len_long):
            if i < len_short:
                res += word1[i]
                res += word2[i]
            else:
                res += long_word[i]

        return res
```

我的思路：

1. 先识别更长的字符串，并为它定义一个别名。
2. 然后算出长短两个字符串各自的长度。
3. 在 `i < len_short` 时，交替添加 `word1[i]` 和 `word2[i]`。
4. 超出较短长度后，只添加较长字符串剩下的部分。

## 学习笔记

### $O$ 是什么？

大 $O$ 记号用来描述：当**输入规模**变大时，算法消耗的时间或空间大概按什么趋势增长。

- $O(1)$：常数时间，和数据规模基本无关。
- $O(n)$：数据规模翻倍，时间大约翻倍。
- $O(n^2)$：数据规模翻倍，时间大约变成 4 倍。
- $O(n+m)$：时间和两个字符串的总长度成线性关系。

### 时间复杂度

```python
len_short = min(len(word1), len(word2))
len_long = max(len(word1), len(word2))
```

这里是 $O(1)$，因为 Python 的 `len(str)` 是 $O(1)$。

Python 的字符串对象 `str` 在内部会保存字符串长度，可以粗略理解为：

```python
class str:
    length: int
    data: ...
```

调用 `len(word1)` 时，Python 不是从头到尾数一遍字符，而是直接读取字符串对象里已经存好的长度字段。

```python
if len(word1) > len(word2):
    long_word = word1
else:
    long_word = word2
```

这里也是 $O(1)$。注意 `long_word = word1` 只是引用赋值，不复制字符串。

```python
for i in range(len_long):
    if i < len_short:
        res += word1[i]
        res += word2[i]
    else:
        res += long_word[i]
```

循环次数是 `max(n, m)`。而 $O(\max(n,m)) = O(n+m)$，因为 $\max(n,m) \leq n+m \leq 2\max(n,m)$，两者是同一个量级。

索引访问 `word1[i]`、`word2[i]`、`long_word[i]` 是 $O(1)$，判断 `i < len_short` 也是 $O(1)$。

所以如果把 `res += ...` 看作 $O(1)$，总时间就是 $O(\max(n,m)) = O(n+m)$。

### Python 字符串 `+=` 的隐藏成本

Python 中的字符串 `str` 是不可变的。

```python
res += word1[i]
```

大致相当于：

```python
res = res + word1[i]
```

它不是真的在原来的字符串后面「原地追加」，而是创建一个新字符串，把旧 `res` 的内容和新增的那个字符复制进去。

设最终结果的长度为 $k = n+m$。你的循环一共会追加 $k$ 次字符，因为每个字符都会被加一次。

如果第 1 次追加复制 1 个字符，第 2 次复制 2 个字符……第 $k$ 次复制 $k$ 个字符，那么总复制量约为：

$1 + 2 + 3 + \cdots + k = \frac{k(k+1)}{2}$

所以严格按「字符串不可变、每次拼接都复制」的模型，时间复杂度是 $O(k^2) = O((n+m)^2)$。

这就是为什么很多题解推荐这么写：

```python
res = []
res.append(...)
return "".join(res)
```

因为 `list.append` 是均摊 $O(1)$，最后 `join` 一次性构造结果，总时间稳定为 $O(n+m)$。

不过在 CPython 中，对 `res += x` 有时会有优化，实际经常接近线性。但做算法分析时，最好不要依赖这种实现细节。

### 空间复杂度

空间复杂度描述的是：**算法运行过程中额外占用多少内存，随输入规模如何增长**。

要区分两个概念：

- **总空间**：输入 + 输出 + 辅助变量。
- **辅助空间**：除输入和输出之外，额外使用的空间。

你的代码中：

```python
len_short
len_long
long_word
i
```

这些都是常数个变量，辅助空间是 $O(1)$。

`long_word = word1` 或 `long_word = word2` 只是引用，不复制整个字符串，所以不会增加 $O(n+m)$ 的额外空间。

但是结果字符串 `res` 的最终长度是 $n+m$，所以总空间是 $O(n+m)$。

因此可以说辅助空间复杂度 $O(1)$；如果算上返回结果，总空间复杂度是 $O(n+m)$。
