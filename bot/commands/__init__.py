
from .llm import (
    llm_generate_command,
    get_prefix_command,
    set_prefix_command,
)
from .karma import (
    set_karma_mode_command,
    get_karma_command,
    get_karma_all_command,
    set_karma_all_command,
    positive_karma_update_command
)
from .language import (
    set_lang_command,
    get_supported_lang_command,
)
# from .antiflood import (
#    set_antiflood_command,
# )
from aiogram import Router
from aiogram.dispatcher.filters import Command
from filters import StartWithFilter, AdminCommandsFilter
from configuration import BOT_CONFIG


def register_commands(router: Router):
    # router.message.register(set_antiflood_command, Command(
    #    commands=SYSTEM_COMMANDS.SET_ANTIFLOOD_command))

    router.message.register(get_supported_lang_command, Command(
        commands=BOT_CONFIG.GET_LANG_COMMANDS.command))
    router.message.register(set_lang_command, Command(
        commands=BOT_CONFIG.SET_LANG_COMMANDS.command))
    router.message.register(set_karma_mode_command, Command(
        commands=BOT_CONFIG.SET_KARMA_MODE_COMMANDS.command))
    router.message.register(get_karma_all_command, Command(
        commands=BOT_CONFIG.GET_KARMA_ALL_COMMANDS.command))
    router.message.register(set_karma_all_command, AdminCommandsFilter(
        commands=BOT_CONFIG.SET_KARMA_ALL_COMMANDS.command))
    router.message.register(get_karma_command, Command(
        commands=BOT_CONFIG.GET_KARMA_COMMANDS.command))
    router.message.register(positive_karma_update_command, StartWithFilter(
        commands=BOT_CONFIG.KARMA_POSITIVE_UPDATE_COMMANDS.command))
    router.message.register(get_prefix_command, Command(
        commands=BOT_CONFIG.GET_PREFIX_COMMANDS.command))
    router.message.register(set_prefix_command, Command(
        commands=BOT_CONFIG.SET_PREFIX_COMMANDS.command))
    router.message.register(llm_generate_command)
