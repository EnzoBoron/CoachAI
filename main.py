import random, math, csv, os
from tkinter import *
from tkinter import messagebox

# Weight initialization
w1_game = random.uniform(-0.5, 0.5)
w2_game = random.uniform(-0.5, 0.5)
w3_game = random.uniform(-0.5, 0.5)
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
neuron_out = 0
a_out = []

# Output weights (between the hidden layer and the output)
v1 = random.uniform(-0.5, 0.5)
v2 = random.uniform(-0.5, 0.5)
v3 = random.uniform(-0.5, 0.5)
b_out = random.uniform(0.001, 0.01)


# Initialization of the array to store the data in data.csv
data = []

# Input initialization
x_game = 0
x_fatigue = 0
x_motivation = 0
x_duo = 0

# Initialization of the correction variables
delta_1 = 0

# Initialization of the learning variables
learning = 0.03
bool_learning = True

# Initialization of the activation variables
a_h1 = 0
a_h2 = 0
a_h3 = 0

# Initialization of the correction UI
button_yes = None
bouton_no = None
question_label = None
label_prediction = None

# Initialization of variables for rate_schedule()
correct_sequence = 0
incorrect_sequence = 0

def rate_scheduler():
    global correct_sequence, incorrect_sequence, bool_learning, learning

    if not bool_learning: return

    if correct_sequence == 10:
        correct_sequence = 0
        incorrect_sequence = 0
        learning *= 0.8

    if incorrect_sequence == 3:
        incorrect_sequence = 0
        correct_sequence = 0
        learning *= 1.2

def early_stopping():
    global bool_learning, a_out

    if len(a_out) == 50:
        gap = [abs(a_out[i+1] - a_out[i]) for i in range(len(a_out) - 1)]
        average_gap = sum(gap) / len(gap)

        if average_gap <= 0.01:
            bool_learning = False
        elif average_gap >= 0.02:
            bool_learning = True

