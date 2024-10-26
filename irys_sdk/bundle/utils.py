def byte_array_to_long(byte_array: bytearray):
    value = 0
    for i in range(len(byte_array)-1, -1, -1):
        value = value * 256 + byte_array[i]
    return value


def long_to_n_byte_array(N: int, long: int) -> bytearray:
    byte_array = bytearray(N)
    if (long < 0):
        raise Exception("Array is unsigned, cannot represent -ve numbers")
    if (long > 2 ** (N * 8) - 1):
        raise Exception(
            "Number {} is too long to represent in an array of {} bytes".format(long, N))
    for index in range(0, len(byte_array), 1):
        byte = long & 0xff
        byte_array[index] = byte
        long = (long - byte) // 256

    return byte_array


def short_to_2_byte_array(long: int) -> bytearray:
    return long_to_n_byte_array(2, long)


def long_to_8_byte_array(long: int) -> bytearray:
    return long_to_n_byte_array(8, long)


def long_to_16_byte_array(long: int) -> bytearray:
    return long_to_n_byte_array(16, long)


def long_to_32_byte_array(long: int) -> bytearray:
    return long_to_n_byte_array(32, long)


def set_bytes(dest: bytearray, src: bytearray, offset: int):
    for i in range(offset, offset + len(src), 1):
        dest[i] = src[i - offset]
