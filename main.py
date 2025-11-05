import random, math, csv
from tkinter import *
from tkinter import messagebox

data = []
game_norm = 0
fatigue_norm = 0
motivation_norm = 0
duo_norm = 0
button_norm = 0
xjeu = random.uniform(-0.5, 0.5)
xfatigue = random.uniform(-0.5, 0.5)
xmotivation = random.uniform(-0.5, 0.5)
xduo = random.uniform(-0.5, 0.5)
biais = random.uniform(0.001, 0.01)
learning = 0.05
sig = 0
boutonOui = None
boutonNon = None
question_label = None
label_prediction = None

def save():
    global game_norm, fatigue_norm, motivation_norm, duo_norm, biais, button_norm

    with open("data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([game_norm, fatigue_norm, motivation_norm, duo_norm, biais, button_norm])

def sigmoid(x):
    return (1 / (1 + math.exp(-x)))

def hide_feedback():
    global question_label, boutonOui, boutonNon, button_norm, label_prediction, game_value, fatigue_value, motivation_value, duo_value

    question_label.grid_forget()
    boutonOui.grid_forget()
    boutonNon.grid_forget()
    label_prediction.grid_forget()
    game_value.set("")
    fatigue_value.set("")
    motivation_value.set("")
    duo_value.set("")

def handle_oui():
    global button_norm
    button_norm = 1
    save()
    hide_feedback()

def handle_non():
    global button_norm
    button_norm = 0
    correction()
    save()
    hide_feedback()


def prediction():
    global question_label, boutonOui, boutonNon, label_prediction, button_norm
    global game_norm, fatigue_norm, motivation_norm, duo_norm

    if not game_value.get():
        messagebox.showwarning("Attention", "Choisis un jeu avant de prédire !")
        return
    if not fatigue_value.get():
        messagebox.showwarning("Attention", "Indique ton niveau de fatigue !")
        return
    if not motivation_value.get():
        messagebox.showwarning("Attention", "Indique ton niveau de motivation !")
        return
    if not duo_value.get():
        messagebox.showwarning("Attention", "Choisis Solo ou Duo !")
        return
    
    game_norm = int(game_value.get())
    fatigue_norm = int(fatigue_value.get()) / 5
    motivation_norm = int(motivation_value.get()) / 5
    duo_norm = int(duo_value.get())


    prediction = (game_norm * xjeu) \
                + (fatigue_norm * xfatigue) \
                + (motivation_norm * xmotivation) \
                + (duo_norm * xduo) \
                + biais

    sig = sigmoid(prediction)

    label_prediction = Label(fenetre)
    if sig >= 0 and sig < 0.25:
        label_prediction.config(text=f"quasi sûr de perdre: {sig*100:.2f}%")
    elif sig >= 0.25 and sig < 0.45:
        label_prediction.config(text=f"probablement perdant: {sig*100:.2f}%")
    elif sig >= 0.45 and sig < 0.55:
        label_prediction.config(text=f"incertain: {sig*100:.2f}%")
    elif sig >= 0.55 and sig < 0.75:
        label_prediction.config(text=f"plutôt gagnant: {sig*100:.2f}%")
    elif sig >= 0.75 and sig < 1.00:
        label_prediction.config(text=f"quasi sûr de gagner: {sig*100:.2f}%")
    else:
        label_prediction.config(text="Erreur de prediction")

    label_prediction.grid(row=9, column=5, padx=10, pady=10, sticky="SE")

    question_label = Label(fenetre, text="Was true ?")
    button_value = StringVar() 
    boutonOui = Button(fenetre, text="Oui", command=handle_oui)
    boutonNon = Button(fenetre, text="Non", command=handle_non)
    question_label.grid(row=10, column=0, sticky="SW", padx=10, pady=10)
    boutonOui.grid(row=11, column=0, sticky="SW", padx=10, pady=10)
    boutonNon.grid(row=11, column=1, sticky="SW", padx=10, pady=10)


def correction():
    global xjeu, xfatigue, xmotivation, xduo, biais, sig
    global game_norm, fatigue_norm, motivation_norm, duo_norm, learning

    erreur = button_norm - sig

    xjeu += erreur * learning * game_norm
    xfatigue += erreur * learning * fatigue_norm
    xmotivation += erreur * learning * motivation_norm
    xduo += erreur * learning * duo_norm

    biais += erreur * learning

# def init():
    # initialiser l'ia avec l'historique (log.cvs)

fenetre = Tk()
fenetre.title("coachAI")
largeur = fenetre.winfo_screenwidth()
hauteur = fenetre.winfo_screenheight()
fenetre.geometry(f"{int(largeur*0.7)}x{int(hauteur*0.4)}")

menubar = Menu(fenetre)
menu1 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Editer", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Aide", menu=menu3)

