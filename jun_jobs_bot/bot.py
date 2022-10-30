from jun_jobs_bot import settings
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=settings.TG_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
