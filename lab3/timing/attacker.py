import bad_server
import api
import time
import random
import gc
from typing import Optional

class Client:
    def __init__(self, remote: bad_server.BadServer):
        self._remote = remote

    def steal_password(self, l: int) -> Optional[str]:
        if l <= 32:
            a, b, x = 100, 200, 1.5e-6
        else:
            a, b, x = 97, 177, 0.65e-6
        password = ''
        while len(password) < 2 * l: # generating hex characters, 2 hex chars to 1 byte
            times = []
            for char in self.chars():
                char_times = []
                for _ in range(b):
                    req = api.VerifyRequest(password + char)
                    gc.disable()
                    start = time.time()
                    for _ in range(a):
                        self._remote.verify_password(req)
                    end = time.time()
                    gc.enable()
                    char_times.append(end - start)
                times.append((min(char_times), char)) # take the min value w/ least noise (closest to true)
            times.sort(reverse=True)
            best, new = times[0]
            avg = sum([time for time, _ in times])/len(times)
            if best - avg < x:
                password = password[:-1]
            else:
                password += new # go with the char that takes the longest to verify
            # print(password)

        req = api.VerifyRequest(password)
        if self._remote.verify_password(req).ret:
            return password
 
    def chars(self):
        chars = '0123456789abcdef'
        possible = [char for char in chars]
        random.shuffle(possible)
        return possible


if __name__ == "__main__":
    pass
    # passwd1 = '37a4e5bf84763017'
    # passwd2 = '37a4e5bf847630173da7e6d19991bb8d'
    # passwd3 = '37a4e5bf847630173da7e6d19991bb8d37a4e5bf847630173da7e6d19991bb8d'
    passwd4 = ''.join(['0' for _ in range(128)])
    # print(passwd4)
    passwd = passwd4
    nbytes = len(passwd) // 2
    server = bad_server.BadServer(passwd)
    alice = Client(server)
    print(alice.steal_password(nbytes))
    # passwd = passwd2
    # nbytes = len(passwd) // 2
    # server = bad_server.BadServer(passwd)
    # alice = Client(server)
    # print(alice.steal_password(nbytes))
    # passwd = passwd3
    # nbytes = len(passwd) // 2
    # server = bad_server.BadServer(passwd)
    # alice = Client(server)
    # print(alice.steal_password(nbytes))
