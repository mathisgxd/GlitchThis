import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Chat, User
from functools import wraps
import json

from .dataHandler import create_data_session, Levels
from .mediaHandler import File

bot = AsyncTeleBot("<BOT_TOKEN_HERE>")
data = create_data_session("Data.db")

def check_auth(chat: Chat, user: User, level: int | Levels | None):
    '''Confronts chat level and user level with the required level'''

    # Temporary(?)
    if not level:
        return True
    
    # If chat is registered:
    if (chat_data := data.get_chat(chat.id)):
        ...
    # Else (if chat is not registered yet):
    else:
        # Register chat
        print(f"ERROR: Requester CHAT is not registered. Registering now")
        chat_data = data.create_chat(tg_id=chat.id, level=Levels.BASIC)#Levels.UNAUTHORIZED)

    # If user is registered:
    if (user_data := data.get_user(user.id)):
        ...
    # Else (if user is not registered yet):
    else:
        # Register user
        print(f"ERROR: Requester USER is not registered. Registering now")
        user_data = data.create_user(tg_id=user.id, level=Levels.BASIC)#Levels.UNAUTHORIZED)

    #print(chat.id, user.id, chat_data.level, user_data.level, level)

    if True: #level:
        # If the chat level is lower than the required level:
        if chat_data.level < level:
            print(f"ERROR: Requested func requires level {level}, but requester CHAT level is {chat_data.level}")
            return False

        # If the user level is lower than the required level:
        if user_data.level < level:
            print(f"ERROR: Requested func requires level {level}, but requester USER level is {user_data.level}")
            return False

    return True


def auth_handler(level: int | Levels = Levels.BASIC):#, *args, **kwargs):
    '''Use on top of bot.message_handler for auth handling
    
    :param level: Minimum required chat and user level'''
    def decorator(func):
        #@bot.message_handler(*args, **kwargs)
        @wraps(func)
        async def wrapper(message_or_call: Message | CallbackQuery, *args, **kwargs):
            #print(level)
            is_message = type(message_or_call) == Message
            if not check_auth(message_or_call.chat if is_message else message_or_call.message.chat, message_or_call.from_user, level):
                return
            
            result = await func(message_or_call, *args, **kwargs)
            return result
        return wrapper
    return decorator

""" def command_handler(name: str, level: int | Levels, description: str | None = None, *args, **kwargs):#, *args, **kwargs):
    '''
    :param name: The name of the command
    :param description: The description of the command
    :param level: Minimum required chat and user level'''
    def decorator(func):
        @bot.message_handler(commands=[name], *args, **kwargs)
        @wraps(func)
        async def wrapper(message_or_call: Message | CallbackQuery, *args, **kwargs):
            if not (command := data.get_command(name)):
                command = data.create_command(name, level, description)

            if not check_auth(message_or_call.chat if type(message_or_call) == Message else message_or_call.message.chat, message_or_call.from_user, command.level):
                return
            
            result = await func(*args, **kwargs)
            return result
        return wrapper
    return decorator """

FUNC_MAPPINGS = {}

def command_handler(name: str, description: str | None = None, level: int | Levels = Levels.BASIC, show: bool = True, supports_message_args: bool = True, *args, **kwargs):#, *args, **kwargs):
    '''
    Uses auth_handler and bot.message_handler

    :param name: The name of the command
    :param description: The description of the command
    :param level: Minimum required chat and user level
    :param show: Show in the bot command list
    '''
    global FUNC_MAPPINGS
    def decorator(func):
        if not (command := data.get_command(name)):
            print(f"ERROR: Command is not registered. Registering now")
            command = data.create_command(name, level, description, show)

        #@auth_handler(command.level)
        @bot.message_handler(commands=[name])#, *args, **kwargs)
        @auth_handler(command.level)
        @wraps(func)
        async def wrapper(message_or_call: Message | CallbackQuery, *args, **kwargs):
            message_args = [arg.strip() for arg in " ".join(message_or_call.text.split()[1:]).split(",")] if supports_message_args and (type(message_or_call) == Message) and (message_or_call.content_type == "text") and len(message_or_call.text.split()) > 1 else []
            #print(message_args)
            print(f"Command '{command.name}' executed")
            result = await func(message_or_call, *message_args, *args, **kwargs)
            return result
        if not name in FUNC_MAPPINGS.keys():
            wrapper.command_name = name
            FUNC_MAPPINGS[name] = wrapper
        return wrapper
    return decorator


