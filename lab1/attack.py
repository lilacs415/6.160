from common import H, H_empty, H_kv, H_internal, traversal_path, Proof
from store import Store

class AttackOne:
    def __init__(self, s):
        self._store = s

    def attack_fake_key(self):
        return b"hell"

    def lookup(self, key):
        return Proof(key, b"oworld", [])

class AttackTwo:
    def __init__(self, s):
        self._store = Store()
        for i in range(1024):
            self._store.insert(str(i).encode(), b'')

    def attack_fake_keys(self):
        return {str(i).encode() for i in range(1024)}

    def attack_key_value(self):
        return self._store.root._children[0].hashval(), self._store.root._children[1].hashval()

    def lookup(self, key):
        return self._store.lookup(key)

class AttackThree:
    def __init__(self, s):
        self._store = s

    def lookup(self, key):
        proof = self._store.lookup(key)
        new_key = H_kv(proof.key, proof.val)
        path = traversal_path(key)
        for leaf_direction, sibling in reversed(list(zip(path[2:], proof.siblings[2:]))):
            children = [None, None]
            children[int(leaf_direction)] = new_key
            children[int(not leaf_direction)] = sibling
            new_key = H_internal(children)
        if not path[1]:
            return Proof(new_key, proof.siblings[1], [proof.siblings[0]])
        else:
            return Proof(proof.siblings[1], new_key, [proof.siblings[0]])

class AttackFour:
    def __init__(self, s):
        self._store = s

    def insert(self, key, val):
        return self._store.insert(key, val)

    def attack_fake_key(self):
        return b''

    def lookup(self, key):
        return self._store.lookup(key)
