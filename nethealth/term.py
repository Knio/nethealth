#! /usr/bin/python3.10
# -*- coding: utf-8 -*-


import argparse
import enum
import locale
import os
import sys
from enum import Enum, IntEnum

try:
    import termios
except ImportError:
    termios = None


def t_term():
    print('** Terminal settings ' + '*' * 40)
    print()
    print(f'System default encoding:    {sys.getdefaultencoding()}')
    print(f'Locale preferred encoding:  {locale.getpreferredencoding()}')
    print(f'Default locale: {locale.getdefaultlocale()}')
    print(f'Current locale: {locale.getlocale()}')
    print('stdin')
    print(f'    encoding: {sys.stdin.encoding}')
    print(f'    tty:      {sys.stdin.isatty()}')
    print(f'    errors:   {sys.stdin.errors}')
    print('stdout')
    print(f'    encoding: {sys.stdout.encoding}')
    print(f'    tty:      {sys.stdout.isatty()}')
    print(f'    errors:   {sys.stdout.errors}')
    if termios:
        print('termios attrs:')
        attrs = termios.tcgetattr(sys.stdin.fileno())
        print(f'    input:    {attrs[0]:016b}  {attrs[0]:04x}')
        print(f'    output:   {attrs[1]:016b}  {attrs[1]:04x}')
        print(f'    control:  {attrs[2]:016b}  {attrs[2]:04x}')
        print(f'    local:    {attrs[3]:016b}  {attrs[3]:04x}')
        print(f'    ispeed:   {attrs[4]}')
        print(f'    ospeed:   {attrs[5]}')
        print(f'    chars:    {b"".join(attrs[6]).hex(" ")}')
        # TODO: termcap



