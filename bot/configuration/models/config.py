from googletrans import Translator
import os
import json


translator = Translator()


class Message():

    def __init__(self, message: str, default_lang: str):
        self.data = {}
        self.set(message, default_lang)
        self.default_lang = default_lang

    def get(self, lang: str = None, auto_translate: bool = False):
        if lang is None:
            lang = self.default_lang
        # if hasattr(self, lang):
        #    return getattr(self, lang)
        if lang in self.data:
            return self.data[lang]
        else:
            print('перевод сообщения')
            return translator.translate(
                text=self.get(),
                src=self.default_lang,
                dest=lang).text

    def set(self, message: str, lang: str):
        # setattr(self, lang, message)
        self.data[lang] = message

    def get_all(self):
        # dict = {}
        # keys = dir(self)
        # for key in keys:
        #   dict[key] = getattr(self, key)
        return self.data


class Command():

    def __init__(self,
                 command: list[str],
                 description: str,
                 default_lang: str):
        self.command = command
        self.description = Message(description, default_lang)


class Config():
    locales_dir = 'locales/'
    messages_key = 'messages'
    commands_key = 'commands'

    def __init__(self, language_codes: list[str]):
        self.get_locales_from_file(language_codes)
        self.gen_locale(language_codes)
        self.set_locales_to_file(language_codes)

    def gen_locale(self, language_codes: list[str]):

        attr_names = dir(self)
        for attr_name in attr_names:
            attr = getattr(self, attr_name)
            if isinstance(attr, Message):

                print(attr_name)
                print(attr.data)
                self.translate_message(message=attr,
                                       language_codes=language_codes)
            elif isinstance(attr, Command):
                print(attr.description.get())
                self.translate_message(message=attr.description,
                                       language_codes=language_codes)

    def set_locales_to_file(self, language_codes: list[str]):
        attr_names = dir(self)
        new_locales = {self.commands_key: {},
                       self.messages_key: {}}
        for attr_name in attr_names:
            attr = getattr(self, attr_name)
            if isinstance(attr, Message):
                new_locales[self.messages_key][attr_name] = attr.get_all()
            elif isinstance(attr, Command):
                new_locales[self.commands_key][attr_name] = attr.description.get_all()
        print(new_locales)
        if not os.path.exists(self.locales_dir):
            os.makedirs(self.locales_dir)
        with open(f'{self.locales_dir}locales.json', 'w') as outfile:
            json.dump(new_locales, outfile, indent=4,
                      sort_keys=True, ensure_ascii=False)

    def get_locales_from_file(self, language_codes: list[str]):
        try:
            file = open(f'{self.locales_dir}locales.json')
            data = json.load(file)
            for attr_name in data[self.messages_key]:
                self.messages = data[self.messages_key][attr_name]
                for lang in self.messages:
                    getattr(self, attr_name).set(
                        self.messages[lang], lang)
            for attr_name in data[self.commands_key]:
                command = data[self.commands_key][attr_name]
                for lang in command:
                    getattr(self, attr_name).description.set(
                        command[lang], lang)
            file.close()
        except FileNotFoundError:
            pass

    def translate_message(self,
                          message: Message,
                          language_codes: list[str]):
        for lang in language_codes:
            # if not hasattr(message, lang):
            if lang not in message.data:

                translated_message = translator.translate(
                    text=message.get(),
                    src=message.default_lang,
                    dest=lang).text
                print(
                    f'translate {message.get()} to {translated_message}')
                message.set(translated_message, lang)
