import pydase
from kanki_server.utils.enums import (
    Language,
    RomanisationType,
    Characters
)

class VocabularySettings(pydase.DataService):
    def __init__(self) -> None:
        super().__init__()
    
        self._new_words_per_day = 3
        self._language = Language.Deutsch
        self._romanisation_type = RomanisationType.Yale
        self._characters = Characters.Traditional

    @property
    def new_words_per_day(self) -> int:
        return self._new_words_per_day
    
    @new_words_per_day.setter
    def new_words_per_day(self, value: int) -> None:
        self._new_words_per_day = value

    @property
    def language(self) -> Language:
        return self._language
    
    @language.setter
    def language(self, value: Language) -> None:
        self._language = value

    @property
    def romanisation_type(self) -> RomanisationType:
        return self._romanisation_type
    
    @romanisation_type.setter
    def romanisation_type(self, value: RomanisationType) -> None:
        self._romanisation_type = value

    @property
    def characters(self) -> Characters:
        return self._characters
    
    @characters.setter
    def characters(self, value: Characters) -> None:
        self._characters = value
