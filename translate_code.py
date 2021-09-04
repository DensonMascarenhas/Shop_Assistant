from datetime import date

import googletrans
import speech_recognition as sr
import gtts
import pyttsx3
import pyodbc
import datetime


recognizer = sr.Recognizer()
listener= sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
total_amount=0
counter=0
id=0
price=0
stock=0
total_amount=0
total_qty=0
now=datetime.datetime.now()
t_qty=0;
t_price=0.000
def welcome():
    pyttsx3.speak("Hello. This is your billing assistant. Items from inventory are being loaded. this may take a while")



welcome()
datie=str(datetime.datetime.now().day )
# print(datie)
pyttsx3.speak("Please wait..")
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-A2K8SCL;'
                      'Database=shop_assistant;'
                      'Trusted_Connection=yes;')
pyttsx3.speak("Inventory items are loaded successfully and the assistant is ready to run")
engine.runAndWait()



cursor=conn.cursor()
# query="SELECT * FROM shop_assistant.dbo.entries WHERE date=(?)"
# cursor.execute(query,(datetime.datetime.now().date()))
# for row in cursor:
#     print(row)



pyttsx3.speak("Assistant is listening...")
while(True):

    with sr.Microphone() as source:
        recognizer.pause_threshold = 0.5
        pyttsx3.speak("tell item name...")

        print("Listening...")
        voice = recognizer.listen(source,phrase_time_limit=5)
        text = recognizer.recognize_google(voice)
        text=text.lower()
        # print(text)
        if "finish" in text:
            pyttsx3.speak("Total quantity of items are {}. Total amount is to pay is {}....Thank you for shopping with us...".format(total_qty,total_amount))
            if total_amount>0 and total_qty>0:
                query="INSERT INTO shop_assistant.dbo.entr (qty,price,date) VALUES(?,?,?)"
                cursor.execute(query,(total_qty,total_amount,datetime.datetime.today()))
                conn.commit()
            exit(0)

        elif "report" in text:
            cursor.execute("select * from shop_assistant.dbo.entr")
            for row in cursor:
                if str(datetime.datetime.now().day) in row[3]:
                    t_qty += row[1]
                    t_price += row[2]
            # print(t_qty)
            # print(t_price)
            pyttsx3.speak("Total quantity of items purchased today are {}. Total amount are {}....Thank you.".format(t_qty,t_price))

            t_qty=t_price=0;


        else:

            cursor=conn.cursor()
            cursor.execute('SELECT * FROM shop_assistant.dbo.stock')
            for row in cursor:
                if row[1] == text:
                    counter = 1
                    id = row[0]
                    price = row[2]
                    stock = row[3]


            if(counter==1):
                # print(id, price, stock)
                pyttsx3.speak("Specified item is found in your inventory")
                while(True):
                    try:

                        with sr.Microphone() as src:
                            pyttsx3.speak("Specify the quantity...")
                            print("Listening...")
                            listener.pause_threshold = 0.5
                            qty_voice = recognizer.listen(src, phrase_time_limit=5)
                            qty_text = recognizer.recognize_google(qty_voice)
                            # print(qty_text)
                            pyttsx3.speak("Specified quantity is...")
                            pyttsx3.speak(qty_text)
                            qty_text = int(qty_text)
                            if (qty_text < stock):
                                total_qty+=qty_text
                                total_amount = total_amount + (qty_text * price)
                                stock = stock - qty_text
                                # print(stock, total_amount)

                                cursor.execute('UPDATE shop_assistant.dbo.stock SET stock={} WHERE id={}'.format(stock, id))
                                conn.commit()
                                # print(total_amount)
                                print("Successful")
                                # with open('Record.csv','r+')as f:
                                #     datalist=f.readlines();
                                #
                                #     f.writelines(f'\n{text},{qty_text},{total_amount},{datie}')

                                counter=0
                                id=0
                                stock=0
                                price=0





                            else:
                                pyttsx3.speak("Not enough stock to sell this item.")

                            # print(qty_text)
                        break

                    except:
                        pyttsx3.speak("Could not get you sir. Please pronounce the digit properly...")






            else:
                pyttsx3.speak("Item is Not present in your inventory")





