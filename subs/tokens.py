import random
from hashlib import sha256


class Verify():
    def GetSubToken():
        num = random.randint(0, 100)
        Token = sha256(str(num).encode('utf-8')).hexdigest()
        return Token