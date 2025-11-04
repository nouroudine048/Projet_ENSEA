import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import RPi.GPIO as GPIO
from gpiozero import Buzzer, LED, Button, MotionSensor
import smtplib
from picamera2 import Picamera2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# ---------------- Configuration du matériel ----------------

# Buzzer sur GPIO 26
buzzer = Buzzer(26)  

# Configuration du digicode
colonnes = [6, 13, 19]      # C1, C2, C3
lignes = [17, 27, 22, 5]    # L1, L2, L3, L4

touches = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

GPIO.setmode(GPIO.BCM)
for pin in colonnes:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
for pin in lignes:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ---------------- Variables globales et de configuration ----------------

CODE_CORRECT = "1234"
is_active = False         # Indique si le système est armé
countdown_started = False # Permet d'éviter de lancer plusieurs comptes à rebours
remaining_time = 0
saved_time = 10
alarm_triggered = False
stop_alarm = False
input_code = ""

# ---------------- Configuration du capteur de porte (MC38) ----------------

# La fonction mc38 retourne True si la porte est fermée et False si la porte est ouverte
# On initialise le capteur de porte sur GPIO 21 (à garder si votre montage est ainsi)
door_sensor = Button(21)  # Notez que Button est ici utilisé pour lire l'état du capteur

def mc38():
    return door_sensor.is_pressed  # True = porte fermée, False = porte ouverte



# ---------------- Fonctions principales ----------------

def lire_touche():
    """Lit la touche pressée sur le clavier matriciel."""
    for col_index, col_pin in enumerate(colonnes):
        GPIO.output(col_pin, GPIO.LOW)
        for row_index, row_pin in enumerate(lignes):
            if not GPIO.input(row_pin):
                GPIO.output(col_pin, GPIO.HIGH)
                return touches[row_index][col_index]
        GPIO.output(col_pin, GPIO.HIGH)
    return None

def verifier_code():
    global is_active, remaining_time, alarm_triggered, stop_alarm, input_code
    if input_code == CODE_CORRECT:
        is_active = False
        remaining_time = 0
        time_label.config(text="---")
        update_status(False)
        messagebox.showinfo("Succès", "Code correct ! Système désactivé.")
        btn_activate.config(state=tk.NORMAL)
        if alarm_triggered:
            stop_alarm = True
            alarm_triggered = False
            buzzer.off()
    else:
        messagebox.showwarning("Erreur", "Code incorrect !")
    input_code = ""
    entry_code.config(text="")

def update_status(active):
    if active:
        status_label.config(text="SYSTÈME ACTIVÉ", background="#ff4d4d")
    else:
        status_label.config(text="SYSTÈME DÉSACTIVÉ", background="#4CAF50")

def start_timer():
    """Initialise le temps du compte à rebours et lance le suivi de la porte.
       Le compte à rebours démarre uniquement lorsque la porte est ouverte."""
    global remaining_time, is_active, saved_time, countdown_started
    try:
        saved_time = int(entry_time.get())
        entry_time_display.config(text=f"Temps enregistré : {saved_time}s")
    except ValueError:
        messagebox.showwarning("Erreur", "Veuillez entrer un nombre valide.")
        return
    if saved_time <= 0:
        messagebox.showwarning("Erreur", "Veuillez entrer un temps valide (supérieur à 0).")
        return
    
    # Armement du système
    remaining_time = saved_time
    is_active = True
    countdown_started = False  # Le compte à rebours n'a pas encore démarré
    update_status(True)
    btn_activate.config(state=tk.DISABLED)
    messagebox.showinfo("Système activé", "Le système est activé.\nLe compte à rebours démarrera à l'ouverture de la porte.")

def countdown():
    """Compte à rebours une fois la porte ouverte."""
    global remaining_time, is_active
    while remaining_time > 0 and is_active:
        time_label.config(text=f"{remaining_time}s")
        time.sleep(1)
        remaining_time -= 1
        root.update()
    if remaining_time == 0 and is_active:
        trigger_alarm()
        update_status(False)
        is_active = False
    btn_activate.config(state=tk.NORMAL)

