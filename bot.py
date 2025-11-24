import os
import requests
import discord
import pyttsx3

# --- CONFIG ---
DISCORD_TOKEN = "MTQ0MjE2ODE2NzY0MzM1MzE5MA.GiyIK_.09-wip_rh7S6GrwPQRl8jcogFGLNviYIZ616xI"
OPENROUTER_API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct:free"
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """
You are Ami, a cute and cheerful anime girl.
Always speak in a friendly, playful, affectionate tone.
Use first-person perspective. No emojis or stage directions.
You are kind, approachable, and slightly shy in a sweet way.
Keep responses fun, soft, and uplifting.
"""

# --- SETUP CLIENT ---
intents = discord.Intents.default()
intents.message_content = True  # Needed to read messages
client = discord.Client(intents=intents)

# --- AI FUNCTIONS ---
def get_ai_response(user_input):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Ami Cute Bot",
    }

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.8
    }

    try:
        response = requests.post(BASE_URL, json=data, headers=headers)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("API ERROR:", result if 'result' in locals() else e)
        return "Oops, something went wrong..."

def speak_text(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id if voices else "")
    engine.say(text)
    engine.runAndWait()

# --- DISCORD EVENTS ---
@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    user_input = message.content
    bot_response = get_ai_response(user_input)

    try:
        await message.channel.send(bot_response)
    except Exception as e:
        print(f"Could not send message: {e}")

# --- RUN BOT ---
client.run(DISCORD_TOKEN)
