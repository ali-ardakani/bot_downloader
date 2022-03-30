from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from models import User, Link
import re
import peewee as pw
import requests

def add_link(update: Update, context: CallbackContext):
    """This function is called when the command /add_link is issued.
    param update: The update that contains the message.
    type update: telegram.update.Update
    param context: The context of the command.
    type context: telegram.ext.callbackcontext.CallbackContext

    return: None
    rtype: None
    """
    update.message.reply_text(
        "Please enter the link(s) e.g.\
            https://www.youtube.com/\
            https://www.geeksforgeeks.org/")

def _add_link(update: Update, context: CallbackContext, user: User, url: str):
    """Add a link to the user's list of links.
    :param update: The update that contains the message.
    :type update: telegram.update.Update
    :param context: The context of the command.
    :type context: telegram.ext.callbackcontext.CallbackContext
    param user: The user to add the link to.
    type user: models.User
    param url: The link to add.
    type url: str

    return: None
    rtype: None
    """
    try:
        Link.create(user=user, url=url)
    except pw.IntegrityError:
        link = Link.get(url=url)
        if link.user == user:
            update.message.reply_text(
                "You already have this link.")
        else:
            update.message.reply_text(
                f"This link is already in use by {link.user.username}.")
    else:
        update.message.reply_text(
            "Successfully added link %s" % url)

def validator_link(url: str):
    """Validate the link.
    :param url: The url to validate.
    type url: str

    return: True if the link is valid, False otherwise.
    rtype: bool
    """
    try:
        headers=requests.head(url, allow_redirects=True).headers
    except requests.exceptions.RequestException:
        return False
    content_type = headers.get('content-type')

    if 'text' in content_type.lower():
        downloadable = False
    elif 'html' in content_type.lower():
        downloadable =  False
    else:
        downloadable = True
    
    return downloadable

def _handle_link(update: Update, context: CallbackContext):
    """Handle the link(s).
    :param update: The update that contains the message.
    :type update: telegram.update.Update
    :param context: The context of the command.
    :type context: telegram.ext.callbackcontext.CallbackContext

    :return: None
    :rtype: None
    """
    # Text from the bot contains the \", so we need to remove it.
    text = re.sub('"', '', update.message.text).strip().split()

    for url in text:
        if validator_link(url):
            try:
                user = User.get(username=update.message.from_user.id)
            except User.DoesNotExist:
                user = User.create(username=update.message.from_user.id)
                update.message.reply_text(
                    "You are not registered. We created an account for you.")
            _add_link(update, context, user, url)
        else:
            update.message.reply_text(
                "Sorry '%s' is not a valid URL" % url)

def _get_links(update: Update, context: CallbackContext, user: bool=False, url: str=None, status: str=None):
    """Get the links.
    :param update: The update that contains the message.
    :type update: telegram.update.Update
    :param context: The context of the command.
    :type context: telegram.ext.callbackcontext.CallbackContext
    param user: The user to get the links from.
    type user: models.User
    param url: The url to get the links from.
    type url: str
    param status: The status of the links to get.
    type status: str

    return: None or list of links or link
    rtype: None or list of models.Link or models.Link

    description:
        If user is False, then the links are from the all users(default).
        If user is True, then the links are from the user specified.

        If url is False, then the links are from all urls(default).
        If url is True, then return the link with the url specified.

        If status is None, then the links are from all statuses(default).
        If status is not None, then the links are from the status specified(active, error, etc).
    """
    try:
        if url:
            links = Link.get(Link.url == url)
        else:
            if user:
                try:
                    user = User.get(username=update.message.from_user.id)
                except User.DoesNotExist:
                    update.message.reply_text(
                        "ِYou are not registered.\nPlease use /add_user to register and then add links(for help use /add_link).")
                    return None
                links = Link.select().where(Link.user == user)
            else:
                links = Link.select()           

            if status:
                links = links.where(Link.status == status)
    except Link.DoesNotExist:
        links = None
    
    return links

def list_links(update: Update, context: CallbackContext):
    """This function is called when the command /list_links is issued.
    param update: The update that contains the message.
    type update: telegram.update.Update
    param context: The context of the command.
    type context: telegram.ext.callbackcontext.CallbackContext
    return: None
    rtype: None
    """

    links = _get_links(update, context, user=True)
    if links:
        update.message.reply_text(
            "Your links are:\n%s" % '\n'.join([link.url for link in links]))
    else:
        update.message.reply_text(
            "You have no links.\nPlease use /add_link to add links(for help use /add_link).")

def list_errors_links(update: Update, context: CallbackContext):
    """This function is called when the command /list_errors is issued.
    param update: The update that contains the message.
    type update: telegram.update.Update
    param context: The context of the command.
    type context: telegram.ext.callbackcontext.CallbackContext
    return: None
    rtype: None
    """
    try:
        user = User.get(username=update.message.from_user.id)
    except User.DoesNotExist:
        update.message.reply_text(
            "You are not registered.\nPlease use /add_user to register and then add links(for help use /add_link).")
    links = _get_links(update, context, user, status='error')
    if links:
        update.message.reply_text(
            "Your links that have errors:\n%s" % '\n'.join([link.url+"\n"+link.error if link.error else link.url for link in links]))
    else:
        update.message.reply_text(
            "You have no links that have errors.")


def remove(update: Update, context: CallbackContext, url: str):
    """Handle unknown commands.
    :param update: The update that contains the message.
    :type update: telegram.update.Update
    :param context: The context of the command.
    :type context: telegram.ext.callbackcontext.CallbackContext
    
    :return: None
    :rtype: None
    """
    link = _get_links(update, context, url=url)
    if link:
        link.delete_instance()
        update.message.reply_text(
            "Successfully removed link %s" % url)
    else:
        update.message.reply_text(
            "Sorry '%s' is not a valid URL" % url)

def clear(update: Update, context: CallbackContext):
    """Delete all links.
    :param update: The update that contains the message.
    :type update: telegram.update.Update
    :param context: The context of the command.
    :type context: telegram.ext.callbackcontext.CallbackContext

    :return: None
    :rtype: None
    """
    Link.delete().execute()
    update.message.reply_text(
        "Successfully removed all links.")
