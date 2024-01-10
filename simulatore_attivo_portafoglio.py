import time

def leggi_storico(file_path):
    """Legge il valore corrente e lo storico delle operazioni dal file."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            valore_corrente = float(lines[0].strip())
            storico = [tuple(line.strip().split(", ")) for line in lines[1:]]
            storico = [(data, operazione, float(valore)) for data, operazione, valore in storico]
            return valore_corrente, storico
    except FileNotFoundError:
        return 0.0, []

def salva_valore_e_storico(file_path, valore, operazione, valore_operazione, storico):
    """Salva il nuovo valore e l'operazione nello storico nel file."""
    timestamp = time.strftime("%Y-%m-%d")
    nuova_operazione = (timestamp, operazione, float(valore_operazione))
    storico.append(nuova_operazione)

    with open(file_path, 'w') as file:
        file.write(f"{valore:.2f}\n")
        for operazione in storico:
            file.write(", ".join(map(str, operazione)) + '\n')

def aggiorna_valore(valore_iniziale):
    """Aggiorna il valore in base al numero inserito dall'utente."""
    valore_da_aggiungere = float(input("Inserisci il valore (usa il segno '-' per sottrarre): "))
    nuovo_valore = valore_iniziale + valore_da_aggiungere
    operazione = "Somma" if valore_da_aggiungere >= 0 else "Sottrazione"
    return nuovo_valore, operazione, valore_da_aggiungere

def mostra_operazioni_maggiori(storico):
    """Mostra le tre più grandi somme e le tre più grandi sottrazioni."""
    somme = [op for op in storico if op[1] == "Somma"]
    sottrazioni = [op for op in storico if op[1] == "Sottrazione"]

    somme_ordinate = sorted(somme, key=lambda x: x[2], reverse=True)
    sottrazioni_ordinate = sorted(sottrazioni, key=lambda x: x[2])

    print("Top 3 maggiori somme:")
    for operazione in somme_ordinate[:3]:
        print(f"{operazione[0]}: {operazione[1]} di {operazione[2]:.2f}")

    print("\nTop 3 maggiori sottrazioni:")
    for operazione in sottrazioni_ordinate[:3]:
        print(f"{operazione[0]}: {operazione[1]} di {abs(operazione[2]):.2f}")

def vuole_continuare():
    """Chiede all'utente se vuole continuare."""
    risposta = input("Vuoi continuare? (sì/no): ").strip().lower()
    if risposta in ['sì', 'si', 's', 'yes', 'y', 'ye', 'eys']:
        return True
    else:
        return False

file_path = "valore_salvato.txt"
valore_iniziale, storico = leggi_storico(file_path)

while True:
    print(f"Valore attuale: {valore_iniziale:.2f}")
    nuovo_valore, operazione, valore_operazione = aggiorna_valore(valore_iniziale)
    salva_valore_e_storico(file_path, nuovo_valore, operazione, valore_operazione, storico)

    print(f"Nuovo valore: {nuovo_valore:.2f}")

    if not vuole_continuare():
        break

    valore_iniziale = nuovo_valore

mostra_operazioni_maggiori(storico)

