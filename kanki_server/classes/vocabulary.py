import json
import os
import random
from pathlib import Path
from datetime import datetime, timezone
from playsound3 import playsound

from kanki_server.utils.enums import Language, RomanisationType, Type

from pydase import DataService
from pydase.utils.decorators import frontend
from kanki_server.utils.system_conversion import jyutping_to_yale
from kanki_server.utils.enums import (
    Characters,
    InitialsJyutping,
    MiddlesJyutping,
    Finals,
    Tones,
)
from fsrs import (
    Scheduler,
    Card,
    Rating,
    ReviewLog,
)



class Phoneme(DataService):
    def __init__(
            self,
            phoneme_dict: dict,
            mapping_dict: dict,
            language: Language,
            romanisation_type: RomanisationType,
            characters: Characters
        ) -> None:
        super().__init__()
        if characters == Characters.Traditional:
            self.character = phoneme_dict["Traditional Character"]
        elif characters == Characters.Simplified:
            self.character = phoneme_dict["Simplified Character"]

        initial = InitialsJyutping(phoneme_dict["Romanisation"]["Initial"])
        middle = MiddlesJyutping(phoneme_dict["Romanisation"]["Middle"])
        final = Finals(phoneme_dict["Romanisation"]["Final"])
        tone = Tones(phoneme_dict["Romanisation"]["Tone"])

        if romanisation_type == RomanisationType.Jyutping:
            self.romanisation = (
                initial.value
                + middle.value
                + final.value
                + tone.value
            )
        elif romanisation_type == RomanisationType.Yale:
            self.romanisation = jyutping_to_yale(
                initial,
                middle,
                final,
                tone
            )

        match language:
            case Language.Deutsch:
                self.translation = phoneme_dict["Übersetzung"]
            case Language.English:
                self.translation = phoneme_dict["Translation"]
        
        initial_mapping = mapping_dict["Initials"][initial.value]
        middle_mapping = mapping_dict["Middles"][middle.value]
        final_mapping = mapping_dict["Finals"][final.value]
        tone_mapping = mapping_dict["Tones"][tone.value]

        self.mapping = (
            initial_mapping + ", "
            + middle_mapping + ", "
            + final_mapping + ", "
            + tone_mapping
        )


class Word:
    def __init__(
            self,
            id: int,
            words_dict: dict,
            mapping_dict: dict,
            language: Language,
            romanisation_type: RomanisationType,
            characters: Characters,
            ) -> None:

        word_dict = words_dict[str(id)]

        if word_dict["Type"] == "Phoneme":
            self.type = Type.Phoneme
            phoneme = Phoneme(
                word_dict,
                mapping_dict,
                language,
                romanisation_type,
                characters,
            )
            self.character = phoneme.character
            self.romanisation = phoneme.romanisation
            self.mapping = phoneme.mapping
        elif word_dict["Type"] == "Composite":
            self.type = Type.Composite
            self.character = ""
            self.romanisation = ""
            self.phonemes = []
            for phoneme_id in word_dict["Phonemes"]:
                phoneme = Phoneme(
                    words_dict[phoneme_id],
                    mapping_dict,
                    language,
                    romanisation_type,
                    characters,
                )
                self.character += phoneme.character
                self.romanisation += phoneme.romanisation + " "
                self.phonemes.append(phoneme)
            
        match language:
            case Language.Deutsch:
                self.translation = word_dict["Übersetzung"]
                self.example = word_dict["Beispiel"]
                self.comment = word_dict["Kommentar"]
            case Language.English:
                self.translation = word_dict["Translation"]
                self.example = word_dict["Example"]
                self.comment = word_dict["Comment"]

        
class FrontsideForward(DataService):
    """Used to display frontside of wordcard
    from cantonese to english/german."""
    def __init__(
            self,
            word: Word,
    ) -> None:
        super().__init__()
        
        self._character = word.character
        self._romanisation = word.romanisation

    @property
    def character(self) -> str:
        return self._character

    @property
    def romanisation(self) -> str:
        return self._romanisation


class FrontsideReversed(DataService):
    """Used to display frontide of wordcard
    from english/german to cantonese."""
    def __init__(
            self,
            word: Word,
    ) -> None:
        super().__init__()

        self._translation = word.translation

    @property
    def translation(self) -> str:
        return self._translation
 

class BacksideForwardComposite(DataService):
    """Used to display backside of wordcard
    from cantonese to english/german when the
    shown word is a composite type."""
    def __init__(
        self,
        word: Word,
    ) -> None:
        super().__init__()

        self._translation = word.translation
        self._phonemes = word.phonemes
        self._example = word.example
        self._comment = word.comment

    @property
    def translation(self) -> str:
        return self._translation
    
    @property
    def phonemes(self) -> list[Phoneme]:
        return self._phonemes
    
    @property
    def example(self) -> str:
        return self._example
    
    @property
    def comment(self) -> str:
        return self._comment
    
class BacksideForwardPhoneme(DataService):
    """Used to display backside of wordcard
    from cantonese to english/german when the
    shown word is a phoneme type."""
    def __init__(
        self,
        word: Word,
    ) -> None:
        super().__init__()

        self._translation = word.translation
        self._mapping = word.mapping
        self._example = word.example
        self._comment = word.comment

    @property
    def translation(self) -> str:
        return self._translation
    
    @property
    def mapping(self) -> str:
        return self._mapping
    
    @property
    def example(self) -> str:
        return self._example
    
    @property
    def comment(self) -> str:
        return self._comment
    

