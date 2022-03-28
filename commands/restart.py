from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from config.settings import updater
import subprocess
import os

def restart(update: Update, context: CallbackContext):
    """restart the bot.
    :param update: The update that contains the message.
    :type update: telegram.update.Update
    :param context: The context of the command.
    :type context: telegram.ext.callbackcontext.CallbackContext
    
    :return: None
    :rtype: None
    """
    update.message.reply_text(
        "restarting bot.")
    # os.system("pkill -9 -f manage.py && python manage.py run")
    subprocess.call("commands/restart.sh", shell=True)
