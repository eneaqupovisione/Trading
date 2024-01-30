from scipy.stats import skewnorm
import numpy as np
import random
import matplotlib.pyplot as plt
import csv
import tkinter as tk
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
#PARAMETRI 
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

def input_experiment_parameters():
    modalita_selezionata = scegli_modalita()

    if modalita_selezionata == "manuale":
        volume = Interfaccia("Seleziona il volume del portafoglio", 0, 10000, 1000, 100, "Volume del Portafoglio").run()
        min_bet = Interfaccia("Seleziona l'importo minimo della scommessa", 0, volume, 50, 1, "Importo Minimo Ad Operazione").run()
        max_bet = Interfaccia("Seleziona l'importo massimo della scommessa", min_bet, volume, max(min_bet, volume // 2), 1, "Importo Massimo Ad Operazione").run()
        num_experiments = Interfaccia("Indica il numero di esperimenti da eseguire", 0, 500000, 3000, 100, "Numero di Operazioni").run()
        mean_value = Interfaccia("Definisci la distribuzione di probabilità: Indica il valore medio", -1000, 1000, 0, 0.05, "Risultato Medio").run()
        #skew_value = Interfaccia("Indica il valore di Skewness",-50,50,-10,0.1, "Grado Di Asimmetria Della Distribuzione").run()
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
        #skew_value = scegli_profilo("skew_value", profili)
        std_deviation = scegli_profilo("std_deviation", profili)
        risk_reward_ratio = scegli_profilo("risk_reward_ratio", profili)
        max_loss_per_operation = scegli_profilo("max_loss_per_operation", profili)
        total_max_loss_value = scegli_profilo("total_max_loss_value", profili)
        final_goal = scegli_profilo("final_goal", profili)


    return (volume, min_bet, max_bet, num_experiments, mean_value, std_deviation, risk_reward_ratio, max_loss_per_operation, total_max_loss_value, final_goal )

def run_experiments(params):
    (portfolio_volume, bet_range_min, bet_range_max, num_experiments_max, mu, std_deviation, risk_reward_ratio, max_loss_per_operation, total_max_loss_value, final_goal) = params
    #(portfolio_volume, bet_range_min, bet_range_max, num_experiments_max, mu, sigma, win_percent, loss_percent, loss_limit, win_goal) = params

    total_profit = 0
    num_experiments, total_wins, total_losses = 0, 0, 0
    max_win_streak, max_loss_streak, win_streak, loss_streak = 0, 0, 0, 0
    stop_for_losses = portfolio_volume - total_max_loss_value
    stop_for_profits = portfolio_volume + final_goal
    profits, losses = 0, 0
    dynamic_tolerance = (portfolio_volume - stop_for_losses) * max_loss_per_operation / 100
    min_portfolio_value, max_portfolio_value = portfolio_volume, portfolio_volume
    num_of_profits, num_of_losses = 0, 0
    total_win_prob_sum = 0
    win_streak_lengths = []  
    loss_streak_lengths = []
    
    while num_experiments < num_experiments_max:
        bet_amount = round(random.uniform(bet_range_min, min(bet_range_max, portfolio_volume + total_profit)), 2)
        win_prob_log_normal = np.random.lognormal(mean=mu, sigma=std_deviation)
        win_prob = win_prob_log_normal / (1 + win_prob_log_normal)
        total_win_prob_sum += win_prob
        loss_amount = round(-bet_amount * max_loss_per_operation / 100, 2)
        win_amount = abs(risk_reward_ratio*loss_amount)
        result = np.random.choice([win_amount, loss_amount], p=[win_prob, 1 - win_prob])
        total_profit += result
        current_portfolio_value = portfolio_volume + total_profit
        min_portfolio_value = min(min_portfolio_value, current_portfolio_value)
        max_portfolio_value = max(max_portfolio_value, current_portfolio_value)
    

        if result > 0:
            profits +=result
            if loss_streak > 0:  # Se c'è stata una serie di perdite, aggiungila alla lista
                loss_streak_lengths.append(loss_streak)
                loss_streak = 0
            win_streak += 1
            num_of_profits += 1
            max_win_streak = max(max_win_streak, win_streak)
        else:
            losses+=result
            if win_streak > 0:  # Se c'è stata una serie di vittorie, aggiungila alla lista
                win_streak_lengths.append(win_streak)
                win_streak = 0
            loss_streak += 1
            num_of_losses += 1
            max_loss_streak = max(max_loss_streak, loss_streak)

        current_portfolio_value = portfolio_volume + total_profit
        

        if current_portfolio_value <= stop_for_losses + dynamic_tolerance:
            print("Limite di perdita raggiunto o quasi. Terminazione del programma.")
            break
        if current_portfolio_value >= stop_for_profits:
            print("Obiettivo di vincita raggiunto. Terminazione del programma.")
            break

        num_experiments += 1
        
    if win_streak > 0:
        win_streak_lengths.append(win_streak)
    if loss_streak > 0:
        loss_streak_lengths.append(loss_streak)

    
    average_win_streak_length = np.mean(win_streak_lengths) if win_streak_lengths else 0
    average_loss_streak_length = np.mean(loss_streak_lengths) if loss_streak_lengths else 0
    average_win_streak_length = np.mean(win_streak_lengths) if win_streak_lengths else 0
    average_loss_streak_length = np.mean(loss_streak_lengths) if loss_streak_lengths else 0
    win_percentage = (num_of_profits / num_experiments) * 100 if num_experiments > 0 else 0
    loss_percentage = (num_of_losses / num_experiments) * 100 if num_experiments > 0 else 0
    
    average_win_prob = total_win_prob_sum / num_experiments if num_experiments > 0 else 0

    net_max_loss= portfolio_volume-min_portfolio_value
    net_max_profit= max_portfolio_value-portfolio_volume
    net_result= abs(portfolio_volume-current_portfolio_value)
    ratio= abs((profits/losses)) if losses != 0 else 0 

    # Stampa delle statistiche
    
    print(f"Totale vincite: {profits:.2f}")
    print(f"Totale perdite: {losses:.2f}")
    print (f"Rapporto totale tra vincite e perdite: {ratio:.2f} (il volume delle vincite è {ratio:.2f} volte le perdite)")
    
    if net_result>0:
        print(f"Valore finale del portafoglio: {current_portfolio_value:.2f}, (+{net_result:.2f})")
    else:
        print(f"Valore finale del portafoglio: {current_portfolio_value:.2f}, (-{net_result:.2f})")
    print(f"Valore minimo del portafoglio raggiunto: {min_portfolio_value:.2f}, (-{net_max_loss:.2f})")
    print(f"Valore massimo del portafoglio raggiunto: {max_portfolio_value:.2f}, (+{net_max_profit:.2f})")
    
    print(f"Numero totale di esperimenti: {num_experiments}")
    print(f"Probabilità complessiva media di vincita: {(average_win_prob*100):.2f}%")
    print(f"Numero totale di vittorie: {num_of_profits}, (il {win_percentage:.2f}%)")
    print(f"Numero totale di perdite: {num_of_losses}, (il {loss_percentage:.2f}%)")
    
    print(f"Numero massimo di vittorie consecutive: {max_win_streak}")
    print(f"Numero massimo di sconfitte consecutive: {max_loss_streak}")
    print(f"Media delle lunghezze delle serie di vittorie consecutive: {average_win_streak_length:.2f}")
    print(f"Media delle lunghezze delle serie di perdite consecutive: {average_loss_streak_length:.2f}")
    
    

    # Sovrapposizione della curva di densità
    
   


# Esecuzione del programma
experiment_params = input_experiment_parameters()
if experiment_params:
    run_experiments(experiment_params)
else:
    print("Esperimento non eseguito a causa di input non validi.")
