from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext.updater import Updater
import commands as cmd
from config.settings import updater, db

def handlers(updater: Updater):
    """Add commands to updater.
    :param updater: The updater that contains the commands.
    :type updater: telegram.ext.updater.Updater
    """
    updater.dispatcher.add_handler(CommandHandler('start', cmd.start))
    updater.dispatcher.add_handler(CommandHandler('restart', cmd.restart))
    updater.dispatcher.add_handler(CommandHandler('help', cmd.help))
    updater.dispatcher.add_handler(CommandHandler('add_user', cmd.add_user))
    updater.dispatcher.add_handler(CommandHandler('add_link', cmd.add_link))
    updater.dispatcher.add_handler(CommandHandler('list_links', cmd.list_links))
    updater.dispatcher.add_handler(CommandHandler('list_errors', cmd.list_errors_links))
    updater.dispatcher.add_handler(CommandHandler('clear', cmd.clear))
    updater.dispatcher.add_handler(CommandHandler('download', cmd.download))
    updater.dispatcher.add_handler(CommandHandler('stop', cmd.stop))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, cmd.unknown_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, cmd.unknown_text))