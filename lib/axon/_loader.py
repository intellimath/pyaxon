# coding: utf-8

#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: language_level=3
#cython: embedsignature=True

# The MIT License (MIT)
# 
# Copyright (c) <2011-2016> <Shibzukhov Zaur, szport at gmail dot com>
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

import sys

import axon.errors as errors
import array
from collections import OrderedDict as odict

###
### Exceptions
###

import cython

#
#######################################################################
#

if sys.version_info.major == 3:
    int_mode = 'i'
else:
    int_mode = b'i'
    
_builder_dict = {
    'safe': SafeBuilder(),
    'strict': StrictBuilder(),
    'mixed': MixedBuilder()
}

def register_builder(mode, builder):
    _builder_dict[mode] = builder

def get_builder(mode):
    return _builder_dict.get(mode, None)

#
# Loader
#
class Loader:

    '''
    Loader from line oriented unicode text inputs.

    .. py:attribute:: line

        Current input unicode line

    .. py:attribute:: pos

        Position of current unicode character

    .. py:attribute:: lnum

        Number of current input unicode line

    .. py:attribute:: errto

        Name of file for reporting errors

    '''
    #
    def __init__(self, fd, mode='safe', errto=None):
        '''
        .. py:function:: Loader(fd, readline, builder="safe", sbuilder="default", errto=None)

            :param fd:

                File-like object with `.readline()` and `.close()` method

            :param mode:

                Specifies the method of building python objects for complex values

            :param errto:

                Name of file for reporting errors
        '''
        self.fd = fd
        self.readline = fd.readline
        
        self.bc = 0
        self.bs = 0
        self.bq = 0
        self.ba = 0
        
        self.labeled_objects = {}

        self.builder = get_builder(mode)
        if self.builder is None:
            raise ValueError("Invalid mode: %s", mode)

        self.sbuilder = SimpleBuilder()

        self.c_constants = c_constants.copy()

        if errto is None:
            self.errto = sys.stderr
        else:
            self.errto = open(errto, 'wt')

        self.da = array.array(int_mode, (0,0,0))
        self.ta = array.array(int_mode, (0,0,0,0))
        self.to = array.array(int_mode, (0,0))

        self.is_nl = 0

        self.lnum = 0
        
        self.next_line()
    #
    def _check_pairs(self):
        if self.bc > 0:
            errors.error(self, 'Missed closing }')
        elif self.bc < 0:
            errors.error(self, 'Extra closing }')
        
        if self.bs > 0:
            errors.error(self, 'Missed closing ]')
        elif self.bs < 0:
            errors.error(self, 'Extra closing ]')
        
        if self.bq > 0:
            errors.error(self, 'Missed closing )')
        elif self.bq < 0:
            errors.error(self, 'Extra closing )')
        
        if self.ba > 0:
            errors.error(self, 'Missed closing >')
        elif self.ba < 0:
            errors.error(self, 'Extra closing >')
    #
    def load(self):
        '''
        Load all values.
        '''
        is_odict = 0

        self.skip_spaces()
        if self.eof:
            self.fd.close()
            self._check_pairs()
            if self.errto != sys.stderr:
                self.errto.close()
            return []

        val = self.get_keyval_or_value()        
        if type(val) is KeyVal:
            is_odict = 1
            keyval = val
            mapping = c_new_odict([])
            mapping[keyval.key] = keyval.val
        else:
            sequence = [val]

        while 1:
            self.skip_spaces()
            if self.eof:
                self.fd.close()
                self._check_pairs()
                if self.errto != sys.stderr:
                    self.errto.close()
                break
            
            if is_odict:
                self.get_keyval_odict(mapping)
            else:
                val = self.get_value(0, 0)
                if type(val) is KeyVal:
                    errors.error_unexpected_keyval(self)
                else:
                    sequence.append(val)

        if is_odict:
            return mapping
        else:
            return sequence
    #
    def iload(self):
        '''
        Iterative get value
        '''
        is_odict = 0

        self.skip_spaces()
        if self.eof:
            self.fd.close()
            self._check_pairs()
            if self.errto != sys.stderr:
                self.errto.close()
            return

        val = self.get_keyval_or_value(0, 0)
        if type(val) is KeyVal:
            is_odict = 1
        yield val

        while 1:
            self.skip_spaces()
            if self.eof:
                self.fd.close()
                self._check_pairs()
                if self.errto != sys.stderr:
                    self.errto.close()
                break

            val = self.get_keyval_or_value(0, 0)
            if is_odict and not type(val) is KeyVal:
                errors.error_expected_keyval(self)
            elif not is_odict and type(val) is KeyVal:
                errors.error_unexpected_keyval(self)
            
            yield val
    #
    def __iter__(self):
        '''
        Return iterator for iterative loading of values.
        '''
        return self
    #
    #def skip_char(self):
    #    self.pos += 1
    #
    #def next_char(self):
    #    self.pos += 1
    #    #return self.line[self.pos]
    #    return c_unicode_char(self.line, self.pos)
    #
    #def current_char(self):
    #    #return self.line[self.pos]
    #    return c_unicode_char(self.line, self.pos)
    #
    def next_line(self):

        line = self.readline()

        if line == '':
            self.eof = 1
            self.pos = 0
            self.col = 0
        else:
            ch = c_unicode_char(line, c_unicode_length(line) - 1)
            if ch != '\n':
                line += '\n'
            self.eof = 0
            self.lnum += 1

            self.line = line
            self.pos = 0
            self.col = 0
    #
    def skip_spaces(self):
        self.is_nl = 0
        if self.eof:
            return 0

        ch = current_char(self)
        prev_ch = '\0'
        while ch <= ' ':
            if ch == '\n':
                self.next_line()
                if prev_ch != '\\':
                    self.is_nl = 1
                if self.eof:
                    return 0
                prev_ch = ch
                ch = current_char(self)
            elif ch == '\t':
                prev_ch = ch
                ch = next_char(self)
                self.col += 8
            else:
                prev_ch = ch
                ch = next_char(self)
                self.col += 1
            
        return ch
    #
    def skip_whitespace(self):
        ch = current_char(self)
        while ch == ' ' or ch == '\t':
            ch = next_char(self)
            if ch == '\t':
                self.col += 8
            else:
                self.col += 1
    #
    #def valid_end_item(self):
    #    ch = current_char(self)
    #    return ch <= ' ' or ch == '}' or ch == ']' or ch == ')' or ch == 0
    #
    def try_get_int(self, maxsize):

        val = 0
        ch = current_char(self)
        i = 0
        while ch >= '0' and ch <= '9':
            if i == maxsize:
                skip_char(self)
                break

            ch0 = ch
            val = 10*val + (ch0 - 48)
            ch = next_char(self)
            i += 1

        if i == 0:
            return -1

        return val
    #
    def get_date(self):

        val = self.try_get_int(4)
        if val < 0:
            return -1
        else:
            self.da[0] = val

        ch = current_char(self)
        if ch == '-':
            skip_char(self)
        else:
            return -1

        val = self.try_get_int(2)
        if val < 0:
            return -1
        else:
            self.da[1] = val

        ch = current_char(self)
        if ch == '-':
            skip_char(self)
        else:
            return -1

        val = self.try_get_int(2)
        if val < 0:
            return -1
        else:
            self.da[2] = val

        ch = current_char(self)
        if '0' <= ch <= '9':
            return -1

        return 0
    #
    def get_time(self):
        val = self.try_get_int(2)
        if val < 0:
            return -1
        else:
            self.ta[0] = val

        ch = current_char(self)
        if ch == ':':
            skip_char(self)
        else:
            return -1

        val = self.try_get_int(2)
        if val < 0:
            return -1
        else:
            self.ta[1] = val

        ch = current_char(self)
        if ch == ':':
            skip_char(self)
        elif '0' <= ch <= '9':
            return -1
        else:
            self.ta[2] = 0
            self.ta[3] = 0
            return 0

        val = self.try_get_int(2)
        if val < 0:
            return -1
        else:
            self.ta[2] = val

        ch = current_char(self)
        if ch == '.':
            skip_char(self)
        elif '0' <= ch <= '9':
            return -1
        else:
            self.ta[3] = 0
            return 0

        val = self.try_get_int(6)
        if val < 0:
            return -1
        else:
            self.ta[3] = val

        ch = current_char(self)
        if '0' <= ch <= '9':
            return -1

        return 0
    #
    def get_time_offset(self):

        val = self.try_get_int(2)
        if val < 0:
            return -1
        else:
            self.to[0] = val

        ch = current_char(self)
        if ch == ':':
            skip_char(self)
        elif '0' <= ch <= '9':
            return -1
        else:
            self.to[1] = 0
            return 0

        val = self.try_get_int(2)
        if val < 0:
            return -1
        else:
            self.to[1] = val

        ch = current_char(self)
        if '0' <= ch <= '9':
            return -1

        return 0
    #
    def get_tzinfo(self):
        v = 0
        sign = 0
        ch = current_char(self)
        if ch == '-':
            skip_char(self)
            sign = 1
            v = self.get_time_offset()
            if v < 0:
                errors.error_invalid_time(self)
        elif ch == '+':
            skip_char(self)
            v = self.get_time_offset()
            if v < 0:
                errors.error_invalid_time(self)
        elif '0' <= ch <= '9':
            v = self.get_time_offset()
            if v < 0:
                errors.error_invalid_time(self)
        else:
            return None

        h = self.to[0]
        m = self.to[1]

        minutes = h * 60 + m

        if minutes > 1440 or minutes < 0:
            errors.error_invalid_time(self)

        if sign:
            minutes = -minutes

        tzinfo = self.sbuilder.create_tzinfo(minutes)

        return tzinfo
    #
    def get_number(self):
        numtype = 1
        pos0 = self.pos
        ch = next_char(self)
        while ch >= '0' and ch <= '9':
            ch = next_char(self)

        if ch == '.':
            numtype = 2
            ch = next_char(self)
            while ch >= '0' and ch <= '9':
                ch = next_char(self)
        elif ch == '-':
            self.pos = pos0

            v = self.get_date()
            if v < 0:
                errors.error_invalid_datetime(self)

            ch = current_char(self)
            if ch == 'T':
                skip_char(self)
                v = self.get_time()
                if v < 0:
                    errors.error_invalid_datetime(self)

                tzinfo = self.get_tzinfo()

                val = self.sbuilder.create_datetime(
                            self.da[0], self.da[1], self.da[2],
                            self.ta[0], self.ta[1], self.ta[2], self.ta[3], tzinfo)
            else:
                val = self.sbuilder.create_date(
                            self.da[0], self.da[1], self.da[2])

            return val
        elif ch == ':':
            self.pos = pos0

            v = self.get_time()
            if v < 0:
                errors.error_invalid_time(self)

            tzinfo = self.get_tzinfo()

            val = self.sbuilder.create_time(self.ta[0], self.ta[1], self.ta[2], self.ta[3], tzinfo)
            return val

        if ch == 'e' or ch == 'E':
            numtype = 2
            ch = next_char(self)
            if ch == '-' or ch == '+':
                ch = next_char(self)
            if ch >= '0' and ch <= '9':
                ch = next_char(self)
                while ch >= '0' and ch <= '9':
                    ch = next_char(self)
            else:
                errors.error_getnumber(self)

        text = get_chunk(self, pos0)

        if ch == 'd' or ch == 'D': # or ch == '$':
            skip_char(self)
            return self.sbuilder.create_decimal(text)

        if numtype == 1:
            return self.sbuilder.create_int(text)
        else:
            return self.sbuilder.create_float(text)
    #
    def get_date_time(self):
        pos0 = self.pos
        ch = current_char(self)
        while ch >= '0' and ch <= '9':
            ch = next_char(self)

        if ch == '-':
            self.pos = pos0

            v = self.get_date()
            if v < 0:
                errors.error_invalid_datetime(self)

            ch = current_char(self)
            if ch == 'T':
                skip_char(self)
                v = self.get_time()
                if v < 0:
                    errors.error_invalid_datetime(self)

                tzinfo = self.get_tzinfo()

                val = self.sbuilder.create_datetime(
                            self.da[0], self.da[1], self.da[2],
                            self.ta[0], self.ta[1], self.ta[2], self.ta[3], tzinfo)
            else:
                val = self.sbuilder.create_date(
                            self.da[0], self.da[1], self.da[2])

            return val
        elif ch == ':':
            self.pos = pos0

            v = self.get_time()
            if v < 0:
                errors.error_invalid_time(self)

            tzinfo = self.get_tzinfo()

            val = self.sbuilder.create_time(self.ta[0], self.ta[1], self.ta[2], self.ta[3], tzinfo)
            return val
    #
    def _get_name(self):
        pos0 = self.pos
        ch = current_char(self)
        while ch.isalnum() or ch == '_':
            ch = next_char(self)
        
        if self.pos == pos0:
            return ''
                    
        name0 = get_chunk(self, pos0)
        return c_get_cached_name(name0)
    #
    def get_name(self):
        pos0 = self.pos
        ch = next_char(self)
        while ch.isalnum() or ch == '_':
            ch = next_char(self)
            
        # if ch == '.':
        #     ch = next_char(self)
        #     while ch.isalnum() or ch == '_':
        #         ch = next_char(self)

        name0 = get_chunk(self, pos0)
        name = c_get_cached_name(name0)
        return name
    #
    def get_key(self):
        pos0 = self.pos
        ch = next_char(self)
        while ch.isalnum() or ch == '_':
            ch = next_char(self)

        return get_chunk(self, pos0)
    #
    def get_label(self):
        pos0 = self.pos
        ch = current_char(self)

        while ch.isalnum() or ch == '_':
            ch = next_char(self)

        if self.pos == pos0:
            errors.error_unexpected_value(self, ' after &')

        return get_chunk(self, pos0)
    #
    def get_unicode_hex(self):

        flag = 1
        val = 0
        for i in range(4):
            ch = current_char(self)
            if ch >= '0' and ch <= '9':
                    ch0 = ch
                    val = 16*val + (ch0 - 48)
                    skip_char(self)
            elif ch >= 'a' and ch <= 'f':
                    ch0 = ch
                    val = 16*val + (ch0 - 87)
                    skip_char(self)
            elif ch >= 'A' and ch <= 'F':
                    ch0 = ch
                    val = 16*val + (ch0 - 55)
                    skip_char(self)
            else:
                flag = 0
                break
        if flag:
            return PyUnicode_FromOrdinal(val)
        else:
            errors.error(self, 'Invalid unicode character %r' % self.line[self.pos-4:self.pos+1])
    #
    def get_string(self, endch):
        text = None
        ch = next_char(self)
        pos0 = self.pos
        while 1:
            if ch == endch:
                if text is None:
                    text = get_chunk(self, pos0)
                else:
                    text += get_chunk(self, pos0)
                skip_char(self)
                return text

            elif ch == '\n' or ch == '\r':
                if text is None:
                    text = get_chunk(self, pos0)
                else:
                    text += get_chunk(self, pos0)
                text += '\n'

                self.next_line()
                if self.eof:
                    errors.error_unexpected_end_string(self)

                #self.skip_whitespace()

                pos0 = self.pos
                ch = current_char(self)
            elif ch == '\\':
                if text is None:
                    text = get_chunk(self, pos0)
                else:
                    text += get_chunk(self, pos0)

                ch = next_char(self)
                if ch == endch:
                    if endch == "'":
                        text += "'"
                    elif endch == '"':
                        text += '"'
                    elif endch == '`':
                        text += '`'
                    else:
                        raise errors.error(self, "String error")
                    skip_char(self)
                elif ch == '\n' or ch == '\r':
                    if text is None:
                        text = get_chunk(self, pos0)
                    else:
                        text += get_chunk(self, pos0)

                    self.next_line()
                    if self.eof:
                        errors.error_unexpected_end_string(self)
