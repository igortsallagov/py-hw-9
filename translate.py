import requests
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = 'Originals'
translated_dir = 'Translations'

source_files_dict = {
    'DE.txt': 'de',
    'ES.txt': 'es',
    'FR.txt': 'fr'
}

def translate_it(file_name):
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
        'lang': "{}-ru".format(from_lang),
        'text': ' ',
    }

    source_file = os.path.join(current_dir, source_dir, file_name)
    translated_file = os.path.join(current_dir, translated_dir, file_name)

    with open(source_file, 'r', encoding='UTF-8') as file:
        file_data = file.read()

    params['text'] = file_data

    response = requests.get(url, params=params).json()
    translation = ' '.join(response.get('text', []))

    with open(translated_file, 'w', encoding='UTF-8') as f:
        f.write(translation)

def core():
    input_1 = input("Введите имя файла для перевода: ")
    input_2 = input("Введите имя папки для переведенных файлов: ")
    input_3 = input("Введите язык, на который перевести (в формате ru, en, es, fr и т.д.): ")
    file_name = input_1
    to_lang = input_3
    translate_it(file_name)

if __name__ == '__main__':
    core()