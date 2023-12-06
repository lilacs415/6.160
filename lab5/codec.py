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

def encode(input):
    data = bytearray(input)
    buffer = bytearray()
    for byte in data:
        if byte in printable:
            buffer.append(byte)
        else:
            buffer.extend(b"!" + bytes([printable[byte // 16], printable[byte % 16]]) + b"!")


    return bytes(buffer)

def decode(buf):
    output = bytearray()
    i = 0
    
    while i < len(buf):
        if buf[i] == ord("!") and i + 3 <= len(buf):
            hex_str = chr(buf[i+1]) + chr(buf[i+2])
            print('hex_str', hex_str)
            decoded_byte = bytes.fromhex(hex_str)
            output.extend(decoded_byte)
            i += 4
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
# encode_and_decode(b"hello world")
# encode_and_decode(b"\x00\x01\x02\x03")
# encode_and_decode(b" ")
encode_and_decode(b"\n")