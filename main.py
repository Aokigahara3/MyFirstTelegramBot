import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode

from config import settings

dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    url = 'https://upload.wikimedia.org/wikipedia/commons/e/e1/Tie-dye.png'
    await message.answer(
        text=f'{markdown.hide_link(url)}Привет я бот Миши,{markdown.hbold(message.from_user.full_name)}',
        parse_mode=ParseMode.HTML,
    )


@dp.message(Command("help"))
async def handle_help(message: types.Message):
    # text = "По сути я ничего не делаю.\nПиши сообщения дуралей"
    # entity_bold = types.MessageEntity(
    #     type='bold',
    #     offset=len('По сути я '),
    #     length=5,
    # )
    # entities = [entity_bold]
    # await message.answer(text=text, entities=entities)
    text = "По сути я ничего не делаю\nПиши сообщения дуралей"
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message()
async def echo_message(message: types.Message):
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text="Start processing...",
    # )
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text="Detected message...",
    #     reply_to_message_id=message.message_id,
    # )

    await message.answer(
        text="Ща погоди",
    )
    # if message.text:
    #     await message.answer(
    #         text=message.text
    #     )
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Что то новенькое 🙂")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.bot_token,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
