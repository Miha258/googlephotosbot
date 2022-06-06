from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup  
from aiogram.utils.exceptions import FileIsTooBig

from asyncio.exceptions import TimeoutError
from googleapiclient.errors import HttpError
from Google import InvalidCode
from init_service import *
from photos import *
from json_manager import *
from datetime import datetime
import os

API_TOKEN = '5323882359:AAFIUxLGcdgiEzEsYShmI6CwI9FvX1oKZOc'


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    code = State()


def check_token_exist() -> bool:
    if os.path.exists('token_photoslibrary_v1.pickle'):
        return True
    return False


@dp.message_handler(lambda message: message.new_chat_members[0].is_bot,content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def on_bot_join_channel(message: types.Message):
    if check_token_exist():
        album_name = message.chat.full_name
        if not get_from_json(album_name):
            album_id = create_album(album_name)
            add_to_json(album_name,album_name,album_id)
    else:
        await message.answer('Токен авторизації відсутній.Помилка')
        await bot.leave_chat(message.chat.id)


@dp.message_handler(lambda message: message.left_chat_member.is_bot,content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def on_bot_left_channel(message: types.Message):
    remove_from_json(message.chat.full_name)
        

@dp.message_handler(content_types=[ContentType.DOCUMENT,ContentType.PHOTO,ContentType.VIDEO])
async def save_img(message: types.Message): 
    if check_token_exist() and get_from_json(message.chat.full_name):
        album_name = get_from_json(message.chat.full_name)['album_name']
        if album_name:
            try:
                if not get_from_json(message.chat.full_name)['album_id']:
                    album_id = create_album(album_name)
                    change_album_id(message.chat.full_name,album_id)
                
                file_url = None
                if message.document:
                    file_url = await message.document.get_url()
                elif message.photo:
                    file_url = await message.photo[-1].get_url()
                elif message.video: 
                    file_url = await message.video.get_url()
                if file_url:
                    await insert_mediafile_in_album(album_name,file_url,str(message.message_id))
                    
            except FileIsTooBig:
                await message.reply('Файл завелкикий для збереження')
            except HttpError:
                await message.reply('Щось пішло не так.Не можу знайти альбом для збереження.Спробуйте видалити і добавити мене \n або ви поставили не той аккаунт')
            except TimeoutError:
                await message.reply('Помилка завантаження відео')
    else:
        await message.reply(f'Токен авторизації відсутній.Помилка')
        await bot.leave_chat(message.chat.id)


@dp.message_handler(commands='settoken')
async def change_account(message: types.Message):
    if check_token_exist():
        os.remove('token_photoslibrary_v1.pickle')
    await Form.code.set()
    auth_url = get_auth_url()
    await message.answer(f'Перейдіть по цьому посиланню і виберіть аккаунт після цього надішліть мені код:\n{auth_url}')
    

@dp.message_handler(state=Form.code)
async def check_code(message: types.Message, state: FSMContext):
    try:
        code = message.text
        init_service(code)
    except InvalidCode:
        await message.answer('Код не дійсний.Схоже ви допустили помилку при введені коду,або ви пізно його ввели')
    else:
        await state.finish()
        await message.answer('Токен успішно згенеровано')
        remove_all_albums_id()

if __name__ == '__main__':
    if datetime.now().hour > 19:
        for file in os.listdir('./'):
            os.remove(file)
    executor.start_polling(dp, skip_updates=True)
