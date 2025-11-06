import random, math, csv, os
from tkinter import *
from tkinter import messagebox

# Initialisation des poids
w1_jeu = random.uniform(-0.5, 0.5)
w2_jeu = random.uniform(-0.5, 0.5)
w3_jeu = random.uniform(-0.5, 0.5)
w1_fatigue = random.uniform(-0.5, 0.5)
w2_fatigue = random.uniform(-0.5, 0.5)
w3_fatigue = random.uniform(-0.5, 0.5)
w1_motivation = random.uniform(-0.5, 0.5)
w2_motivation = random.uniform(-0.5, 0.5)
w3_motivation = random.uniform(-0.5, 0.5)
w1_duo = random.uniform(-0.5, 0.5)
w2_duo = random.uniform(-0.5, 0.5)
w3_duo = random.uniform(-0.5, 0.5)
b1 = random.uniform(0.001, 0.01)
b2 = random.uniform(0.001, 0.01)
b3 = random.uniform(0.001, 0.01)
neurone_out = 0
a_out = []
# Poids de sortie (entre la couche cachée et la sortie)
v1 = random.uniform(-0.5, 0.5)
v2 = random.uniform(-0.5, 0.5)
v3 = random.uniform(-0.5, 0.5)
b_out = random.uniform(0.001, 0.01)


# initialisation du tableau pour enregistré les donnée dans data.csv
data = []

# Initialisation des entrées
x_game = 0
x_fatigue = 0
x_motivation = 0
x_duo = 0

# initialisation des variable de correction
delta_1 = 0

# Initialisation des variable d'apprentissage
learning = 0.03
bool_learning = True

# Initialisation des variables d'activation
a_h1 = 0
a_h2 = 0
a_h3 = 0

# Initialisation de l'UI de correction
boutonOui = None
boutonNon = None
question_label = None
label_prediction = None

# Initialisation de variable pour le rate_schedule()
suite_correct = 0
suite_incorrect = 0

def rate_scheduler():
    global suite_correct, suite_incorrect, bool_learning, learning

    if not bool_learning: return

    if suite_correct == 10:
        suite_correct = 0
        suite_incorrect = 0
        learning *= 0.8

    if suite_incorrect == 3:
        suite_incorrect = 0
        suite_correct = 0
        learning *= 1.2

def early_stopping():
    global bool_learning, a_out

    if len(a_out) == 50:
        ecart = [abs(a_out[i+1] - a_out[i]) for i in range(len(a_out) - 1)]
        moyenne_ecart = sum(ecart) / len(ecart)

        if moyenne_ecart <= 0.01:
            bool_learning = False
        elif moyenne_ecart >= 0.02:
            bool_learning = True

