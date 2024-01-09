import datetime
import csv
import logging
import os

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Operazione:
    def __init__(self, operatore, volume, prezzo, take_profit, stop_loss, nome_asset):
        if volume <= 0 or prezzo <= 0 or take_profit <= 0 or stop_loss <= 0:
            raise ValueError("Volume, prezzo, take_profit e stop_loss devono essere maggiori di zero.")

        self.operatore = operatore
        self.volume = volume
        self.prezzo = prezzo
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.nome_asset = nome_asset
        self.timestamp = datetime.datetime.now()

    def calcola_percentuale_take_profit(self):
        differenza = abs(self.take_profit - self.prezzo)
        return (differenza / self.prezzo) * 100

    def calcola_percentuale_stop_loss(self):
        differenza = abs(self.prezzo - self.stop_loss)
        return (differenza / self.prezzo) * 100

    def rR(self):
        if self.stop_loss == 0:
            raise ValueError("Lo stop loss non può essere zero.")
        return self.take_profit / self.stop_loss

    def to_csv(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')},{self.volume},{self.prezzo},{self.calcola_percentuale_take_profit()},{self.calcola_percentuale_stop_loss()},{self.nome_asset}\n"

def salva_operazione_csv(operazione, filename=None):
    directory = "C:/Users/Enea/PythonScripts"
    if not os.path.exists(directory):
        os.makedirs(directory)

    if filename is None:
        timestamp_str = operazione.timestamp.strftime("%Y%m%d_%H%M")
        filename = f"{operazione.operatore}_{operazione.nome_asset}_{timestamp_str}.csv"
    full_path = os.path.join(directory, filename)

    campi = ['Timestamp', 'Volume', 'Prezzo', 'Percentuale Take Profit', 'Percentuale Stop Loss', 'Nome Asset']
    try:
        with open(full_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=campi)
            writer.writeheader()
            writer.writerow({
                'Timestamp': operazione.timestamp.strftime("%Y-%m-%d %H:%M"),
                'Volume': operazione.volume,
                'Prezzo': operazione.prezzo,
                'Percentuale Take Profit': operazione.calcola_percentuale_take_profit(),
                'Percentuale Stop Loss': operazione.calcola_percentuale_stop_loss(),
                'Nome Asset': operazione.nome_asset
            })
    except Exception as e:
        logging.error(f"Errore durante il salvataggio del file: {e}")

def input_numerico(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Per favore inserisci un valore numerico.")

def crea_operazione_da_input():
    operatore = input("Inserisci il nome dell'operatore: ")
    volume = input_numerico("Inserisci il volume: ")
    prezzo = input_numerico("Inserisci il prezzo: ")
    take_profit = input_numerico("Inserisci il take profit: ")
    stop_loss = input_numerico("Inserisci lo stop loss: ")
    nome_asset = input("Inserisci il nome dell'asset: ")

    try:
        return Operazione(operatore, volume, prezzo, take_profit, stop_loss, nome_asset)
    except ValueError as e:
        print(f"Errore nella creazione dell'operazione: {e}")
        return None

# Esempio d'uso
operazione = crea_operazione_da_input()
if operazione is not None:
    print("Operazione creata con successo!")
    salva_operazione_csv(operazione)
    print(f"Dettagli dell'operazione salvati in {operazione.operatore}_{operazione.nome_asset}_{operazione.timestamp.strftime('%Y%m%d_%H%M')}.csv")