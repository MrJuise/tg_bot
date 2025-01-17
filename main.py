from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import handlers

api = "XXX"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.message_handler(commands=["start"])(handlers.start)
dp.message_handler(text="Информация о боте")(handlers.info)
dp.message_handler(text="Перевести")(handlers.translate_menu)
dp.callback_query_handler(text="trans_bot")(handlers.trans_bot)
dp.message_handler(state=handlers.Photo.photo_bot, content_types=types.ContentType.PHOTO)(handlers.translate_bot)
dp.callback_query_handler(text="trans_giga")(handlers.trans_giga)
dp.message_handler(state=handlers.Photo.photo_giga, content_types=types.ContentType.PHOTO)(handlers.translate_giga)
dp.message_handler(state=handlers.Photo.photo_bot, content_types=[types.ContentType.TEXT
    , types.ContentType.STICKER])(handlers.handle_text)
dp.message_handler(state=handlers.Photo.photo_giga, content_types=[types.ContentType.TEXT
    , types.ContentType.STICKER])(handlers.handle_text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
