import datetime
import csv
import logging
import os
import json

# Configurazione del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Classe Operazione
class Operazione:
    def __init__(self, operatore, nome_asset, tipo_operazione, volume, prezzo, take_profit, stop_loss):
        if volume <= 0 or prezzo <= 0 or take_profit <= 0 or stop_loss <= 0:
            raise ValueError("Volume, prezzo, take_profit e stop_loss devono essere maggiori di zero.")
        if tipo_operazione not in [1, -1]:
            raise ValueError("Tipo operazione deve essere 1 (long) o -1 (short).")

        self.operatore = operatore
        self.nome_asset = nome_asset
        self.tipo_operazione = tipo_operazione
        self.volume = volume
        self.prezzo = prezzo
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.timestamp = datetime.datetime.now()

    def calcola_percentuale_take_profit(self):
        differenza = abs(self.take_profit - self.prezzo)
        return (differenza / self.prezzo) * 100

    def calcola_percentuale_stop_loss(self):
        differenza = abs(self.prezzo - self.stop_loss)
        return (differenza / self.prezzo) * 100

    def to_dict(self):
        return {
            'operatore': self.operatore,
            'nome_asset': self.nome_asset,
            'tipo_operazione': self.tipo_operazione,
            'volume': self.volume,
            'prezzo': self.prezzo,
            'take_profit': self.take_profit,
            'stop_loss': self.stop_loss,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

    @classmethod
    def from_dict(cls, data):
        data['timestamp'] = datetime.datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
        return cls(**data)

# Funzioni per la gestione del file CSV
def salva_operazione_csv(operazione, filename=None):
    directory = "C:/Users/Enea/PythonScripts"
    if not os.path.exists(directory):
        os.makedirs(directory)
    tipo_op_str = "long" if operazione.tipo_operazione == 1 else "short"
    if filename is None:
        timestamp_str = operazione.timestamp.strftime("%Y%m%d_%H%M")
        filename = f"{operazione.operatore}_{tipo_op_str}_{operazione.nome_asset}_{timestamp_str}.csv"
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

# Funzioni per il salvataggio e il caricamento da JSON
def salva_operazione_json(operazione, filename):
    with open(filename, 'w') as file:
        json.dump(operazione.to_dict(), file)

def carica_operazione_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return Operazione.from_dict(data)

# Funzioni per gestire gli input dell'utente
def input_numerico(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Per favore inserisci un valore numerico.")

def conferma_risposta(messaggio):
    while True:
        risposta = input(messaggio).lower()
        if risposta in ['sì', 'si', 'yes']:
            return True
        elif risposta in ['no','nop','nope','nn']:
            return False
        else:
            print("Risposta non valida. Per favore rispondi con 'sì' o 'no'.")

def crea_operazione_da_input():
    operatore = input("Inserisci il nome dell'operatore: ")
    nome_asset = input("Inserisci il nome dell'asset: ")

    while True:
        tipo_input = input("Inserisci il tipo di operazione (long/short): ").lower()
        if tipo_input in ['long','l', 'lo', 'lon']:
            tipo_operazione = 1
            break
        elif tipo_input in ['short','s','sh','sho','shor']:
            tipo_operazione = -1
            break
        else:
            print("Per favore inserisci 'long' o 'short'.")

    volume = input_numerico("Inserisci il volume (in euro): ")
    prezzo = input_numerico("Inserisci il prezzo: ")

    while True:
        take_profit = input_numerico("Inserisci il take profit: ")
        if tipo_operazione == 1 and take_profit <= prezzo:
            print("Il livello di take profit deve essere maggiore del prezzo di ingresso per un'operazione long.")
        elif tipo_operazione == -1 and take_profit >= prezzo:
            print("Il livello di take profit deve essere minore del prezzo di ingresso per un'operazione short.")
        else:
            break

    while True:
        stop_loss = input_numerico("Inserisci lo stop loss: ")
        if tipo_operazione == 1 and stop_loss >= prezzo:
            print("Il livello di stop loss deve essere minore del prezzo di ingresso per un'operazione long.")
        elif tipo_operazione == -1 and stop_loss <= prezzo:
            print("Il livello di stop loss deve essere maggiore del prezzo di ingresso per un'operazione short.")
        else:
            break

    operazione = Operazione(operatore, nome_asset, tipo_operazione, volume, prezzo, take_profit, stop_loss)

    if conferma_risposta("Vuoi salvare questi dati? (sì/no): "):
        filename_json = input("Inserisci un nome per il file (es: PersonaggioUno): ") + ".json"
        salva_operazione_json(operazione, filename_json)
        print(f"Operazione salvata nel file {filename_json}")

    return operazione


def scegli_modalita():
    while True:
        risposta = input("Vuoi utilizzare la modalità 'Semi-Automatica' o 'Manuale'? Inserisci una risposta: ")

        if risposta in ['2','s','S','semi','Semi']:
            return 'Semi-Automatica'
        elif risposta in ['1','m','M','manual','Manual','manuale','Manuale']:
            return 'Manuale'
        else:
            print ("Risposta non valida. Riprova")





#--------------------------------------------------------------------------------------------
# Main
def main():
    modalita_scelta = scegli_modalita()
    print(f"Hai scelto la modalità {modalita_scelta}.")
    
    if modalita_scelta == 'Manuale':
        operazione = crea_operazione_da_input()
        if operazione is not None:
            print("Operazione creata con successo!")
            salva_operazione_csv(operazione)
            print(f"Dettagli dell'operazione salvati in CSV con nome {operazione.operatore}_{operazione.nome_asset}_{('long' if operazione.tipo_operazione == 1 else 'short')}_{operazione.timestamp.strftime('%d_%m_%Y_%H:%M')}.csv")
            print("Ecco delle valutazioni sull'operazione appena salvata:")
            print(f"Il rapporto di rischio-rendimento è pari a {operazione.calcola_percentuale_take_profit() / operazione.calcola_percentuale_stop_loss()}")
    else:
        print("ok")

if __name__ == "__main__":
    main()

