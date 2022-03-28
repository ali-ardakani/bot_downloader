from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

def help(update: Update, context: CallbackContext):
    """This function is called when the command /help is issued.
    param update: The update that contains the message.
    type update: telegram.update.Update
    param context: The context of the command.
    type context: telegram.ext.callbackcontext.CallbackContext

    return: None
    rtype: None
    """

    update.message.reply_text(f"""
    This is a bot that can be used to download everithing you want.You can use it to download videos, images, audio, documents, etc. 
    All downloads are saved in a media/{update.message.from_user.id} folder.
    
    You can use the following commands:
    /help - Show this message.
    /add_user - Add your user
    /add_link - Add a link to download.
    /list_links - List all links.
    /list_errors - List all links with errors.
    /remove - Remove a url from the queue e.g. /remove http://www.google.com
    /clear - Clear all links.
    /restart - Restart the bot.
    /download - Download all links.
    """)
