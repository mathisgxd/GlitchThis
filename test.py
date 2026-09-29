from BotBase import *

#data.chats[0].set_level(Levels.OWNER)

# START
@command_handler("start_A", show=False, level=Levels.BASIC)
async def start_A(call):
    await reply_to(call, "A clicked!")

@command_handler("start_B", show=False, level=Levels.BASIC)
async def start_B(call):
    await reply_to(call, "B clicked!")

@command_handler("start_C", show=False, level=Levels.BASIC)
async def start_C(call):
    await reply_to(call, "C clicked!")

@command_handler("start", "Basic example", level=Levels.BASIC)
async def start(message_or_call):
    reply_markup = InlineKeyboardMarkup([[FuncInlineKeyboardButton("A", start_A)],
                                         [FuncInlineKeyboardButton("B", start_B)],
                                         [FuncInlineKeyboardButton("C", start_C)],
                                         [FuncInlineKeyboardButton("self", start)]])
    await reply_to(message_or_call, "Hello!", reply_markup=reply_markup)

run()