def save():
    global w1_game, w1_fatigue, w1_motivation, w1_duo, b1
    global w2_game, w2_fatigue, w2_motivation, w2_duo, b2
    global w3_game, w3_fatigue, w3_motivation, w3_duo, b3
    global learning, a_out, a_h1, a_h2, a_h3, delta_1
    global v1, v2, v3, b_out

    row = [
        w1_game, w1_fatigue, w1_motivation, w1_duo, b1,
        w2_game, w2_fatigue, w2_motivation, w2_duo, b2,
        w3_game, w3_fatigue, w3_motivation, w3_duo, b3,
        v1, v2, v3, b_out,
        learning, bool_learning, delta_1, a_out[-1] if a_out else 0
    ]

    with open("data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def sigmoid(x):
    return (1 / (1 + math.exp(-x)))

def hide_feedback():
    global question_label, button_yes, bouton_no, delta_1, label_prediction
    global game_value, fatigue_value, motivation_value, duo_value

    question_label.grid_forget()
    button_yes.grid_forget()
    bouton_no.grid_forget()
    label_prediction.grid_forget()
    game_value.set("")
    fatigue_value.set("")
    motivation_value.set("")
    duo_value.set("")

def handle_yes():
    global correct_sequence

    correct_sequence += 1
    save()
    hide_feedback()
    early_stopping()
    rate_scheduler()

def handle_no():
    global delta_1, incorrect_sequence

    delta_1 = 0 
    incorrect_sequence += 1
    correction()
    save()
    hide_feedback()
    early_stopping()
    rate_scheduler()

def prediction():
    global question_label, button_yes, bouton_no, label_prediction, delta_1
    global x_game, x_fatigue, x_motivation, x_duo, a_h1
    global w1_game, w2_game, w3_game, w1_fatigue, w2_fatigue, w3_fatigue, w1_motivation, w2_motivation, w3_motivation, w1_duo, w2_duo, w3_duo, b1, b2, b3, neuron_out, a_out

    if not game_value.get():
        messagebox.showwarning("Be careful!", "Choose a game before predicting!")
        return
    if not fatigue_value.get():
        messagebox.showwarning("Be careful!", "Indicate your fatigue level!")
        return
    if not motivation_value.get():
        messagebox.showwarning("Be careful!", "Indicate your motivation level!")
        return
    if not duo_value.get():
        messagebox.showwarning("Be careful!", "Select solo or duo!")
        return
    
    x_game = float(game_value.get())
    x_fatigue = float(fatigue_value.get())
    x_motivation = float(motivation_value.get())
    x_duo = float(duo_value.get())

    neuron1 = (x_game * w1_game) \
                + (x_fatigue * w1_fatigue) \
                + (x_motivation * w1_motivation) \
                + (x_duo * w1_duo) \
                + b1
    
    neuron2 = (x_game * w2_game) \
                + (x_fatigue * w2_fatigue) \
                + (x_motivation * w2_motivation) \
                + (x_duo * w2_duo) \
                + b2
    
    neuron3 = (x_game * w3_game) \
                + (x_fatigue * w3_fatigue) \
                + (x_motivation * w3_motivation) \
                + (x_duo * w3_duo) \
                + b3

    a_h1 = (sigmoid(neuron1))
    a_h2 = (sigmoid(neuron2))
    a_h3 = (sigmoid(neuron3))

    neuron_out = (a_h1 * v1) \
                + (a_h2 * v2) \
                + (a_h3 * v3) + b_out
    
    a_out.append(sigmoid(neuron_out))
   
    label_prediction.grid(row=9, column=5, padx=10, pady=10, sticky="SE")
    if a_out[-1] >= 0 and a_out[-1] < 0.25:
        label_prediction.config(text=f"Almost certainly losing: {a_out[-1]*100:.2f}%")
    elif a_out[-1] >= 0.25 and a_out[-1] < 0.45:
        label_prediction.config(text=f"Probably losing: {a_out[-1]*100:.2f}%")
    elif a_out[-1] >= 0.45 and a_out[-1] < 0.55:
        label_prediction.config(text=f"Uncertain: {a_out[-1]*100:.2f}%")
    elif a_out[-1] >= 0.55 and a_out[-1] < 0.75:
        label_prediction.config(text=f"Probably winning: {a_out[-1]*100:.2f}%")
    elif a_out[-1] >= 0.75 and a_out[-1] < 1.00:
        label_prediction.config(text=f"Almost certainly winning: {a_out[-1]*100:.2f}%")
    else:
        label_prediction.config(text="Almost certainly winning")

    question_label = Label(window, text="Correct prediction?")
    button_yes = Button(window, text="Yes", command=handle_yes)
    bouton_no = Button(window, text="No", command=handle_no)
    question_label.grid(row=9, column=0, sticky="W", padx=10, pady=10)
    button_yes.grid(row=10, column=0, sticky="W", padx=10, pady=10)
    bouton_no.grid(row=10, column=1, sticky="W", padx=10, pady=10)

def correction():
    global w1_game, w1_fatigue, w1_motivation, w1_duo, b1
    global w2_game, w2_fatigue, w2_motivation, w2_duo, b2
    global w3_game, w3_fatigue, w3_motivation, w3_duo, b3
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

    w1_game += delta_h1 * learning * x_game
    w1_fatigue += delta_h1 * learning * x_fatigue
    w1_motivation += delta_h1 * learning * x_motivation
    w1_duo += delta_h1 * learning * x_duo
    b1 += delta_h1 * learning

    w2_game += delta_h2 * learning * x_game
    w2_fatigue += delta_h2 * learning * x_fatigue
    w2_motivation += delta_h2 * learning * x_motivation
    w2_duo += delta_h2 * learning * x_duo
    b2 += delta_h2 * learning

    w3_game += delta_h3 * learning * x_game
    w3_fatigue += delta_h3 * learning * x_fatigue
    w3_motivation += delta_h3 * learning * x_motivation
    w3_duo += delta_h3 * learning * x_duo
    b3 += delta_h3 * learning

def reboot():
    os.system("bash reboot.sh")

def initialization():
    global w1_game, w1_fatigue, w1_motivation, w1_duo, b1
    global w2_game, w2_fatigue, w2_motivation, w2_duo, b2
    global w3_game, w3_fatigue, w3_motivation, w3_duo, b3
    global learning, a_out, a_h1, a_h2, a_h3, delta_1
    global v1, v2, v3, b_out
    global bool_learning

    with open("data.csv", "r") as f:
        lines = f.readlines()

    if not lines:
        return
    
    last_line = lines[-1].strip()

    values = last_line.split(",")

    w1_game = float(values[0])
    w1_fatigue = float(values[1])
    w1_motivation = float(values[2])
    w1_duo = float(values[3])
    b1 = float(values[4])
    w2_game = float(values[5])
    w2_fatigue = float(values[6])
    w2_motivation = float(values[7])
    w2_duo = float(values[8])
    b2 = float(values[9])
    w3_game = float(values[10])
    w3_fatigue = float(values[11])
    w3_motivation = float(values[12])
    w3_duo = float(values[13])
    b3 = float(values[14])
    v1 = float(values[15])
    v2 = float(values[16])
    v3 = float(values[17])
    b_out = float(values[18])
    learning = float(values[19])
    bool_learning = bool(values[20])
    delta_1 = float(values[21])
    a_out.append(float(values[22]))

# Début du programme
initialization()
window = Tk()
window.title("coachAI")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f"{int(width*0.7)}x{int(height*0.4)}")

