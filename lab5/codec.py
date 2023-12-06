import string

printable = string.printable[:94].encode('ascii')
alphanumeric = (string.ascii_letters + string.digits).encode('ascii')

# Requirements:
#
# - Your codec must encode bytes into bytes, and decode back into bytes.
# - Your codec must encode arbitrary bytes.  It must be possible to
#   encode any byte sequence, and decode it correctly.
# - The encoding must be printable (every encoding byte must be in the
#   `printable` bytes object.  Your encodings cannot contain non-printable
#   bytes.
# - Alphanumeric inputs (where every character is in string.ascii_letters
#   or string.digits) must be encoded one-to-one: the encoding must be the
#   same as the input.
# - The encoding should be at most 3x the size of the input, in the worst case.
# - The encoding must be recoverable.  This means that, if you take an encoding
#   and chop off some parts of it (at the beginning or at the end), then decoding
#   that chopped part should produce the corresponding part of the original string,
#   modulo things that might have gotten cut off at each end.

FROM_HEX = {key: val for key, val in zip(printable[65:].decode(), [i for i in range(16)])}
TO_HEX = {val: key for key, val in FROM_HEX.items()}
OTHER_HEX = {key: val for key, val in zip(printable[65:].decode(), ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'])}

def encode(input):
    data = bytearray(input)
    buffer = bytearray()
    for byte in data:
        if byte in alphanumeric:
            buffer.append(byte)
        else:
            # print(byte % 16)
            # print(TO_HEX[byte // 16] + TO_HEX[byte % 16])
            # print((TO_HEX[byte // 16] + TO_HEX[byte % 16]).encode('ascii'))
            buffer.extend(b"!" + (TO_HEX[byte // 16] + TO_HEX[byte % 16]).encode('ascii'))
    return bytes(buffer)

def decode(buf):
    output = bytearray()
    an, np = float('inf'), float('inf')
    if b'!' in buf:
        np = buf.index(b'!')
    for i, char in enumerate(buf):
        if char in alphanumeric:
            an = i
            break
    i = min(an, np)
    
    while i < len(buf):
        if buf[i] == ord("!") and i + 2 < len(buf):
            hex_str = buf[i+1:i+3]
            # print('hex_str', hex_str)
            if len(hex_str) == 2:
                # print(hex_str[0], hex_str[1])
                hex_byte = OTHER_HEX[chr(hex_str[0])] + OTHER_HEX[chr(hex_str[1])]
                decoded_byte = bytes.fromhex(hex_byte)
                # print(decoded_byte)
                # print(bytes(decoded_byte))
                # print(decoded_byte.encode('ascii'))
                output.extend(decoded_byte)
            i += 3
        else:
            output.append(buf[i])
            i += 1

    return bytes(output)

def encode_and_decode(i):
    enc = encode(i)
    dec = decode(enc)
    print(len(i), len(enc), len(dec))
    print(i, "->", enc, "->", dec)

# print(encode(b"\n"))
# buffer = b'!0a'
# buf = buffer[0:3-1]
print(decode(b'!$'))
# encode_and_decode(b"hello world")
# encode_and_decode(b"\x00\x01\x02\x03")
# print(bytes.fromhex('0a'))
# encode_and_decode(b"\n")
# encode_and_decode(b"\n!\n\n")