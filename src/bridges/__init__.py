"""
    Модуль позволяет переводить в читабельный для программы формат расписания
"""

from abc import ABC, abstractmethod
from models import Schedule
from typing import List, AsyncGenerator

class LessonInfo(Schedule):
    weekday:str | None = None

class Bridge(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    async def generateLessons(self) -> AsyncGenerator:
        pass