def t_unicode():
    # https://emojipedia.org/unicode-10.0/
    print('** Unicode support ' + '*' * 40)
    print()

    print('''Unicode 15.0 (Unreleased):
        🫨 🩵 🩶 🩷 🫸 🫷 🫎 🫏 🪽 🪿 🪼 🫚 🪻 🫛 🪭 🪮 🪇 🪈 🪯 🛜''')
    print('''Unicode 14.0 (2021-09-14):
        🫢 🫣 🫡 🫥 🫤 🥹 🫱 🫲 🫳 🫴 🫰 🫵 🫶 🫦 🫅 🫃 🫄 🧌 🪸 🪷 🪹
        🪺 🫘 🫗 🫙 🛝 🛞 🛟 🪬 🪩 🪫 🩼 🩻 🫧 🪪 🟰''')
    print('''Unicode 13.0 (2020-03-10):
        🥲 🥸 🤌 🫀 🫁 🥷 🫂 🦬 🦣 🦫 🦤 🪶 🦭 🪲 🪳 🪰 🪱 🪴 🫐 🫒 🫑
        🫓 🫔 🫕 🫖 🧋 🪨 🪵 🛖 🛻 🛼 🪄 🪅 🪆 🪡 🪢 🩴 🪖 🪗 🪘 🪙 🪃
        🪚 🪛 🪝 🪜 🛗 🪞 🪟 🪠 🪤 🪣 🪥 🪦 🪧''')
    print('''Unicode 12.0 (2019-03-05):
        🥱 🤎 🤍 🤏 🦾 🦿 🦻 🧏 🧍 🧎 🦧 🦮 🦥 🦦 🦨 🦩 🧄 🧅 🧇 🧆 🧈
        🦪 🧃 🧉 🧊 🛕 🦽 🦼 🛺 🪂 🪐 🤿 🪀 🪁 🦺 🥻 🩱 🩲 🩳 🩰 🪕 🪔
        🪓 🦯 🩸 🩹 🩺 🪑 🪒 🟠 🟡 🟢 🟣 🟤 🟥 🟧 🟨 🟩 🟦 🟪 🟫''')
    print('''Unicode 11.0 (2018-06-05):
        🥰 🥵 🥶 🥴 🥳 🥺 🦵 🦶 🦷 🦴 🦸 🦹 🦰 🦱 🦳 🦲 🦝 🦙 🦛 🦘🦡
        🦢 🦚 🦜 🦟 🦠 🥭 🥬 🥯 🧂 🥮 🦞 🧁 🧭 🧱 🛹 🧳 🧨 🧧 🥎 🥏 🥍
        🧿 🧩 🧸 🧵 🧶 🥽 🥼 🥾 🥿 🧮 🧾 🧰 🧲 🧪 🧫 🧬 🧴 🧷 🧹 🧺 🧻
        🧼 🧽 🧯''')
    print('''Unicode 10.0 (2017-06-20):
        🤩 🤪 🤭 🤫 🤨 🤮 🤯 🧐 🤬 🧡 🤟 🤲 🧠 🧒 🧑 🧔 🧓 🧕 🤱 🧙 🧚
        🧛 🧜 🧝 🧞 🧟 🧖 🧗 🧘 🦓 🦒 🦔 🦕 🦖 🦗 🥥 🥦 🥨 🥩 🥪 🥣 🥫
        🥟 🥠 🥡 🥧 🥤 🥢 🛸 🛷 🥌 🧣 🧤 🧥 🧦 🧢 ₿''')
    print('''Unicode 9.0 (2016-06-21):
        🤣 🤥 🤤 🤢 🤧 🤠 🤡 🖤 🤚 🤞 🤙 🤛 🤜 🤝 🤳 🤦 🤷 🤴 🤵 🤰 🤶
        🕺 🤺 🤸 🤼 🤽 🤾 🤹 🦍 🦊 🦌 🦏 🦇 🦅 🦆 🦉 🦎 🦈 🦋 🥀 🥝 🥑
        🥔 🥕 🥒 🥜 🥐 🥖 🥞 🥓 🥙 🥚 🥘 🥗 🦐 🦑 🥛 🥂 🥃 🥄 🛵 🛴 🛑
        🛶 🥇 🥈 🥉 🥊 🥋 🥅 🥁 🛒 ''')
    print('''Unicode 8.0 (2015-06-17):
        🙃 🤑 🤗 🤔 🤐 🙄 🤒 🤕 🤓 🤖 🤘 🏻 🏼 🏽 🏾 🏿 🦁 🦄 🦃 🦂 🧀
        🌭 🌮 🌯 🍿 🦀 🍾 🏺 🕌 🕍 🕋 🏐 🏏 🏑 🏒 🏓 🏸 📿 🏹 🛐 🕎 ''')
    print('''Unicode 7.0 (2014-06-16):
        🙂 🙁 🕳️ 🗨️ 🗯️ 🖐️ 🖖 🖕 👁️ 🕵️ 🕴️ 🏌️ 🏋️ 🛌 🗣️ 🐿️ 🕊️ 🕷️ 🕸️ 🏵️ 🌶️
        🍽️ 🗺️ 🏔️ 🏕️ 🏖️ 🏜️ 🏝️ 🏞️ 🏟️ 🏛️ 🏗️ 🏘️ 🏚️ 🏙️ 🏎️ 🏍️ 🛣️ 🛤️ 🛢️ 🛳️ 🛥️
        🛩️ 🛫 🛬 🛰️ 🛎️ 🕰️ 🌡️ 🌤️ 🌥️ 🌦️ 🌧️ 🌨️ 🌩️ 🌪️ 🌫️ 🌬️ 🎗️ 🎟️ 🎖️ 🏅 🕹️
        🖼️ 🕶️ 🛍️ 🎙️ 🎚️ 🎛️ 🖥️ 🖨️ 🖱️ 🖲️ 🎞️ 📽️ 📸 🕯️ 🗞️ 🏷️ 🗳️ 🖋️ 🖊️ 🖌️ 🖍️
        🗂️ 🗒️ 🗓️ 🖇️ 🗃️ 🗄️ 🗑️ 🗝️ 🛠️ 🗡️ 🛡️ 🗜️ 🛏️ 🛋️ 🕉️ ⏸️ ⏹️ ⏺️ 🏴 🏳️
        🏲 🖷 🖏 🕭 🕪 🗪 🎕 🖅 🖿 🕼 🕱 🕮 🗴 🎝 🛊 🗇 🛦 🖰 🗶 🖳 🗷 🛧 🗉 🕈 🛈 🗬 🔾 🕬 🖧 🕾 🖪
        🖶 🖑 🛪 🖣 🗹 🗢 🕨 🖾 🖓 🖠 🗅 🗵 🖉 🖩 🖎 🗕 🗮 🖄 🗠 🖹 🗎 🕲 🗭 🖡 🖔 🗸 🗆 🖸 🌣 🛱 🖽
        🖭 🖒 🖚 🔿 🖫 🖯 🗫 🖵 🕄 🎘 🗌 🗥 🌢 🗘 🖜 🗀 🗏 🖬 🗖 🗤 🖁 🏶 🕩 🖙 🖀 🏱 🗗 🗰 🛉 🖢 🖺
        🖟 🕽 🎔 🕿 🖞 🖗 🖝 🗟 🗐 🛆 🖦 🖮 🛇 🗁 🖻 🗱 📾 🖘 🕫 🗍 🗈 🖴 🖃 🗙 🗛 🖛 🎜 🕅 🛨 🗚 🕻
        🗋 🕇 🗧 🗦 🗲 🛲 🕆 🖂 🗊 🗩 🖈 🗔 🖆 ''')

    print('''Unicode 6.1 (Unknown):
        😀 😗 😙 😛 😑 😬 😴 😕 😟 😮 😯 😦 😧 🕀 🕁 🕃 🕂 ''')
    # TODO
    # print('''Unicode 5.0 (2017-06-20): ''')
    # print('''Unicode 4.0 (2017-06-20): ''')
    # print('''Unicode 3.0 (2017-06-20): ''')
    # print('''Unicode 2.0 (2017-06-20): ''')
    # print('''Unicode 1.0 (2017-06-20): ''')

    print()

    def print_codes(name, codes):
        codes = list(codes)
        print(f'{name}:')
        span = 32

        for i in range(0, len(codes), span):
            print(' ' * 8 + ' '.join(codes[i:i+span]))


    # https://unicode-table.com/en/blocks/spacing-modifier-letters/
    print_codes('Arrows',           map(chr, range(0x2190, 0x2200)))
    print_codes('Control pictures', map(chr, range(0x2400, 0x2440)))
    print_codes('Box drawing',      map(chr, range(0x2500, 0x2580)))
    print_codes('Block elements',   map(chr, range(0x2580, 0x25a0)))
    print_codes('Geometric shapes', map(chr, range(0x25a0, 0x2600)))
    print_codes('Miscellaneous symbols',
                                    map(chr, range(0x2b00, 0x2c00)))

    print()


