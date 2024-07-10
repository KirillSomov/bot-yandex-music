
import asyncio
# import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from config_data.config import Config, load_config
from handlers import user_handlers
from states.states import storage


async def main():
    # Загружаем конфиг
    config: Config = load_config(None)

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    # Регистрируем асинхронную функцию в диспетчере,
    # которая будет выполняться на старте бота,
    # dp.startup.register(set_main_menu)
    # Регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
