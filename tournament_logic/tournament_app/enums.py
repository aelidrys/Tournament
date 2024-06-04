from enum import Enum
from enum import auto

class Round(Enum):
    QUATER = 8
    HALF = 4
    FAINAL = 2

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Tourn_status(Enum):
    PENDING = 'pending'
    CLOSED = 'closed'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
    

class M_status(Enum):
    UNPLAYED = 'unplayed'
    PLAYED = 'played'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)