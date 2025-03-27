---
title:  "Welcome to Jekyll!"
header:
  teaser: "/assets/images/500x300.png"
categories: 
  - Jekyll
tags:
  - update
---

You'll find this post in your `_posts` directory. Go ahead and edit it and re-build the site to see your changes. You can rebuild the site in many different ways, but the most common way is to run `jekyll serve`, which launches a web server and auto-regenerates your site when a file is updated.

To add new posts, simply add a file in the `_posts` directory that follows the convention `YYYY-MM-DD-name-of-post.ext` and includes the necessary front matter. Take a look at the source for this post to get an idea about how it works.

Jekyll also offers powerful support for code snippets:

```ruby
def print_hi(name)  # 定义一个函数
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
```

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll's GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].


```ruby
ls | length  # 打印出当前目录下文件数量
ls **/*.ipynb  # 列出所有嵌套在当前目录下的非隐藏文件
ls -a **/*.nu

ls | sort-by modified | reverse  # 打印所有文件，并按最新更该的顺序排序
ls | where size > 5b  # 打印大小大于5b的文件
ls | where name =~ rm  # =~表示使用正则表达式
ls *dilate_4 | each { |i1| ls $i1.name | each { |i2| ls ( $i1.name | $i2.name ) | where name =~ csv | each { |i3| cp $i3.name ( $i2.name | path join "threshold75" ) } } }

# ^echo表示调用外部命令，而不是nushell内置的echo
ls | get name| each { |i| ^echo $i }  # 从ls的内容中获取name，即所有文件的名字。然后each，遍历打印这些名字
ls | each { |i| $"文件($i.name)的大小为($i.size)" } | save rm_rjx.txt
ls | where type == dir | each { |i| touch ($i.name | path join "rm_rjx.txt") }  # 在当前目录的文件夹下新建rm_rjx.txt文件

ls | sort-by size | reverse | first | get name | cp $in ../  # 命令有时会接受一个参数而不是管道输入，于是提供内置变量$in

# 背景：当前目录下有3个目录，每个目录中有1个目录以及一堆csv文件。
# 目的：将所有csv文件复制到同级目录中
# 代码逻辑：
#   1. ls出当前目录，并each遍历以及命名变量为i1。
#   2. 再ls出$i1中的所有内容，并where name =~.csv，再对这些内容遍历以及命名变量为i2。
#   3. 此时i1.name为第一级目录名，i2.name为第二级csv名。
#   4. 然后组合i1.name和第二级目录“threshold75”为路径。
#   5. 并通过cp $i2.name $in进行复制操作。
ls |
  each {|i1| ls $i1.name | where name =~ .csv |
  each {|i2| ( $i1.name | path join threshold75) |
  cp $i2.name $in}}

# 经验：each之后就ls（最多增加where来筛选）。ls之后就each继续迭代。
ls | where name =~ "IBP" or name =~ "control" |
  each {|i1| ls $i1.name | where name =~ "self"|  # i1就是IBP和control。但是ls $i1查找其内部的文件，于是过滤self
  each {|i2| ls $i2.name |  # i2就是Glasser/BNA/sphere
  each {|i3| ($i3.name | path join "threshold75" "rm_rjx") |  # i3就是I/E/M
  $in}}}  # 最终操作

^ps  # 外部的ps命令
ps | get name  # 打印当前程序名字
ps | where name == nu.exe  # 打印出nu.exe程序的信息
ps | where name == nu.exe | get cpu  # 打印出nu.exe程序cpu使用量

sys users | get 3.name  # 3是序号

help commands | explore  # 输出很长时，可发送到explore

ls [a-z]*  # 打印第一个字母是小写的文件

cd ...  # 返回父目录的父目录

let x = if true {-1} else {1}
```

高级通配符（\*，?，[]），以及：

```ruby
let rjx = 'rm_rjx'
let rjx_glob = ($"*($rjx)*" | into glob)
ls $rjx_glob
# 或者
let rjx = 'rm_rjx'
ls ...(glob $"*($rjx)*")  # ...：这是 Nushell 中的命令展开语法，它会将 glob 返回的结果传递给 ls 命令。

ls | where name =~ network | each { |i| $i.name | path join "*" | into glob | rm $in }
```

[jekyll-docs]: http://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/