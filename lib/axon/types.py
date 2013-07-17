# coding: utf-8

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
    str_type = builtins.str
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
