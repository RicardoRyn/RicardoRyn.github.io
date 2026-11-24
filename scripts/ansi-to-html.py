#!/usr/bin/env python3
"""把带 ANSI 颜色的终端输出转成 Hugo 能渲染的 HTML。

用法：

    python3 scripts/ansi-to-html.py                     # 转换 content/ 下所有 .ansi 文件
    python3 scripts/ansi-to-html.py path/to/log.ansi    # 只转换指定文件

每个 `foo.ansi` 会在同目录生成 `foo.ansi.htmlfrag`，文章里用 `{{</* ansi "foo.ansi" */>}}` 引用。

颜色以 class 输出（`c0` 到 `c15` 是前景色，`bg0` 到 `bg15` 是背景色，
`b`/`d`/`i`/`u` 是粗体、暗淡、斜体、下划线），具体色值在
`assets/sass/_custom.scss` 里按 Catppuccin Latte / Mocha 定义，所以会跟随站点深浅色切换。

256 色和真彩色会被归到最接近的 16 色槽位，这样才能用主题化的 CSS 上色。
jj 的默认输出只用 0 到 15，不会损失颜色。
"""

import html
import re
import sys
from pathlib import Path

# 标准 xterm 16 色，用来把 256 色和真彩色归到最接近的槽位
BASE_16 = [
    (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
    (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
    (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
    (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255),
]
CUBE = (0, 95, 135, 175, 215, 255)

CSI = re.compile(r"\x1b\[[0-9;:<=>?]*[ -/]*[@-~]")
OSC = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")
OTHER_ESC = re.compile(r"\x1b[@-Z\\-_]")


def color256_to_rgb(index):
    if index < 16:
        return BASE_16[index]
    if index < 232:
        index -= 16
        return (CUBE[index // 36 % 6], CUBE[index // 6 % 6], CUBE[index % 6])
    gray = 8 + (index - 232) * 10
    return (gray, gray, gray)


def nearest_slot(rgb):
    return min(range(16), key=lambda i: sum((a - b) ** 2 for a, b in zip(BASE_16[i], rgb)))


class State:
    """当前生效的 SGR 状态。"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.fg = None
        self.bg = None
        self.bold = False
        self.dim = False
        self.italic = False
        self.underline = False

    def classes(self):
        out = []
        if self.fg is not None:
            out.append(f"c{self.fg}")
        if self.bg is not None:
            out.append(f"bg{self.bg}")
        out += [name for name, on in (("b", self.bold), ("d", self.dim),
                                      ("i", self.italic), ("u", self.underline)) if on]
        return out

    def apply(self, params):
        i = 0
        while i < len(params):
            code = params[i]
            if code == 0:
                self.reset()
            elif code == 1:
                self.bold = True
            elif code == 2:
                self.dim = True
            elif code == 3:
                self.italic = True
            elif code == 4:
                self.underline = True
            elif code in (21, 22):
                self.bold = self.dim = False
            elif code == 23:
                self.italic = False
            elif code == 24:
                self.underline = False
            elif code == 39:
                self.fg = None
            elif code == 49:
                self.bg = None
            elif 30 <= code <= 37:
                self.fg = code - 30
            elif 90 <= code <= 97:
                self.fg = code - 90 + 8
            elif 40 <= code <= 47:
                self.bg = code - 40
            elif 100 <= code <= 107:
                self.bg = code - 100 + 8
            elif code in (38, 48):
                slot, used = self._extended(params, i + 1)
                if slot is None:
                    return
                if code == 38:
                    self.fg = slot
                else:
                    self.bg = slot
                i += used
            i += 1

    @staticmethod
    def _extended(params, start):
        """解析 38;5;N 和 38;2;R;G;B，返回 (槽位, 消耗的参数个数)。"""
        if start >= len(params):
            return None, 0
        mode = params[start]
        if mode == 5 and start + 1 < len(params):
            return nearest_slot(color256_to_rgb(params[start + 1] % 256)), 2
        if mode == 2 and start + 3 < len(params):
            return nearest_slot(tuple(p % 256 for p in params[start + 1:start + 4])), 4
        return None, 0


def convert(text):
    """把带转义序列的文本转成 HTML 片段。"""
    # 去掉 OSC（含超链接）和其它非 SGR 的控制序列，只保留 CSI 交给下面处理
    text = OSC.sub("", text)
    text = OTHER_ESC.sub("", text)

    state = State()
    pending = []
    out = []
    pos = 0

    def flush():
        if not pending:
            return
        chunk = html.escape("".join(pending), quote=False)
        pending.clear()
        classes = state.classes()
        # 空白不需要上色，也就不用包 span（粗体对空格没有视觉效果）
        if not chunk.strip() and not any(c.startswith(("c", "bg")) for c in classes):
            out.append(chunk)
        elif classes:
            out.append(f'<span class="{" ".join(classes)}">{chunk}</span>')
        else:
            out.append(chunk)

    for match in CSI.finditer(text):
        if match.start() > pos:
            pending.append(text[pos:match.start()])
        sequence = match.group(0)
        if sequence.endswith("m"):
            flush()
            body = sequence[2:-1]
            params = [int(p) for p in body.split(";") if p.isdigit()]
            state.apply(params or [0])
        # 非 SGR 的 CSI（光标移动等）直接丢弃
        pos = match.end()

    pending.append(text[pos:])
    flush()
    return "".join(out).rstrip("\n")


def render(text):
    return f'<pre class="ansi"><code>{convert(text)}</code></pre>\n'


def process(path):
    path = Path(path)
    source = path.read_text(encoding="utf8", errors="replace")
    # Hugo 会把 content/ 下的 .html 当成页面，所以生成物用 .htmlfrag 后缀
    target = path.with_suffix(path.suffix + ".htmlfrag")
    target.write_text(render(source), encoding="utf8")
    return target


def main(argv):
    targets = [Path(a) for a in argv[1:]]
    if not targets:
        root = Path(__file__).resolve().parent.parent / "content"
        targets = sorted(root.rglob("*.ansi"))
    if not targets:
        print("没有找到 .ansi 文件")
        return 0
    for path in targets:
        if not path.exists():
            print(f"跳过（文件不存在）：{path}")
            continue
        out = process(path)
        print(f"{path} → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