class ANSI:
  # https://en.wikipedia.org/wiki/ANSI_escape_code#Description

  ESC = '\x1b'    # also known as '\033',  '\e',  '^['
  CSI = '['       # control sequence introducer
  OSC = ']'       # operating system command

  # CSI codes
  class CONTROL:
    SGR         = 'm'   # select graphical representation
    MOUSE_ON    = 'h'
    MOUSE_OFF   = 'l'
    RESET       = 'c'

    class CURSOR(enum.StrEnum):
      UP              = 'A'
      DOWN            = 'B'
      FORWARD         = 'C'
      BACK            = 'D'
      DOWN_BEGINNING  = 'E'
      UP_BEGINNING    = 'F'
      COLUMN          = 'G'
      POSITION        = 'H'

    ERASE_DISPLAY   = 'J'
    ERASE_LINE      = 'K'

  class GRAPHICS(IntEnum):
    RESET   = 0
    BOLD    = 1
    DIM     = 2
    ITALIC  = 3
    UNDERLINE=4
    BLINK   = 5
    BLINK2  = 6
    REVERSE = 7
    BLACK   = 8
    STRIKE  = 9

  class COLOR(IntEnum):
    FG8     = 30
    BG8     = 40
    BRIGHT8 = 60
    FG      = 38
    BG      = 48
    CS256   = 5
    CS24B   = 2

  class COLOR8(IntEnum):
    BLACK   = 0
    RED     = 1
    GREEN   = 2
    YELLOW  = 3
    BLUE    = 4
    MAGENTA = 5
    CYAN    = 6
    WHITE   = 7

  class MOUSE(IntEnum):
    X10               = 9       # doesn't work in mobaxterm
    VT200             = 1000    # button clicks
    VT200_HIGHLIGHT   = 1001    # doesn't work in mobaxterm
    BTN_EVENT         = 1002    # button clicks plus motion when button down
    ANY_EVENT         = 1003    # doesn't work in mobaxterm
    FOCUS_EVENT       = 1004    # doesn't work in mobaxterm

    ALTERNATE_SCROLL  = 1007    # ??
    EXT_MODE          = 1005
    SGR_EXT_MODE      = 1006    # different encoding for larger coordinates
    URXVT_EXT_MODE    = 1015
    PIXEL_POSITION    = 1016


  @staticmethod
  def graphics(x):
    return f'{ANSI.ESC}{ANSI.CSI}{x}{ANSI.CONTROL.SGR}'

  @staticmethod
  def color_fg8(x):
    return ANSI.graphics(ANSI.COLOR.FG8 + x)

  @staticmethod
  def color_bg8(x):
    return ANSI.graphics(ANSI.COLOR.BG8 + x)

  @staticmethod
  def color_fg256(x):
    return ANSI.graphics(f'{ANSI.COLOR.FG};{ANSI.COLOR.CS256};{x}')

  @staticmethod
  def color_bg256(x):
    return ANSI.graphics(f'{ANSI.COLOR.BG};{ANSI.COLOR.CS256};{x}')

  @staticmethod
  def color_fg24b(r,g,b):
    return ANSI.graphics(f'{ANSI.COLOR.FG};{ANSI.COLOR.CS24B};{r};{g};{b}')

  @staticmethod
  def color_bg24b(r,g,b):
    return ANSI.graphics(f'{ANSI.COLOR.BG};{ANSI.COLOR.CS24B};{r};{g};{b}')

  @staticmethod
  def graphics_reset():
    return ANSI.graphics(ANSI.GRAPHICS.RESET)

  @staticmethod
  def control(*x):
    return f'{ANSI.ESC}{ANSI.CSI}{";".join(map(str, x))}'

  @staticmethod
  def mouse(x):
    return ANSI.control('?', ANSI.CONTROL.MOUSE_ON)

  @staticmethod
  def mouse_off(x):
    return ANSI.control('?' , ANSI.CONTROL.MOUSE_OFF)

  @staticmethod
  def cursor_column(col):
    return ANSI.control(col, ANSI.CONTROL.CURSOR.COLUMN)

  @staticmethod
  def cursor_pos(row, col):
    return ANSI.control(row, col, ANSI.CONTROL.CURSOR.POSITION)

  @staticmethod
  def erase_display(x=2):
    return ANSI.control(x, ANSI.CONTROL.ERASE_DISPLAY)

  @staticmethod
  def erase_line(x=0):
    return ANSI.control(x, ANSI.CONTROL.ERASE_LINE)



