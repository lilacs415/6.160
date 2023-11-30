from hashall import *
from hashbig import *
import math

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# return password, where toy_hash(password) = 7efe6b06e7c7
def problem_2a():
    for password in all_strings(0, 10):
        if toy_hash(password.encode()).hex() == "7efe6b06e7c7":
            return password

# return password, where toy_hash(password) is in hashes.txt
def problem_2c():
    hashes = set()
    with open("hashes.txt") as f:
        for hash_pwd in f:
            hashes.add(hash_pwd.strip())

    for password in all_strings(0, 10):
        if toy_hash(password.encode()).hex() in hashes:
            return password
    return password

# return probability of being in bin k
def problem_3a(B, N):
    return 1/N

# return probability of both balls being in bin k
def problem_3b(B,N):
    return (1/N)**2

# return number of ball pairs
def problem_3c(B):
    return math.comb(B, 2)

# return reasonable upper bound
def problem_3d(B,N):
    return problem_3b(B,N) * problem_3c(B) * N
    
# return reasonable upper bound
def problem_3e(L,N):
    prob = problem_3d(L, 2**N)
    return prob

# return h1,h2 where H(h1) == H(h2)
def problem_4b():
    fast = "lila".encode()
    slow = "lila".encode()
    for i in range(2**28):
        fast = H(fast)
        slow = H(H(slow))
        if fast == slow:
            break
    fast = slow
    slow = "lila".encode()
    for j in range(i):
        if H(fast) == H(slow) and fast != slow:
            return fast, slow
        slow = H(slow)
        fast = H(fast)

def all_strings(min_len, max_len):
    def generate(length, prefix=''):
        if length == 0:
            yield prefix
            return
        for letter in ALPHABET:
            yield from generate(length - 1, prefix + letter)
    for i in range(min_len, max_len + 1):
        yield from generate(i)