import wget
from telegram.update import Update
from telegram.user import User
from telegram.ext.callbackcontext import CallbackContext
from models import User, Link
from pathlib import Path
from config.settings import path_root
from urllib.error import HTTPError

def get_links():
    """
    Get the links from the database.
    :return: A list of links.
    :rtype: list of links or None if there are no links.
    """
    try:
        links = Link.select().where(Link.status == 'active')
    except Link.DoesNotExist:
        links = None

    return links

_update = None

def bar_adaptive(current, total, width=80):
    """
    Show a progress bar in the bot.
    :param current: The current progress.
    :type current: int
    :param total: The total progress.
    :type total: int
    :param width: The width of the progress bar.
    :type width: int

    :return: None
    :rtype: None
    """

    global _update
    output = wget.bar_adaptive(current, total, width=width)
    _update.message.reply_text(output)
    

def download(update: Update, context: CallbackContext):
    """
    Download the link.
    :param update: The update that contains the message.
    :type update: telegram.update.Update
    :param context: The context of the command.
    :type context: telegram.ext.callbackcontext.CallbackContext

    :return: None
    :rtype: None
    """
    global _update
    global _link
    _update = update
    links = get_links()
    if links:
        for link in links:
            _link = link
            path = f'{path_root}/media/{update.message.from_user.id}/'
            Path(path).mkdir(parents=True, exist_ok=True)
            try:
                wget.download(link.url, out=path, bar=bar_adaptive)
            except HTTPError as e:
                update.message.reply_text(f'Error: {e}')
                link.status = 'error'
                link.error = str(e)
                link.save()
            else:    
                link.status = 'completed'
                link.save()
                update.message.reply_text(
                    "Downloaded %s" % link.url)

    else:
        update.message.reply_text(
            "No links to download")