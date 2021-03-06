from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import subprocess
import os
import sys

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
    
    os.execv(sys.executable, ['python'] + sys.argv)
