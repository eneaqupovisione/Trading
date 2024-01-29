import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
import matplotlib.pyplot as plt
import csv
#-----------------------------------------------------------
#COSTRUZIONE DEL BOTTONE A COMPARSA
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

#-----------------------------------------------------------
#SEZIONE INIZIALE: SCELTA DELLA MODALITA DI INSERIMENTO DATI
def scegli_modalita():
    modalita = tk.Tk()
    modalita.title("Scegli Modalità di Inserimento")
    modalita.geometry("400x300")

    scelta = tk.StringVar(value="manuale")

    tk.Label(modalita, text="Seleziona la Modalità di Inserimento", font=("Arial", 14)).pack(pady=10)
    
    manuale_btn = tk.Radiobutton(modalita, text="Manuale", variable=scelta, value="manuale")
    manuale_btn.pack()
    createToolTip(manuale_btn, "Parametri inseriti manualmente")

    semiauto_btn = tk.Radiobutton(modalita, text="Semi-automatica", variable=scelta, value="semiauto")
    semiauto_btn.pack()
    createToolTip(semiauto_btn, "Parametri semplificati")

 
    conferma_btn = tk.Button(modalita, text="Conferma", command=lambda: conferma_scelta(modalita, scelta))
    conferma_btn.pack(pady=20)

    modalita.mainloop()
    return scelta.get()

def conferma_scelta(modalita, scelta):
    scelta_scelta = scelta.get()
    modalita.quit()
    modalita.destroy()
    return scelta_scelta

#-----------------------------------------------------------
#MODALITA MANUALE
class Interfaccia:
    def __init__(self, title, min_val, max_val, default_val, resolution, label):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("800x200+300+300")
        self.root.configure(bg='lightgray')

        self.slider_value = tk.DoubleVar(value=default_val)

        self.scale = tk.Scale(self.root, from_=min_val, to=max_val, resolution=resolution, orient='horizontal', length=700, variable=self.slider_value, label=label)
        self.scale.configure(bg='lightgray', fg='blue')
        self.scale.pack()

        self.entry = tk.Entry(self.root, textvariable=self.slider_value, width=20)
        self.entry.pack()

        self.button = tk.Button(self.root, text="Conferma", command=self.confirm)
        self.button.pack()

    def confirm(self):
        try:
            value = float(self.entry.get()) if self.entry.get() else self.slider_value.get()
            if self.validate(value):
                self.slider_value.set(value)
                self.root.quit()
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Errore", "Per favore inserisci un valore numerico valido.")
            self.entry.configure(fg='red')

    def validate(self, value):
        # Qui puoi aggiungere eventuali validazioni specifiche
        return True

    def run(self):
        self.root.mainloop()
        if self.root.winfo_exists():  
            self.root.destroy()
        return self.slider_value.get()
    
#-----------------------------------------------------------   
descrizioni_parametri = {
    "volume": "Volume del Portafoglio",
    "min_bet": "Importo Minimo Ad Operazione",
    "max_bet": "Importo Massimo Ad Operazione",
    "num_experiments": "Numero di Operazioni", 
    "mean_value": "Risultato Medio", 
    "skew_value": "Grado Di Asimettria Della Distribuzione", 
    "std_deviation": "Misura Della Dispersione Dei Dati", 
    "risk_reward_ratio": "Rapporto Tra Vincite e Perdite", 
    "max_loss_per_operation": "StopLoss Massimo Ad Operazione", 
    "total_max_loss_value": "Perdita Del Portafoglio Massima", 
    "final_goal": "Profitto Ambito"
}
#-----------------------------------------------------------
#MODALITA SEMIAUTOMATICA
def scegli_profilo(parametro, profili):
    finestra = tk.Tk()
    titolo_parametro = descrizioni_parametri.get(parametro, parametro)
    finestra.title(f"Seleziona {titolo_parametro}")
    finestra.geometry("400x300")

    scelta = tk.StringVar(value=list(profili[parametro].keys())[0])

    tk.Label(finestra, text=f"Seleziona {titolo_parametro}", font=("Arial", 14)).pack(pady=10)

    
    for opzione, valore in profili[parametro].items():
        rb = tk.Radiobutton(finestra, text=f"{opzione.capitalize()}: {valore}", variable=scelta, value=opzione, font=("Arial", 10))
        rb.pack()
        #createToolTip(rb, f"Informazioni su {titolo_parametro}: {valore}") # Aggiungi un tooltip per ogni Radiobutton

    conferma_btn = tk.Button(finestra, text="Conferma", command=lambda: conferma_scelta_profilo(finestra, scelta, profili, parametro))
    conferma_btn.pack(pady=20)

    finestra.mainloop()
    return profili[parametro][scelta.get()]

def conferma_scelta_profilo(finestra, scelta, profili, parametro):
    valore_scelto = profili[parametro][scelta.get()]
    finestra.quit()
    finestra.destroy()
    return valore_scelto


