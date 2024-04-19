import pyttsx3
from openai import OpenAI
import speech_recognition as sr

from voices import speak



client = OpenAI(api_key = "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")

start_sequence = "\nAI: "
restart_sequence ="\nHuman: "

prompt = "This is an Ai speaking"

engine = pyttsx3.init()

def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listning..")

        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(query)
    except Exception as e:
        print(e)
        speak("Can you repeat please...")
        return "None"
    return query


speak("Hello")

def gpt(prompt):
    chat_completion = client.chat.completions.create(

        messages=[
            {
                "role":"user",
                "content": prompt
            }
        ],
        model = "gpt-3.5-turbo",
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    data = chat_completion.choices[0].message.content
    print(data)
    speak(data)

while True:
     query = takeCommandMic()
     gpt(query)