def t_colors():
    print('** Color support ' + '*' * 40)
    bpx = '⬛'
    box = '▀▄'


    print('8 Color FG:    ', end=' ')
    for color in ANSI.COLOR8:
        print(f'{ANSI.color_fg8(color.value)} {color.name:^8} {ANSI.graphics_reset()}', end=' ')

    print('\n8 Color BG:    ', end=' ')
    for color in ANSI.COLOR8:
        print(f'{ANSI.color_bg8(color.value)} {color.name:^8} {ANSI.graphics_reset()}', end=' ')

    print('\n8 Color BRIGHT:', end=' ')
    for color in ANSI.COLOR8:
        print(f'{ANSI.color_fg8(ANSI.COLOR.BRIGHT8 + color.value)} {color.name:^8} {ANSI.graphics_reset()}', end=' ')

    print('\n8 Color BOLD:  ', end=' ')
    for color in ANSI.COLOR8:
        print(f'{ANSI.graphics(ANSI.GRAPHICS.BOLD)}{ANSI.color_fg8(color.value)} {color.name:^8} {ANSI.graphics_reset()}', end=' ')

    print('\n8 Color DIM:   ', end=' ')
    for color in ANSI.COLOR8:
        print(f'{ANSI.graphics(ANSI.GRAPHICS.DIM)}{ANSI.color_fg8(color.value)} {color.name:^8} {ANSI.graphics_reset()}', end=' ')

    print('\nStyles:\n        ', end=' ')
    for style in ANSI.GRAPHICS:
        print(f'{ANSI.graphics(style.value)} {style.name:^8} {ANSI.graphics_reset()}', end=' ')

    print('\n 8x8 Color:')
    for fg in ANSI.COLOR8:
        for bg in ANSI.COLOR8:
            print(f'{ANSI.color_fg8(fg.value)}{ANSI.color_bg8(bg.value)}{box}{ANSI.graphics_reset()}', end='')
        print()

    print('\n256 Color:')
    print('{:17s}{:17s}{:17s}{}'.format('Red/Green', 'Green/Blue', 'Blue/Red', 'Grey'))
    for y in range(6):
        for x in range(6): # R/G
            r, g, b = y, x, 0
            c = 16 + 36 * r + 6 * g + b
            print(f'{ANSI.color_fg256(c)}{box}{ANSI.graphics_reset()}', end='')
        print('    ', end=' ')
        for x in range(6): # G/B
            r, g, b = 0, y, x
            c = 16 + 36 * r + 6 * g + b
            print(f'{ANSI.color_fg256(c)}{box}{ANSI.graphics_reset()}', end='')
        print('    ', end=' ')
        for x in range(6): # G/B
            r, g, b = x, 0, y
            c = 16 + 36 * r + 6 * g + b
            print(f'{ANSI.color_fg256(c)}{box}{ANSI.graphics_reset()}', end='')
        print('    ', end=' ')
        for x in range(4): # G/B
            c = 232 + y * 4 + x
            print(f'{ANSI.color_fg256(c)}{box}{ANSI.graphics_reset()}', end='')
        print()

    print('\n24-Bit Color:')
    X = 16
    for y in range(X):
        for x in range(X):
            r, g, b = y * X + x, 0, 0
            print(f'{ANSI.color_fg24b(r,g,b)}{box}{ANSI.graphics_reset()}', end='')
        print('    ', end=' ')
        for x in range(X):
            r, g, b = 0, y *X + x, 0
            print(f'{ANSI.color_fg24b(r,g,b)}{box}{ANSI.graphics_reset()}', end='')
        print('    ', end=' ')
        for x in range(X):
            r, g, b = 0, 0, y * X + x
            print(f'{ANSI.color_fg24b(r,g,b)}{box}{ANSI.graphics_reset()}', end='')
        print('    ', end=' ')
        for x in range(X):
            r = g = b = y * X + x
            print(f'{ANSI.color_fg24b(r,g,b)}{box}{ANSI.graphics_reset()}', end='')
        print()