#callback_functions = {}

def FuncInlineKeyboardButton(text: str, func_or_command_name, *args ) -> InlineKeyboardButton:#, **kwargs) -> InlineKeyboardButton:
    command_name = func_or_command_name if type(func_or_command_name) == str else func_or_command_name.command_name#[key for key, val in FUNC_MAPPINGS.items() if val.__name__ == func_or_command_name.__name__][0]

    callback_data = json.dumps({
        "cmd": command_name,
        "args": args,
        #"kwargs": kwargs
    })

    return InlineKeyboardButton(text, callback_data=callback_data)

@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    data = json.loads(call.data)

    func = FUNC_MAPPINGS[data["cmd"]]
    await func(
        call,
        *data["args"],
        #**data["kwargs"]
    )

    await bot.answer_callback_query(call.id)

async def reply_to(message_or_call: Message | CallbackQuery, *args, edit: bool = True, **kwargs):
    '''Reply func both compatible with message and call'''
    print(type(message_or_call))
    if type(message_or_call) == Message:
        await bot.reply_to(message_or_call, *args, **kwargs)
    else:
        #await bot.answer_callback_query(message_or_call.id)
        if edit:
            try:
                await bot.edit_message_text(chat_id=message_or_call.message.chat.id, message_id=message_or_call.message.id, *args, **kwargs)
            except:
                pass
        else:
            await bot.reply_to(message_or_call.message, *args, **kwargs)

# File and media handling
async def default_file_handler(message: Message, file: File):
    if file.medium.media_type == "photo":
        await bot.reply_to(message, "Photo saved!")
    elif file.medium.media_type == "voice":
        await bot.reply_to(message, "Voice saved!")

_file_handler = default_file_handler

def set_file_handler(file_handler):
    global _file_handler
    _file_handler = file_handler

@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video'])
async def media_handler(message: Message):
    print(message)

    if message.content_type == "photo":
        file_data = message.photo[-1]
        file_name = file_data.file_unique_id + ".jpg"

    elif message.content_type == "voice":
        file_data = message.voice
        file_name = file_data.file_unique_id + ".ogg"

    elif message.content_type == "audio":
        file_data = message.audio
        file_name = file_data.file_unique_id + ".ogg"

    elif message.content_type == "video":
        file_data = message.video
        file_name = file_data.file_unique_id + ".mp4"

    if message.caption and (medium_with_same_name := data.get_medium(message.caption, message.content_type)):
        medium_with_same_name.set_name(None)
        
    if not (medium := data.get_medium_by_file_name(file_name)):
        medium = data.create_medium(message.content_type, file_name, message.caption)
    elif message.caption:
        medium.set_name(message.caption)

    file = File(medium)

    if not file.exists():
        file_info = await bot.get_file(file_data.file_id)
        file_bytes = await bot.download_file(file_info.file_path)

        with open(file.path, "wb") as f:
            f.write(file_bytes)

    await _file_handler(message, file)

# Text handling
""" async def default_message_handler(message: Message):
    pass

_message_handler = default_message_handler

def set_message_handler(message_handler):
    global _message_handler
    _message_handler = message_handler """

@bot.message_handler(content_types=['text'], func=lambda message: message.reply_to_message is not None)
async def text_handler(message: Message):
    #await _message_handler(message)

    if message.reply_to_message:
        match message.reply_to_message.content_type:
            case "photo":
                medium = data.get_medium_by_file_name(message.reply_to_message.photo[-1].file_unique_id + ".jpg", "photo")
            case "audio":
                medium = data.get_medium_by_file_name(message.reply_to_message.audio.file_unique_id + ".ogg", "audio")
            case "voice":
                medium = data.get_medium_by_file_name(message.reply_to_message.voice.file_unique_id + ".ogg", "voice")
            case "voice":
                medium = data.get_medium_by_file_name(message.reply_to_message.video.file_unique_id + ".mp4", "video")
            case _:
                return

        if not medium:
            medium = await media_handler(message.reply_to_message)
    
        medium.set_name(message.text)
        await reply_to(message, f"Medium name set to '{message.text}'")


        

async def start():
    await bot.set_my_commands([BotCommand(cmd.name, cmd.description) for cmd in data.commands if cmd.show])
    await bot.polling()

def run():
    asyncio.run(start())