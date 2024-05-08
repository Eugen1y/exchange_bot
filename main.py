import asyncio
import logging
import os
import config

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import FSInputFile

from currency import make_answer, generate_excel
from datetime import datetime, timedelta

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties())
dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Привет!")


@dp.message(Command('get_exchange_rate'))
async def get_exchange_rate(message: types.Message):
    excel_filename = await generate_excel()
    await message.answer_document(document=FSInputFile(excel_filename))

    os.remove(excel_filename)


async def scheduled():
    while True:

        while True:
            now = datetime.now()

            next_hour = now + timedelta(hours=1)
            next_hour = next_hour.replace(minute=0, second=0, microsecond=0)

            delta = next_hour - now

            await asyncio.sleep(delta.total_seconds())
            await make_answer()


async def main():
    await asyncio.gather(
        dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()),
        scheduled()
    )


if __name__ == "__main__":
    logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(main())