def t_mouse():
    # https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-Mouse-Tracking


    def getch():
        # TODO make windows version
        import tty, termios
        orig_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        c = os.read(sys.stdin.fileno(), 128)
        # c = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
        return c

    def parse_mouse_event(b):
        return b[0] == 0x1b

    mode = ANSI.MOUSE.BTN_EVENT
    mode = ANSI.MOUSE.VT200_HIGHLIGHT
    try:
        # enable mouse tracking
        print(ANSI.mouse(mode), end='', flush=True)
        print(ANSI.mouse(ANSI.MOUSE.SGR_EXT_MODE), end='', flush=True)

        while 1:
            print('Press a key: ([q] to quit)', end=' ', flush=True)
            c = getch()
            print(f'Got input: {c!r}\n')
            if b'q' in c:
                break
            if parse_mouse_event(c):
                # handle highlight tracking?
                print(ANSI.control('1;10;10;20;20T'))

    finally:
        # reset mouse tracking
        print(ANSI.mouse_off(mode), end='', flush=True)
        print(ANSI.mouse_off(ANSI.MOUSE.SGR_EXT_MODE), end='', flush=True)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    tests = [f[2:] for f in globals() if f.startswith('t_')]
    parser.add_argument('tests',
        nargs='*',
        choices=tests,
        default=tests,
    )
    args = parser.parse_args()

    for i in args.tests:
        globals()[f't_{i}']()

if __name__ == '__main__':
    main()
