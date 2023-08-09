import os
from dotenv import load_dotenv
import json
from .models import Config, Command, Message


load_dotenv()
# SUPPORTED_LANGUAGES = list(LANGUAGES.keys())

POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_NAME = os.environ.get("POSTGRES_NAME")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASS = os.environ.get("POSTGRES_PASS")

REDIS_DB = None
REDIS_PASSWORD = os.environ.get("REDIS_PASS")
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")


def __get_words_from_json(path):
    file = open(path)
    patterns = []
    data = json.load(file)
    for i in data['words']:
        patterns.append(i)
    file.close()
    return patterns


SUPPORTED_LANGUAGES = {
    'Russian': 'ru',
    'English': 'en',
    'Ukrainian': 'uk',
    'Hindi': 'hi',
    'Indonesian': 'id',
    'Portuguese': 'pt'
}
SUPPORTED_LANGUAGES_CODES = SUPPORTED_LANGUAGES.values()
SUPPORTED_LANGUAGES_NAMES = SUPPORTED_LANGUAGES.keys()
DEFAULT_LANGUAGE = 'ru'


class BotConfig(Config):
    SUPPORTED_LANGUAGES = {
        'Russian': 'ru',
        'English': 'en',
        'Ukrainian': 'uk',
        'Hindi': 'hi',
        'Indonesian': 'id',
        'Portuguese': 'pt'
    }
    SUPPORTED_LANGUAGES_CODES = SUPPORTED_LANGUAGES.values()
    SUPPORTED_LANGUAGES_NAMES = SUPPORTED_LANGUAGES.keys()

    LLM_LANG = 'en'
    LLM_MAX_LEN = 5

    POSITIVE_KARMA_CHANGE = 1
    NEGATIVE_KARMA_CHANGE = -1

    DEFAULT_KARMA_MODE = False
    DEFAULT_LANG = 'ru'
    DEFAULT_KARMA_VALUE = 0
    DEFAULT_ANTIFLOOD = True
    DEFAULT_PREFIX = ''

    KARMA_POSITIVE_UPDATE_COMMANDS = Command(['спасибо', '+', 'спс', 'согласен'],
                                             'используйте эти слова чтобы повысить карму участника',
                                             DEFAULT_LANGUAGE)
    GET_KARMA_COMMANDS = Command(
        ['get_karma'], 'возвращает вашу карму', DEFAULT_LANGUAGE)
    SET_KARMA_ALL_COMMANDS = Command(
        ['set_karma_all'], 'set_karma_all [value], ставит карму всех участников чата на указаное значение', DEFAULT_LANGUAGE)
    GET_KARMA_ALL_COMMANDS = Command(
        ['get_karma_all'], 'возвращает карму всех участников чата', DEFAULT_LANGUAGE)
    SET_LANG_COMMANDS = Command(
        ['set_lang'], 'set_lang [lang_code] устанавливает язык из списка поддерживаемых языков', DEFAULT_LANGUAGE)
    GET_LANG_COMMANDS = Command(
        ['get_langs'], 'возвращает список поддерживаемых языков', DEFAULT_LANGUAGE)
    SET_KARMA_MODE_COMMANDS = Command(
        ['karma_mode'], 'karma_mode [on, off] включает/выключает режим кармы', DEFAULT_LANGUAGE)
    ADD_STOP_WORD_COMMANDS = Command(
        ['add_stop_word'], 'добавляет стоп слова', DEFAULT_LANGUAGE)
    GET_STOP_WORD_COMMANDS = Command(
        ['get_stop_words'], 'возвращает все стоп слова', DEFAULT_LANGUAGE)
    DELETE_STOP_WORD_COMMANDS = Command(
        ['delete_stop_word'], 'delete_stop_word [word] удаляет указанное вами стоп слово', DEFAULT_LANGUAGE)
    SET_ANTIFLOOD_COMMANDS = Command(
        ['antiflood'], 'antiflood [on, off] включает/выключает антифлуд', DEFAULT_LANGUAGE)
    GET_PREFIX_COMMANDS = Command(
        ['get_prefix'], 'возвращает прификс для языковой модели', DEFAULT_LANGUAGE)
    SET_PREFIX_COMMANDS = Command(
        ['set_prefix'], 'set_prefix [text] устанавливает префикс для языковой модели', DEFAULT_LANGUAGE)
    SUCCESSFUL_ADD_STOP_WORDS_MESSAGE = Message(
        'стоп слова успешно добавлены', DEFAULT_LANGUAGE)
    STOP_WORDS_NOT_FOUND_MESSAGE = Message(
        'стоп слова не найдены', DEFAULT_LANGUAGE)
    ARG_NOT_RECOGNIZED_MESSAGE = Message(
        'аргумент не распознан', DEFAULT_LANGUAGE)
    LANGUAGE_NOT_SUPPORTED_MESSAGE = Message(
        'этот язык не поддерживается', DEFAULT_LANGUAGE)
    KARMA_MODE_EXCEPTION_MESSAGE = Message(
        'режим кармы отключен', DEFAULT_LANGUAGE)
    SUCCESSFUL_LANG_SET_MESSAGE = Message(
        'язык успешно изменен', DEFAULT_LANGUAGE)
    KARMA_POSITIVE_UPDATE_MESSAGE = Message(
        'вам повысили карму, ваша карма - ', DEFAULT_LANGUAGE)
    ZERO_KARMA_MEMBERS_MESSAGE = Message(
        'карма всех участников - ', DEFAULT_LANGUAGE)
    KARMA_MODE_UPDATE_MESSAGE = Message('режим кармы ', DEFAULT_LANGUAGE)
    SUCCESS_RESULT_MESSAGE = Message(
        'команда выполнена успешно', DEFAULT_LANGUAGE)
    UNSUCCESS_RESULT_MESSAGE = Message(
        'не удалось выполнить команду', DEFAULT_LANGUAGE)
    PARSING_ERROR_MESSAGE = Message('аргумент не распознан', DEFAULT_LANGUAGE)
    KARMA_STATE_MESSAGE = Message('ваша карма - ', DEFAULT_LANGUAGE)
    ON = Message('включен', DEFAULT_LANGUAGE)
    OFF = Message('выключен', DEFAULT_LANGUAGE)
    ON_STATE = 'on'
    OFF_STATE = 'off'

    def get_on_state(self, lang):
        return self.ON.get(lang)

    def get_off_state(self, lang):
        return self.OFF.get(lang)

    def get_successful_add_stop_words_message(self, lang):
        return self.SUCCESSFUL_ADD_STOP_WORDS_MESSAGE.get(lang)

    def get_stop_words_not_found_message(self, lang):
        return self.STOP_WORDS_NOT_FOUND_MESSAGE.get(lang)

    def get_arg_not_recognized_message(self, lang):
        return self.ARG_NOT_RECOGNIZED_MESSAGE.get(lang)

    def get_language_not_supported_message(self, lang):
        return self.LANGUAGE_NOT_SUPPORTED_MESSAGE.get(lang)

    def get_karma_mode_exception_message(self, lang):
        return self.KARMA_MODE_EXCEPTION_MESSAGE.get(lang)

    def get_successful_lang_set_message(self, lang):
        return self.SUCCESSFUL_LANG_SET_MESSAGE.get(lang)

    def get_success_result_message(self, lang):
        return self.SUCCESS_RESULT_MESSAGE.get(lang)

    def get_unsuccess_result_message(self, lang):
        return self.UNSUCCESS_RESULT_MESSAGE.get(lang)

    def get_zero_karma_members_message(self, lang, default_value):
        return f'{self.ZERO_KARMA_MEMBERS_MESSAGE.get(lang)}{default_value}'

    def get_karma_mode_update_message(self, lang, is_karma_mode):
        if is_karma_mode:
            mode = self.ON.get(lang)
        else:
            mode = self.OFF.get(lang)
        return f'{self.KARMA_MODE_UPDATE_MESSAGE.get(lang)}{mode}'

    def get_karma_positive_update_message(self, lang: str, user_name: str, karma_value: int):
        return f'@{user_name}, {self.KARMA_POSITIVE_UPDATE_MESSAGE.get(lang)}{karma_value}'

    def get_karma_state_message(self, lang, karma_value):
        return f'{self.KARMA_STATE_MESSAGE.get(lang)}{karma_value}'

    def get_stop_word_list_message(self, words):
        message = ''
        for i, word in enumerate(words):
            message += f'{i}: {word} '

    def get_supported_languages_message(self):
        message = ''
        for lang_code in SUPPORTED_LANGUAGES:
            message += f'{lang_code}: {SUPPORTED_LANGUAGES[lang_code]}\n'
        return message


BOT_CONFIG = BotConfig(SUPPORTED_LANGUAGES_CODES)
