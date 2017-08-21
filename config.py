# encoding=utf-8
import os

VERSION = '0.1'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
WORD_DIR = os.path.join(BASE_DIR, 'vocab_db')  # 存储练习的信息
VOICE_DIR = os.path.join(BASE_DIR, 'voice_cache')  # 缓存本地 voice 文件
VOICE_URL = 'http://dict.youdao.com/dictvoice?type=2&audio={word}'  # youdao 的发音 api type=1英音 2美音


def prepare():
    """

    :return:
    """
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
    if not os.path.exists(WORD_DIR):
        os.mkdir(WORD_DIR)
    if not os.path.exists(VOICE_DIR):
        os.mkdir(VOICE_DIR)
