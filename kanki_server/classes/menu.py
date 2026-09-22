import pydase
from kanki_server.settings.vocabulary_settings import VocabularySettings
from kanki_server.settings.tone_trainer_settings import ToneTrainerSettings

class Menu(pydase.DataService):
    def __init__(self) -> None:
        super().__init__()

        self.vocabulary_settings = VocabularySettings()
        self.tone_trainer_settings = ToneTrainerSettings()
