from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

#------------- Generating Random Words ---------------#
current_card = {}
words = {}

try:
    data = pandas.read_csv("words_to_learn.csv.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    words = original_data.to_dict(orient="records")
else:
    words = data.to_dict(orient="records")


def random_words():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words)
    french_word = current_card["French"]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=f"{french_word}", fill="black")
    canvas.itemconfig(card_image, image=card_front)
    flip_timer = window.after(3000, flip_card)

#-------------------Flipping the card-----------------#


def flip_card():
    english_word = current_card["English"]
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=f"{english_word}", fill="white")
    canvas.itemconfig(card_image, image=card_back)

#------------------ Removing Known Words------------------#


def remove_known():
    words.remove(current_card)
    data = pandas.DataFrame(words)
    data.to_csv("words_to_learn.csv", index=False)
    random_words()

#------------------ UI SETUP----------------------#
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=100, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="card_front.png")
card_back = PhotoImage(file="card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
card_text = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

tick = PhotoImage(file="right.png")
tick_mark = Button(image=tick, highlightthickness=0, command=remove_known)
tick_mark.config(padx=50, pady=50)
tick_mark.place(x=580, y=520)

cross = PhotoImage(file="wrong.png")
cross_mark = Button(image=cross, highlightthickness=0, command=random_words)
cross_mark.config(padx=50, pady=50)
cross_mark.place(x=80, y=520)

random_words()


window.mainloop()

