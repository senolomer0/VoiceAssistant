import time
import sqlite3

import wikipedia
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
import wolframalpha

class Voice_Assistant():
    def __init__(self):
        super().__init__()
        self.i = 0
        self.first_date()
        
    def first_date(self):
        con = sqlite3.connect("user.db")
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS USER(Name TEXT,Surname TEXT)")
        con.commit()

        cursor.execute("select * from USER")
        self.name = cursor.fetchall()
        if(len(self.name)==0):
            self.speak("Hi. My name is Carla. I will always be here for you. What is your name sir?")
            self.response = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.response.listen(source)
            try:
                self.phrase = self.response.recognize_google(audio, language="tr-TR")
                self.phrase = self.phrase.lower()
                print(self.phrase)
            except sr.UnknownValueError:
                self.speak("Sorry, I did not get that.Please repeat")
            
            self.name_list = self.phrase.split(" ")

            cursor.execute("insert into USER VALUES(?,?)",(self.name_list[0],self.name_list[1]))
            con.commit()

            cursor.execute("select * from USER")
            self.name = cursor.fetchall()
            self.greeting()
        else:
            self.greeting()
        
    def speak(self,say):
        self.engine = pyttsx3.init()
        self.engine.say(say)
        self.engine.runAndWait()

    def re_listen(self):
        self.response = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.response.listen(source)
        try:
            self.phrase = self.response.recognize_google(audio, language="en-in")
            self.phrase = self.phrase.lower()
            print(self.phrase)
        except sr.UnknownValueError:
            self.speak("You don't say anything.")
            self.phrase = "repeat"
        return self.phrase

    def listen(self):
        self.speak("How can i help you?")
        while(1):
            self.response = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.response.listen(source)
            if self.i==3:
                self.speak("I close the program because you did not make any requests.")
                time.sleep(1)
                self.speak("Have a good day "+self.name[0][0])
                break
            try:
                self.phrase = self.response.recognize_google(audio, language="en-in")
                self.phrase = self.phrase.lower()
                print(self.phrase)
            except sr.UnknownValueError:
                self.speak("You don't say anything. I will close soon.")
                self.i += 1
                self.phrase = ""

            if(len(self.phrase)!=0):
                self.i = 0

            if "open" in self.phrase:
                list = self.phrase.split(" ")
                a = list.index("open")
                if("." in list[a+1]):
                    webbrowser.open_new_tab("https://www."+list[a+1])
                else:
                    webbrowser.open_new_tab("https://www."+list[a+1]+".com")
                self.speak("I am opening "+list[a+1])

            elif "don't listen" in self.phrase or "stop listening" in self.phrase or "stop listen" in self.phrase:
                self.speak("for how much second you want")
                try:
                    a = int(self.re_listen())
                    self.speak("Okay. I am not listen to "+ str(a) +"second.")
                    time.sleep(a)
                    self.speak("I am back and ready for listen.")
                except:
                    pass

            elif "what is your name" in self.phrase:
                self.speak("My Name Is Carla")

            elif "how are you" in self.phrase:
                self.speak("Fine thank you.")

            elif "how old are you" in self.phrase:
                self.speak("We are at the same age. Did you forget?")

            elif "who are you" in self.phrase:
                self.speak("I am your voice assistant created by you")

            elif "time" in self.phrase:
                time_now = datetime.now().strftime("%H:%M:%S")    
                self.speak("The time is {}".format(time_now))

            elif "carla" == self.phrase:
                self.speak("Yes I am here "+self.name[0][0] + ". I listening you.")

            elif "close" in self.phrase or "exit" in self.phrase or "stop" in self.phrase or "shut down" in self.phrase or "goodbye" in self.phrase:
                self.speak("I am closing")
                time.sleep(1)
                self.speak("Have a good day "+self.name[0][0])
                break
            
            elif "youtube" in self.phrase and "search" in self.phrase:
                list = self.phrase.split(" ")
                a = list.index("youtube")
                search = ""
                for i in list[a+1:]:
                    search += str(i+" ")
                webbrowser.open_new_tab("http://www.youtube.com/results?search_query="+search)
                self.speak("I am searching"+search+"in youtube") 

            elif "who is" in self.phrase or "who's" in self.phrase:
                list = self.phrase.split(" ")
                a = list.index("who")
                search = ""
                for i in list[a+2:]:
                    search += str(i+" ")
                try:
                    sentence = wikipedia.summary(search,sentences=2)
                    print(sentence)
                    self.speak(sentence)
                except:
                    try:
                        client = wolframalpha.Client("YOUR API KEY")
                        res = client.query(self.phrase)
                        print(next(res.results).text)
                        self.speak(next(res.results).text)
                    except:
                        self.speak("I could not find anything about it.")

            elif "search" in self.phrase or "google" in self.phrase:
                list = self.phrase.split(" ")
                a = list.index("search")
                search = ""
                for i in list[a+1:]:
                    search += str(i+" ")
                webbrowser.open_new_tab("https://www.google.com/search?q=+"+search)
                if "on google" in self.phrase:
                    self.speak("I am searching "+search)
                else:
                    self.speak("I am searching "+search+"on Google")

            elif "where is" in self.phrase:
                list = self.phrase.split(" ")
                a = list.index("where")
                search = ""
                for i in list[a+2:]:
                    search += str(i+" ")
                webbrowser.open_new_tab("https://www.google.com/maps/place/"+search+"/&amp;")
                self.speak("I am show you "+search+"location")
                
            elif "wikipedia" in self.phrase:
                list = self.phrase.split(" ")
                a = list.index("wikipedia")
                search = ""
                for i in list[a+1:]:
                    search += str(i+" ")
                try:
                    sentence = wikipedia.summary(search,sentences=2)
                    print(sentence)
                    self.speak(sentence)
                except:
                    self.speak("I could not find anything about it.")
               
            else:
                try:
                    client = wolframalpha.Client("YOUR API KEY")
                    res = client.query(self.phrase)
                    print(next(res.results).text)
                    self.speak(next(res.results).text)
                except:
                    self.speak("I could not find anything about it.")

    def greeting(self):
        hour = datetime.now().hour
        if(hour>=7 and hour<12):
            self.speak("Good Morning " + self.name[0][0])
        elif(hour>=12 and hour<18):
            self.speak("Good Afternoon " + self.name[0][0])
        elif(hour>=18 and hour<22):
            self.speak("Good Evening " + self.name[0][0])
        else:
            self.speak("Good Night " + self.name[0][0])
        
        self.listen()
       
assistant = Voice_Assistant()