fenetre.config(menu=menubar)

game_label = Label(fenetre, text="Choose your game:")
game_value = StringVar() 
overwatch = Radiobutton(fenetre, text="Overwatch", variable=game_value, value=1)
fortnite = Radiobutton(fenetre, text="Fortnite", variable=game_value, value=2)
game_label.grid(row=0, column=0, padx=10, pady=10)
overwatch.grid(row=0, column=1, padx=10, pady=10)
fortnite.grid(row=0, column=2, padx=10, pady=10)

fatigue_label = Label(fenetre, text="Niveau de fatigue:")
fatigue_value = StringVar() 
fatigue0 = Radiobutton(fenetre, text="Aucune fatigue", variable=fatigue_value, value=1)
fatigue1 = Radiobutton(fenetre, text="Légère fatigue", variable=fatigue_value, value=2)
fatigue2 = Radiobutton(fenetre, text="Fatigue moyenne", variable=fatigue_value, value=3)
fatigue3 = Radiobutton(fenetre, text="Fatigue importante", variable=fatigue_value, value=4)
fatigue4 = Radiobutton(fenetre, text="Fatigue extrême", variable=fatigue_value, value=5)
fatigue_label.grid(row=2, column=0, padx=10, pady=10)
fatigue0.grid(row=2, column=1, padx=10, pady=10)
fatigue1.grid(row=2, column=2, padx=10, pady=10)
fatigue2.grid(row=2, column=3, padx=10, pady=10)
fatigue3.grid(row=2, column=4, padx=10, pady=10)
fatigue4.grid(row=2, column=5, padx=10, pady=10)

motivation_label = Label(fenetre, text="Niveau de motivation:")
motivation_value = StringVar() 
motivation0 = Radiobutton(fenetre, text="Aucune motivation", variable=motivation_value, value=1)
motivation1 = Radiobutton(fenetre, text="Motivation faible", variable=motivation_value, value=2)
motivation2 = Radiobutton(fenetre, text="Motivation moyenne", variable=motivation_value, value=3)
motivation3 = Radiobutton(fenetre, text="Bonne motivation", variable=motivation_value, value=4)
motivation4 = Radiobutton(fenetre, text="Motivation maximale", variable=motivation_value, value=5)
motivation_label.grid(row=4, column=0, padx=10, pady=10)
motivation0.grid(row=4, column=1, padx=10, pady=10)
motivation1.grid(row=4, column=2, padx=10, pady=10)
motivation2.grid(row=4, column=3, padx=10, pady=10)
motivation3.grid(row=4, column=4, padx=10, pady=10)
motivation4.grid(row=4, column=5, padx=10, pady=10)

duo_label = Label(fenetre, text="Solo or duo:")
duo_value = StringVar() 
duo0 = Radiobutton(fenetre, text="Solo", variable=duo_value, value=1)
duo1 = Radiobutton(fenetre, text="Duo", variable=duo_value, value=2)
duo_label.grid(row=6, column=0, padx=10, pady=10)
duo0.grid(row=6, column=1, padx=10, pady=10)
duo1.grid(row=6, column=2, padx=10, pady=10)

boutonPredir=Button(fenetre, text="predire", command=prediction)
boutonPredir.grid(row=8, column=0, columnspan=6, sticky="WE", padx=10, pady=20)

fenetre.mainloop()
