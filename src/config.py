#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, json

PLATFORM = "LINUX"

if os.name == "nt":
    PLATFORM = "WINDOWS"

KEY1 = "Key1"
KEY2 = "Key2"
KEY3 = "Key3"

# Basic template of configuration
DEFAULT_CONF = {'settings': {''}
                }

conf = {}  # configurations
dirs = {}  # important directories of project


class Dirs:
    def __init__(self):
        self.console = os.getcwd()
        self.src = os.path.dirname(__file__)
        self.data = os.path.join(self.src, "data")
        self.appicon = os.path.join(self.data, "appicon.png")
        self.app = os.path.join(self.src, "freg.py")
        self.home = os.path.expanduser("~")


def init():
    '''# Initialize conf
    if os.path.isfile(dirs["config"]):
        try:
            conf = json.load(open('config.json'))
        except:
            print("[!] Config file is not valid. Loading default configurations.")
            set_default_conf()
    else:
        print("[!] There is no config file. I am creating one for you :)")
        set_default_conf()
    '''
    pass


def set_default_conf():
    global conf
    conf = DEFAULT_CONF.copy()
    save_conf()


def save_conf():
    json.dump(conf, open(dirs["config"], 'w'))


def encrypt(value, k=KEY1):
    if value == "":
        return ""
    return xor(value, k)


def decrypt(value, k=KEY1):
    if value == "":
        return ""
    value = "".join(map(chr, value))
    value = xor(value, k)
    value = "".join(map(chr, value))
    return value


def xor(s, k=KEY1):
    k = k * (int(len(s) / len(k)) + 1)
    return [ord(s[i]) ^ ord(k[i]) for i in range(len(s))]


init()
