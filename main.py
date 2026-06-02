from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# ---------------------------- DATA LOADING ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- CARD FLIP MECHANISM ------------------------------- #
def translate_word():
    canvas.itemconfig(image, image=back_card_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def next_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(image, image=card_front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=translate_word)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_word()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy - Language Learning App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=translate_word)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold")) # اندازه فونت به ۶۰ تغییر کرد
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

back_card_img = PhotoImage(file="images/card_back.png")
wrong_card_img = PhotoImage(file="images/wrong.png")
right_card_img = PhotoImage(file="images/right.png")

unknown_button = Button(image=wrong_card_img, highlightthickness=0, command=next_word)
unknown_button.grid(row=1, column=0)

known_button = Button(image=right_card_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_word()

window.mainloop()