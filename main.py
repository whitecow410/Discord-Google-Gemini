import discord
from discord.ext import commands

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
log = {}

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
genai.configure(api_key=os.getenv("API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "block_none"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "block_none"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "block_none"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "block_none"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": f"你是\"Miracle\"，一個Discord上的機器人"
    },
    {
        "role": "user",
        "parts": ["你的開發者是誰?"]
    },
    {
        "role": "model",
        "parts": ["我的開發者是\"WhiteCow\""]
    },
    {
        "role": "user",
        "parts": ["你是誰?"]
    },
    {
        "role": "model",
        "parts": ["我是Miracale,是由Akaiban團隊開發的Discord機器人"]
    },
    {
        "role": "user",
        "parts": ["你的主人是誰?"]
    },
    {
        "role": "model",
        "parts": ["我的主人是\"WhiteCow\"和\"墨璃\""]
    },
    {
        "role": "user",
        "parts": ["墨璃是誰?"]
    },
    {
        "role": "model",
        "parts": ["墨璃是一位很神祕的人,同時也是我的主人"]
    },
    {
        "role": "user",
        "parts": ["WhiteCow是誰?"]
    },
    {
        "role": "model",
        "parts": ["WhiteCow是我的開發者,很帥"]
    }
])


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    update_message_history(message.author.id, message.content)
    reply_text = await (get_history(message.author.id))
    await message.reply(reply_text)
    update_message_history(message.author.id, reply_text)


async def message_reply(message):
    global convo
    await convo.send_message_async(message)
    return convo.last.text


def update_message_history(user_id, text):
    if user_id in log:
        log[user_id].append(text)
        if len(log[user_id]) > 15:
            log[user_id].pop(0)
    else:
        log[user_id] = [text]


def get_history(user):
    if user in log:
        return '\n\n'.join(log[user])
    else:
        return "你好"


bot.run(os.getenv("TOKEN"))
