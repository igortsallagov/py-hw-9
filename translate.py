import requests
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
source_files_dict = dict()


def files_list(source_name):
    source_dir = os.path.join(current_dir, source_name)
    all_files_list = os.listdir(path=source_dir)
    print("Доступны следующие файлы для перевода: ")
    for source_file in all_files_list:
        source_files_dict[source_file] = source_file.rstrip(".txt").lower()
        print(source_file)


def translate_it(source_name, file_name, translated_name, to_lang):
    """
    YANDEX translation plugin
    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20180924T152332Z.4f8a66a938f672a4.e08b5f3facc34bd1bd442cade4e04276ff2d8fcf'

    from_lang = source_files_dict[file_name]
    params = {
        'key': key,
        'lang': "{}-{}".format(from_lang, to_lang),
        'text': ' ',
    }

    source_file = os.path.join(current_dir, source_name, file_name)

    with open(source_file, 'r', encoding='UTF-8') as f:
        file_data = f.read()

    params['text'] = file_data

    response = requests.get(url, params=params).json()
    translation = ' '.join(response.get('text', []))

    translated_path = os.path.join(current_dir, translated_name)
    if not os.path.exists(translated_path):
        os.mkdir(translated_path)

    new_file_name = to_lang.upper() + '.txt'
    translated_file = os.path.join(current_dir, translated_name, new_file_name)

    with open(translated_file, 'w', encoding='UTF-8') as f:
        f.write(translation)


def core():
    source_name = input("Введите имя папки с исходными файлами: ")
    files_list(source_name)
    file_name = input("Введите имя файла из списка: ")
    translated_name = str(input("Введите имя папки для переведенных файлов (по умолчанию - Translations): "))
    if len(translated_name) == 0:
        translated_name = "Translations"
    input_4 = str(input("Введите язык, на который перевести в формате ru, en, es, fr и т.д. (по умолчанию - ru): "))
    if len(input_4) < 2:
        to_lang = 'ru'
    else:
        to_lang = input_4
    translate_it(source_name, file_name, translated_name, to_lang)


if __name__ == '__main__':
    core()