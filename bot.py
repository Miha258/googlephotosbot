from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from Google import InvalidCode
from init_service import *
from photos import *
from json_manager import *

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


#run dcoker file
os.system('cd server')
os.system('docker run -p 49160:3000 -d m1haa/node-web-app')

@dp.message_handler(lambda message: message.new_chat_members[0].is_bot,content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def on_bot_join_channel(message: types.Message):
    if check_token_exist():
        album_name = message.chat.full_name
        album_id = create_album(album_name)
        add_to_json(album_name,album_name,album_id)
    else:

        await message.answer('Токен авторизації відсутній.Помилка')
        await bot.leave_chat(message.chat.id)


@dp.message_handler(lambda message: message.left_chat_member.is_bot,content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def on_bot_left_channel(message: types.Message):
    remove_from_json(message.chat.full_name)
        

@dp.message_handler(content_types=[ContentType.DOCUMENT,ContentType.PHOTO])
async def save_img(message: types.Message):
    if check_token_exist():
        album_name = get_from_json(message.chat.full_name)['album_name']
        if album_name:
            file_name = f'{message.message_id}.jpg'
            if message.document:
                await message.document.download(destination_file=file_name)
            else:
                await message.photo[-1].download(destination_file=file_name)
            insert_mediafile_in_album(album_name,file_name)


@dp.message_handler(commands='settoken')
async def change_account(message: types.Message):
    if check_token_exist():
        os.remove('token_photoslibrary_v1.pickle')
    await Form.code.set() 
    auth_url = get_auth_url()
    await message.answer(f'Перейдіть по цьому посиланню і виберіть аккаунт після надішліть кінцеве посилання мені:\n{auth_url}')
    

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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)