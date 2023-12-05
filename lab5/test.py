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

# def correct_str(data):
#     fuzzer = atheris.FuzzedDataProvider(data)
#     out = fuzzer.ConsumeUnicodeNoSurrogates(32)

#     thing = msgpacker.packb(out)
#     new = msgpacker.unpackb(thing, strict_map_key=False, raw=False)
#     assert out == new, 'wrong'

if __name__ == "__main__":
    test = test_str
    atheris.Setup(sys.argv, test)
    atheris.Fuzz()