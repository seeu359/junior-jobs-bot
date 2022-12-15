from aiogram import executor
from jun_jobs_bot.bot import dp
from jun_jobs_bot.handlers.info_handler import register_info_handlers
from jun_jobs_bot.handlers.primary_handler import register_primary_handlers
from loguru import logger

"""Entry point"""


def main():
    register_primary_handlers(dp)
    register_info_handlers(dp)
    logger.info('Bot started!')
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