label_prediction = Label(window)

menu_bar = Menu(window)
menu1 = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Fichier", menu=menu1)
menu1.add_command(label="Ouvrir", command=lambda: print("Ouvrir"))
menu1.add_separator()
menu1.add_command(label="Rénitialisé", command=lambda: print("Rénitialisé"))
menu1.add_separator()
menu1.add_command(label="Quitter", command=window.quit)

menu2 = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Editer", menu=menu2)
menu2.add_command(label="Copier", command=lambda: print("Copier"))

menu3 = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="A propos", menu=menu3)
menu3.add_command(label="Aide", command=lambda: print("aide"))

window.config(menu=menu_bar)

game_label = Label(window, text="Choose your game:")   
game_value = StringVar() 
overwatch = Radiobutton(window, text="Overwatch", variable=game_value, value=0)
fortnite = Radiobutton(window, text="Fortnite", variable=game_value, value=1)
game_label.grid(row=0, column=0, padx=10, pady=10)
overwatch.grid(row=0, column=1, padx=10, pady=10)
fortnite.grid(row=0, column=2, padx=10, pady=10)

fatigue_label = Label(window, text="Fatigue level:")
fatigue_value = StringVar() 
fatigue0 = Radiobutton(window, text="No fatigue", variable=fatigue_value, value=0.1)
fatigue1 = Radiobutton(window, text="Light fatigue", variable=fatigue_value, value=0.2)
fatigue2 = Radiobutton(window, text="Moderate fatigue", variable=fatigue_value, value=0.3)
fatigue3 = Radiobutton(window, text="High fatigue", variable=fatigue_value, value=0.4)
fatigue4 = Radiobutton(window, text="Extreme fatigue", variable=fatigue_value, value=0.5)
fatigue_label.grid(row=2, column=0, padx=10, pady=10)
fatigue0.grid(row=2, column=1, padx=10, pady=10)
fatigue1.grid(row=2, column=2, padx=10, pady=10)
fatigue2.grid(row=2, column=3, padx=10, pady=10)
fatigue3.grid(row=2, column=4, padx=10, pady=10)
fatigue4.grid(row=2, column=5, padx=10, pady=10)

motivation_label = Label(window, text="Niveau de motivation:")
motivation_value = StringVar() 
motivation0 = Radiobutton(window, text="No motivation", variable=motivation_value, value=0.1)
motivation1 = Radiobutton(window, text="Light motivation", variable=motivation_value, value=0.2)
motivation2 = Radiobutton(window, text="Moderate motivation", variable=motivation_value, value=0.3)
motivation3 = Radiobutton(window, text="High motivation", variable=motivation_value, value=0.4)
motivation4 = Radiobutton(window, text="Motivation maximal", variable=motivation_value, value=0.5)
motivation_label.grid(row=4, column=0, padx=10, pady=10)
motivation0.grid(row=4, column=1, padx=10, pady=10)
motivation1.grid(row=4, column=2, padx=10, pady=10)
motivation2.grid(row=4, column=3, padx=10, pady=10)
motivation3.grid(row=4, column=4, padx=10, pady=10)
motivation4.grid(row=4, column=5, padx=10, pady=10)

duo_label = Label(window, text="Solo or duo:")
duo_value = StringVar() 
duo0 = Radiobutton(window, text="Solo", variable=duo_value, value=0)
duo1 = Radiobutton(window, text="Duo", variable=duo_value, value=1)
duo_label.grid(row=6, column=0, padx=10, pady=10)
duo0.grid(row=6, column=1, padx=10, pady=10)
duo1.grid(row=6, column=2, padx=10, pady=10)

boutonPredir=Button(window, text="Predict", command=prediction)
boutonPredir.grid(row=8, column=0, columnspan=6, sticky="WE", padx=10, pady=20)

boutonReboot=Button(window, text="Reboot", command=reboot)
boutonReboot.grid(row=0, column=5, sticky="NE", padx=5, pady=5)

window.mainloop()
