"""
fake_driver_station_ble.py
──────────────────────────
Script Python de test pour le firmware Auriga (Mega 2560 + BLE Makeblock).
Remplace le Fake Driver Station UDP du module robot-firmware ESP32.

Protocole :
  → Envoyer des commandes texte via BLE WRITE (FFE3) : "SET_MOTORS:50,50,-50,-50\n"
  ← Recevoir des données capteurs via BLE NOTIFY (FFE2) : frames Makeblock binaires

Keepalive :
  Un watchdog côté firmware stoppe les moteurs si aucune commande n'arrive en 500 ms.
  Ce script envoie automatiquement les vitesses courantes toutes les 400 ms en arrière-plan,
  même pendant que tu tapes dans le menu.

Prérequis :
  pip install bleak

Lancement :
  python fake_driver_station_ble.py        ← menu interactif
  python fake_driver_station_ble.py scan   ← chercher l'adresse MAC
"""

import asyncio
import struct
import sys
from bleak import BleakClient, BleakScanner

# ── Configuration ────────────────────────────────────────────────
DEVICE_NAME = "Makeblock"               # Nom BLE affiché par l'Auriga
DEVICE_MAC  = "00:1B:10:FB:2D:E0"      # ← METS TON ADRESSE MAC ICI
                                        #   (python -m bleak pour la trouver)

NOTIFY_UUID = "0000ffe2-0000-1000-8000-00805f9b34fb"  # Arduino → Python
WRITE_UUID  = "0000ffe3-0000-1000-8000-00805f9b34fb"  # Python → Arduino

CONNECT_TIMEOUT = 10.0  # secondes


# ── Parseur Makeblock ────────────────────────────────────────────
class MakeblockParser:
    """Décode les frames binaires envoyées par l'Auriga."""

    TYPE_BYTE   = 1
    TYPE_FLOAT  = 2
    TYPE_SHORT  = 3
    TYPE_STRING = 4
    TYPE_LONG   = 6

    def __init__(self):
        self.buffer = bytearray()

    def feed(self, data: bytes):
        """Ajoute des données au buffer et retourne les valeurs décodées."""
        self.buffer.extend(data)
        results = []

        while len(self.buffer) >= 2:
            # Cherche l'en-tête [0xFF 0x55]
            if self.buffer[0] != 0xFF:
                self.buffer.pop(0)
                continue
            if self.buffer[1] != 0x55:
                self.buffer.pop(0)
                continue

            # En-tête trouvé — tente de décoder
            decoded, consumed = self._decode_frame(self.buffer[2:])
            if consumed is None:
                break  # Frame incomplète, attend plus de données
            self.buffer = self.buffer[2 + consumed:]
            results.extend(decoded)

        return results

    def _decode_frame(self, data: bytearray):
        """
        Décode les données après [FF 55].
        Retourne (liste_valeurs, nb_octets_consommés) ou ([], None) si incomplet.
        """
        offset  = 0
        results = []

        while offset < len(data):
            b = data[offset]

            if b == 0x0A:  # Fin de frame (newline)
                return results, offset + 1

            t = b
            offset += 1

            if t == self.TYPE_BYTE:
                if offset + 1 > len(data): return [], None
                results.append(("byte", data[offset]))
                offset += 1

            elif t == self.TYPE_FLOAT:
                if offset + 4 > len(data): return [], None
                v = struct.unpack_from('<f', data, offset)[0]
                results.append(("float", v))
                offset += 4

            elif t == self.TYPE_SHORT:
                if offset + 2 > len(data): return [], None
                v = struct.unpack_from('<h', data, offset)[0]
                results.append(("short", v))
                offset += 2

            elif t == self.TYPE_LONG:
                if offset + 4 > len(data): return [], None
                v = struct.unpack_from('<l', data, offset)[0]
                results.append(("long", v))
                offset += 4

            elif t == self.TYPE_STRING:
                if offset + 1 > len(data): return [], None
                n = data[offset]; offset += 1
                if offset + n > len(data): return [], None
                s = data[offset:offset + n].decode("utf-8", errors="replace")
                results.append(("string", s))
                offset += n

            else:
                # Type inconnu → ignore et cherche prochain en-tête
                return [], None

        return [], None  # Frame incomplète


# ── Fonction utilitaire ──────────────────────────────────────────
def encode_command(cmd: str) -> bytes:
    """Encode une commande texte en bytes pour l'envoi BLE."""
    return (cmd + "\n").encode("utf-8")


# ── Affichage des données capteurs ───────────────────────────────
def display_sensors(values):
    """Affiche les données capteurs décodées depuis une frame Makeblock."""
    labels = ["gyro(°)", "batt(%)", "enc0", "enc1", "enc2", "enc3"]
    line = ""
    for i, (dtype, val) in enumerate(values):
        label = labels[i] if i < len(labels) else f"val{i}"
        if dtype == "float":
            line += f"  {label}={val:.1f}"
        else:
            line += f"  {label}={val}"
    if line:
        print(f"← Capteurs :{line}")


