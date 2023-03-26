import os
import playsound
import speech_recognition as sr
import time
from gtts import gTTS
import openai
import random


# Text - to - speech: Khai báo hàm chuyển đổi văn bản thành giọng nói
def speak(text):
    print("GPT: {}".format(text))
    tts = gTTS(text=text, lang='vi', slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", True)
    os.remove("sound.mp3")


# Speech - to - text: Khai báo hàm chuyển đổi giọng nói thành văn bản
def get_text():
    print("GPT: Đang nghe...")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print("Tôi: ", end='')
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text.lower()
        except:
            #print("Đang nghe...")
            return 0
        
       
# Khai báo hàm đợi câu hỏi của GPT
def get_again():
    for i in range(5):
        text = get_text()
        if text:
            return text.lower()
        elif i < 4:
            #speak("Máy không nghe rõ. Bạn nói lại được không!")
            time.sleep(0)
    time.sleep(0)
    speak(" Tạm biệt")
    return 0


        
# ChatGPT 
def chat_gpt():
    speak("xin chào, Tôi là chatgpt. bạn cần gì?")
    question = get_again()
    while True:
        try:
            openai.api_key = "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"
            model_engine = "text-davinci-003"
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=question,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            contents = completions.choices[0].text
            speak("Câu trả lời là: " + contents)
            time.sleep(1)
        except:
            time.sleep(2) 
        speak(random.choice([
                            "Bạn còn cần gì nữa không","Bạn cần gì nữa", "Bạn muốn biết thêm không",
                            "Tôi đã xong, bạn muốn biết gì thêm", "Xin đặt thêm câu hỏi",
                            "Bạn muốn biết thêm gì nữa", "Đó là những gì tôi biết",
                            "Hy vọng bạn hài lòng với câu trả lời","Tôi đang đợi thêm câu hỏi",
                            "Tôi đang chờ bạn hỏi thêm"
                        ]))       
        question = get_again()            
        if "tạm biệt" in question or "không cần" in question:
            speak("Hẹn gặp lại bạn. Tạm biệt!")
            time.sleep(1)
            break

# Gọi lệnh chạy ChatGPT
chat_gpt()