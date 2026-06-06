"""
fake_driver_station.py
─────────────────────
Script Python de test pour le firmware robot ESP32.

Permet de tester chaque commande du protocole sans avoir besoin
du vrai Driver Station du Groupe A.

Prérequis :
  - Ton PC doit être connecté au Wi-Fi "Robot-ESP32" (mot de passe : robot1234)
  - L'ESP32 doit être allumé et le firmware robot_esp32 téléversé

Lancement :
  python fake_driver_station.py
"""

import socket
import threading
import time

# ── Configuration ────────────────────────────────────────────────
ROBOT_IP   = "192.168.4.1"   # IP fixe du hotspot ESP32
ROBOT_PORT = 4210
LOCAL_PORT = 4211             # Port local pour recevoir les réponses
TIMEOUT    = 1.0              # secondes avant d'abandonner l'attente

# ── Socket UDP ───────────────────────────────────────────────────
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", LOCAL_PORT))
sock.settimeout(TIMEOUT)


# ── Récepteur de messages entrants (tourne en arrière-plan) ──────
incoming_messages = []
receiver_running  = True

def receiver_thread():
    """Reçoit en continu les messages ENCODERS et GYRO envoyés par le robot."""
    while receiver_running:
        try:
            data, _ = sock.recvfrom(1024)
            msg = data.decode()
            incoming_messages.append(msg)
        except socket.timeout:
            pass   # Normal, on reboucle

t = threading.Thread(target=receiver_thread, daemon=True)
t.start()


# ── Fonctions d'envoi ────────────────────────────────────────────
def send(message: str):
    """Envoie un message UDP au robot."""
    sock.sendto(message.encode(), (ROBOT_IP, ROBOT_PORT))


def send_and_wait(message: str) -> str:
    """Envoie un message et attend une réponse directe (ex : PING → PONG)."""
    # Vider la file des messages entrants
    incoming_messages.clear()
    send(message)
    deadline = time.time() + TIMEOUT
    while time.time() < deadline:
        if incoming_messages:
            return incoming_messages.pop(0)
        time.sleep(0.05)
    return "(pas de réponse)"


def drain_incoming() -> list[str]:
    """Retourne tous les messages reçus depuis le dernier appel."""
    time.sleep(0.3)   # Laisser le temps au robot de répondre
    msgs = list(incoming_messages)
    incoming_messages.clear()
    return msgs


# ── Menu interactif ──────────────────────────────────────────────
MENU = """
╔══════════════════════════════════════════╗
║        Fake Driver Station               ║
║  Robot : {ip}:{port:<5}              ║
╠══════════════════════════════════════════╣
║  1  →  PING (vérifier connexion)         ║
║  2  →  SET_MOTORS (toutes vitesses)      ║
║  3  →  SET_SERVOS (tous angles)          ║
║  4  →  Lire ENCODERS (1 cycle)           ║
║  5  →  Lire GYRO (1 cycle)              ║
║  6  →  Test automatique complet          ║
║  q  →  Quitter                           ║
╚══════════════════════════════════════════╝
""".format(ip=ROBOT_IP, port=ROBOT_PORT)


def test_ping():
    print("\n→ Envoi : PING")
    rep = send_and_wait("PING")
    print(f"← Reçu  : {rep}")


def test_set_motors():
    print("\nVitesses moteurs M0..M5 (-255 à +255)")
    values = []
    for i in range(6):
        v = input(f"  M{i} = ").strip() or "0"
        values.append(v)
    cmd = "SET_MOTORS:" + ",".join(values)
    print(f"\n→ Envoi : {cmd}")
    send(cmd)
    msgs = drain_incoming()
    for m in msgs:
        print(f"← Reçu  : {m}")


def test_set_servos():
    print("\nAngles servos S0..S2 (0 à 180°)")
    values = []
    for i in range(3):
        v = input(f"  S{i} = ").strip() or "90"
        values.append(v)
    cmd = "SET_SERVOS:" + ",".join(values)
    print(f"\n→ Envoi : {cmd}")
    send(cmd)
    msgs = drain_incoming()
    for m in msgs:
        print(f"← Reçu  : {m}")


def test_read_encoders():
    print("\n→ Envoi : SET_MOTORS:0,0,0,0,0,0 (pour déclencher un cycle)")
    send("SET_MOTORS:0,0,0,0,0,0")
    msgs = drain_incoming()
    encoders = [m for m in msgs if m.startswith("ENCODERS:")]
    if encoders:
        print(f"← Reçu  : {encoders[-1]}")
        values = encoders[-1].replace("ENCODERS:", "").split(",")
        for i, v in enumerate(values):
            print(f"   Encodeur {i} : {v} ticks")
    else:
        print("← Aucun message ENCODERS reçu")


def test_read_gyro():
    print("\n→ Envoi : SET_MOTORS:0,0,0,0,0,0 (pour déclencher un cycle)")
    send("SET_MOTORS:0,0,0,0,0,0")
    msgs = drain_incoming()
    gyros = [m for m in msgs if m.startswith("GYRO:")]
    if gyros:
        raw = int(gyros[-1].replace("GYRO:", ""))
        angle = raw / 10.0
        print(f"← Reçu  : {gyros[-1]}  →  {angle}°")
    else:
        print("← Aucun message GYRO reçu")


def test_auto():
    print("\n━━━ Test automatique complet ━━━")

    # PING
    print("\n[1/5] PING...")
    rep = send_and_wait("PING")
    ok = "✓" if rep == "PONG" else "✗"
    print(f"  {ok} PING → {rep}")

    # SET_MOTORS
    print("\n[2/5] SET_MOTORS:100,50,-100,-50,0,0 ...")
    send("SET_MOTORS:100,50,-100,-50,0,0")
    msgs = drain_incoming()
    enc = [m for m in msgs if m.startswith("ENCODERS:")]
    ok = "✓" if enc else "✗"
    print(f"  {ok} Encodeurs reçus : {enc[0] if enc else 'aucun'}")

    # SET_SERVOS
    print("\n[3/5] SET_SERVOS:90,45,135 ...")
    send("SET_SERVOS:90,45,135")
    time.sleep(0.2)
    print("  ✓ Commande envoyée (vérifie le Moniteur Série de l'ESP32)")

    # ENCODERS après arrêt
    print("\n[4/5] Arrêt moteurs + lecture encodeurs...")
    send("SET_MOTORS:0,0,0,0,0,0")
    msgs = drain_incoming()
    enc = [m for m in msgs if m.startswith("ENCODERS:")]
    print(f"  {'✓' if enc else '✗'} {enc[0] if enc else 'aucun encodeur'}")

    # GYRO
    print("\n[5/5] Lecture gyro...")
    gyros = [m for m in msgs if m.startswith("GYRO:")]
    if gyros:
        raw = int(gyros[-1].replace("GYRO:", ""))
        print(f"  ✓ Gyro : {raw / 10.0}°")
    else:
        print("  ✗ Aucun GYRO reçu")

    print("\n━━━ Test terminé ━━━")


# ── Boucle principale ────────────────────────────────────────────
def main():
    print(MENU)
    while True:
        choix = input("Ton choix : ").strip().lower()

        if   choix == "1": test_ping()
        elif choix == "2": test_set_motors()
        elif choix == "3": test_set_servos()
        elif choix == "4": test_read_encoders()
        elif choix == "5": test_read_gyro()
        elif choix == "6": test_auto()
        elif choix == "q":
            print("Au revoir !")
            break
        else:
            print("Choix non reconnu.")

        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nArrêt.")
    finally:
        receiver_running = False
        sock.close()
