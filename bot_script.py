from aiogram import executor
from jun_jobs_bot import bot
from jun_jobs_bot.handlers.info_handler import register_info_handlers
from jun_jobs_bot.handlers.primary_handler import register_primary_handlers
from loguru import logger

"""Entry point"""


def main():
    register_primary_handlers(bot.dp)
    register_info_handlers(bot.dp)
    logger.info('Bot started!')
    executor.start_polling(bot.dp, skip_updates=True)


if __name__ == '__main__':
    main()
