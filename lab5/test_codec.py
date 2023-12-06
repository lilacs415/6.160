import atheris

with atheris.instrument_imports():
    import codec
    import random
    import sys

def test_str(data):
    fuzzer = atheris.FuzzedDataProvider(data)
    out = fuzzer.ConsumeBytes(32)

    encoding = codec.encode(out)

    assert type(encoding) == bytes, "encoding must be bytes"
    assert all([char in codec.printable for char in encoding]), "encoding must be printable"
    assert codec.encode(b"Apples") == b"Apples", "encoding must be 1 to 1"
    assert len(encoding) <= 3 * len(out), "too long"

    dec = codec.decode(encoding)

    assert type(dec) == bytes, "decoded must be bytes"
    assert out == dec, 'wrong'

def test_recoverable(data):
    fuzzer = atheris.FuzzedDataProvider(data)
    out = fuzzer.ConsumeBytes(32)

    encoding = codec.encode(out)

    cut_begin = random.randint(0, len(encoding) // 2)
    cut_end = random.randint(0, len(encoding) // 2)

    encoding = encoding[cut_begin:len(encoding) - cut_end]
    dec = codec.decode(encoding)

    assert dec in out, "not recoverable"


if __name__ == "__main__":
    test = test_recoverable
    atheris.Setup(sys.argv, test)
    atheris.Fuzz()