# Telegram Translator Bot

Этот проект представляет собой Telegram-бота, который позволяет пользователям переводить текст с изображений с помощью
различных методов распознавания и перевода текста, включая EasyOCR и GigaChat API.

## Описание

Бот принимает фотографии и интегрирует функции распознавания текста и перевода. Он поддерживает распознавание текста на
английском, немецком и испанском языках. Пользователи могут выбрать локальную обработку с помощью EasyOCR или
использовать API GigaChat для получения переводов.


## Использование

1. Запустите бота в Telegram и нажмите /start.
   ![1](https://github.com/user-attachments/assets/15849cf1-1c1e-4413-b338-7f8154a4bd67)

2. Выберите опцию "Перевести", чтобы начать процесс перевода.
   ![3](https://github.com/user-attachments/assets/0bb55d05-c473-4610-902c-a2495c9df0b8)

3. Отправьте фотографию с текстом, который нужно распознать и перевести.
   ![4](https://github.com/user-attachments/assets/d6686482-7800-4694-970c-aec8fdda6b11)

4. Бот ответит вам с оригинальным текстом и его переводом.
   ![5](https://github.com/user-attachments/assets/dc4ce11c-41f3-4b1e-80af-a95181eb6b5d)

## Структура проекта

- ├── `main.py`          # Основной файл бота
- ├── `gigachat.py`      # Модуль для работы с GigaChat API
- ├── `handlers.py`      # Модуль с хендлерами
- ├── `keyboard.py`      # Модуль с клавиатурами
- └── `requirements.tx`t # Список зависимостей

### Метод

- `translate_bot(message: types.Message, state: FSMContext)`: Загружает изображение, извлекает текст с помощью EasyOCR и переводит извлеченный текст с помощью GoogleTras.

## Классы

### Auth

Класс для аутентификации в GigaChat API.

#### Методы

- `get_token()`: Получает токен доступа для работы с GigaChat API.

### Upload_to_giga

Класс для загрузки изображений в GigaChat API.

#### Методы

- `download_giga(auth_token, content, image_data)`: Загружает изображение и отправляет запрос на перевод.

### Extract

Класс для извлечения текста с изображений.

#### Метод

- `extracting(auth_token, file_id)`: Извлекает переведенный текст по идентификатору файла из GigaChat API.


