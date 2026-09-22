import json
import random
import os
from playsound3 import playsound
import pydase
from pydase import DataService
from pydase.utils.decorators import frontend
from kanki_server.utils.enums import Tones

class ToneTrainer(pydase.DataService):
    def __init__(
            self,
            ask_tone1: bool,
            ask_tone2: bool,
            ask_tone3: bool,
            ask_tone4: bool,
            ask_tone5: bool,
            ask_tone6: bool,
        ) -> None:
        super().__init__()

        self._deck_directory = os.environ["KANKI_DECK_DIR"]

        self._ask_tone1 = ask_tone1
        self._ask_tone2 = ask_tone2
        self._ask_tone3 = ask_tone3
        self._ask_tone4 = ask_tone4
        self._ask_tone5 = ask_tone5
        self._ask_tone6 = ask_tone6

        # load the word dictionaries
        with open(self._deck_directory / "vocabulary/words.json") as fp:
            self._words_dict = json.load(fp)
        
        self._ids = list(self._words_dict.keys())
        self._current_id= None # Will be defined by _ask_tones()
        self._ask_tones(True)

    @frontend
    def tone1(self) -> None:
        self._process_rating(Tones.one)

    @frontend
    def tone2(self) -> None:
        self._process_rating(Tones.two)

    @frontend
    def tone3(self) -> None:
        self._process_rating(Tones.three)

    @frontend
    def tone4(self) -> None:
        self._process_rating(Tones.four)
    
    @frontend
    def tone5(self) -> None:
        self._process_rating(Tones.five)

    @frontend
    def tone6(self) -> None:
        self._process_rating(Tones.six)


    def _ask_tones(self, rating: bool) -> None:
        # randomly sample a word from the dictionary

        if rating:
            found_word = False
            while not found_word:
                if len(self._ids) == 0: # if all ids were removed, reload dictionary
                    self._ids = list(self._words_dict.keys())
                self._current_id = random.choice(self._ids)
                self._ids.remove(self._current_id)
                if (
                        self._words_dict[self._current_id]["Type"] == "Phoneme" and
                        True # TODO: Check if tone is selected
                ):
                    files = list(
                        self._deck_directory.glob(f"audio/{int(self._current_id):04d}_*.mp3")
                        )
                    if files:
                        found_word = True
                        playsound(files[0], False)
        else:
            files = list(
            self._deck_directory.glob(f"audio/{int(self._current_id):04d}_*.mp3")
            )
            playsound(files[0], False)


            
    def _process_rating(self, rated_tone: Tones) -> None:
        current_tone = Tones(
                            self._words_dict[self._current_id]["Romanisation"]["Tone"]
                        )
        print(f"pressed: {rated_tone}, true: {current_tone}")
        if rated_tone != current_tone:
            self._ask_tones(rating = False)
        else:
            self._ask_tones(rating = True)
