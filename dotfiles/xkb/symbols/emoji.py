# -*- encoding: utf-8 -*-
import unicodedata

emojis = u'😂😊❤😘😱👍👏⛄😴🎉😛😋😍😞😁😡'

for char in emojis:
    print('#  ', char, '   U%05X' % ord(char), unicodedata.name(char, '...'))
