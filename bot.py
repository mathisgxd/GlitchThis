from BotBase import *
import executer

# Windows commands
@command_handler("hide_windows", "Hide windows on the pc")
async def hide_windows(message_or_call):
    executer.hide_windows()

    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Show windows", show_windows)]])
    await reply_to(message_or_call, "Windows hidden", reply_markup=reply_markup)


@command_handler("show_windows", "Show windows on the pc")
async def show_windows(message_or_call):
    executer.show_windows()

    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Hide windows", hide_windows)]])
    await reply_to(message_or_call, "Windows shown", reply_markup=reply_markup)

@command_handler("close_window", "Close the top window on the pc")
async def close_window(message_or_call):
    executer.close_window()

    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Close another", close_window)]])
    await reply_to(message_or_call, "Window closed", reply_markup=reply_markup)

# Locker commands
@command_handler("lock_mouse", "Lock mouse cursor on the pc")
async def lock_mouse(message_or_call):
    res = executer.MouseLocker.lock()

    text = "Mouse locked" if res else "Mouse is already locked"
    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Unlock", unlock_mouse)]])

    await reply_to(message_or_call, text, reply_markup=reply_markup)


@command_handler("unlock_mouse", "Lock mouse cursor on the pc", show=False)
async def unlock_mouse(message_or_call):
    res = executer.MouseLocker.unlock()

    text = "Mouse unlocked" if res else "Mouse is not locked"
    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Lock", lock_mouse)]])

    await reply_to(message_or_call, text, reply_markup=reply_markup)

@command_handler("lock_keyboard", "Lock keyboard on the pc")
async def lock_keyboard(message_or_call):
    res = executer.KeyboardLocker.lock()

    text = "Keyboard locked" if res else "Keyboard is already locked"
    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Unlock", unlock_keyboard)]])

    await reply_to(message_or_call, text, reply_markup=reply_markup)


@command_handler("unlock_keyboard", "Lock keyboard on the pc", show=False)
async def unlock_keyboard(message_or_call):
    res = executer.KeyboardLocker.unlock()

    text = "Keyboard unlocked" if res else "Keyboard is not locked"
    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Lock", lock_keyboard)]])

    await reply_to(message_or_call, text, reply_markup=reply_markup)

# Shutdown commands
@command_handler("shutdown", "Shutdown the pc")
async def shutdown(message_or_call):
    await reply_to(message_or_call, "The pc is shutting down...")
    executer.shutdown()

@command_handler("reboot", "Reboot the pc")
async def restart(message_or_call):
    await reply_to(message_or_call, "The pc is rebooting...")
    executer.restart()

@command_handler("logoff", "Logoff the pc")
async def logoff(message_or_call):
    await reply_to(message_or_call, "The pc is loggong off...")
    executer.logoff()

@command_handler("hibernate", "Hibernate the pc")
async def hibernate(message_or_call):
    await reply_to(message_or_call, "The pc is hibernating...")
    executer.hibernate()

@command_handler("crash", "Crash the pc (BSOD)")
async def crash(message_or_call):
    await reply_to(message_or_call, "The pc is crashing...")
    executer.crash()


# Media
async def photo_handler(call, medium_id: int, cmd: str):
    medium = data.get_medium_by_id(medium_id)
    photo = executer.Photo(medium)

    match cmd:
        case "open":
            photo.open()
        case "close":
            photo.close()
        case "close_all":
            photo.close_all()
        case "wallpaper":
            photo.set_as_wallpaper()

async def audio_handler(call, medium_id: int, cmd: str):
    medium = data.get_medium_by_id(medium_id)
    audio = executer.Audio(medium)

    match cmd:
        case "play":
            audio.play()
        case "stop":
            audio.stop()

async def video_handler(call, medium_id: int, cmd: str):
    medium = data.get_medium_by_id(medium_id)
    video = executer.Video(medium)

    match cmd:
        case "open":
            video.open()
        case "close":
            video.close()

async def file_handler(message: Message, file: File):
    if file.medium.media_type == "photo":
        text = "Photo"
        reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Open", photo_handler, file.medium.id, "open")],
                                             [FuncInlineKeyboardButton("Close", photo_handler, file.medium.id, "close")],
                                             [FuncInlineKeyboardButton("Set as wallpaper", photo_handler, file.medium.id, "wallpaper")]])
    elif file.medium.media_type in ("voice", "audio"):
        text = "Voice" if file.medium.media_type == "voice" else "Audio"
        reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Play", audio_handler, file.medium.id, "play")],
                                             [FuncInlineKeyboardButton("Stop", audio_handler, file.medium.id, "stop")],])
    elif file.medium.media_type == "video":
        text = "Video"
        reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("Open", video_handler, file.medium.id, "open")],
                                             [FuncInlineKeyboardButton("Close", video_handler, file.medium.id, "close")],])

    await reply_to(message, text, reply_markup=reply_markup)

set_file_handler(file_handler)



run()


