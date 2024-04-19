import pyttsx3
import datetime
import speech_recognition as sr
import smtplib
from secrets_1 import senderEmail, emailPassword, emailTo
from email.message import EmailMessage
import pyautogui
import webbrowser as web
from time import sleep
import wikipedia
import pywhatkit
import requests
from newsapi import NewsApiClient
import clipboard
import os
import pyjokes
import time as tt
from nltk.tokenize import word_tokenize
from voices import speak
from openai import OpenAI
import gradio as gr
import sounddevice as sd
from scipy.io.wavfile import write
from transformers import GPT2LMHeadModel, GPT2Tokenizer


client = OpenAI(api_key = "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")


# engine = pyttsx3.init()

# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()

def summarize_text_gpt2(input_text, max_length=50):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    summary_ids = model.generate(input_ids, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2)
    gpt_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return gpt_summary

def record_meeting(duration=10, fs=44100, filename='meeting_recording.wav'):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write(filename, fs, recording)

def speech_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text

def meeting_summarization():
    record_meeting()  # You can specify the duration
    meeting_text = speech_to_text('meeting_recording.mp3')
    summary = summarize_text_gpt2(meeting_text)
    print(summary)
    speak(summary)



def gpt(prompt):
    chat_completion = client.chat.completions.create(

        messages=[
            {"role":"user", "content": prompt},
            {"role": "system","content":"act like a voice assistant like siri and google voice assistant. Make the answers short and precise"}
        ],
        model = "gpt-3.5-turbo",
        temperature=1,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    data = chat_completion.choices[0].message.content
    print(data)
    speak(data)

def time():
    Time = datetime.datetime.now().strftime("%I:%M")# hour = I, minutes = M, seconds = S.
    speak("The time is")
    speak(Time)

def date():
    date = int(datetime.datetime.now().day)
    month = datetime.datetime.now().month
    year = int(datetime.datetime.now().year)
    speak(date)
    speak(month)
    speak(year)

def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour <12:
        speak("good morning")
    elif hour >= 12 and hour <18:
        speak("good afternoon")
    elif hour >=18 and hour <24:
        speak("good evening")
    else:
        speak("good night")

def wishme():
    greeting()
    speak("How can i help you ?")

def takeCommandCMD():
    query = input("How can i help you ?")
    return query

def sendEmail(reciever, subject, content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(senderEmail, emailPassword)
    #server.sendmail(senderEmail, emailTo,content)
    email = EmailMessage()
    email['From'] = senderEmail
    email['To'] = reciever
    email['subject'] = subject
    email.set_content(content)
    server.send_message(email)
    server.close()

def sendWhasappmsg(phone_no, message):
    Message = message
    web.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+Message)
    sleep(10)
    pyautogui.press('enter')

def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..")

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

def standbymode():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say Nora to activate")

        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(query)
    except Exception as e:
        print(e)
        return "None"
    return query


def googlesearch():
    speak('what should i search for ?')
    search = takeCommandMic()
    web.open('https://www.google.com/search?q='+search)

def news():
    newsapi = NewsApiClient(api_key='490d4d6adcb44beebd8884a535f1ef97')
    speak('what topic do you want ?')
    topic = takeCommandMic()
    data = newsapi.get_top_headlines(q=topic, language='en', page_size=5)

    newsdata = data['articles']
    for x,y in enumerate(newsdata):
        print((f'{x}{y["description"]}'))
        speak((f'{x}{y["description"]}'))

    speak("thats it for now")

def text2speech():
    text = clipboard.paste()
    print(text)
    speak(text)

def screenshot():
    name_img = tt.time()
    name_img = f'C:\\Users\\kedir\\Pictures\\Screenshots\\{name_img}.png'
    img = pyautogui.screenshot(name_img)
    img.show()

if __name__ =="__main__":
    print("voice ai is active")
    wakeword = "nora"
    while True:
        query = standbymode().lower()

        if wakeword in query:
            wishme()
             
            while True:
                try:
                    query = takeCommandMic().lower()
                    query1 = query
                    print(query)
                    

                    if 'time' in query:
                        time()
                        break 
                    elif 'date' in query:
                        date()
                        break
                    elif 'email' in query:
                        email_list = {
                            'to my friend':'kedirdin-98@hotmail.com'
                        }
                        try:
                            speak("Who should i send a email to ?")
                            name = takeCommandMic()
                            reciever = email_list[name]

                            speak("what is the subject ?")
                            subject = takeCommandMic()

                            speak("What should i write ?")
                            content = takeCommandMic()

                            sendEmail(reciever, subject, content)
                            speak("Email has been sent")
                            
                        except Exception as e:
                            print(e)
                            speak("The email could not be sent")
                    elif 'message' in query:
                        user_name = {
                            'to my friend':'91147808'
                        }
                        try:
                            speak("Who should i send a message to ?")
                            name = takeCommandMic()
                            phone_no = user_name[name]

                            speak("What should i write ?")
                            message = takeCommandMic()

                            sendWhasappmsg(phone_no,message)
                            speak("message has been sent")
                            break
                        except Exception as e:
                            print(e)
                            speak("The message could not be sent")
                    elif 'wikipedia search' in query:
                        speak('searching on wikipedia...')
                        query = query.replace("wikipedia", "")
                        result = wikipedia.summary(query, sentences = 2)
                        print(result)
                        speak(result)
                        break
                    elif 'google search' in query:
                        googlesearch()
                        break
                    
                    elif 'search on youtube' in query:
                        speak("searching on youtube ?")
                        query = query.replace("youtube", "")
                        pywhatkit.playonyt(query)
                        break
                    
                    elif 'weather' in query:
                        
                        url = 'https://api.openweathermap.org/data/2.5/weather?q=oslo&units=imperial&appid=4f668cb5c06c87529e4b50578d950fc1'

                        res = requests.get(url)
                        data = res.json()
                        weather = data['weather'] [0] ['main']
                        temp = data['main']['temp']
                        description = data['weather'] [0] ['description']
                        temp = round((temp - 32) * 5/9)
                        print(weather)
                        print(temp)
                        print(description)
                        speak('Temperature : {} degree'.format(temp))
                        speak('weather is {}'.format(description))
                        break

                    elif 'news' in query:
                        news()
                        break

                    elif 'read' in query:
                        text2speech()
                        break

                    elif 'open discord' in query:
                        codepath = '"C:\\Users\\kedir\\Desktop\\Discord.lnk"'
                        os.startfile(codepath)
                        break

                    elif 'open file explorer' in query:
                        os.system('explorer C://{}'.format(query.replace('open','')))
                        break

                    elif 'joke' in query:
                        speak(pyjokes.get_joke())
                        break

                    elif 'screenshot' in query:
                        screenshot()
                        break

                    elif 'remember something' in query:
                        speak("what should i remember ?")
                        data = takeCommandMic()
                        speak("i will remember that"+data)
                        remember = open('data.txt','w')
                        remember.write(data)
                        remember.close()
                        break

                    elif 'do you remember' in query:
                        remember = open('data.txt', 'r')
                        speak("you told me to remember that"+remember.read())
                        break


                    elif 'sleep' in query:
                        speak("okay sir")
                        quit()
                    

                    elif 'record' in query:
                        speak("starting recording")
                        meeting_summarization()
                        break
                        

                    else:
                        gpt(query1)
                        break
                
                

                except Exception as e:
                    print(f"Error: {e}")
                    break
                    
        if 'terminate' in query:
            speak("terminating")
            quit()
  