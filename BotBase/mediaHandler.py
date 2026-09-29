import os
from .dataHandler import Medium, DataSession
import pygetwindow as gw
import shutil

MEDIA_PATH = "media"

type_path = lambda t: os.path.join(MEDIA_PATH, t)
 
class File:
    def __init__(self, medium: Medium):
        self.medium = medium
        self.path = os.path.join(type_path(self.medium.media_type), self.medium.file_name)

    def delete(self):
        try:
            self.close_all()
        except:
            pass

        try:
            self.medium.delete_from_session(self.medium)
        except:
            pass

        try:
            os.remove(self.path)
        except:
            pass

    def open(self):
        os.startfile(self.path)

    def close(self):
        windows = gw.getWindowsWithTitle(self.medium.file_name)

        if windows:
            windows [0].close()

    def close_all(self):
        for window in gw.getWindowsWithTitle(self.medium.file_name):
            window.close()

    def exists(self):
        return os.path.exists(self.path)

def delete_files(data_session: DataSession, types: Medium.Types | tuple[Medium.Types] | None = None):
    try:
        data_session.delete_media(types)
    except:
        pass

    types = ([types] if type(types) == Medium.Types else types) if types else tuple(t.value for t in Medium.Types)
    for t in types:
        path = type_path(t)
        print(path)
        if os.path.exists(path):
            shutil.rmtree(path)
        
        os.makedirs(path, exist_ok=True)