def save():
    global w1_jeu, w1_fatigue, w1_motivation, w1_duo, b1
    global w2_jeu, w2_fatigue, w2_motivation, w2_duo, b2
    global w3_jeu, w3_fatigue, w3_motivation, w3_duo, b3
    global learning, a_out, a_h1, a_h2, a_h3, delta_1
    global v1, v2, v3, b_out

    row = [
        w1_jeu, w1_fatigue, w1_motivation, w1_duo, b1,
        w2_jeu, w2_fatigue, w2_motivation, w2_duo, b2,
        w3_jeu, w3_fatigue, w3_motivation, w3_duo, b3,
        v1, v2, v3, b_out,
        learning, bool_learning, delta_1, a_out[-1] if a_out else 0
    ]

    with open("data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def sigmoid(x):
    return (1 / (1 + math.exp(-x)))

def hide_feedback():
    global question_label, boutonOui, boutonNon, delta_1, label_prediction, game_value, fatigue_value, motivation_value, duo_value

    question_label.grid_forget()
    boutonOui.grid_forget()
    boutonNon.grid_forget()
    label_prediction.grid_forget()
    game_value.set("")
    fatigue_value.set("")
    motivation_value.set("")
    duo_value.set("")

def handle_oui():
    global delta_1, suite_correct

    delta_1 = 1
    suite_correct += 1
    correction()
    save()
    hide_feedback()
    early_stopping()
    rate_scheduler()

def handle_non():
    global delta_1, suite_incorrect

    delta_1 = 0 
    suite_incorrect += 1
    correction()
    save()
    hide_feedback()
    early_stopping()
    rate_scheduler()

def prediction():
    global question_label, boutonOui, boutonNon, label_prediction, delta_1
    global x_game, x_fatigue, x_motivation, x_duo, a_h1
    global w1_jeu, w2_jeu, w3_jeu, w1_fatigue, w2_fatigue, w3_fatigue, w1_motivation, w2_motivation, w3_motivation, w1_duo, w2_duo, w3_duo, b1, b2, b3, neurone_out, a_out

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
    
    x_game = float(game_value.get())
    x_fatigue = float(fatigue_value.get())
    x_motivation = float(motivation_value.get())
    x_duo = float(duo_value.get())

    neurone1 = (x_game * w1_jeu) \
                + (x_fatigue * w1_fatigue) \
                + (x_motivation * w1_motivation) \
                + (x_duo * w1_duo) \
                + b1
    
    neurone2 = (x_game * w2_jeu) \
                + (x_fatigue * w2_fatigue) \
                + (x_motivation * w2_motivation) \
                + (x_duo * w2_duo) \
                + b2
    
    neurone3 = (x_game * w3_jeu) \
                + (x_fatigue * w3_fatigue) \
                + (x_motivation * w3_motivation) \
                + (x_duo * w3_duo) \
                + b3

    a_h1 = (sigmoid(neurone1))
    a_h2 = (sigmoid(neurone2))
    a_h3 = (sigmoid(neurone3))

    neurone_out = (a_h1 * v1) \
                + (a_h2 * v2) \
                + (a_h3 * v3) + b_out
    
    a_out.append(sigmoid(neurone_out))
   
    label_prediction.grid(row=9, column=5, padx=10, pady=10, sticky="SE")
    if a_out[-1] >= 0 and a_out[-1] < 0.25:
        label_prediction.config(text=f"quasi sûr de perdre: {a_out[-1]*100:.2f}%")
    elif a_out[-1] >= 0.25 and a_out[-1] < 0.45:
        label_prediction.config(text=f"probablement perdant: {a_out[-1]*100:.2f}%")
    elif a_out[-1] >= 0.45 and a_out[-1] < 0.55:
        label_prediction.config(text=f"incertain: {a_out[-1]*100:.2f}%")
    elif a_out[-1] >= 0.55 and a_out[-1] < 0.75:
        label_prediction.config(text=f"plutôt gagnant: {a_out[-1]*100:.2f}%")
    elif a_out[-1] >= 0.75 and a_out[-1] < 1.00:
        label_prediction.config(text=f"quasi sûr de gagner: {a_out[-1]*100:.2f}%")
    else:
        label_prediction.config(text="Erreur de prediction")

    question_label = Label(fenetre, text="Prédiction correcte ?")
    boutonOui = Button(fenetre, text="Oui", command=handle_oui)
    boutonNon = Button(fenetre, text="Non", command=handle_non)
    question_label.grid(row=10, column=0, sticky="SW", padx=10, pady=10)
    boutonOui.grid(row=11, column=0, sticky="SW", padx=10, pady=10)
    boutonNon.grid(row=11, column=1, sticky="SW", padx=10, pady=10)

def correction():
    global w1_jeu, w1_fatigue, w1_motivation, w1_duo, b1
    global w2_jeu, w2_fatigue, w2_motivation, w2_duo, b2
    global w3_jeu, w3_fatigue, w3_motivation, w3_duo, b3
    global v1, v2, v3, b_out
    global x_game, x_fatigue, x_motivation, x_duo
    global learning, a_out, a_h1, a_h2, a_h3, delta_1

    delta_out = delta_1 - a_out[-1]


    delta_h1 = (v1 * delta_out) * a_h1 * (1 - a_h1)
    delta_h2 = (v2 * delta_out) * a_h2 * (1 - a_h2)
    delta_h3 = (v3 * delta_out) * a_h3 * (1 - a_h3)

    v1 += delta_out * learning * a_h1
    v2 += delta_out * learning * a_h2
    v3 += delta_out * learning * a_h3
    b_out += learning * delta_out

    w1_jeu += delta_h1 * learning * x_game
    w1_fatigue += delta_h1 * learning * x_fatigue
    w1_motivation += delta_h1 * learning * x_motivation
    w1_duo += delta_h1 * learning * x_duo
    b1 += delta_h1 * learning

    w2_jeu += delta_h2 * learning * x_game
    w2_fatigue += delta_h2 * learning * x_fatigue
    w2_motivation += delta_h2 * learning * x_motivation
    w2_duo += delta_h2 * learning * x_duo
    b2 += delta_h2 * learning

    w3_jeu += delta_h3 * learning * x_game
    w3_fatigue += delta_h3 * learning * x_fatigue
    w3_motivation += delta_h3 * learning * x_motivation
    w3_duo += delta_h3 * learning * x_duo
    b3 += delta_h3 * learning

def reboot():
    os.system("bash reboot.sh")

# def init():
    # initialiser l'ia avec l'historique (log.cvs)

fenetre = Tk()
fenetre.title("coachAI")
largeur = fenetre.winfo_screenwidth()
hauteur = fenetre.winfo_screenheight()
fenetre.geometry(f"{int(largeur*0.7)}x{int(hauteur*0.2)}")

label_prediction = Label(fenetre)

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
overwatch = Radiobutton(fenetre, text="Overwatch", variable=game_value, value=0)
fortnite = Radiobutton(fenetre, text="Fortnite", variable=game_value, value=1)
game_label.grid(row=0, column=0, padx=10, pady=10)
overwatch.grid(row=0, column=1, padx=10, pady=10)
fortnite.grid(row=0, column=2, padx=10, pady=10)

fatigue_label = Label(fenetre, text="Niveau de fatigue:")
fatigue_value = StringVar() 
fatigue0 = Radiobutton(fenetre, text="Aucune fatigue", variable=fatigue_value, value=0.1)
fatigue1 = Radiobutton(fenetre, text="Légère fatigue", variable=fatigue_value, value=0.2)
fatigue2 = Radiobutton(fenetre, text="Fatigue moyenne", variable=fatigue_value, value=0.3)
fatigue3 = Radiobutton(fenetre, text="Fatigue importante", variable=fatigue_value, value=0.4)
fatigue4 = Radiobutton(fenetre, text="Fatigue extrême", variable=fatigue_value, value=0.5)
fatigue_label.grid(row=2, column=0, padx=10, pady=10)
fatigue0.grid(row=2, column=1, padx=10, pady=10)
fatigue1.grid(row=2, column=2, padx=10, pady=10)
fatigue2.grid(row=2, column=3, padx=10, pady=10)
fatigue3.grid(row=2, column=4, padx=10, pady=10)
fatigue4.grid(row=2, column=5, padx=10, pady=10)

motivation_label = Label(fenetre, text="Niveau de motivation:")
motivation_value = StringVar() 
motivation0 = Radiobutton(fenetre, text="Aucune motivation", variable=motivation_value, value=0.1)
motivation1 = Radiobutton(fenetre, text="Motivation faible", variable=motivation_value, value=0.2)
motivation2 = Radiobutton(fenetre, text="Motivation moyenne", variable=motivation_value, value=0.3)
motivation3 = Radiobutton(fenetre, text="Bonne motivation", variable=motivation_value, value=0.4)
motivation4 = Radiobutton(fenetre, text="Motivation maximale", variable=motivation_value, value=0.5)
motivation_label.grid(row=4, column=0, padx=10, pady=10)
motivation0.grid(row=4, column=1, padx=10, pady=10)
motivation1.grid(row=4, column=2, padx=10, pady=10)
motivation2.grid(row=4, column=3, padx=10, pady=10)
motivation3.grid(row=4, column=4, padx=10, pady=10)
motivation4.grid(row=4, column=5, padx=10, pady=10)

duo_label = Label(fenetre, text="Solo or duo:")
duo_value = StringVar() 
duo0 = Radiobutton(fenetre, text="Solo", variable=duo_value, value=0)
duo1 = Radiobutton(fenetre, text="Duo", variable=duo_value, value=1)
duo_label.grid(row=6, column=0, padx=10, pady=10)
duo0.grid(row=6, column=1, padx=10, pady=10)
duo1.grid(row=6, column=2, padx=10, pady=10)

boutonPredir=Button(fenetre, text="predire", command=prediction)
boutonPredir.grid(row=8, column=0, columnspan=6, sticky="WE", padx=10, pady=20)

boutonReboot=Button(fenetre, text="Reboot", command=reboot)
boutonReboot.grid(row=10, column=0, columnspan=6, sticky="WE", padx=10, pady=20)


fenetre.mainloop()
