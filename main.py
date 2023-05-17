import json
import requests
import pyaudio
import pyttsx3
import webbrowser
from vosk import Model, KaldiRecognizer

engine = pyttsx3.init()
engine.setProperty('rate', 125)

model = Model('small_model_en')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']


print('say: find <word>')
for text in listen():
    print(f'user: {text}')
    if 'find' in text:
        word = text.split(" ")[1]
        link = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
        try:
            data = requests.get(link).json()[0]
        except:
            print('robo: No Definitions Found')
            engine.say('No Definitions Found')
            engine.runAndWait()
            break
        print('robo: For exit of the branch say exit')
        engine.say('For exit of the branch say exit')
        engine.runAndWait()

        for text0 in listen():
            print(f'user: {text0}')
            if text0 == 'link':
                webbrowser.open(link, new=1)
                print('robo: link opened')
                engine.say('link opened')
                engine.runAndWait()
            elif text0 == 'save':
                with open('file.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                print('robo: File will save after closing the program')
                engine.say('File will save after closing the program')
                engine.runAndWait()
            elif text0 == 'meaning':
                print(f'robo: {data["meanings"][0]["definitions"][0]["definition"]}')
                engine.say(str(data["meanings"][0]["definitions"][0]["definition"]))
                engine.runAndWait()
                engine.say('For exit of the branch say exit')
                engine.runAndWait()
                for text1 in listen():
                    print(f'user: {text1}')
                    if text1 == 'example':
                        try:
                            print(f'robo: {data["meanings"][0]["definitions"][0]["example"]}')
                            engine.say(f'{data["meanings"][0]["definitions"][0]["example"]}')
                            engine.runAndWait()
                            break
                        except:
                            print(f'robo: example dont exist for this word')
                            engine.say('example dont exist for this word')
                            engine.runAndWait()
                            break
                    elif text1 == 'exit':
                        print('robo: exit from branch')
                        engine.say('exit from branch')
                        engine.runAndWait()
                        break
                    else:
                        print('robo: command not recognized, request error')
                        engine.say('command not recognized, request error')
                        engine.runAndWait()
            elif text0 == 'exit':
                print('robo: exit from branch')
                engine.say('exit from branch')
                engine.runAndWait()
                break
            else:
                print('robo: command not recognized, request error')
                engine.say('command not recognized, request error')
                engine.runAndWait()
    elif text == 'exit':
        exit()
    else:
        print('robo: command not recognized, request error')
        engine.say('command not recognized, request error')
        engine.runAndWait()
