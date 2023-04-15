import openai
import telebot
import time
import speech_recognition as sr
import io
from pydub import AudioSegment
from gtts import gTTS

openai.api_key = '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'
messages = [
    {"role": "system", "content": "You are a kind helpful assistant."},
]

TOKEN = '6177524583:AAGL89Gh-7aiKHaqkXfu-FccWYSuVWbNdEo'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Create a recognizer object
r = sr.Recognizer()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    javob = "Hello I am virtual asistent!"
    javob += "\n How Can I help you?"
    bot.reply_to(message, javob)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    javob ='''-I am  AI language model, I don't have a physical self or a personal 
life like humans do. However, I possess the ability to comprehend and process natural 
language and generate responses that aim to help and assist users in various tasks
and inquiries. I was designed to utilize sophisticated algorithms and machine  learning 
techniques to provide high-quality responses that simulate human-like interactions. 
So, you can think of me as a virtual assistant or a digital aide that is always here to 
assist you with anything you need.'''
    bot.reply_to(message, javob)

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Convert the downloaded file to a compatible format using Pydub
    audio_bytes = io.BytesIO(downloaded_file)
    audio = AudioSegment.from_file(audio_bytes, format='ogg')
    audio.export('voice_message.wav', format='wav')

    # Use SpeechRecognition to transcribe the audio
    with sr.AudioFile('voice_message.wav') as source:
      audio = r.record(source)
      text = r.recognize_google(audio, language='en-US')

    # Pass the transcribed text to your chatbot
    messages.append(
        {"role": "user", "content": text},
    )
    bot.send_chat_action(message.chat.id, 'typing')
    chat = openai.ChatCompletion.create(
        model="text-davinci-002", messages=messages
    )
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    javob = chat.choices[0].text
    messages.append({"role": "assistant", "content": javob})

    speech = gTTS(text=javob, lang='en', slow=False)
    speech.save("voice_message.mp3")

    # Send the voice message to the user
    with open("voice_message.mp3", "rb") as file:
        bot.send_voice(message.chat.id, file)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    text = message.text
    if message:
        messages.append(
            {"role": "user", "content": text},
        )
        bot.send_chat_action(message.chat.id, 'typing')
        chat = openai
