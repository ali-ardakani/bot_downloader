from telegram.ext.updater import Updater
from peewee import SqliteDatabase
import os
from dotenv import load_dotenv

path_root = os.getcwd()
path_env = path_root + '/config/.env'
load_dotenv(path_env)
token = os.getenv('TOKEN')
updater = Updater(token,
                  use_context=True)
db = SqliteDatabase(f'{path_root}/queue.db')

