import sys
from config.settings import updater, db
from models import User, Link
from config.handlers import handlers





if __name__ == '__main__':
    if sys.argv[1] == 'run':
        handlers(updater)
        updater.start_polling()
    elif sys.argv[1] == 'migrate':
        db.connect()
        db.create_tables([User, Link], safe=True)
