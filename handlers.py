from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import os
import easyocr
from googletrans import Translator
from aiogram import types
from keyboard import *
from gigachat import *

render = easyocr.Reader(['en', 'de', 'es'])  # английский, немецкий, испанский
translator = Translator()


class Photo(StatesGroup):
    photo_bot = State()
    photo_giga = State()


auth = Auth()
uploader = Upload_to_giga()
extractor = Extract()
token = auth.get_token()


async def download_photo(message: types.Message):
    from main import bot
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


async def start(message):
    await message.answer(f"Привет {message.from_user.username}, я бот переводчик", reply_markup=kb)


async def info(message):
    await message.answer("Я могу перевести текст по фото с разных языков. Английский, немецкий и испанский.")


async def translate_menu(message):
    await message.answer("Перевести с помощью:", reply_markup=kb_in)


async def trans_bot(call):
    await call.message.answer("Сфотографируйте то что нужно перевести")
    await Photo.photo_bot.set()


async def translate_bot(message: types.Message, state: FSMContext):
    file_path = await download_photo(message)
    await message.reply("Ожидайте, идет обработка фото.")
    result = render.readtext(file_path)
    extract_text = ' '.join([i[1] for i in result])
    await message.reply(f'Текст на фото: \n {extract_text}')
    translated_text = translator.translate(extract_text, dest='ru').text
    await message.reply(f'Переведенный текст: \n {translated_text}')
    os.remove(file_path)
    await state.finish()


async def trans_giga(call):
    await call.message.answer("Сфотографируйте то что нужно перевести")
    await Photo.photo_giga.set()


async def translate_giga(message: types.Message, state: FSMContext):
    file_path = await download_photo(message)
    await message.reply("Ожидайте, отправляем фото на сервер.")
    with open(file_path, 'rb') as image_file:
        image_data = image_file.read()
    photo_id = uploader.download_giga(token, 'Пример текста', image_data)
    extracted_text = extractor.extracting(token, photo_id)
    await message.reply(f"Переведенный текст т фото:\n{extracted_text}")
    os.remove(file_path)
    await state.finish()


async def handle_text(message: types.Message, state: FSMContext):
    await message.reply("Пожалуйста, отправьте фото для перевода.")