def trigger_alarm():
    global alarm_triggered, stop_alarm
    alarm_triggered = True
    stop_alarm = False
    for _ in range(5):  # Vous pouvez ajuster le nombre de répétitions
        if stop_alarm:
            break
        buzzer.on()
        time.sleep(0.4)
        buzzer.off()
        time.sleep(0.4)
    alarm_triggered = False

def lire_digicode():
    """Lecture en boucle du digicode."""
    global input_code
    while True:
        touche = lire_touche()
        if touche:
            if touche == '#':
                verifier_code()
            elif touche == '*':
                input_code = ""
                entry_code.config(text="")
            else:
                input_code += touche
                entry_code.config(text="*" * len(input_code))
        time.sleep(0.4)


def monitor_door():
    """Surveille l'état de la porte.
       Dès que porte est ouverte et que le système est activé, le compte à rebours démarre."""
    global countdown_started
    while True:
        if is_active and not countdown_started:
            # Si mc38() retourne False, la porte est ouverte
            if not mc38():
                countdown_started = True
                # Lancer le compte à rebours dans un thread séparé pour ne pas bloquer la surveillance
                threading.Thread(target=countdown, daemon=True).start()
        time.sleep(0.5)

# ---------------- Threads de surveillance ----------------

digicode_thread = threading.Thread(target=lire_digicode, daemon=True)
digicode_thread.start()

activation_thread = threading.Thread(target=monitor_activation_button, daemon=True)
activation_thread.start()

door_thread = threading.Thread(target=monitor_door, daemon=True)
door_thread.start()

# ---------------- Interface Graphique ----------------

root = tk.Tk()
root.title("Système de Surveillance")
root.geometry("350x400")
root.configure(bg="#f4f4f4")

style = ttk.Style()
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TLabel", font=("Arial", 12))

frame_status = tk.Frame(root, bg="#4CAF50", padx=10, pady=10)
frame_status.pack(fill="x", pady=10)
status_label = tk.Label(frame_status, text="SYSTÈME DÉSACTIVÉ", bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), width=30)
status_label.pack()

frame_code = ttk.LabelFrame(root, text="Code d'accès", padding=10)
frame_code.pack(fill="x", padx=10, pady=5)
entry_code = tk.Label(frame_code, text="", font=("Arial", 14))
entry_code.pack(pady=5)
ttk.Button(frame_code, text="Valider", command=verifier_code).pack(pady=5)

frame_time = ttk.LabelFrame(root, text="Paramètres du Système", padding=10)
frame_time.pack(fill="x", padx=10, pady=5)
entry_time = ttk.Entry(frame_time)
entry_time.insert(0, str(saved_time))
entry_time.pack()
entry_time_display = ttk.Label(frame_time, text=f"Temps enregistré : {saved_time}s")
entry_time_display.pack(pady=5)

# Même si le système est activé via le bouton physique, nous laissons ce bouton en GUI pour un éventuel test.
btn_activate = ttk.Button(root, text="Activer Système (GUI)", command=lambda: threading.Thread(target=start_timer).start())
btn_activate.pack(pady=10)

frame_timer = tk.Frame(root, bg="#ff4d4d", padx=10, pady=10)
frame_timer.pack(fill="x", padx=10, pady=5)
ttk.Label(frame_timer, text="Temps restant:", background="#ff4d4d", foreground="white", font=("Arial", 12, "bold")).pack()
time_label = tk.Label(frame_timer, text="---", bg="#ff4d4d", fg="white", font=("Arial", 16, "bold"))
time_label.pack()

root.protocol("WM_DELETE_WINDOW", lambda: (GPIO.cleanup(), root.destroy()))
root.mainloop()
