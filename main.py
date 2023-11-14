from aiogram.utils import executor
import logging
from config import dp
from db.commands import Database
from handlers import funcs, fsm

funcs.register_handlers_client(dp)
fsm.register_handlers_fsm(dp)

async def on_startup(_):
    db = Database()
    db.sql_create_db()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates = True, on_startup=on_startup)