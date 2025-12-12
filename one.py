import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Adjusting for ambient noise... please wait")
    r.adjust_for_ambient_noise(source, duration=2)
    print("Say something!")
    audio = r.listen(source)
    print("Got it! Recognizing...")

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except Exception as e:
    print("Error:", e)
