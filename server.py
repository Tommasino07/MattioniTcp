import socket
import random
import time

HOST = '0.0.0.0'  # Accetta connessioni su tutte le interfacce di rete
PORT = 12345      # Porta su cui il server ascolta

# Creo un socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))  # Associo il socket all'indirizzo e porta specificati

print(f"[SERVER] In ascolto su {HOST}:{PORT}...")

# Set per tenere traccia degli ID dei messaggi già ricevuti (per gestire duplicati)
received_msgs = set()

# Contatori per statistiche
total_messages = 10
unique_received = 0     # Messaggi unici elaborati
duplicate_received = 0  # Messaggi duplicati ricevuti

while True:
    # Ricevo dati dal client, fino a 1024 byte
    data, addr = server_socket.recvfrom(1024)
    message = data.decode()
    print(f"[SERVER] Ricevuto da {addr}: {message}")

    # Estraggo l'ID del messaggio dal testo (assumo formato "Messaggio #n")
    try:
        msg_id = int(message.split('#')[1])
    except (IndexError, ValueError):
        msg_id = None  # Se non riesco ad estrarlo, metto None

    # Simulo perdita del messaggio con probabilità 30%
    if random.random() < 0.3:
        print(f"[SERVER] Messaggio scartato (simulazione perdita).")
        continue  # Non mando ACK, quindi il client non riceverà risposta

    # Controllo se è un messaggio duplicato
    if msg_id in received_msgs:
        duplicate_received += 1
        print(f"[SERVER] Messaggio duplicato #{msg_id} ricevuto, invio solo ACK.")
    else:
        unique_received += 1
        received_msgs.add(msg_id)  # Registro il messaggio come ricevuto
        print(f"[SERVER] Nuovo messaggio #{msg_id} elaborato.")

    # Ritardo casuale tra 0 e 5 secondi per simulare latenza di rete o elaborazione
    delay = random.uniform(0, 5)
    print(f"[SERVER] Ritardo di {delay:.2f} secondi prima di inviare ACK.")
    time.sleep(delay)

    # Invio ACK con ID del messaggio ricevuto (per enumerazione)
    ack_message = f"ACK #{msg_id}"
    server_socket.sendto(ack_message.encode(), addr)

    # Stampo riepilogo statistiche finora
    print(f"[SERVER] Messaggi unici ricevuti: {unique_received}/{total_messages} | Duplicati: {duplicate_received}\n")