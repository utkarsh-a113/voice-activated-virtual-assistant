import google.generativeai as genai
genai.configure(api_key="AIzaSyAsaT-9opk0hb995xSR3sTTMValSgLQXmA")

for m in genai.list_models():
    print(m.name)
