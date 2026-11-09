import sys
import os
import runpy
import traceback
from kitty.fast_data_types import Screen
from kitty.tab_bar import DrawData, ExtraData, TabBarData, draw_title
from kitty.utils import color_as_int

def as_rgb(x: int) -> int:
    return (x << 8) | 2



def is_DEBUG():
    """
    To reload tab_bar.py:

    $ touch /tmp/tab_bar.reload
    $ rm /tmp/tab_bar.reload
    """
    return os.path.exists('/tmp/tab_bar.reload')

if not hasattr(sys, 'NTABS'):
    sys.NTABS = 1

def draw_tab(*args, **kwargs):
    try:
        global _draw_tab
        if is_DEBUG():
            print('reloading', __file__)
            mod = runpy.run_path(__file__)
            _draw_tab = mod['_draw_tab']
        return _draw_tab(*args, **kwargs)
    except:
        traceback.print_exc()

def fix_title(title):
    title = title.replace('demouser-DGX-Station: ', 'dgx: ')
    title = title.replace('~/anaconda/', '🅐 /')
    title = title.replace('~/pypy/misc', '🅟 /🅜 /')
    title = title.replace('~/pypy/', '🅟 /')
    title = title.replace('🅚 ', '🅚  ')
    if is_DEBUG():
        title = '🚧 ' + title
    return title


def _draw_tab(
    draw_data: DrawData, screen: Screen, tab: TabBarData,
    before: int, max_title_length: int, index: int, is_last: bool,
    extra_data: ExtraData
) -> int:
    if is_last:
        sys.NTABS = index

    orig_fg = screen.cursor.fg
    orig_bg = screen.cursor.bg
    left_sep, right_sep = ('', '')

    title = fix_title(tab.title)

    # I don't really understand why I need the -5, but it seems that without it, the text overflows and I get '...' even for short tab titles
    tab_width = (screen.columns) // sys.NTABS - 5
    title = title.center(tab_width)
    tab = tab._replace(title=title)

    def draw_sep(which: str) -> None:
        #print(f"{draw_data.default_bg = }")
        #screen.cursor.bg = draw_data.default_bg
        screen.cursor.bg = as_rgb(color_as_int(draw_data.default_bg))
        screen.cursor.fg = orig_bg
        screen.draw(which)
        screen.cursor.bg = orig_bg
        screen.cursor.fg = orig_fg

    if max_title_length <= 1:
        screen.draw('…')
    elif max_title_length == 2:
        screen.draw('…|')
    elif max_title_length < 6:
        draw_sep(left_sep)
        screen.draw((' ' if max_title_length == 5 else '') + '…' + (' ' if max_title_length >= 4 else ''))
        draw_sep(right_sep)
    else:
        draw_sep(left_sep)
        screen.draw(' ')
        draw_title(draw_data, screen, tab, index)
        extra = screen.cursor.x - before - max_title_length
        print("extra:%d" %(extra))
        if extra >= 0:
            screen.cursor.x -= extra + 3
            screen.draw('…')
        elif extra == -1:
            screen.cursor.x -= 2
            screen.draw('…')
        screen.draw(' ')
        draw_sep(right_sep)
        draw_sep(' ')

    return screen.cursor.x
