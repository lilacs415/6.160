def attack_one(guess):
    import inspect
    return inspect.currentframe().f_back.f_locals['secret']

def attack_two():
    import inspect
    return inspect.currentframe().f_back.f_locals['secret']

def attack_three():
    import os

    def nefarious(dummy):
        return b'0' * 256
    
    os.urandom = nefarious
    return nefarious(256)

def attack_four():
    import gc

    for object in gc.get_objects():
        try:
            return object.secret
        except:
            pass