class BacksideReversed(DataService):
    """Used to display backside of wordcard
    from english/german to cantonese."""
    def __init__(
        self,
        word: Word,
    ) -> None:
        super().__init__()

        self._character = word.character
        self._romanisation = word.romanisation
        self._example = word.example
        self._comment = word.comment
        self._mapping = word.mapping

    @property
    def character(self) -> str:
        return self._character
    
    @property
    def romanisation(self) -> str:
        return self._romanisation
    
    @property
    def example(self) -> str:
        return self._example
    
    @property
    def comment(self) -> str:
        return self._comment
    
    @property
    def mapping(self) -> str:
        return self._mapping


class WordCard(DataService):
    def __init__(
        self,
        word: Word | None,
        id: int,
        show_frontside: bool,
        show_backside: bool,
        deck_directory,
    ) -> None:
        super().__init__()
        if isinstance(word, Word):
            if show_frontside:
                if id > 0:
                    files = list(deck_directory.glob(
                        f"vocabulary/audio/{id:04d}_*.mp3")
                    )
                    if files:
                        playsound(files[0], False)
                    else:
                        print(f"No matching file found for id: {id:04d}")
                    self.frontside = FrontsideForward(word)
                elif id < 0:
                    self.frontside = FrontsideReversed(word)
            
            if show_backside:
                if id > 0:
                    if word.type == Type.Composite:
                        self.backside = BacksideForwardComposite(word)
                    elif word.type == Type.Phoneme:
                        self.backside = BacksideForwardPhoneme(word)
                elif id < 0:
                    files = list(deck_directory.glob(
                        f"vocabulary/audio/{abs(id):04d}_*.mp3"
                    ))
                    if files:
                        playsound(files[0], False)
                    else:
                        print(f"No matching file found for id: {abs(id):04d}")
                    self.backside = BacksideReversed(word)
        else:
            self.Fertig = "für heute.."
        

class Vocabulary(DataService):

    def __init__(
            self,
            new_words_per_day: int,
            language: Language,
            romanisation_type: RomanisationType,
            characters: Characters,
        ) -> None:
        super().__init__()

        self._language = language
        self._romanisation_type = romanisation_type
        self._new_words_per_day = new_words_per_day
        self._characters = characters

        self._deck_directory = Path(os.environ["KANKI_DECK_DIR"])
        self._scheduler = Scheduler() # TODO: Import from json

        # load the mapping dictionary
        with open(
            self._deck_directory / "personal/mapping.json") as fp:
            self._mapping_dict = json.load(fp)
        
        # load the word dictionaries
        with open(self._deck_directory / "vocabulary/words.json") as fp:
            self._words_dict = json.load(fp)

        # load the card dictionary
        with open(self._deck_directory / "personal/cards.json") as fp:
            self._cards_dict = json.load(fp)

        # define the ids for the new words
        self._query_ids = []
        last_word_id = len(self._words_dict)
        last_card_id = len(self._cards_dict) // 2 # for every word there are two cards
        assert last_word_id >= last_card_id, "There are more cards than words."
        for id in range(
            last_card_id + 1,
            min(last_card_id + 1 + self._new_words_per_day, last_word_id + 1),
        ):
            self._query_ids.extend([id, -id])

        # define the ids for the due words
        now = datetime.now(timezone.utc)

        for card_id in self._cards_dict:
            due = datetime.fromisoformat(self._cards_dict[card_id]["due"])
            if due <= now:
                self._query_ids.append(int(card_id))


        self._current_word = self._get_word()
        self._show_frontside()

    @frontend
    def again(self) -> None:
        self._process_rating(Rating.Again)

    @frontend
    def hard(self) -> None:
        self._process_rating(Rating.Hard)

    @frontend
    def good(self) -> None:
        self._process_rating(Rating.Good)

    @frontend
    def easy(self) -> None:
        self._process_rating(Rating.Easy)

    def _get_word(self) -> Word | None:
        if len(self._query_ids) > 0:
            # pick a random id from the list
            idx = random.randint(0, len(self._query_ids) - 1)
            self._current_id = self._query_ids.pop(idx)

            return Word(
                abs(self._current_id),
                self._words_dict,
                self._mapping_dict,
                self._language,
                self._romanisation_type,
                self._characters,
            )
        else:
            return None

    def _show_frontside(self) -> None:
            self.wordcard = WordCard(
                self._current_word,
                self._current_id,
                True,
                False,
                self._deck_directory
            )
            self._start_time = datetime.now(timezone.utc)

    @frontend
    def reveal_backside(self) -> None:
        if isinstance(self._current_word, Word):
            self.wordcard = WordCard(
                self._current_word,
                self._current_id,
                True,
                True,
                self._deck_directory
            )

    def _process_rating(self, rating: Rating) -> None:
        if isinstance(self._current_word, Word):
            stop_time = datetime.now(timezone.utc) # TODO: Add timing information

            # create or load card object for current word
            if str(self._current_id) in self._cards_dict:
                current_card_dict = self._cards_dict[str(self._current_id)]
                current_card = Card().from_dict(current_card_dict)
            else:
                current_card = Card(self._current_id)

            # review card with rating
            current_card, current_review_log = (
                self._scheduler.review_card(current_card, rating)
            )

            # save updated card to dict
            current_card_dict = current_card.to_dict()
            self._cards_dict[str(self._current_id)] = current_card_dict
            
            # save card dict json
            with open(self._deck_directory / "personal/cards.json", "w") as fp:
                json.dump(self._cards_dict, fp, indent=4)
            
            
            self._current_word = self._get_word()
            self._show_frontside()
