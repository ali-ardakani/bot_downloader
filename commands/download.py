from dis import show_code
import wget
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from pathlib import Path
from config.settings import path_root
from urllib.error import HTTPError
from .link import _get_links
import requests

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


def _download(url: str, path: str):
    """
    Download a file from a url.
    :param url: The url of the file.
    :type url: str
    :param path: The path of the file.
    :type path: str

    :return: None
    :rtype: None
    """
    get_response = requests.get(url, stream=True, allow_redirects=True)
    file_name = url.split("/")[-1]
    if get_response.status_code == 200:
        with open(f"{path}/{file_name}", 'wb') as f:
    
            _current_size = 0
            total_size = get_response.headers.get('content-length')
            
            if total_size is None:
                f.write(get_response.content)
            else:
                total_size = int(total_size)
                if total_size < 1048563 * 10:
                    step = 24
                elif total_size < 1048563 * 100:
                    step = 12
                elif total_size < 1048563 * 300:
                    step = 6
                else:
                    step = 1
                show_bar = None
                for data in get_response.iter_content(chunk_size=4096):
                    f.write(data)
                    _current_size += len(data)
                    done = int(50 * _current_size / total_size)
                    
                    # If the download is done or the _current_size divided by step equals to zero,
                    # then print the progress bar.
                    if not show_bar or 100 * _current_size // total_size == show_bar:
                        show_bar = (100 * _current_size // total_size) + step
                        bar_adaptive(_current_size, total_size, width=100)
                        
                    
                    if done == 100:
                        break
    else:
        raise HTTPError(get_response.status_code)


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
    links = _get_links(update, context, user=True, status="active")
    if links:
        for link in links:
            _link = link
            path = f'{path_root}/media/{update.message.from_user.id}/'
            Path(path).mkdir(parents=True, exist_ok=True)
            try:
                _download(link.url, path)
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
