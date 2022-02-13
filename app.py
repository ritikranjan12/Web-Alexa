import pyjokes
import wikipedia
from flask import Flask,render_template,redirect,request

import warnings
warnings.filterwarnings('ignore')


import speech_recognition as sr
import webbrowser
import datetime
import requests,json
import wolframalpha
import pyttsx3



listener = sr.Recognizer()


app = Flask("__name__")

def talk(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def audio():
        r = sr.Recognizer ()
        with sr.Microphone () as source:
            audio = r.listen (source)

            try:
                statement = r.recognize_google (audio, language='en-in')  # en at hi for english

            except Exception as e:
                return "None"
            return statement



def main():
    command = audio()
    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current Time is' + time)
    elif 'joke' in command:
        get_j = pyjokes.get_joke()
        talk(get_j)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        talk(info)
    elif 'weather' in command:
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        talk("where are you sir?...")
        city = audio ()
        api_key = "92bad23e10f926d81bd613de3a2c03b9"
        URL = BASE_URL + "q=" + city + "&appid=" + api_key
        response = requests.get (URL)
        if response.status_code == 200:
            data = response.json ()
            main = data ['main']
            temperature = main ['temp'] - 273.15
            t = round (temperature, 2)
            talk(f"The temperature of {city} is {t} degree celcius")
        else:
            talk("can't find the city sir")
    elif 'open facebook' in command:
        webbrowser.get().open("https://www.facebook.com")
        talk("facebook is open now")


    elif "open instagram" in command:
        webbrowser.get().open("https://www.instagram.com")
        talk("Instagram is open now")
    elif 'open stack overflow' in command:
       webbrowser.get().open("https://www.stackoverflow.com")
       talk("stackoverflow is open now")

    elif 'open gmail' in command:
        webbrowser.get().open("gmail.com")
        talk("Google Mail open now")

    elif 'who are you' in command or 'what can you do' in command:
        talk('I am chatBot. version 10.0. An Advanced personal assistant. I am programmed to do minor tasks, check wheather  and answer any computational or geographical questions !,built by Ritik Ranjan')
    elif 'stop' in command:
        talk("Good bye")
    elif 'wikipedia' in command:
        talk('Searching Wikipedia...')
        query = command.replace("wikipedia", "")
        results = wikipedia.summary(query)
        talk("According to Wikipedia")
        print(results)
        talk(results)

    elif "result" in command:
        talk("What do you want to know sir?")
        question = audio()
        app_id = "X4L38Q-RKHH3972QG"
        client = wolframalpha.Client('X4L38Q-RKHH3972QG')
        res = client.query(question)
        answer = next(res.results).text
        talk(answer)

@app.route('/')
def hello():
    return render_template("ritik.html")

@app.route("/home")
def home():
    return redirect('/')

@app.route('/',methods=['POST', 'GET'])
def submit():
    while True:
        main()
    return render_template("ritik.html")

if __name__ == "__main__":
    app.run()

