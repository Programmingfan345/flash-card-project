from tkinter import *
import tkinter as tk
import csv, pandas
import pandas as pd
import random, os, sys

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Hindi to English Flashcards")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)

if os.path.exists('words_to_learn.csv'):
    data = pandas.read_csv('words_to_learn.csv')
    data_dictionary = pd.Series(data.English.values,index=data.Hindi).to_dict()
    data_keys = list(data_dictionary.keys())
    
else:
    data = pandas.read_csv("flash-card-project-start/data/hindi_words.csv")
    data_dictionary = pd.Series(data.English.values,index=data.Hindi).to_dict()
    data_keys = list(data_dictionary.keys())

canvas = Canvas(height= 528, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="flash-card-project-start/images/card_front.png", height=528, width=800)
back_img = PhotoImage(file="flash-card-project-start/images/card_back.png", height=528, width=800)

front = canvas.create_image(400,264, image=back_img)
title = canvas.create_text(400,150,text="Hindi", font=("Arial", 40, "italic"))

if len(data_keys) == 0:
    sys.exit("You have memorized all the words!")

updated_word = random.choice(data_keys)
word = canvas.create_text(400,263,text=updated_word, font=("Arial", 60, "bold"))


df = pd.DataFrame({'Hindi': data_dictionary.keys(), 'English': data_dictionary.values()})
df.to_csv("words_to_learn.csv", index=False)


def flip():
    global side, flipping
    interface()
    if canvas.itemcget(front,"image") == "pyimage1":
        side = back_img
    else:
        side = front_img
    canvas.itemconfig(front, image=side)
    
    flipping = window.after(3000,flip)
    

def interface():
    if canvas.itemcget(front,"image") == "pyimage1":
        canvas.itemconfig(word,text=data_dictionary[updated_word], fill="white")
        canvas.itemconfig(title,text="English", fill="white")
    else:
        canvas.itemconfig(word,text=updated_word, fill="black")
        canvas.itemconfig(title,text="Hindi", fill="black")   

def complete():
    window.after_cancel(flipping)
    right_button.destroy()
    wrong_button.destroy()
    canvas.itemconfig(title, text="Complete!")
    canvas.itemconfig(word, text="")
    

def button_press(input):
    try:
        global updated_word, df
        window.after_cancel(flipping)
        canvas.itemconfig(front, image=back_img)
        flip()

        if input == "right":
            data_keys.remove(updated_word)
            word_index = df.index[df['Hindi'] == updated_word].tolist()
            df = df.drop(index=word_index)
            df.to_csv("words_to_learn.csv", index=False)
        updated_word = random.choice(data_keys)
                    
        canvas.itemconfig(word,text=updated_word)
        
    except IndexError:
        complete()       

canvas.grid(column=0, row=0, columnspan=2)

right_image = PhotoImage(file="flash-card-project-start/images/right.png")
right_button = Button(image=right_image, highlightthickness=0,command=lambda: button_press("right"))
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file="flash-card-project-start/images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0,command=lambda: button_press("wrong"))
wrong_button.grid(column=0, row=1)

flip()

window.mainloop()