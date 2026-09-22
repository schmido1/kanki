
from enum import Enum


class Mode(Enum):
    Menu = "Menu"
    Heisig = "Heisig"
    Vokabeln = "Vokabeln"
    Töne = "Töne"
    Aussprache = "Aussprache"
    Redewendungen = "Redewendungen"

class Language(Enum):
    English = "English"
    Deutsch = "Deutsch"

class RomanisationType(Enum):
    Yale = "Yale"
    Jyutping = "Jyutping"

class Type(Enum):
    Phoneme = "Phoneme",
    Composite = "Composite"

class Characters(Enum):
    Traditional = "traditionell'" #"Traditional" TODO: Make adaptable
    Simplified = "vereinfacht'" #"Simplified"

class InitialsYale(Enum):
    b = "b"
    p = "p"
    f = "f"
    m = "m"
    d = "d"
    t = "t"
    s = "s"
    n = "n"
    g = "g"
    k = "k"
    h = "h"
    ng = "ng"
    kw = "kw"
    gw = "gw"
    j = "j"
    ch = "ch"
    l = "l"
    w = "w"
    y = "y"
    _ = ""

class MiddlesYale(Enum):
    i = "i"
    e = "e"
    yu = "yu"
    eu = "eu"
    a = "a"
    aa = "aa"
    o = "o"
    u = "u"
    _ = ""


class InitialsJyutping(Enum):
    b = "b"
    p = "p"
    f = "f"
    m = "m"
    d = "d"
    t = "t"
    s = "s"
    n = "n"
    g = "g"
    k = "k"
    h = "h"
    ng = "ng"
    kw = "kw"
    gw = "gw"
    z = "z"
    c = "c"
    l = "l"
    w = "w"
    j = "j"
    _ = ""

class MiddlesJyutping(Enum):
    i = "i"
    e = "e"
    yu = "yu"
    oe = "oe"
    eo = "eo"
    a = "a"
    aa = "aa"
    o = "o"
    u = "u"
    _ = ""

class Finals(Enum):
    i = "i"
    u = "u"
    m = "m"
    n = "n"
    ng = "ng"
    p = "p"
    t = "t"
    k = "k"
    _ = ""

class Tones(Enum):
    one = "1"
    two = "2"
    three = "3"
    four = "4"
    five = "5"
    six = "6"
