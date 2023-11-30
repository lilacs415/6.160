from ecdsa import SigningKey, NIST256p
import hashlib 
from datetime import datetime

def problem_1a(date_string, public_key):
    start_date = datetime(*[int(num) for num in date_string.split('-')])
    start_time = int(start_date.timestamp())

    for i in range(start_time, start_time + 86401):
        time = b'%d' % i
        h = hashlib.sha256(time).digest()
        secexp = int.from_bytes(h, "big")
        sk = SigningKey.from_secret_exponent(secexp, curve=NIST256p)
        if sk.verifying_key == public_key:
            return sk


def problem_2b(sig1, sig2, Hm1, Hm2):
    r1, s1 = sig1
    r2, s2 = sig2
    q = 6277101735386680763835789423176059013767194773182842284081

    numerator = (s1 * Hm2 - s2 * Hm1)
    denominator = (r1 * s2 - r2 * s1)
    alpha = numerator * pow(denominator, -1, q) % q 

    return alpha