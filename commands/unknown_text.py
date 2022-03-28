from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from .link import _handle_link

def unknown_text(update: Update, context: CallbackContext):
    """Handle unknown commands.
    :param update: The update that contains the message.
    :type update: telegram.update.Update
    :param context: The context of the command.
    :type context: telegram.ext.callbackcontext.CallbackContext
    
    :return: None
    :rtype: None
    """

    if update.message.text:
        _handle_link(update, context)
    else:
        update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text)