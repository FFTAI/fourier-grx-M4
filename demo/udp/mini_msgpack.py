"""
Copyright (C) [2024] [Fourier Intelligence Ltd.]

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

--------------------------------------------------
Minimal MessagePack codec, implemented with only the Python standard library
(struct). Used by the demo/udp examples so that no third-party package
(including msgpack itself) is required.

Encode supports: None / bool / int / float / str / list / tuple / dict
Decode supports: fixint / fixstr / fixarray / fixmap / nil / bool /
                 bin8-32 / float32-64 / uint8-64 / int8-64 / str8-32 /
                 array16-32 / map16-32

Protocol reference: https://github.com/msgpack/msgpack/blob/master/spec.md
"""

import struct


# --------------------------------------------------------------------------- encode

def packb(obj) -> bytes:
    """Encode a Python object into MessagePack bytes."""
    if obj is None:
        return b"\xc0"
    if obj is False:
        return b"\xc2"
    if obj is True:
        return b"\xc3"
    if isinstance(obj, int):
        return _pack_int(obj)
    if isinstance(obj, float):
        return b"\xcb" + struct.pack(">d", obj)
    if isinstance(obj, str):
        return _pack_str(obj)
    if isinstance(obj, (list, tuple)):
        return _pack_array(obj)
    if isinstance(obj, dict):
        return _pack_map(obj)
    raise TypeError(f"mini_msgpack: unsupported type {type(obj)}")


def _pack_int(value: int) -> bytes:
    if 0 <= value < 0x80:
        return bytes([value])  # positive fixint
    if -32 <= value < 0:
        return bytes([0x100 + value])  # negative fixint
    if 0 <= value <= 0xFF:
        return b"\xcc" + struct.pack(">B", value)
    if 0 <= value <= 0xFFFF:
        return b"\xcd" + struct.pack(">H", value)
    if 0 <= value <= 0xFFFFFFFF:
        return b"\xce" + struct.pack(">I", value)
    if value >= 0:
        return b"\xcf" + struct.pack(">Q", value)
    if value >= -0x80:
        return b"\xd0" + struct.pack(">b", value)
    if value >= -0x8000:
        return b"\xd1" + struct.pack(">h", value)
    if value >= -0x80000000:
        return b"\xd2" + struct.pack(">i", value)
    return b"\xd3" + struct.pack(">q", value)


def _pack_str(value: str) -> bytes:
    data = value.encode("utf-8")
    n = len(data)
    if n < 32:
        return bytes([0xA0 | n]) + data
    if n <= 0xFF:
        return b"\xd9" + struct.pack(">B", n) + data
    if n <= 0xFFFF:
        return b"\xda" + struct.pack(">H", n) + data
    return b"\xdb" + struct.pack(">I", n) + data


def _pack_array(value) -> bytes:
    n = len(value)
    if n < 16:
        head = bytes([0x90 | n])
    elif n <= 0xFFFF:
        head = b"\xdc" + struct.pack(">H", n)
    else:
        head = b"\xdd" + struct.pack(">I", n)
    return head + b"".join(packb(item) for item in value)


def _pack_map(value: dict) -> bytes:
    n = len(value)
    if n < 16:
        head = bytes([0x80 | n])
    elif n <= 0xFFFF:
        head = b"\xde" + struct.pack(">H", n)
    else:
        head = b"\xdf" + struct.pack(">I", n)
    return head + b"".join(packb(k) + packb(v) for k, v in value.items())


# --------------------------------------------------------------------------- decode

def unpackb(data: bytes):
    """Decode MessagePack bytes into a Python object."""
    value, _ = _unpack(data, 0)
    return value


def _read(data: bytes, offset: int, size: int, fmt: str):
    return struct.unpack_from(fmt, data, offset)[0], offset + size


def _unpack(data: bytes, offset: int):
    head = data[offset]
    offset += 1

    # positive fixint / negative fixint
    if head <= 0x7F:
        return head, offset
    if head >= 0xE0:
        return head - 0x100, offset

    # fixstr
    if 0xA0 <= head <= 0xBF:
        n = head & 0x1F
        return data[offset:offset + n].decode("utf-8"), offset + n

    # fixarray
    if 0x90 <= head <= 0x9F:
        return _unpack_array(data, offset, head & 0x0F)

    # fixmap
    if 0x80 <= head <= 0x8F:
        return _unpack_map(data, offset, head & 0x0F)

    if head == 0xC0:
        return None, offset
    if head == 0xC2:
        return False, offset
    if head == 0xC3:
        return True, offset

    # bin family
    if head == 0xC4:
        n, offset = _read(data, offset, 1, ">B")
        return data[offset:offset + n], offset + n
    if head == 0xC5:
        n, offset = _read(data, offset, 2, ">H")
        return data[offset:offset + n], offset + n
    if head == 0xC6:
        n, offset = _read(data, offset, 4, ">I")
        return data[offset:offset + n], offset + n

    # float32 / float64
    if head == 0xCA:
        return _read(data, offset, 4, ">f")
    if head == 0xCB:
        return _read(data, offset, 8, ">d")

    # unsigned int
    if head == 0xCC:
        return _read(data, offset, 1, ">B")
    if head == 0xCD:
        return _read(data, offset, 2, ">H")
    if head == 0xCE:
        return _read(data, offset, 4, ">I")
    if head == 0xCF:
        return _read(data, offset, 8, ">Q")

    # signed int
    if head == 0xD0:
        return _read(data, offset, 1, ">b")
    if head == 0xD1:
        return _read(data, offset, 2, ">h")
    if head == 0xD2:
        return _read(data, offset, 4, ">i")
    if head == 0xD3:
        return _read(data, offset, 8, ">q")

    # str8 / str16 / str32
    if head == 0xD9:
        n, offset = _read(data, offset, 1, ">B")
        return data[offset:offset + n].decode("utf-8"), offset + n
    if head == 0xDA:
        n, offset = _read(data, offset, 2, ">H")
        return data[offset:offset + n].decode("utf-8"), offset + n
    if head == 0xDB:
        n, offset = _read(data, offset, 4, ">I")
        return data[offset:offset + n].decode("utf-8"), offset + n

    # array16 / array32
    if head == 0xDC:
        n, offset = _read(data, offset, 2, ">H")
        return _unpack_array(data, offset, n)
    if head == 0xDD:
        n, offset = _read(data, offset, 4, ">I")
        return _unpack_array(data, offset, n)

    # map16 / map32
    if head == 0xDE:
        n, offset = _read(data, offset, 2, ">H")
        return _unpack_map(data, offset, n)
    if head == 0xDF:
        n, offset = _read(data, offset, 4, ">I")
        return _unpack_map(data, offset, n)

    raise ValueError(f"mini_msgpack: unsupported type byte 0x{head:02x}")


def _unpack_array(data: bytes, offset: int, n: int):
    items = []
    for _ in range(n):
        value, offset = _unpack(data, offset)
        items.append(value)
    return items, offset


def _unpack_map(data: bytes, offset: int, n: int):
    result = {}
    for _ in range(n):
        key, offset = _unpack(data, offset)
        value, offset = _unpack(data, offset)
        result[key] = value
    return result, offset
