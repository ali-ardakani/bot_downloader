from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

def start(update: Update, context: CallbackContext):
    """This function is called when the command /start is issued.
    param update: The update that contains the message.
    type update: telegram.update.Update
    param context: The context of the command.
    type context: telegram.ext.callbackcontext.CallbackContext

    return: None
    rtype: None
    """
    
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
        /help to see the commands available.")