# ── Fake Driver Station ──────────────────────────────────────────
async def run():
    print(f"\n{'═'*50}")
    print(f"  Fake Driver Station BLE — Auriga")
    print(f"  Connexion à : {DEVICE_MAC}")
    print(f"{'═'*50}\n")

    parser = MakeblockParser()
    last_values  = []

    # Vitesses courantes partagées avec la tâche keepalive
    current_speeds = [0, 0, 0, 0]
    keepalive_running = True

    def notification_handler(sender, data):
        nonlocal last_values
        decoded = parser.feed(bytes(data))
        if decoded:
            last_values = decoded
            display_sensors(decoded)

    async with BleakClient(DEVICE_MAC, timeout=CONNECT_TIMEOUT) as client:
        print(f"[✓] Connecté\n")

        await client.start_notify(NOTIFY_UUID, notification_handler)

        # ── Keepalive : envoie les vitesses courantes toutes les 400 ms ──
        # Sans ça, le watchdog du firmware stoppe les moteurs dès que le
        # menu attend une saisie (après ~500 ms de silence).
        async def keepalive():
            while keepalive_running:
                cmd = "SET_MOTORS:" + ",".join(str(s) for s in current_speeds)
                try:
                    await client.write_gatt_char(WRITE_UUID, encode_command(cmd))
                except Exception:
                    pass  # Connexion perdue → on laisse la boucle principale gérer
                await asyncio.sleep(0.4)

        keepalive_task = asyncio.create_task(keepalive())

        while True:
            print("""
┌─────────────────────────────────────────┐
│  1  →  PING                             │
│  2  →  SET_MOTORS (4 moteurs)           │
│  3  →  SET_SERVOS (3 servos)            │
│  4  →  STOP moteurs                     │
│  5  →  Afficher derniers capteurs       │
│  q  →  Quitter                          │
└─────────────────────────────────────────┘""")

            choice = await asyncio.get_event_loop().run_in_executor(
                None, lambda: input("Choix : ").strip()
            )

            if choice == "q":
                keepalive_running = False
                keepalive_task.cancel()
                # Sécurité : stoppe les moteurs avant de quitter
                await client.write_gatt_char(
                    WRITE_UUID, encode_command("SET_MOTORS:0,0,0,0")
                )
                break

            elif choice == "1":
                print("\n→ Envoi : PING")
                await client.write_gatt_char(WRITE_UUID, encode_command("PING"))
                await asyncio.sleep(0.5)

            elif choice == "2":
                print("\nVitesses moteurs M1..M4 (-255 à +255)")
                speeds = []
                for i in range(1, 5):
                    v = input(f"  M{i} = ").strip() or "0"
                    speeds.append(v)
                # Met à jour les vitesses courantes → le keepalive les envoie en boucle
                current_speeds[:] = [int(s) for s in speeds]
                cmd = "SET_MOTORS:" + ",".join(speeds)
                print(f"\n→ Envoi : {cmd}")
                await client.write_gatt_char(WRITE_UUID, encode_command(cmd))

            elif choice == "3":
                print("\nAngles servos S0..S2 (0 à 180°)")
                angles = []
                for i in range(3):
                    a = input(f"  S{i} = ").strip() or "90"
                    angles.append(a)
                cmd = "SET_SERVOS:" + ",".join(angles)
                print(f"\n→ Envoi : {cmd}")
                await client.write_gatt_char(WRITE_UUID, encode_command(cmd))

            elif choice == "4":
                current_speeds[:] = [0, 0, 0, 0]
                print("\n→ Envoi : SET_MOTORS:0,0,0,0")
                await client.write_gatt_char(
                    WRITE_UUID, encode_command("SET_MOTORS:0,0,0,0")
                )

            elif choice == "5":
                if last_values:
                    display_sensors(last_values)
                else:
                    print("(pas encore de données reçues)")

            else:
                print("Choix invalide")

        await client.stop_notify(NOTIFY_UUID)
        print("\n[✓] Déconnecté proprement")


# ── Scan BLE (aide pour trouver l'adresse MAC) ───────────────────
async def scan():
    print("Scan BLE en cours (5 secondes)...\n")
    devices = await BleakScanner.discover(timeout=5.0)
    found = [d for d in devices if d.name and "makeblock" in d.name.lower()]
    if found:
        print("Dispositifs Makeblock trouvés :")
        for d in found:
            print(f"  {d.address}  →  {d.name}")
    else:
        print("Aucun dispositif Makeblock trouvé.")
        print("Tous les dispositifs visibles :")
        for d in devices:
            print(f"  {d.address}  →  {d.name or '(sans nom)'}")


# ── Point d'entrée ───────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        asyncio.run(scan())
    else:
        asyncio.run(run())
