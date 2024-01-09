import numpy as np
import csv
import random
import hashlib
import time

def simulate_bets(num_sets, num_bets, bet_range_min, bet_range_max, win_percent, loss_percent):
    detailed_results = []
    total_sum = 0
    total_loss = 0
    total_wins = 0
    negative_sets = 0
    weighted_win_prob_sum = 0

    for i in range(num_sets):
        win_prob = round(random.uniform(0.00001, 0.1), 2)
        weighted_win_prob_sum += win_prob * num_bets

        bets = []
        for _ in range(num_bets):
            bet_amount = round(random.uniform(bet_range_min, bet_range_max), 2)
            win_amount = round(bet_amount * win_percent, 2)
            loss_amount = round(-bet_amount * loss_percent, 2)
            result = np.random.choice([win_amount, loss_amount], p=[win_prob, 1 - win_prob])
            bets.append(result)

        set_sum = round(np.sum(bets), 2)
        set_mean = round(np.mean(bets), 2)
        detailed_results.append((i+1, win_prob, bets, set_sum, set_mean))
        total_sum += set_sum
        total_loss += round(np.sum([bet for bet in bets if bet < 0]), 2)
        total_wins += round(np.sum([bet for bet in bets if bet > 0]), 2)
        if set_sum < 0:
            negative_sets += 1

    average = round(total_sum / num_sets, 2)
    weighted_win_prob = round(weighted_win_prob_sum / (num_sets * num_bets), 2)
    return detailed_results, total_sum, average, negative_sets, total_loss, total_wins, weighted_win_prob

def write_to_csv(simulated_bets, total, average, negative_sets, total_loss, total_wins, weighted_win_prob):
    unique_hash = hashlib.md5(str(time.time()).encode()).hexdigest()
    file_name = f'scommesse_{unique_hash}.csv'

    try:
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Set', 'P', 'Res.', 'Sum', 'M'])
            for set_num, win_prob, bets, set_sum, set_mean in simulated_bets:
                writer.writerow([f'Set {set_num}', f'{win_prob:.2f}', bets, set_sum, set_mean])
            writer.writerow(['Totale Effettivo', '', '', total, ''])
            writer.writerow(['Media Complessiva', '', '', '', average])
            writer.writerow(['Set Negativi', '', '', '', negative_sets])
            writer.writerow(['Solo Perdite', '', '', '', total_loss])
            writer.writerow(['Solo Vincite', '', '', '', total_wins])
            writer.writerow(['Probabilità Media', '', '', '', f'{weighted_win_prob:.2f}'])
        print(f"I risultati sono stati salvati con successo in '{file_name}'.")
    except Exception as e:
        print(f"Si è verificato un errore durante la scrittura del file: {e}")

def input_parameters():
    try:
        num_sets = int(input("Inserisci il numero di set di scommesse da simulare: "))
        num_bets = int(input("Inserisci il numero di lanci per ogni set: "))
        bet_range_min = float(input("Inserisci l'importo minimo della scommessa: "))
        bet_range_max = float(input("Inserisci l'importo massimo della scommessa: "))
        win_percent = float(input("Inserisci la percentuale di vincita (es: 0.10 per 10%): "))
        loss_percent = float(input("Inserisci la percentuale di perdita (es: 0.03 per 3%): "))
        return num_sets, num_bets, bet_range_min, bet_range_max, win_percent, loss_percent
    except ValueError:
        print("Input non valido. Per favore inserisci valori numerici.")
        return None

parameters = input_parameters()

if parameters:
    num_sets, num_bets, bet_range_min, bet_range_max, win_percent, loss_percent = parameters
    simulated_bets, total, average, negative_sets, total_loss, total_wins, weighted_win_prob = simulate_bets(num_sets, num_bets, bet_range_min, bet_range_max, win_percent, loss_percent)
    
    for set_num, win_prob, bets, set_sum, set_mean in simulated_bets:
        print(f"Set {set_num}: P: {win_prob:.2f}, -> {bets}, Sum: {set_sum}, M: {set_mean}")

    print("\n")
    print(f"Numero di set con risultato negativo: {negative_sets} su {num_sets}")
    print(f"Totale Solo Perdite: {total_loss:.2f}")
    print(f"Totale Solo Vincite: {total_wins:.2f}")
    print(f"Totale effettivo dei {num_sets} set: {total:.2f}")
    print(f"Probabilità Media di Successo: {weighted_win_prob:.2f}")
    print(f"Media complessiva: {average}")

    write_to_csv(simulated_bets, total, average, negative_sets, total_loss, total_wins, weighted_win_prob)
else:
    print("Simulazione non eseguita a causa di input non validi.")





