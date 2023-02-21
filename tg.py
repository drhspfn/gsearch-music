import logging
from aiogram import Dispatcher, Bot, executor, types
from api import mAPI


logging.basicConfig(level=logging.INFO)

bot = Bot(token="5309391326:AAFCmpu7w0ZZCDOtUMfluBiJoBu3hO7GmEs")
dp = Dispatcher(bot)



api = mAPI(defb=True)



@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.reply(message.text)


@dp.message_handler()
async def handle_search(message: types.Message):

    try:
        data_path = await api.searchmusic(message.text, logprefix="[B] ->")

        if data_path:

            aud = open(data_path, "rb")
            await message.answer_audio(aud)
            aud.close()
        else:
            await message.answer("Not founded....")


    except KeyboardInterrupt:
        await message.answer("Break search... ctrl + c ;((")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)