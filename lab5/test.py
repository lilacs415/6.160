import atheris

with atheris.instrument_imports():
    import msgpacker as msgpacker
    import sys

def test_int(data):
    fuzzer = atheris.FuzzedDataProvider(data)
    out = fuzzer.ConsumeInt(8)

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

    out = {out_int: out_str, out_str: out_byte, out_byte: out_str}

    enc = msgpacker.encoder()
    enc.encode(out)
    res = enc.get_buf()

    dec = msgpacker.decoder(res)
    assert out == dec.decode(), 'wrong'

def test_array(data):
    fuzzer = atheris.FuzzedDataProvider(data)
    # out_int = fuzzer.ConsumeInt(8)
    # out_str = fuzzer.ConsumeUnicodeNoSurrogates(32)
    # out_byte = fuzzer.ConsumeBytes(2^32-1)

    # out = {out_int: out_str, out_str: out_byte, out_byte: out_str}

    out = fuzzer.ConsumeIntListInRange(2^32-1, 0, 2^32-1)

    enc = msgpacker.encoder()
    enc.encode(out)
    res = enc.get_buf()

    dec = msgpacker.decoder(res)
    assert out == dec.decode(), 'wrong'

if __name__ == "__main__":
    test = test_array
    atheris.Setup(sys.argv, test)
    atheris.Fuzz()