import atheris

with atheris.instrument_imports():
    import msgpacker
    import sys

def TestOneInput(data):
    enc = msgpacker.encoder()
    enc.encode(data)
    res = enc.get_buf()

    dec = msgpacker.decoder(res)
    if data != dec.decode():
        raise RuntimeError("wrong")

if __name__ == "__main__":
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()