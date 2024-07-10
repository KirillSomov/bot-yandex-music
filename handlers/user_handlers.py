
from enum import Enum, EnumMeta
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.methods.create_forum_topic import CreateForumTopic
from aiogram.types import Message, CallbackQuery, ForumTopic, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from yandex_api.yandex_api import get_playlist_df, genre_stat


router = Router()

# Хэндлер для команды /start
@router.message()
async def process_start_command(msg: Message):
    if "https://music.yandex.ru/users/" in msg.text:
        genre_stat(get_playlist_df(msg.text))
        # stat_img = InputFile("/yandex-music-stat.png")
        # await msg.answer_photo(photo=stat_img)
        await msg.answer_photo(photo=FSInputFile("yandex-music-stat.png"))
