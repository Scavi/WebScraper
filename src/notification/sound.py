from time import sleep

import chime
from src.notification.abstract_notification import AbstractNotification


class Sound(AbstractNotification):
    def __init__(self, duration: int = 60000, frequency: int = 440) -> None:
        self._duration = duration
        self._frequency = frequency

    def notify(self) -> None:
        while True:
            chime.theme('mario')
            chime.error()
            sleep(3)
