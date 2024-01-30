import asyncio
import csv
import logging
import io
from re import Match

from magic_filter import RegexpMode
from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.client.session import aiohttp

from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode, ChatAction


from config import settings


dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    url = 'https://i.pinimg.com/564x/f2/fc/b6/f2fcb6cbd71d7ee7ce94789855d0c2d3.jpg'
    await message.answer(
        text=f'{markdown.hide_link(url)}Привет, это мой первый бот 🕷,{markdown.hbold(message.from_user.full_name)}',
        parse_mode=ParseMode.HTML,
    )


@dp.message(Command("help", prefix='/!%'))
async def handle_help(message: types.Message):
    # text = "По сути я ничего не делаю.\nПиши сообщения дуралей"
    # entity_bold = types.MessageEntity(
    #     type='bold',
    #     offset=len('По сути я '),
    #     length=5,
    # )
    # entities = [entity_bold]
    # await message.answer(text=text, entities=entities)
    url = 'https://i.pinimg.com/564x/17/ff/d4/17ffd43e60b2ef257f4c49895aab2aca.jpg'
    await message.answer(
        text=f'{markdown.hide_link(url)}Я простой эхо-бот🕸\nПока что я ничего не могу:,{markdown.hbold(message.from_user.full_name)}',
        parse_mode=ParseMode.HTML,
    )


@dp.message(Command("text"))
async def send_txt_file(message: types.Message):
    file = io.StringIO()
    file.write("Это обычный файл который передаётся в блокнот\n")
    file.write("Прикольно что я могу сюда положить любую инфу\n")
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue().encode("utf-8"),
            filename="text.txt",
        ),
    )

@dp.message(Command("csv"))
async def send_txt_file(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    file = io.StringIO()
    csv_writer = csv.writer(file)
    csv_writer.writerow([
        ['Misha Roma Artem Masha']
    ])
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue().encode("utf-8"),
            filename="people.csv",
        ),
    )


@dp.message(Command('pic_file'))
async  def send_pic_file_bufferend(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    url = 'https://i.pinimg.com/736x/22/52/74/2252747ea3be1bfc5052091dd19174fa.jpg'
    async with aiohttp.ClientSession() as sesion:
        async with sesion.get(url) as response:
            result_bytes = await response.read()

    await message.reply_document(
        document=types.BufferedInputFile(
            file=result_bytes,
            filename='one-people-black.jpg'
        ),
    )



@dp.message(Command("code", prefix="/!%"))
async def handle_command_code(message: types.Message):
    text = markdown.text(
        "Here's Python code:",
        "",
        markdown.markdown_decoration.pre_language(
            # markdown.markdown_decoration.pre(
            markdown.text(
                "print('Hello world!')",
                "\n",
                "def foo():\n    return 'bar'",
                sep="\n",
            ),
            language="python"
        ),
    )
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message(Command('pic', prefix=('/!%')))
async def handle_command_pic(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    await message.reply_photo(
        photo=url,
        caption='маленький пин'
    )
url = 'https://i.pinimg.com/736x/22/52/74/2252747ea3be1bfc5052091dd19174fa.jpg'


# F_ITS_MAGIC_FILTERS PHOTO
@dp.message(F.photo, ~F.caption)
async def handle_photo_wo_caption(messege: types.Message):
    await messege.reply('Это фото')

any_media_filters = F.photo | F.video | F.Documents


@dp.message(any_media_filters, ~F.caption)
async def handle_any_media_wo_caption(message: types.Message):
    if message.document:
        await  message.reply_document(
            document=message.document.file_id,
            action=ChatAction.UPLOAD_PHOTO,
        )
    elif message.video:
        await message.reply_video(
            video=message.video.file_id,
            action=ChatAction.UPLOAD_PHOTO,
        )
    else:
        await message.reply('Я вижу файл')


@dp.message(F.from_user.id.in_({42, 996567711}), F.text == 'secret')
async def secret_admin_message(message: types.Message):
    await message.reply('Привет админ')


@dp.message(F.text.regexp(r"(\d+)", mode=RegexpMode.MATCH).as_("code"))
async def handle_code(message: types.Message, code: Match[str]):
    await message.reply(f"Your code: {code.group()}")


@dp.message()
async def echo_message(message: types.Message):
    await message.answer(
        text="Ща погоди 🕷",
    )


    try:
        await message.copy_to(chat_id=message.chat.id)
        # await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Что то новенькое")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.bot_token,
        parse_mode=ParseMode.HTML
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
