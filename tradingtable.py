#COSTRUZIONE DI UNA CLASSE 
class Trade:
    def __init__(self, timestamp, direzione, volume, prezzo, tp,  sl):
        self.timestamp = timestamp
        self.direzione = direzione
        self.volume = volume
        self.prezzo = prezzo
        self.tp = tp
        self.sl = sl
        
#------------------------------------------------------------------------------- 
#COSTRUZIONE DI METODI PER IL CALCOLO DI TP E SL
    
    def calculate_tp_percentage(self):
        """Calcola il T.P."""
        if self.prezzo != 0: 
            self.tp_percentuale = ((self.tp - self.prezzo) / self.prezzo)*100
        else:
            self.tp_percentuale = 0 
            
    def takeprofit_percentage(self):
        if self.direzione == "long":
            return ((self.tp - self.prezzo) / self.prezzo)*100 if self.prezzo !=0 else 0
        elif self.direzione == "short":
            return ((self.prezzo - self.tp) / self.prezzo)*100 if self.prezzo !=0 else 0

    def calculate_tp_euro_value(self):
        if self.direzione == "long":
            self.tp_euro = self.volume * (self.tp - self.prezzo)
        elif self.direzione == "short":
            self.tp_euro = self.volume * (self.prezzo - self.tp)
            
#------------------
    
    def calculate_sl_percentage(self):
        """Calcola lo S.L. """
        if self.prezzo != 0: 
            self.tp_percentuale = ((self.tp - self.prezzo) / self.prezzo) * 100
        else:
            self.tp_percentuale = 0 
    def stoploss_percentage(self):
        if self.direzione == "long":
            return ((self.tp - self.prezzo) / self.prezzo)*100 if self.prezzo !=0 else 0
        elif self.direzione == "short":
            return ((self.prezzo - self.tp) / self.prezzo)*100 if self.prezzo !=0 else 0

    def calculate_sl_euro_value(self):
        if self.direzione == "long":
            self.tp_euro = self.volume * (self.sl - self.prezzo)
        elif self.direzione == "short":
            self.tp_euro = self.volume * (self.prezzo - self.sl)
            
    #------------------------------------------------------------------------------- 
    def __str__(self):
        return (
        f"Trade Info:\n"
        f"Timestamp: {self.timestamp}\n"
        f"Direzione: {self.direzione}\n"
        f"Volume: {self.volume}\n"
        f"Prezzo: {self.prezzo}\n"
        f"T.P.: {self.tp}\n"
        f"S.L.: {self.sl}\n"
      

