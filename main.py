import pandas as pd
from tkinter import *
import random

BACKGROUND_COLOR = "#B1DDC6"
list_of_words = {}
current_card = {}

try:
    data = pd.read_csv("data/Palabras para aprender.cs")
except FileNotFoundError:
    original_data = pd.read_csv("data/Eng_words.csv")
    list_of_words = original_data.to_dict(orient="records")
else:
    list_of_words = data.to_dict(orient="records")

# en_word, esp_word = random.choice(list(list_of_words.items()))


def next_card():
    # en_word = random.choice(list(list_of_words))
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(list_of_words)
    canvas.itemconfig(card_title, text="Ingles", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="Espanol", fill="white")
    canvas.itemconfig(card_word, text=current_card["Esp"], fill="white")
    canvas.itemconfig(card_background, image=card_back)


def is_known():
    list_of_words.remove(current_card)
    data = pd.DataFrame(list_of_words)
    data.to_csv("data/Palabras para aprender.csv", index=False)
    next_card()


window = Tk()
window.title('Flashy')
window.config(pady=50, padx=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)


# card front
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# X
wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

# checkmark
check_mark = PhotoImage(file="images/right.png")
right_button = Button(image=check_mark, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
