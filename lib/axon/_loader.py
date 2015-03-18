# coding: utf-8

#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: language_level=3


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

import sys

import axon.errors as errors
import array
from collections import OrderedDict as odict

###
### Exceptions
###


def as_name(name):
    return c_as_name(name)

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
    def __init__(self, fd, mode='safe', errto=None, json=False):
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

        if json:
            self.json = 1
        else:
            self.json = 0

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
        
        #self.global_context = {}

        self.next_line()
    #
    def __next__(self):
        '''
        Get next value.
        '''
        self.skip_spaces()
        if self.eof:
            self.fd.close()
            self._check_pairs()
            if self.errto != sys.stderr:
                self.errto.close()
            raise StopIteration
        return self.get_value(0)
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
        sequence = []
        while 1:
            self.skip_spaces()
            if self.eof:
                self.fd.close()
                self._check_pairs()
                if self.errto != sys.stderr:
                    self.errto.close()
                break

            val = self.get_value(0)
            sequence.append(val)

        return sequence
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
        if self.eof:
            return 0
        self.is_nl = 0

        ch = current_char(self)
        while ch <= ' ':
            if ch == '\n' or ch == '\r':
                self.next_line()
                self.is_nl = 1
                if self.eof:
                    return 0
                ch = current_char(self)
            elif ch == '\t':
                ch = next_char(self)
                self.col += 8
            else:
                ch = next_char(self)
                self.col += 1
            
        return ch
    #
    def moveto_next_token(self):
        if self.eof:
            errors.error_unexpected_end(self)
        self.is_nl = 0

        ch = current_char(self)
        while ch <= ' ':
            if ch == '\n' or ch == '\r':
                self.next_line()
                self.is_nl = 1
                if self.eof:
                    errors.error(self, 'Unexpected end before start of next value')
                ch = current_char(self)
            elif ch == '\t':
                ch = next_char(self)
                self.col += 8
            else:
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

        if ch == 'd' or ch == 'D' or ch == '$':
            skip_char(self)
            return self.sbuilder.create_decimal(text)

        if numtype == 1:
            return self.sbuilder.create_int(text)
        else:
            return self.sbuilder.create_float(text)
    #
    def get_name(self):
        pos0 = self.pos
        ch = next_char(self)
        while ch.isalnum() or ch == '_':
            ch = next_char(self)
            
        if ch == '.':
            ch = next_char(self)
            while ch.isalnum() or ch == '_':
                ch = next_char(self)

        name0 = get_chunk(self, pos0)
        name = dict_get(name_cache, name0, None)
        if name is None:
            name_cache[name0] = name0
            return name0
        else:
            return name
    #
    def get_key(self):
        pos0 = self.pos
        ch = next_char(self)
        while ch.isalnum() or ch == '_':
            ch = next_char(self)

        return get_chunk(self, pos0)
    #
    def try_get_name(self):
        ch = current_char(self)
        if ch.isalpha() or ch == '_':
            return self.get_name()
        elif ch == "'":
            return self.get_string(ch)
        else:
            return None
    #
    def try_get_key(self):
        ch = current_char(self)
        if ch.isalpha() or ch == '_':
            return self.get_key()
        elif ch == '"':
            return self.get_string(ch)
        else:
            return None
    #
    def try_get_label(self):
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
    def get_constant_or_string(self, name):
        if name == 'Infinity':
            ch = current_char(self)
            if ch == '$':
                skip_char(self)
                return self.sbuilder.create_decimal_inf()
            else:
                return self.sbuilder.create_inf()
        elif name == 'NaN':
            ch = current_char(self)
            if ch == '$':
                skip_char(self)
                return self.sbuilder.create_decimal_nan()
            else:
                return self.sbuilder.create_nan()
            
        name2 = dict_get(self.c_constants, name, c_undefined)
        if name2 is c_undefined:
            return name
        else:
            return name2
    #
    def get_negative_constant(self):

        ch = current_char(self)
        if ch.isalpha():
            name = self.get_name()
            if name == 'Infinity':
                ch = current_char(self)
                if ch == '$':
                    skip_char(self)
                    return self.sbuilder.create_decimal_ninf()
                else:
                    return self.sbuilder.create_ninf()
            else:
                errors.error_invalid_value_with_prefix(self, '-')
        elif ch == '∞':
            ch = next_char(self)
            if ch == 'd' or ch == 'D' or ch == '$':
                skip_char(self)
                return self.sbuilder.create_decimal_ninf()
            else:
                return self.sbuilder.create_ninf()
        else:
            errors.error_invalid_value_with_prefix(self, '-')
    #
    def get_value(self, idn):
        ch = current_char(self)
        if ch == '#':
            self.skip_comments()
            ch = current_char(self)

        if (ch <= '9' and ch >= '0') or ch == '.':
            val = self.get_number()
            return val

        if ch == '-':
            ch = self.line[self.pos+1]
            if ch.isdigit():
                val = self.get_number()
            else:
                skip_char(self)
                val = self.get_negative_constant()
        elif ch == '"':
            val = self.get_string(ch)
        elif ch == '{':
            self.bc += 1
            skip_char(self)
            val = self.get_dict_value()
        elif ch == '[':
            self.bs += 1
            skip_char(self)
            val = self.get_list_value()
        elif ch == '(':
            self.bq += 1
            skip_char(self)
            val = self.get_tuple_value()
        elif ch == '<':
            self.ba += 1
            skip_char(self)
            val = self.get_odict_value()
        else:
            name = self.try_get_name()
            if name is not None:

                val = dict_get(self.c_constants, name, None)
                if val is not None:
                    return val
            
                ch = self.skip_spaces()
                if ch == '{':
                    self.bc += 1
                    skip_char(self)
                    self.skip_spaces()

                    val = self.get_complex_value(name, 0)
                elif ch == ':':
                    skip_char(self)
                    ch = self.skip_spaces()

                    if self.is_nl:
                        if self.eof or self.col <= idn:
                            val = self.builder.create_empty(name)
                        elif self.col > idn:
                            val = self.get_complex_value(name, self.col)
                        else:
                            errors.error_indentation(self, idn)
                    else:
                        errors.error_unexpected_attribute(self, name)
                else:
                    val = self.get_constant_or_string(name)
            elif ch == '|':
                val = self.get_base64()
            elif ch == '∞': # \U221E
                ch = next_char(self)
                if ch == 'D' or ch == 'd' or ch == '$':
                    skip_char(self)
                    val = self.sbuilder.create_decimal_inf()
                else:
                    val = self.sbuilder.create_inf()
            elif ch == '?':
                ch = next_char(self)
                if ch == 'D' or ch == 'd' or ch == '$':
                    skip_char(self)
                    val = self.sbuilder.create_decimal_nan()
                else:
                    val = self.sbuilder.create_nan()
            elif ch == '*':
                skip_char(self)
                label = self.try_get_label()
                if self.eof:
                    errors.error_unexpected_end(self)
                if label is not None:
                    val = self.labeled_objects.get(label, c_undefined)
                else:
                    errors.error(self, "Expected label here")
            elif ch == '&':
                pos0 = self.pos
                skip_char(self)
                label = self.try_get_label()

                self.skip_spaces()

                val = self.get_value(pos0)
                self.labeled_objects[label] = val
            elif ch == '\0':
                errors.error(self, "Unexpected end after name %r" % name)
            else:
                errors.error_unexpected_value(self, 'expected named complex value')

        #if not valid_end_item(self):
        #    errors.error_end_item(self)

        return val
    #
    def get_complex_value(self, name, idn):
        ch = current_char(self)
        if ch == '#':
            self.skip_comments()

        aname = self.try_get_name()

        if aname is not None:

            val = dict_get(self.c_constants, aname, None)
            if val is not None:
                return val

            ch = self.skip_spaces()
            
            if ch == ':':
                skip_char(self)
                self.skip_spaces()

                if self.is_nl:
                    if self.eof or self.col <= idn:
                        sequence = [self.builder.create_empty(aname)]
                        val = self.get_sequence_mapping(name, sequence, idn)
                    elif self.pos > idn:
                        sequence = [self.get_complex_value(aname, self.col)]
                        val = self.get_sequence_mapping(name, sequence, idn)
                    else:
                        errors.error_indentation(self, idn)
                else:
                    mapping = {aname: self.get_value(idn)}
                    val = self.get_mapping_sequence(name, mapping, idn)
            elif ch == '{':
                self.bc += 1
                skip_char(self)

                ch = self.skip_spaces()
                
                sequence = [self.get_complex_value(aname, 0)]
                val = self.get_sequence_mapping(name, sequence, idn)
            else:
                sequence = [self.get_constant_or_string(aname)]
                val = self.get_sequence_mapping(name, sequence, idn)

        else:
            ch = self.skip_spaces()

            if ch == '}':
                self.bc -= 1
                skip_char(self)
                val = self.builder.create_empty(name)
            elif ch == '\0':
                val = self.builder.create_empty(name)
            else:
                sequence = [self.get_value(idn)]
                val = self.get_sequence_mapping(name, sequence, idn)

        return val
    #
    def get_sequence_mapping(self, name, sequence, idn):
        mapping = {}
        v = self.get_sequence_part(sequence, mapping, idn)
        if v:
            v = self.get_mapping_part(mapping, None, idn)
            if v:
                errors.error_unexpected_value(self, 'in named sequence-like structure')

            val = self.builder.create_instance(name, c_as_tuple(sequence), mapping)
        else:
            val = self.builder.create_sequence(name, sequence)

        return val
    #
    def get_mapping_sequence(self, name, mapping, idn):
        sequence = []
        v = self.get_mapping_part(mapping, sequence, idn)
        if v:
            v = self.get_sequence_part(sequence, None, idn)
            if v:
                errors.error_unexpected_value(self, 'in named mapping-like structure')

            val = self.builder.create_element(name, mapping, sequence)
        else:
            val = self.builder.create_mapping(name, mapping)

        return val
    #
    def get_list_value(self):

        sequence = []

        ch = self.skip_spaces()

        while 1:
            if ch == '#':
                self.skip_comments()
                ch = current_char(self)
                
            if ch == ']':
                skip_char(self)
                self.bs -= 1
                return sequence
            elif ch == '\0':
                errors.error(self, "Unexpected end inside of the list")

            val = self.get_value(0)
            sequence.append(val)

            ch = self.skip_spaces()

            if self.json:
                ch = current_char(self)
                if ch == ',':
                    skip_char(self)
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
                errors.error(self, "Unexpected end inside of the tuple")

            val = self.get_value(0)
            sequence.append(val)

            ch = self.skip_spaces()
    #
    def get_dict_value(self):
        mapping = {}

        ch = self.skip_spaces()

        while 1:
        
            if ch == '#':
                self.skip_comments()

            key = self.try_get_key()

            ch = self.skip_spaces()
            
            if key is not None:
                if ch == ':':
                    skip_char(self)
                    self.skip_spaces()

                    val = self.get_value(0)
                    mapping[key] = val
                else:
                    errors.error(self, "Expected ':' after the key in the dict")
            else:
                if ch == '}':
                    skip_char(self)
                    self.bc -= 1
                    return mapping
                elif ch == '\0':
                    errors.error(self, "Unexpected end inside of the dict")
                else:
                    errors.error(self, "Expected '}' or invalid part of the dict")

            ch = self.skip_spaces()

            if self.json:
                ch = current_char(self)
                if ch == ',':
                    skip_char(self)
                    ch = self.skip_spaces()
    #
    def get_odict_value(self):
        sequence = []

        ch = self.skip_spaces()

        while 1:
        
            if ch == '#':
                self.skip_comments()

            key = self.try_get_key()

            ch = self.skip_spaces()
            
            if key is not None:
                if ch == ':':
                    skip_char(self)
                    self.skip_spaces()

                    val = self.get_value(0)
                    sequence.append((key,val))
                else:
                    errors.error(self, "Expected ':' after the key in the ordered dict")
            else:
                if ch == '>':
                    skip_char(self)
                    self.ba -= 1
                    return c_new_odict(sequence)
                elif ch == '\0':
                    errors.error(self, "Unexpected end inside of the ordered dict")
                else:
                    errors.error(self, "Expected '>' or invalid part of the ordered dict")

            ch = self.skip_spaces()
    #
    def get_mapping_part(self, mapping, sequence, idn):

        while 1:
            ch = self.skip_spaces()
            
            if ch == '#':
                self.skip_comments()
            
            if idn:
                if self.eof or self.col < idn or ch == '}' or ch == ']' or ch == ')':
                    return 0
                elif self.col == idn:
                    pass
                elif self.is_nl:
                    errors.error_indentation(self, idn)
            elif self.eof:
                errors.error(self, "Unexpected end inside of mapping part of the named structure")

            name = self.try_get_name()

            if name is not None:

                val = dict_get(self.c_constants, name, None)
                if val is not None:
                    return val

                ch = self.skip_spaces()

                if ch == ':':
                    skip_char(self)
                    self.skip_spaces()

                    if self.is_nl:
                        if self.eof or self.col <= idn:
                            if sequence is not None:
                                val = self.builder.create_empty(name)
                                sequence.append(val)
                            return 1
                        elif self.col > idn:
                            if sequence is not None:
                                val = self.get_complex_value(name, self.col)
                                sequence.append(val)
                            return 1
                        else:
                            errors.error_indentation(self, idn)

                    val = self.get_value(idn)
                    mapping[name] = val
                elif ch == '{':
                    self.bc += 1
                    skip_char(self)
                    self.skip_spaces()

                    if sequence is not None:
                        val = self.get_complex_value(name, 0)
                        sequence.append(val)

                    return 1
                else:
                    if sequence is not None:
                        val = self.get_constant_or_string(name)
                        sequence.append(val)
                    return 1
            else:
                ch = current_char(self)
                if ch == '}':
                    skip_char(self)
                    self.bc -= 1
                    return 0
                else:
                    if sequence is not None:
                        val = self.get_value(idn)
                        sequence.append(val)
                    return 1
    #
    def get_sequence_part(self, sequence, mapping, idn):

        while 1:
            ch = self.skip_spaces()

            if ch == '#':
                self.skip_comments()

            if idn:
                if self.eof or self.col < idn or ch == '}' or ch == ']' or ch == ')':
                    return 0
                if self.col == idn:
                    pass
                elif self.is_nl: # self.col > idn:
                    errors.error_indentation(self, idn)
            elif self.eof:
                errors.error(self, "Unexpected end inside of sequence part of the named structure")

            name = self.try_get_name()

            if name is not None:
                val = dict_get(self.c_constants, name, None)
                if val is not None:
                    return val

                ch = self.skip_spaces()

                if ch == ':':
                    skip_char(self)
                    self.skip_spaces()

                    if self.is_nl:
                        if self.eof or self.col <= idn:
                            val = self. builder.create_empty(name)
                            sequence.append(val)
                            continue
                        elif self.pos > idn:
                            val = self.get_complex_value(name, self.pos)
                            sequence.append(val)
                            continue
                        else:
                            errors.error_indentation(self, idn)

                    if mapping is not None:
                        val = self.get_value(idn)
                        mapping[name] = val
                    return 1
                elif ch == '{':
                    skip_char(self)
                    self.bc += 1

                    self.skip_spaces()

                    val = self.get_complex_value(name, 0)
                    sequence.append(val)
                else:
                    val = self.get_constant_or_string(name)
                    sequence.append(val)
            else:
                ch = current_char(self)
                if ch == '}':
                    skip_char(self)
                    self.bc -= 1
                    return 0
                else:
                    val = self.get_value(idn)
                    sequence.append(val)
    #
