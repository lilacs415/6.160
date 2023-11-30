import pywasm
import wasi

def sha256(v):
    wasimod = wasi.Wasi(['sha-export.wasm'])
    runtime = pywasm.load('sha-export.wasm', { 'wasi_snapshot_preview1': wasimod.imports() })

    n = len(v)
    memory = runtime.store.memory_list[0].data

    d = runtime.exec('malloc', [n])
    memory[d:d+n] = v

    md = runtime.exec('malloc', [32])
    
    runtime.exec('SHA256', [d, n, md])
    return bytes(memory[md:md+32])
