import os
import zlib

class Attacker:
    def __init__(self, v):
        self.victim = v

    def attack_one(self, plaintext, ciphertext, attack_msg):
        crc = lambda message: zlib.crc32(message).to_bytes(4, "big")
        secret = bytes([p ^ c for p, c in zip(ciphertext[:3] + plaintext + crc(plaintext), ciphertext)])
        forged_packet = bytes([a ^ s for a, s in zip(ciphertext[:3] + attack_msg + crc(attack_msg), secret)])
        return forged_packet

    def attack_two(self, ciphertext, attack_msg):
        crc = lambda message: zlib.crc32(message).to_bytes(4, "big")
        iv, msg, ct_crc = ciphertext[:3], ciphertext[3:-4], ciphertext[-4:]
        message = bytes([a ^ c for c, a in zip(msg, attack_msg)])
        checksum = bytes([a ^ c ^ z for c, a, z in zip(ct_crc, crc(attack_msg), crc(bytes([0 for _ in range(len(attack_msg))])))])
        forged_packet = iv + message + checksum
        return forged_packet

    def attack_three(self, target):
        # You may NOT call self.victim.send_packet() 
        # or self.victim.receive_packet() here.
        #
        # You may call self.victim.check_packet(),
        # defined in grader.py.
        
        ### Your cleverness here
        return guess_of_secret_msg
