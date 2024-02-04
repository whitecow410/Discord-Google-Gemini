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

convo = model.start_chat(
    history=[
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
            "parts": ["我是Miracale,是由 Akaiban(AwkwardTeam) 團隊開發的Discord機器人"]
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
    ]
)


async def message_reply(message):
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


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.guild.id not in [1130450248888762478, 1203724433034977280]:
        return

    if message.content.lower() == '.reset':
        if message.author.id in log:
            del log[message.author.id]
            return
    elif message.content.lower() == '.info':
        embed = discord.Embed(
            description="機器人由 Akaiban (AwkwardTeam) 製作，本機器人目前處于__私人開發測試階段__，如發現資訊錯誤敬請原諒\n## 開發資訊\n- 開發者: <@726709068835717140> <@753592248670748712>\n## 注意事項\n- 本機器人目前處於測試階段，如發生任何情況本團隊不會為此承擔責任\n- 基於開發階段請勿提供錯誤資訊，否則有可能會被列入測試黑名單",
            color=discord.Color.random()
        )
        embed.set_author(
            name=f"Miracle (AI Chat Beta Version)",
            url="https://discord.com/api/oauth2/authorize?client_id=826244062612553780&permissions=8&scope=bot%20applications.commands",
            icon_url=bot.user.display_avatar,
        )
        embed.set_footer(text=f"Powered by Google-Gemini")
        embed.set_thumbnail(url=bot.get_emoji(1195797791612600370).url)
        await message.channel.send(embed=embed)
        return

    update_message_history(message.author.id, message.content)
    reply_text = await message_reply(get_history(message.author.id))
    await message.reply(reply_text)
    update_message_history(message.author.id, reply_text)

bot.run(os.getenv("TOKEN"))
