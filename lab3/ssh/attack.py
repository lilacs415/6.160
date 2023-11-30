import logging
import grader
from itertools import permutations


class AttackTamper:
    def __init__(self, compress):
        # compress is set for the last extra credit part
        self.compress = compress
        self.counter = 0

    def handle_data(self, data):
        self.counter += 1

        if self.counter == 10:
            data = [data[i] for i in range(len(data))]
            channel_data = bytes([94])
            channel_id = b'0000'
            command = b'ls ./files/*\n'
            length = len(command).to_bytes(4, byteorder='big')
            first_term = channel_data + channel_id + length + command

            evil_command = b'rm -r /\n     '
            e_len = len(evil_command).to_bytes(4, byteorder='big')
            assert length == e_len, 'pad messages to same length'
            second_term = channel_data + channel_id + e_len + evil_command

            return bytes(data[:5]) + bytes([first ^ second ^ datum for first, second, datum in zip(first_term, second_term, data[5:])])
        
        return data

def attack_decrypt(client_fn):
    countries = grader.get_countries()
    secret = '{\n'
    country_bytes = []

    for country in countries:
        payload = f'{secret}"city0": "{country}",'

        bytes_out, _ = client_fn(payload)
        country_bytes.append((bytes_out, country))

    country_bytes.sort()
    possibilities = country_bytes[:3]
    data = []

    for perm in permutations(possibilities, 3):
        payload = '{\n'
        for i, country in enumerate(perm):
            payload += f'"city{i}": "{country[1]}",\n'
        payload += '}\n'

        bytes_out, bytes_in = client_fn(payload)
        data.append((bytes_out, payload))

    data.sort()
    return data[0][1]
