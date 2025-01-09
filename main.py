from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import os
import easyocr
from googletrans import Translator
from gigachat import *

api = "7945958530:AAGg5Hg-3Znq02KQGFGz8WkXSGH19WleEhg"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb_in = InlineKeyboardMarkup()
but_start = KeyboardButton(text="Перевести")
but_start1 = KeyboardButton(text="Информация о боте")

in_button = InlineKeyboardButton(text='Перевод бота', callback_data="trans_bot")
in_button1 = InlineKeyboardButton(text='Перевод GigaChat', callback_data="trans_giga")

kb.row(but_start, but_start1)
kb_in.row(in_button, in_button1)

render = easyocr.Reader(['en', 'de', 'es'])  # английский, немецкий, испанский
translator = Translator()


class Photo(StatesGroup):
    photo = State()


@dp.message_handler(commands="start")
async def start(message):
    await message.answer(f"Привет {message.from_user.username}, я бот переводчик", reply_markup=kb)


@dp.message_handler(text="Информация о боте")
async def info(message):
    await message.answer("Я могу перевести текст по фото.")


@dp.message_handler(text="Перевести")
async def translate_menu(message):
    await message.answer("Перевести с помощью:", reply_markup=kb_in)


@dp.callback_query_handler(text="trans_bot")
async def trans_bot(call):
    await call.message.answer("Сфотографируйте то что нужно перевести")
    await Photo.photo.set()


async def download_photo(message: types.Message):
    try:
        photo = message.photo[-1]
        file_id = photo.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        await bot.download_file(file.file_path, file_path)
        return file_path
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

@dp.message_handler(state=Photo.photo, content_types=types.ContentType.PHOTO)
async def trans_bot(message: types.Message, state: FSMContext):
    file_path = await download_photo(message)
    await message.reply("Ожидайте, идет перевод текста с данного фото.")
    result = render.readtext(file_path)
    extract_text = ' '.join([i[1] for i in result])
    await message.reply(f'Ожидайте, идет перевод текста с фото: \n {extract_text}')
    translated_text = translator.translate(extract_text, dest='ru').text
    await message.reply(f'Переведенный текст: \n {translated_text}')
    os.remove(file_path)
    await state.finish()


auth = Auth()
uploader = Upload_to_giga()
extractor = Extract()
token = auth.get_token()


@dp.callback_query_handler(text="trans_giga")
async def trans_giga(call):
    await call.message.answer("Сфотографируйте то что нужно перевести")
    await Photo.photo.set()


@dp.message_handler(state=Photo.photo, content_types=types.ContentType.PHOTO)
async def trans_giga(message: types.Message, state: FSMContext):
    file_path = await download_photo(message)
    await message.reply("Ожидайте, отправляем фото на сервер.")
    with open(file_path, 'rb') as image_file:
        image_data = image_file.read()
    photo_id = uploader.download_giga(token, 'Пример текста', image_data)
    extracted_text = extractor.extracting(token, photo_id)
    await message.reply(f"Текст на картинке:\n{extracted_text}")
    os.remove(file_path)
    await state.finish()


@dp.message_handler(state=Photo.photo, content_types=[types.ContentType.TEXT, types.ContentType.STICKER])
async def handle_text(message: types.Message, state: FSMContext):
    await message.reply("Пожалуйста, отправьте фото для перевода.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
