from email import message
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import os

def stop(update: Update, context: CallbackContext):
    """Stop the bot.
    :param update: The update that contains the message.
    :type update: telegram.update.Update
    :param context: The context of the command.
    :type context: telegram.ext.callbackcontext.CallbackContext
    
    :return: None
    :rtype: None
    """
    update.message.reply_text("Stopping bot.")
    os._exit(0)