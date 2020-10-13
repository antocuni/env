#!/usr/bin/python3
# Copyright 2010, Alejandro Forero Cuervo
# http://azul.freaks-unidos.net/colorize
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import fcntl
import os
import re
import struct
import sys
import termios

Bold = '\033[1m'
Underline = '\033[2m'
Reverse = '\033[3m'

Black = '\033[0;30m'
Red = '\033[0;31m'
Green = '\033[0;32m'
Yellow = '\033[0;33m'
Blue = '\033[0;34m'
Magenta = '\033[0;35m'
Cyan = '\033[0;36m'
Gray = '\033[0;37m'
White = '\033[97m'

Reset = '\033[0m'

def Colorize(string, color):
  if color:
    return [color, string, Reset]
  return [string]

class Handler(object):
  def Run(self, lines):
    for line in lines:
      print(self.ColorLine(line))

  def ColorLine(self, line):
    return line

  def GetSize(self):
    return struct.unpack('hh', fcntl.ioctl(1, termios.TIOCGWINSZ, ' ' * 4))

class HandlerList(Handler):
  def ColorLine(self, line):
    tokens = self.ColorTokens(line)
    if tokens is None:
      return line
    return ''.join(tokens)

  def ColorTokens(self, line):
    return None

class ColorDict(HandlerList):
  def __init__(self, dict, default=None):
    self.dict = dict
    self.default = default

  def ColorTokens(self, line):
    return Colorize(line, self.dict.get(line, self.default))

def ConstantColor(color):
  return ColorDict({}, color)

class Header(Handler):
  def __init__(self, header, body):
    self.header = header
    self.body = body

  def Run(self, lines):
    try:
      header_line = lines.next()
    except StopIteration:
      return
    self.header.Run([header_line])
    self.body.Run(lines)

class Row(object):
  def __init__(self, token_handler):
    self.token_handler = token_handler

  def Colorize(self, space, text):
    yield space
    yield self.token_handler.ColorLine(text)

def RowConstant(color):
  return Row(ConstantColor(color))

def RowDict(dict, default=None):
  return Row(ColorDict(dict, default))

class Table(HandlerList):
  def __init__(self, rows):
    self.rows = rows

  TOKEN = re.compile('^( *)([^ ]+)(.*)')

  def _ConsumeToken(self, line):
    match = self.TOKEN.match(line)
    if match:
      return match.group(1), match.group(2), match.group(3)
    return '', line, ''

  def ColorTokens(self, line):
    index = 0
    while line:
      space, token, line = self._ConsumeToken(line)
      for s in self.rows[index].Colorize(space, token):
        yield s
      index = min(index + 1, len(self.rows) - 1)

class CharsFunction(HandlerList):
  def __init__(self, color_function):
    self.color_function = color_function

  def ColorTokens(self, line):
    for char in line:
      for s in Colorize(char, self.color_function(char)):
        yield s

def CharsDict(dict, default=None):
  return CharsFunction(lambda x: dict.get(x, default))

class RegexpGroups(HandlerList):
  def __init__(self, regexp_text, handlers):
    self.expr = re.compile(regexp_text)
    self.handlers = handlers

  def ColorTokens(self, line):
    match = self.expr.match(line)
    if not match:
      return None
    output = []
    index = 0
    for text in match.groups():
      output.append(self.handlers[index].ColorLine(text))
      index = min(index + 1, len(self.handlers) - 1)
    return output

def RegexpGroupsColors(expr, *colors):
  return RegexpGroups(expr, [ConstantColor(c) for c in colors])

class Rules(HandlerList):
  def __init__(self, *rules):
    self.rules = rules

  def ColorTokens(self, line):
    for rule in self.rules:
      result = rule.ColorTokens(line)
      if result:
        return result
    return line

def _CleanPath(args):
  path = os.getenv('PATH').split(':')
  path_colorize = os.path.dirname(os.path.abspath(os.path.expanduser(args[0])))
  path_clean = [p for p in path if os.path.abspath(os.path.expanduser(p)) != path_colorize]
  os.environ['PATH'] = ':'.join(path_clean)

def _YieldLines(file):
  while True:
    try:
      line = file.readline()
      if not line:
        return
      yield line[:-1]
    except KeyboardInterrupt:
      pass

def Run(handler_out, handler_err=None):
  for file, handler in ((sys.stdout, handler_out), (sys.stderr, handler_err)):
    if handler and os.isatty(file.fileno()):
      read_end, write_end = os.pipe()
      if os.fork():
        os.close(write_end)
        if file == sys.stderr:
          os.dup2(2, 1)
        handler.Run(_YieldLines(os.fdopen(read_end)))
        sys.exit(0)
      os.close(read_end)
      os.dup2(write_end, file.fileno())

  args = sys.argv
  _CleanPath(args)
  program = [os.path.basename(args[0])] + args[1:]
  os.execvp(program[0], program)
  sys.exit(-1)  # execvp failed
