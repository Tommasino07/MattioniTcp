import socket

HOST = '127.0.0.1'  # IP del server (qui localhost)
PORT = 12345        # Porta del server

# Creo socket UDP per il client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Imposto un timeout di 2.5 secondi per la ricezione dell'ACK
client_socket.settimeout(2.5)

MAX_RETRIES = 5  # Numero massimo di tentativi di invio per ogni messaggio

for i in range(1, 11):  # Ciclo per mandare 10 messaggi numerati
    message = f"Ciao dal client! Messaggio #{i}"
    retries = 0

    while retries < MAX_RETRIES:
        print(f"[CLIENT] Invio: {message} (tentativo {retries + 1})")
        client_socket.sendto(message.encode(), (HOST, PORT))  # Invio messaggio UDP al server

        try:
            # Attendo la risposta (ACK) dal server
            data, addr = client_socket.recvfrom(1024)
            ack = data.decode()

            # Controllo se l'ACK ricevuto corrisponde esattamente al messaggio inviato
            if ack == f"ACK #{i}":
                print(f"[CLIENT] ACK corretto ricevuto per messaggio #{i}, passo al prossimo.")
                break  # Passo al messaggio successivo
            else:
                # Se l'ACK non corrisponde, lo ignoro e continuo ad aspettare o ritentare
                print(f"[CLIENT] ACK inatteso: {ack}, aspetto ancora.")
        except socket.timeout:
            # Se scade il timeout senza ricevere ACK, incremento il contatore tentativi
            retries += 1
            print(f"[CLIENT] Timeout: nessun ACK ricevuto, ritento ({retries}/{MAX_RETRIES})")

    else:
        # Se ho superato il numero massimo di tentativi senza ACK corretto, fermo il client
        print(f"[CLIENT] Fallito dopo {MAX_RETRIES} tentativi per messaggio #{i}, fermo il client.")
        break

# Chiudo il socket alla fine
client_socket.close()
print("[CLIENT] Client terminato.")