import smbus
import time

# --- Configuration ---
bus = smbus.SMBus(1)
STM32_ADDR = 0x55

# --- Registres MD25 ---
REG_SPEED1 = 0x00 # Vitesse Moteur 1 (souvent Gauche)
REG_SPEED2 = 0x01 # Vitesse Moteur 2 (souvent Droit)
REG_MODE   = 0x0F # Mode de fonctionnement

def md25_send(register, value):
    """ Envoie la commande au STM32 (qui transmet au MD25) """
    try:
        # Conversion pour les nombres négatifs (-128 à 127)
        if value < 0:
            value = value + 256
        value = max(0, min(255, value))

        bus.write_byte_data(STM32_ADDR, register, value)
    except OSError:
        print("⚠️ Erreur I2C - STM32 non détecté")

def setup_robot():
    print("Configuration du MD25...")
    # Mode 1 : Contrôle indépendant des moteurs avec valeurs signées
    md25_send(REG_MODE, 1)
    time.sleep(0.1)

# --- Fonctions de Mouvement ---

def stop():
    print("   [STOP]")
    md25_send(REG_SPEED1, 0)
    md25_send(REG_SPEED2, 0)

def avancer(vitesse):
    print(f" ↑ AVANCE (Vitesse {vitesse})")
    # Pour avancer, les deux moteurs tournent dans le même sens "logique"
    md25_send(REG_SPEED1, vitesse)
    md25_send(REG_SPEED2, vitesse)

def reculer(vitesse):
    print(f" ↓ RECULE (Vitesse {vitesse})")
    md25_send(REG_SPEED1, -vitesse)
    md25_send(REG_SPEED2, -vitesse)

def tourner_gauche(vitesse):
    print(f" ← GAUCHE (Pivot)")
    # Pour pivoter à gauche : Moteur G arrière, Moteur D avant
    md25_send(REG_SPEED1, -vitesse)
    md25_send(REG_SPEED2, vitesse)

def tourner_droite(vitesse):
    print(f" → DROITE (Pivot)")
    # Pour pivoter à droite : Moteur G avant, Moteur D arrière
    md25_send(REG_SPEED1, vitesse)
    md25_send(REG_SPEED2, -vitesse)

# --- Scénario de Test ---

if __name__ == "__main__":
    setup_robot()

    try:
        print("\n--- DÉBUT DU TEST ROBOT ---\n")

        # 1. Avancer droit
        avancer(200)
        time.sleep(2)

        stop()
        time.sleep(0.5)

        # 2. Reculer
        reculer(150)
        time.sleep(2)

        stop()
        time.sleep(0.5)

        # 3. Pivoter à gauche sur place
        tourner_gauche(100) # Vitesse un peu plus lente pour tourner
        time.sleep(1.5)

        stop()
        time.sleep(0.5)

        # 4. Pivoter à droite sur place
        tourner_droite(40)
        time.sleep(1.5)

        stop()
        print("\n--- FIN DU TEST ---")

    except KeyboardInterrupt:
        print("\nArrêt d'urgence !")
        stop()