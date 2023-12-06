import atheris

with atheris.instrument_imports():
    import msgpacker as msgpacker
    import random
    import sys

def test_int(data):
    fuzzer = atheris.FuzzedDataProvider(data)
    out = fuzzer.ConsumeIntInRange(-(2**63), 2**32-1)

    enc = msgpacker.encoder()
    enc.encode(out)
    res = enc.get_buf()

    dec = msgpacker.decoder(res)
    assert out == dec.decode(), 'wrong'

def test_str(data):
    fuzzer = atheris.FuzzedDataProvider(data)
    out = fuzzer.ConsumeUnicodeNoSurrogates(32)

    enc = msgpacker.encoder()
    enc.encode(out)
    res = enc.get_buf()

    dec = msgpacker.decoder(res)
    assert out == dec.decode(), 'wrong'

def test_bytes(data):
    fuzzer = atheris.FuzzedDataProvider(data)
    out = fuzzer.ConsumeBytes(2^32-1)

    enc = msgpacker.encoder()
    enc.encode(out)
    res = enc.get_buf()

    dec = msgpacker.decoder(res)
    assert out == dec.decode(), 'wrong'

def test_dict(data):
    fuzzer = atheris.FuzzedDataProvider(data)
    out_int = fuzzer.ConsumeInt(8)
    out_str = fuzzer.ConsumeUnicodeNoSurrogates(32)
    out_byte = fuzzer.ConsumeBytes(2^32-1)
    options = [out_int, out_str, out_byte]

    out = {}
    for _ in range(random.randint(0, 2**16-1)):
        out[random.choice(options)] = random.choice(options)

    enc = msgpacker.encoder()
    enc.encode(out)
    res = enc.get_buf()

    dec = msgpacker.decoder(res)
    assert out == dec.decode(), 'wrong'

def test_array(data):
    fuzzer = atheris.FuzzedDataProvider(data)
    out_int = fuzzer.ConsumeInt(8)
    out_str = fuzzer.ConsumeUnicodeNoSurrogates(32)
    out_byte = fuzzer.ConsumeBytes(2^32-1)
    options = [out_int, out_str, out_byte]

    out = []
    for _ in range(random.randint(0, 2**16-1)):
        out.append(random.choice(options))

    enc = msgpacker.encoder()
    enc.encode(out)
    res = enc.get_buf()

    dec = msgpacker.decoder(res)
    assert out == dec.decode(), 'wrong'

if __name__ == "__main__":
    test = test_int
    atheris.Setup(sys.argv, test)
    atheris.Fuzz()