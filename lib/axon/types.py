# coding: utf-8

# The MIT License (MIT)
# 
# Copyright (c) <2011-2014> <Shibzukhov Zaur, szport at gmail dot com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

import datetime

try:
    from cdecimal import Decimal
except:
    from decimal import Decimal

try:
    unicode_type = builtins.unicode
except AttributeError:
    unicode_type = builtins.str

str_type = builtins.str

try:
    long_type = builtins.long
    int_type = builtins.int
except AttributeError:
    int_type = builtins.int
    long_type = builtins.int

float_type = builtins.float
bool_type = builtins.bool
bytes_type = builtins.bytes
bytearray_type = builtins.bytearray
date_type = datetime.date
time_type = datetime.time
datetime_type = datetime.datetime
decimal_type = Decimal
none_type = type(None)
