import pydase

class ToneTrainerSettings(pydase.DataService):
    def __init__(self) -> None:
        super().__init__()

        self._ask_tone1 = True
        self._ask_tone2 = True
        self._ask_tone3 = True
        self._ask_tone4 = True
        self._ask_tone5 = True
        self._ask_tone6 = True


    @property
    def ask_tone1(self) -> None:
        return self._ask_tone1

    @ask_tone1.setter
    def ask_tone1(self, ask_tone1: bool) -> None:
        self._ask_tone1 = ask_tone1

    @property
    def ask_tone2(self) -> None:
        return self._ask_tone2

    @ask_tone2.setter
    def ask_tone2(self, ask_tone2: bool) -> None:
        self._ask_tone2 = ask_tone2

    @property
    def ask_tone3(self) -> None:
        return self._ask_tone3

    @ask_tone3.setter
    def ask_tone3(self, ask_tone3: bool) -> None:
        self._ask_tone3 = ask_tone3

    @property
    def ask_tone4(self) -> None:
        return self._ask_tone4

    @ask_tone4.setter
    def ask_tone4(self, ask_tone4: bool) -> None:
        self._ask_tone4 = ask_tone4
    
    @property
    def ask_tone5(self) -> None:
        return self._ask_tone5

    @ask_tone5.setter
    def ask_tone5(self, ask_tone5: bool) -> None:
        self._ask_tone5 = ask_tone5

    @property
    def ask_tone6(self) -> None:
        return self._ask_tone6

    @ask_tone6.setter
    def ask_tone6(self, ask_tone6: bool) -> None:
        self._ask_tone6 = ask_tone6