#                 elif ch == 'n':
#                     text += "\n"
#                     skip_char(self)
#                 elif ch == 'r':
#                     text += "\r"
#                     skip_char(self)
#                 elif ch == 't':
#                     text += "\t"
#                     skip_char(self)
#                 elif ch == 'u' or ch == 'U':
#                     skip_char(self)
#                     text += self.get_unicode_hex()
                else:
                    text += '\\'
                pos0 = self.pos
                ch = current_char(self)
            else:
                ch = next_char(self)
    #
    def get_base64(self):

        text = None
        ch = next_char(self)
        pos0 = self.pos
        while 1:
            if ch >= '0' and ch <= '9':
                ch = next_char(self)
            elif ch >= 'a' and ch <= 'z':
                ch = next_char(self)
            elif ch >= 'A' and ch <= 'Z':
                ch = next_char(self)
            elif ch == '+' or ch == '/':
                ch = next_char(self)
            elif ch <= ' ':
                if text is None:
                    text = get_chunk(self, pos0)
                else:
                    text += get_chunk(self, pos0)
                self.skip_spaces()
                if self.eof:
                    errors.error(self, 'MIME Base64 string is not finished')
                pos0 = self.pos
                ch = self.line[pos0]
            elif ch == '=':
                ch = next_char(self)
                if ch == '=':
                    ch = next_char(self)

                if text is None:
                    text = get_chunk(self, pos0)
                else:
                    text += get_chunk(self, pos0)
                return self.sbuilder.create_binary(text)
            else:
                raise errors.error(self, 'Invalid character %r in MIME Base64 string' % ch)
    #
    def skip_comment(self):
        ch = next_char(self)
        while 1:
            if ch == '\n' or ch == '\r':
                self.next_line()
                return
            else:
                ch = next_char(self)
    #
    def skip_comments(self):
        while 1:
            self.skip_comment()

            ch = self.skip_spaces()
            if self.eof:
                break

            if ch == '#':
                skip_char(self)
            else:
                break
    #
    def get_negative_constant(self):

        ch = current_char(self)
        if ch == '∞':
            ch = next_char(self)
            if ch == 'd' or ch == 'D' or ch == '$':
                skip_char(self)
                return self.sbuilder.create_decimal_ninf()
            else:
                return self.sbuilder.create_ninf()
        else:
            errors.error_invalid_value_with_prefix(self, '-')
    #
    def get_value(self, idn, idn0):
        ch = current_char(self)
        if ch == '#':
            self.skip_comments()
            ch = current_char(self)
            
        if (ch <= '9' and ch >= '0'):
            val = self.get_number()
            return val

        if ch == '-':
            ch = self.line[self.pos+1]
            if ch.isdigit():
                return self.get_number()
            else:
                skip_char(self)
                return self.get_negative_constant()
        elif ch == '"':
            text = self.get_string(ch)
            ch = self.skip_spaces()
            if ch == ':':
                errors.error_unexpected_keyval()
            else:                
                return text
        elif ch == '{':
            self.bc += 1
            skip_char(self)
            return self.get_dict_value()
        elif ch == '[':
            self.bs += 1
            skip_char(self)
            return self.get_list_value()
        elif ch == '(':
            self.bq += 1
            skip_char(self)
            return self.get_tuple_value()
        elif ch == '^':
            skip_char(self)
            return self.get_date_time()
        elif ch.isalpha() or ch == '_':
            name = self.get_name()
            val = reserved_name_dict.get(name, c_undefined)
            if val is not c_undefined:
                return val

            ch = self.skip_spaces()
            return self.get_named(name, idn, idn0)                                                  
        elif ch == "`":
            name = self.get_string(ch)
            self.skip_spaces()
            return self.get_named(name, idn, idn0)
        elif ch == '|':
            return self.get_base64()
        elif ch == '∞': # \U221E
            ch = next_char(self)
            if ch == 'D' or ch == 'd' or ch == '$':
                skip_char(self)
                return self.sbuilder.create_decimal_inf()
            else:
                return self.sbuilder.create_inf()
        elif ch == '?':
            ch = next_char(self)
            if ch == 'D' or ch == 'd' or ch == '$':
                skip_char(self)
                return self.sbuilder.create_decimal_nan()
            else:
                return self.sbuilder.create_nan()
        elif ch == '*':
            skip_char(self)
            label = self.get_label()
            #if self.eof:
            #    errors.error_unexpected_end(self)
            if label is None:
                errors.error_expected_label(self)
            else:
                return self.labeled_objects.get(label, c_undefined)
        elif ch == '&':
            #pos0 = self.pos
            skip_char(self)
            label = self.get_label()
            if label is None:
                errors.error_expected_label(self)

            self.skip_spaces()

            val = self.get_value(idn, idn0)
            self.labeled_objects[label] = val
            return val
        elif ch == '$':
            skip_char(self)
            name = self.get_name()
            val = self.c_constants.get(name, c_undefined)
            if val is c_undefined:
                errors.error(self, "Undefined name %r" % name)
            return val
        elif ch == '∅':                 
            skip_char(self)
            return set()
        else:
            errors.error_unexpected_value(self, 'Unexpected value')
    #
    def get_keyval_dict(self, mapping):
        ch = current_char(self)
        if ch == '"':
            key = self.get_string(ch)
        elif ch.isalpha() or ch == '_':
            key = self.get_key()
        else:    
            errors.error_expected_key(self)
            
        ch = self.skip_spaces()
        if ch == ':':
            skip_char(self)
            self.skip_spaces()
            val = self.get_value(0, 0)
            mapping[key] = val
        else:
            errors.error_expected_keyval(self)
    #
    def get_keyval_odict(self, mapping):
        ch = current_char(self)
        if ch == '"':
            key = self.get_string(ch)
        elif ch.isalpha() or ch == '_':
            key = self.get_key()
        else:    
            errors.error_expected_key(self)
            
        ch = self.skip_spaces()
        if ch == ':':
            skip_char(self)
            self.skip_spaces()
            val = self.get_value(0, 0)
            mapping[key] = val
        else:
            errors.error_expected_keyval(self)
    #
    def get_keyval_or_value(self):
        pos0 = self.col
        is_key = 0
        ch = current_char(self)
        if ch == '"':
            is_key = 1
            key = self.get_string(ch)
        elif ch == '``':
            key = self.get_string(ch)
        elif ch.isalpha() or ch == '_':
            key = self.get_name()
        else:    
            return self.get_value(0, 0)            
            
        ch = self.skip_spaces()
        if ch == ':':
            skip_char(self)
            self.skip_spaces()
            val = self.get_value(0, 0)
            return c_new_keyval(key, val)
            
        if is_key:
            return key
                    
        if ch == '{':
            self.bc += 1
            skip_char(self)
            self.skip_spaces()
            val = reserved_name_dict.get(key, c_undefined)
            if val is not c_undefined:
                return val
            return self.get_complex_value(key, 0, 0)
        else:
            if is_key:
                return key
                
            val = reserved_name_dict.get(key, c_undefined)
            if val is not c_undefined:
                return val
                
            if self.is_nl:
                if self.eof or self.col <= pos0:
                    return self.builder.create_node(key, None, None)
                elif self.col > pos0:
                    return self.get_complex_value(key, self.col, pos0)
                else:
                    return key
    #
    def get_named(self, name, idn, idn0):            
        ch = current_char(self)
        if ch == ':':
            errors.error_unexpected_keyval(self)

        if self.is_nl:
            if self.eof or self.col <= idn:
                return self.builder.create_node(name, None, None)
            elif self.col > idn:
                return self.get_complex_value(name, self.col, idn)
            else:
                errors.error_indentation(self, idn)

        ch = current_char(self)
        if ch == '{':
            self.bc += 1
            skip_char(self)
            self.skip_spaces()
            return self.get_complex_value(name, 0, idn)
        else:
            errors.error_unexpected_value(self, 'Expected attribute or complex value with the name %r' % name)
    #
    def get_complex_value(self, name, idn, idn0):
        attrs = c_new_odict([])
        
        vals = self.get_attributes(attrs, idn, idn0)
        if len(attrs) == 0:
            attrs = None
            
        if vals is not None:
            self.get_values(vals, idn, idn0)
                        
        return self.builder.create_node(name, attrs, vals)
    #
    def get_attributes(self, attrs, idn, idn0):                
        while 1:
            ch = self.skip_spaces()
            
            if ch == '#':
                self.skip_comments()
                ch = current_char(self)
                
            if idn:
                if self.eof or self.col <= idn0:
                    return None
                elif self.col == idn:
                    pass
                elif self.is_nl:
                    errors.error_indentation(self, idn)
            elif self.eof:
                errors.error_unexpected_end_complex_value(self)
            
            if ch == '}':
                self.bc -= 1
                skip_char(self)
                return None
            
            if ch.isalpha() or ch == '_':
                key = self.get_name()
            elif ch == '`':
                key = self.get_string(ch)
            else:    
                key = None
        
            ch = self.skip_spaces()
            
            if key is None:
                val = self.get_value(idn0, idn0)
                return [val]

            if ch == ':':
                skip_char(self)
                self.skip_spaces()
                val = self.get_value(idn, idn0)
                attrs[key] = val
            else:
                val = self.get_named(key, idn, idn0)
                return [val]
    #
    def get_values(self, vals, idn, idn0):
        while 1:
            ch = self.skip_spaces()

            if ch == '#':
                self.skip_comments()
                ch = current_char(self)
                
            if idn:
                if self.eof or self.col <= idn0:
                    return 1
                elif self.col == idn:
                    pass
                elif self.is_nl:
                    errors.error_indentation(self, idn)
            elif self.eof:
                errors.error_unexpected_end_complex_value(self)
            
            if ch == '}':
                self.bc -= 1
                skip_char(self)
                return 1
            else:
                val = self.get_value(idn, idn0)
                if type(val) is KeyVal:
                    errors.error_unexpected_keyval(self)
                vals.append(val)
    #
    def get_list_value(self):
        is_odict = 0

        ch = self.skip_spaces()
        
        if ch == '#':
            self.skip_comments()
            ch = current_char(self)
        
        if ch == ']':
            skip_char(self)
            self.bs -= 1
            return []
        elif ch == ':':
            ch = next_char(self)
            if ch == ']':
                skip_char(self)
                self.bs -= 1
                return c_new_odict([])
            else:
                errors.error(self, "Invalid empty ordered dict")
        elif ch == '\0':
            if is_odict:
                errors.error_unexpected_end_odict(self)
            else:    
                errors.error_unexpected_end_list(self)
        
        val = self.get_keyval_or_value()        
        if type(val) is KeyVal:
            is_odict = 1
            keyval = val
            mapping = c_new_odict([])
            mapping[keyval.key] = keyval.val
        else:
            sequence = [val]
            
        ch = self.skip_spaces()

        while 1:
            if ch == '#':
                self.skip_comments()
                ch = current_char(self)
                
            if ch == ']':
                skip_char(self)
                self.bs -= 1
                if is_odict:
                    return mapping
                else:
                    return sequence
            elif ch == '\0':
                if is_odict:
                    errors.error_unexpected_end_odict(self)
                else:    
                    errors.error_unexpected_end_list(self)
            else:
                if is_odict:
                    self.get_keyval_odict(mapping)
                else:
                    val = self.get_value(0, 0)
                    sequence.append(val)
                
            ch = self.skip_spaces()
    #
    def get_tuple_value(self):

        sequence = []

        ch = self.skip_spaces()
        
        while 1:
            if ch == '#':
                self.skip_comments()
                ch = current_char(self)
        
            if ch == ')':
                skip_char(self)
                self.bq -= 1
                return tuple(sequence)
            elif ch == '\0':
                errors.error_unexpected_end_tuple(self)
            else:
                val = self.get_value(0, 0)
                sequence.append(val)

            ch = self.skip_spaces()
    #
    def get_dict_value(self):

        is_dict = 0

        ch = self.skip_spaces()
        
        if ch == '#':
            self.skip_comments()
            ch = current_char(self)
        
        if ch == '}':
            skip_char(self)
            self.bc -= 1
            return {}
        elif ch == '\0':
            errors.error_unexpected_end_list(self)
        else:        
            val = self.get_keyval_or_value()
            if type(val) is KeyVal:
                is_dict = 1
                keyval = val
                mapping = {}
                mapping[keyval.key] = keyval.val
            else:
                sequence = {val}
        
        ch = self.skip_spaces()

        while 1:
            if ch == '#':
                self.skip_comments()
                ch = current_char(self)
                
            if ch == '}':
                skip_char(self)
                self.bc -= 1
                if is_dict:
                    return mapping
                else:
                    return sequence
            elif ch == '\0':
                errors.error_unexpected_end_list(self)
            else:
                if is_dict:
                    self.get_keyval_dict(mapping)
                else:
                    val = self.get_value(0, 0)
                    if type(val) is KeyVal:
                        errors.error(self, "Invalid set item")
                    else:
                        sequence.add(val)

            ch = self.skip_spaces()
    #