#-----------------------------------------------------------
# Definizione dei profili per la modalità semi-automatica
profili = {
    "volume": {
        "molto basso": 500,
        "basso": 1000,
        "medio": 2500,
        "alto": 5000,
        "molto alto":10000
    },
    "min_bet": {
        "molto basso": 10,
        "basso": 50,
        "medio": 150,
        "alto": 250,
        "molto alto":500
    },
    "max_bet": {
        "molto basso": 500,
        "basso": 1000,
        "medio": 2500,
        "alto": 5000,
        "molto alto":10000
    },
    "num_experiments": {
        "molto basso": 500,
        "basso": 1000,
        "medio": 5000,
        "alto": 50000,
        "molto alto":100000
    },
    "mean_value": {
        "estremamente basso":-100,
        "molto basso": -50,
        "basso": -15,
        "medio-basso":-3,
        "medio": 0,
        "medio-alto":3,
        "alto": 15,
        "molto alto":50,
        "estremamente alto":200
    },
    "skew_value": {
        "estremamente basso":-50,
        "molto basso": -17,
        "basso": -5,
        "medio-basso":-2.5,
        "medio": 0,
        "medio-alto":2.5,
        "alto": 5,
        "molto alto":17,
        "estremamente alto":50
    },
    "std_deviation": {
        "basso": 1,
        "medio": 5,
        "alto": 10
    },
    "risk_reward_ratio": {
        "estremamente basso":0.1,
        "molto basso": 0.3,
        "basso": 0.5,
        "medio-basso":1,
        "medio": 2,
        "medio-alto":3,
        "alto": 5,
        "molto alto":10,
        "estremamente alto":20
    },
    "max_loss_per_operation": {
        "estremamente basso":0.1,
        "molto basso": 0.3,
        "basso": 0.5,
        "medio-basso":1,
        "medio": 3,
        "medio-alto":9,
        "alto": 15,
        "molto alto":25,
        "estremamente alto":50
    },
    "total_max_loss_value": {
        "molto basso": 100,
        "basso": 500,
        "medio-basso":750,
        "medio": 1000,
        "medio-alto":2000,
        "alto": 5000,
        "molto alto":10000
    },
    "final_goal": {
        "molto basso": 100,
        "basso": 500,
        "medio-basso":750,
        "medio": 1000,
        "medio-alto":2000,
        "alto": 5000,
        "molto alto":10000
    }
}

#-----------------------------------------------------------
# Ottenere la modalità selezionata
modalita_selezionata = scegli_modalita()

# Blocco if-elif per determinare quale interfaccia mostrare

if modalita_selezionata == "manuale":
    volume = Interfaccia("Seleziona il volume del portafoglio", 0, 10000, 1000, 100, "Volume del Portafoglio").run()
    min_bet = Interfaccia("Seleziona l'importo minimo della scommessa", 0, volume, 50, 1, "Importo Minimo Ad Operazione").run()
    max_bet = Interfaccia("Seleziona l'importo massimo della scommessa", min_bet, volume, max(min_bet, volume // 2), 1, "Importo Massimo Ad Operazione").run()
    num_experiments = Interfaccia("Indica il numero di esperimenti da eseguire", 0, 500000, 3000, 100, "Numero di Operazioni").run()
    mean_value = Interfaccia("Definisci la distribuzione di probabilità: Indica il valore medio", -1000, 1000, 0, 0.05, "Risultato Medio").run()
    skew_value = Interfaccia("Indica il valore di Skewness",-50,50,-10,0.1, "Grado Di Asimmetria Della Distribuzione").run()
    std_deviation = Interfaccia("Indica la deviazione standard", 0, 100, 3, 0.05, "Deviazione Standard").run()
    risk_reward_ratio = Interfaccia("Indica il rapporto di rischio rendimento", 0, 100, 10, 0.01, "Rapporto Tra Vincite e Perdite").run()
    max_loss_per_operation = Interfaccia("Indica la massima perdita ad operazione accettata", 0.0, 100, 10, 0.01, "StopLoss Massimo Ad Operazione").run()
    total_max_loss_value = Interfaccia("Indica la massima perdita accettata", 0.0, volume, volume, 0.01, "Perdita Massima Del Portafoglio").run()
    final_goal = Interfaccia("Indica l'obiettivo desiderato", 0.0, 100000, volume, 0.01, "Goal").run()

elif modalita_selezionata == "semiauto":
    volume = scegli_profilo("volume", profili)
    min_bet = scegli_profilo("min_bet", profili)
    max_bet = scegli_profilo("max_bet", profili)
    num_experiments = scegli_profilo("num_experiments", profili)
    mean_value = scegli_profilo("mean_value", profili)
    skew_value = scegli_profilo("skew_value", profili)
    std_deviation = scegli_profilo("std_deviation", profili)
    risk_reward_ratio = scegli_profilo("risk_reward_ratio", profili)
    max_loss_per_operation = scegli_profilo("max_loss_per_operation", profili)
    total_max_loss_value = scegli_profilo("total_max_loss_value", profili)
    final_goal = scegli_profilo("final_goal", profili)
