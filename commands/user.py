from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from models import User

def add_user(update: Update, context: CallbackContext):
    """This function is called when the command /add_user is issued.
    param update: The update that contains the message.
    type update: telegram.update.Update
    param context: The context of the command.
    type context: telegram.ext.callbackcontext.CallbackContext
    return: None
    rtype: None
    """
    user = User.create(username=update.message.from_user.id)
    update.message.reply_text(
        "Successfully added user %s" % user.username)