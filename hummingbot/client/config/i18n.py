import gettext as _gettext
from pathlib import Path
from urllib.parse import quote

import requests

_DOMAIN = 'hummingbot'
_proxied_gettext = _gettext.gettext


def gettext(message):
    """
    Translate the given message.
    A proxy for gettext. This machanism is used to prevent early import.
    """
    lang = "zh-CN"
    if lang == "en":
        return message
    else:
        return translate_cache(message)

# def init_locale():
#     """Initialize the locale translation."""
#     # from . import config
#     locale_dir = Path(__file__).resolve().parent.parent.parent.parent / 'locale'
#     # language = config.get('language')
#     # 读取系统环境变量中的语言设置
#     import os
#     language = os.getenv('LANG')
#     if language is not None:
#         language = language.split('.')[0].split('_')[0]
#     else:
#         language = "zh_CN"
#
#     if language is not None:
#         translation = _gettext.translation(_DOMAIN, locale_dir, [language], fallback=True)
#         global _proxied_gettext
#         _proxied_gettext = translation.gettext
#     else:
#         # Use default translation, and load locale from env
#         _gettext.bindtextdomain(_DOMAIN, locale_dir)
#         _gettext.textdomain(_DOMAIN)


def translate_i18n(text, to_lang='zh-CN'):
    """
    使用AI翻译接口翻译文本
    :param text:  要翻译的文本
    :param to_lang:  目标语言
    :return:  翻译后的文本
    """
    url = 'https://apps.aiexh.com/translate'
    payload = {
        # text url encode
        "text": quote(text),
        "to": to_lang
    }
    response = requests.post(url, json=payload)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析返回的JSON数据
        data = response.json()
        if data.get('code') == 0:
            print('翻译英文成功:', data.get('data'))
            return data.get('data')
        else:
            print('翻译失败，错误信息：', data.get('msg'))
    else:
        print('请求失败，状态码：', response.status_code)


def translate_cache(key, to_lang='zh-CN'):
    """
    翻译并缓存
    :param key:  要翻译的文本
    :param to_lang:  目标语言
    :return:  翻译后的文本
    """
    md5_key = str_md5(f"{key}") + "_zh_CN"
    cache_file = Path(__file__).resolve().parent.parent.parent.parent / 'cache' / f"{md5_key}.txt"
    if cache_file.exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        result = translate_i18n(key, to_lang)
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(result)
        return result


def str_md5(text):
    import hashlib
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()
