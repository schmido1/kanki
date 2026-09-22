from .enums import (
    InitialsYale,
    MiddlesYale,
    InitialsJyutping,
    MiddlesJyutping,
    Finals,
    Tones,
)

jyutping_to_yale_initials = {
    "b": "b",
    "p": "p",
    "m": "m",
    "f": "f",
    "d": "d",
    "t": "t",
    "n": "n",
    "l": "l",
    "g": "g",
    "k": "k",
    "ng": "ng",
    "h": "h",
    "z": "j",
    "c": "ch",
    "s": "s",
    "gw": "gw",
    "kw": "kw",
    "j": "y",
    "w": "w",
    "": ""
}

jyutping_to_yale_middles = {
    "i": "i",
    "e": "e",
    "yu": "yu",
    "oe": "eu",
    "eo": "eu",
    "a": "a",
    "aa": "aa",
    "o": "o",
    "u": "u",
    "": ""
}


tone_dict = {
    "i": {
        "1": "ī",
        "2": "í",
        "3": "i",
        "4": "ìh",
        "5": "íh",
        "6": "ih"
    },
    "e": {
        "1": "ē",
        "2": "é",
        "3": "e",
        "4": "éh",
        "5": "èh",
        "6": "eh"
    },
    "yu": {
        "1": "yū",
        "2": "yú",
        "3": "yu",
        "4": "yùh",
        "5": "yúh",
        "6": "yuh"
    },
    "eu": {
        "1": "ēu",
        "2": "éu",
        "3": "eu",
        "4": "éuh",
        "5": "èuh",
        "6": "euh"
    },
    "a": {
        "1": "ā",
        "2": "á",
        "3": "a",
        "4": "áh",
        "5": "àh",
        "6": "ah"
    },
    "aa": {
        "1": "āa",
        "2": "áa",
        "3": "aa",
        "4": "áah",
        "5": "àah",
        "6": "aah"
    },
    "o": {
        "1": "ō",
        "2": "ó",
        "3": "o",
        "4": "òh",
        "5": "óh",
        "6": "oh"
    },
    "u": {
        "1": "ū",
        "2": "ú",
        "3": "u",
        "4": "ù",
        "5": "úh",
        "6": "uh"
    },
    "_": {
        "1": "\u0304",
        "2": "\u0301",
        "3": "",
        "4": "\u0300",
        "5": "\u0301h",
        "6": "h"
    }
    
}
def jyutping_to_yale(
        initial: InitialsJyutping,
        middle: MiddlesJyutping,
        final: Finals,
        tone: Tones
    ) -> str:

    # convert the phoneme parts
    initial_yale = jyutping_to_yale_initials[initial.value]
    bare_middle_yale = jyutping_to_yale_middles[middle.value]
    final_yale = final.value

    # add tones to middle or, in absence of middle, to final
    if bare_middle_yale != "":
        middle_yale = tone_dict[bare_middle_yale][tone.value]
    else:
        middle_yale = bare_middle_yale
        final_yale += tone_dict["_"][tone.value]

    # remove spectal case of jyutping word starting with jyu..
    if initial_yale == "y" and middle_yale == "yu":
        initial_yale = ""
    return initial_yale + middle_yale + final_yale

