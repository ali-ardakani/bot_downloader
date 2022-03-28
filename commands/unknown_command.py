from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from .link import remove

def unknown_command(update: Update, context: CallbackContext):
    """Handle unknown commands.
    :param update: The update that contains the message.
    :type update: telegram.update.Update
    :param context: The context of the command.
    :type context: telegram.ext.callbackcontext.CallbackContext
    
    :return: None
    :rtype: None
    """
    if "/remove" in update.message.text:
        remove(update, context, update.message.text.strip().split(" ")[1])
    else:
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text)