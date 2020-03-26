# Copyright 2020 Bateared Collie
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
Base functinoality
'''
"""
Functions that will all take a file pointer and the sample count and return a
NumPy array with the unpacked values.
"""
# from __future__ import (absolute_import, division, print_function,
#                         unicode_literals)
# from future.builtins import *  # NOQA
# from future.utils import native_str

from obsln.core.futureutils import native_str

import ctypes as C  # NOQA
import os
import sys
import warnings

import numpy as np

from obsln.core.compatibility import from_buffer
from .util import clibsegy


# Get the system byte order.
BYTEORDER = sys.byteorder
if BYTEORDER == 'little':
    BYTEORDER = '<'
else:
    BYTEORDER = '>'


clibsegy.ibm2ieee.argtypes = [
    np.ctypeslib.ndpointer(dtype=np.float32, ndim=1,
                           flags=native_str('C_CONTIGUOUS')),
    C.c_int]
clibsegy.ibm2ieee.restype = C.c_void_p


def unpack_4byte_ibm(file, count, endian='>'):
    """
    Unpacks 4 byte IBM floating points.
    """
    # Read as 4 byte integer so bit shifting works.
    data = from_buffer(file.read(count * 4), dtype=np.float32)
    # Swap the byte order if necessary.
    if BYTEORDER != endian:
        data = data.byteswap()
    length = len(data)
    # Call the C code which transforms the data inplace.
    clibsegy.ibm2ieee(data, length)
    return data


# Old pure Python/NumPy code
#
# def unpack_4byte_ibm(file, count, endian='>'):
#    """
#    Unpacks 4 byte IBM floating points.
#    """
#    # Read as 4 byte integer so bit shifting works.
#    data = np.fromstring(file.read(count * 4), dtype=np.int32)
#    # Swap the byte order if necessary.
#    if BYTEORDER != endian:
#        data = data.byteswap()
#    # See https://mail.scipy.org/pipermail/scipy-user/2009-January/019392.html
#    # XXX: Might need check for values out of range:
#    # https://bytes.com/topic/c/answers/
#    #         221981-c-code-converting-ibm-370-floating-point-ieee-754-a
#    sign = np.bitwise_and(np.right_shift(data, 31), 0x01)
#    exponent = np.bitwise_and(np.right_shift(data, 24), 0x7f)
#    mantissa = np.bitwise_and(data, 0x00ffffff)
#    # Force single precision.
#    mantissa = np.require(mantissa, 'float32')
#    mantissa /= 0x1000000
#    # Do the following calculation in a weird way to avoid autocasting to
#    # float64.
#    # data = (1.0 - 2.0 * sign) * mantissa * 16.0 ** (exponent - 64.0)
#    sign *= -2.0
#    sign += 1.0
#    mantissa *= 16.0 ** (exponent - 64)
#    mantissa *= sign
#    return mantissa


def unpack_4byte_integer(file, count, endian='>'):
    """
    Unpacks 4 byte integers.
    """
    # Read as 4 byte integer so bit shifting works.
    data = from_buffer(file.read(count * 4), dtype=np.int32)
    # Swap the byte order if necessary.
    if BYTEORDER != endian:
        data = data.byteswap()
    return data


def unpack_2byte_integer(file, count, endian='>'):
    """
    Unpacks 2 byte integers.
    """
    # Read as 4 byte integer so bit shifting works.
    data = from_buffer(file.read(count * 2), dtype=np.int16)
    # Swap the byte order if necessary.
    if BYTEORDER != endian:
        data = data.byteswap()
    return data


def unpack_4byte_fixed_point(file, count, endian='>'):
    raise NotImplementedError


def unpack_4byte_ieee(file, count, endian='>'):
    """
    Unpacks 4 byte IEEE floating points.
    """
    # Read as 4 byte integer so bit shifting works.
    data = from_buffer(file.read(count * 4), dtype=np.float32)
    # Swap the byte order if necessary.
    if BYTEORDER != endian:
        data = data.byteswap()
    return data


def unpack_1byte_integer(file, count, endian='>'):
    raise NotImplementedError


class OnTheFlyDataUnpacker:
    """
    Tie-up a data sample unpack function with its parameters.

    This class allows for data to be read directly from the disk as needed,
    preventing the need to store data in memory.
    """
    def __init__(self, unpack_function, filename, filemode, seek, count,
                 endian='>'):
        self.unpack_function = unpack_function
        self.filename = filename
        self.filemode = filemode
        self.seek = seek
        self.count = count
        self.endian = endian
        self.mtime = os.path.getmtime(self.filename)

    def __call__(self):
        mtime = os.path.getmtime(self.filename)
        if mtime != self.mtime:
            msg = "File '%s' changed since reading headers" % self.filename
            msg += "; data may be read incorrectly "
            msg += "(modification time = %s)." % mtime
            warnings.warn(msg)
        with open(self.filename, self.filemode) as fp:
            fp.seek(self.seek)
            raw = self.unpack_function(fp, self.count, endian=self.endian)
        return raw
