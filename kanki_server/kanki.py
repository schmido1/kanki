import pydase
from .utils.enums import Mode
from .classes.vocabulary import Vocabulary
from .classes.heisig import  Heisig
from .classes.tone_trainer import ToneTrainer
from .classes.pronounciation import Pronounciation
from .classes.idioms import Idioms
from .classes.menu import Menu


class Kanki(pydase.DataService):
    def __init__(self) -> None:
        super().__init__()
        
        self._mode = Mode.Menu
        self.display = Menu()

    @property
    def mode(self) -> Mode:
        return self._mode
    
    @mode.setter
    def mode(self, value: Mode) -> None:
        # store the settings defined in menu mode
        if self._mode == Mode.Menu:
            self._new_words_per_day = (
                self.display.vocabulary_settings._new_words_per_day
            )
            self._language = (
                self.display.vocabulary_settings._language
            )
            self._romanisation_type = (
                self.display.vocabulary_settings._romanisation_type
            )
            self._characters = self.display.vocabulary_settings._characters

            self._ask_tone1 = (
                self.display.tone_trainer_settings._ask_tone1)
            self._ask_tone2 = (
                self.display.tone_trainer_settings._ask_tone2)
            self._ask_tone3 = (
                self.display.tone_trainer_settings._ask_tone3)
            self._ask_tone4 = (
                self.display.tone_trainer_settings._ask_tone4)
            self._ask_tone5 = ( 
                self.display.tone_trainer_settings._ask_tone5)
            self._ask_tone6 = (
                self.display.tone_trainer_settings._ask_tone6)

        # switch to new mode
        self._mode = value
        match value:
            case Mode.Menu:
                self.display = Menu()
            case Mode.Vokabeln:
                self.display = Vocabulary(
                    self._new_words_per_day,
                    self._language,
                    self._romanisation_type,
                    self._characters,
                )
            case Mode.Heisig:
                self.display = Heisig()
            case Mode.Töne:
                self.display = ToneTrainer(
                    self._ask_tone1,
                    self._ask_tone2,
                    self._ask_tone3,
                    self._ask_tone4,
                    self._ask_tone5,
                    self._ask_tone6
                )
            case Mode.Aussprache:
                self.display = Pronounciation()
            case Mode.Redewendungen:
                self.display = Idioms()
