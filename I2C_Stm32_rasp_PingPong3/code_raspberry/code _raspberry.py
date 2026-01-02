import smbus2
import time
import sys

# --- Configuration I2C ---
# L'adresse configurée dans le STM32 (132 décimal = 0x42 hex)
STM32_ADDRESS = 0x42
BUS_NUMBER = 1        # Généralement 1 sur les Raspberry Pi récents
PING_CMD = "PING"     # Commande de 4 octets
PONG_RSP_LEN = 4      # Attente de 4 octets de réponse

# --- Initialisation ---
try:
    bus = smbus2.SMBus(BUS_NUMBER)
    print(f"Bus I2C {BUS_NUMBER} ouvert pour l'adresse 0x{STM32_ADDRESS:x}.")

    # Convertir la chaîne "PING" en une liste d'octets
    ping_data = [ord(c) for c in PING_CMD]
    print(f"\n[1] Envoi de la commande '{PING_CMD}' (WRITE) au STM32...")

    # ÉTAPE 1: RPi ÉCRIT (WRITE) -> Déclenche HAL_I2C_SlaveRxCpltCallback sur le STM32
    write_msg = smbus2.i2c_msg.write(STM32_ADDRESS, ping_data)
    bus.i2c_rdwr(write_msg)
    print("   -> Commande envoyée avec succès.")

    # Pause courte nécessaire pour s'assurer que le STM32 a eu le temps de finir
    # d'exécuter RxCpltCallback et de se réarmer pour la lecture (moins de 10ms suffisent).
    time.sleep(0.01)

    # ÉTAPE 2: RPi LIT (READ) -> Déclenche HAL_I2C_SlaveTxCpltCallback sur le STM32
    print(f"\n[2] Lecture de la réponse ({PONG_RSP_LEN} octets) du STM32 (READ)...")
    read_msg = smbus2.i2c_msg.read(STM32_ADDRESS, PONG_RSP_LEN)
    bus.i2c_rdwr(read_msg)

    # Convertir les octets lus en une chaîne de caractères
    response_bytes = list(read_msg)
    response_str = "".join([chr(b) for b in response_bytes])

    print(f"   -> Réponse reçue : '{response_str}'")

    if response_str == "PONG":
        print("\n✅ Succès : Le Ping-Pong I2C est fonctionnel !")
    else:
        print(f"\n❌ Échec de la vérification : Attendu 'PONG', reçu '{response_str}'.")

except FileNotFoundError:
    print("Erreur: Le bus I2C n'est pas activé. Vérifiez 'raspi-config'.")
    sys.exit(1)
except OSError as e:
    # IOError est souvent levé ici si le Pi ne reçoit pas d'ACK ou si le bus est bloqué.
    print(f"\n🛑 Erreur I2C : Le STM32 n'a pas répondu ou le bus est bloqué. ({e})")
    print("   -> Vérifiez les pull-ups et la connexion GND.")
    sys.exit(1)
except Exception as e:
    print(f"Une erreur inattendue est survenue : {e}")
    sys.exit(1)
finally:
    if 'bus' in locals():
        bus.close()import smbus2
import time
import sys

# --- Configuration I2C ---
# L'adresse configurée dans le STM32 (132 décimal = 0x42 hex)
STM32_ADDRESS = 0x42
BUS_NUMBER = 1        # Généralement 1 sur les Raspberry Pi récents
PING_CMD = "PING"     # Commande de 4 octets
PONG_RSP_LEN = 4      # Attente de 4 octets de réponse

# --- Initialisation ---
try:
    bus = smbus2.SMBus(BUS_NUMBER)
    print(f"Bus I2C {BUS_NUMBER} ouvert pour l'adresse 0x{STM32_ADDRESS:x}.")

    # Convertir la chaîne "PING" en une liste d'octets
    ping_data = [ord(c) for c in PING_CMD]
    print(f"\n[1] Envoi de la commande '{PING_CMD}' (WRITE) au STM32...")

    # ÉTAPE 1: RPi ÉCRIT (WRITE) -> Déclenche HAL_I2C_SlaveRxCpltCallback sur le STM32
    write_msg = smbus2.i2c_msg.write(STM32_ADDRESS, ping_data)
    bus.i2c_rdwr(write_msg)
    print("   -> Commande envoyée avec succès.")

    # Pause courte nécessaire pour s'assurer que le STM32 a eu le temps de finir
    # d'exécuter RxCpltCallback et de se réarmer pour la lecture (moins de 10ms suffisent).
    time.sleep(0.01)

    # ÉTAPE 2: RPi LIT (READ) -> Déclenche HAL_I2C_SlaveTxCpltCallback sur le STM32
    print(f"\n[2] Lecture de la réponse ({PONG_RSP_LEN} octets) du STM32 (READ)...")
    read_msg = smbus2.i2c_msg.read(STM32_ADDRESS, PONG_RSP_LEN)
    bus.i2c_rdwr(read_msg)

    # Convertir les octets lus en une chaîne de caractères
    response_bytes = list(read_msg)
    response_str = "".join([chr(b) for b in response_bytes])

    print(f"   -> Réponse reçue : '{response_str}'")

    if response_str == "PONG":
        print("\n✅ Succès : Le Ping-Pong I2C est fonctionnel !")
    else:
        print(f"\n❌ Échec de la vérification : Attendu 'PONG', reçu '{response_str}'.")

except FileNotFoundError:
    print("Erreur: Le bus I2C n'est pas activé. Vérifiez 'raspi-config'.")
    sys.exit(1)
except OSError as e:
    # IOError est souvent levé ici si le Pi ne reçoit pas d'ACK ou si le bus est bloqué.
    print(f"\n🛑 Erreur I2C : Le STM32 n'a pas répondu ou le bus est bloqué. ({e})")
    print("   -> Vérifiez les pull-ups et la connexion GND.")
    sys.exit(1)
except Exception as e:
    print(f"Une erreur inattendue est survenue : {e}")
    sys.exit(1)
finally:
    if 'bus' in locals():
        bus.close()