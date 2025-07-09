import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
async def main():
    session = AiohttpSession()
    bot = Bot(token=API_TOKEN, session=session)
    dp = Dispatcher()

    # Register command handler
    @dp.message(Command("start", "help"))
    async def command_start_handler(message: types.Message):
        await message.reply("kam bola kr smza")
        
    @dp.message_handler()
    async def echo(message: types.Message):
        """
        This will return echo
        """
        await message.answer(message.text)

    
    # Start polling
    await dp.start_polling(bot)

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
