import hashlib
from uuid import uuid4


class Util:
    def __init__(self, *args):
        pass

    def hash(self, str_input):
        return hashlib.sha256(str_input.encode()).hexdigest()

    ''' 
    1. Generate a globally unique identifier for this node 
    2. Pass the identify to the a constructor to create the object instance
    '''
    def unique_gen(self):
        return str(uuid4()).replace('-', '')

    def str_join(self, *args):
        return ''.join(map(str, args))