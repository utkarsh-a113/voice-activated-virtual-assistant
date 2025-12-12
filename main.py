import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLib
import requests
import subprocess
import os
from datetime import datetime
import pyautogui
import google.generativeai as genai  # Gemini import

# -------------------- CONFIG --------------------
newsapi = "7a7970bc3fc44fa2a6cac20e54d7d0ae"
weather_api = "70d3370892237394d2833115bdba99ba"
gemini_api = "AIzaSyAsaT-9opk0hb995xSR3sTTMValSgLQXmA"  # Replace with your key

genai.configure(api_key=gemini_api)

# -------------------- TTS SETUP --------------------
engine = pyttsx3.init(driverName='sapi5')  # Windows
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Choose first available voice
engine.setProperty('rate', 170)            # Speech speed

def speak(text):
    print("Ultron (speaking):", text)
    engine.say(text)
    engine.runAndWait()

# -------------------- GEMINI RESPONSE --------------------
def gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return str(response.text)
        elif hasattr(response, "output_text") and response.output_text:
            return str(response.output_text)
        elif hasattr(response, "content") and response.content:
            return str(response.content[0].text)
        else:
            return str(response)
    except Exception as e:
        print("Gemini error:", e)
        return "Sorry, I cannot answer that right now."

# -------------------- NEWS --------------------
def fetch_news():
    try:
        speak("Fetching the latest headlines. Please wait...")
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or data.get("status") != "ok":
            speak("Sorry, I couldn't fetch the news.")
            return

        articles = data.get("articles", [])
        if not articles:
            speak("No news articles found.")
            return

        speak("Here are the top five headlines.")
        for i, article in enumerate(articles[:5], start=1):
            print(f"{i}. {article['title']}")
            speak(article["title"])
    except Exception as e:
        print(f"News fetch error: {e}")
        speak("Something went wrong while fetching the news.")

# -------------------- WEATHER --------------------
def fetch_weather(city="Durgapur"):
    try:
        if not city.strip():
            city = "Durgapur"
        city = city.replace(" ", "%20")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or data.get("cod") != 200:
            speak(f"Sorry, I couldn't find weather info for {city}.")
            return

        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")
    except Exception as e:
        print(f"Weather fetch error: {e}")
        speak("Something went wrong while fetching the weather.")

# -------------------- PROCESS COMMAND --------------------
def processCommand(c):
    c = c.lower()
    print("Command:", c)

    # Web/App shortcuts
    if "youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "google" in c:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "stack overflow" in c:
        speak("Opening Stack Overflow")
        webbrowser.open("https://stackoverflow.com")
    elif "instagram" in c:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    # Music
    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        link = musicLib.music.get(song)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")

    # News
    elif "news" in c:
        fetch_news()

    # Weather
    elif "weather" in c:
        city = c.split("in")[-1].strip() if "in" in c else "Delhi"
        fetch_weather(city)

    # System control
    elif "open" in c or "launch" in c:
        if "notepad" in c:
            subprocess.Popen("notepad.exe")
            speak("Opening Notepad")
        elif "calculator" in c:
            subprocess.Popen("calc.exe")
            speak("Opening Calculator")
        elif "cmd" in c or "command prompt" in c:
            subprocess.Popen("cmd.exe")
            speak("Opening Command Prompt")
        else:
            speak("I cannot open that application.")
    elif "screenshot" in c or "capture screen" in c:
        filename = f"screenshot_{datetime.now().strftime('%H%M%S')}.png"
        pyautogui.screenshot().save(filename)
        speak(f"Screenshot taken and saved as {filename}")

    # Exit
    elif "stop" in c or "exit" in c or "quit" in c:
        speak("Goodbye!")
        exit()

    # Gemini fallback
    else:
        response = gemini_response(c)
        speak(response)

# -------------------- MAIN LOOP --------------------
if __name__ == "__main__":
    speak("Initializing Ultron version 2.1 with Gemini AI...")
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("\nListening for wake word ('Ultron')...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if "ultron" in word.lower():
                speak("Yeah?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                command = recognizer.recognize_google(audio)
                processCommand(command)

        except sr.WaitTimeoutError:
            print("No speech detected, waiting...")
            continue
        except sr.UnknownValueError:
            print("Didn't get that, waiting again...")
            continue
        except sr.RequestError:
            print("Network issue, please check your internet connection.")
        except Exception as e:
            print(f"Ultron error: {e}")
