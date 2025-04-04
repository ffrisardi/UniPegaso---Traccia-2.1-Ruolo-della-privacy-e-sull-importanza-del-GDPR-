import os
import random
import string 
import pandas as pd  
from faker import Faker
from Reading_and_Archiving_User_data import read_data_from_excel

# Istanza di Faker per la lingua italiana
FAKER = Faker('it_IT')
# Numero di utenti da generare
N_USERS = 10
# Path del file Excel in cui vengono salvati i dati degli utenti
EXCEL_PATH = 'utenti.xlsx'


# Genera un identificativo alfanumerico univoco di 5 caratteri 
def generate_uid():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# Genera dati casuali per n_users e resituisce una lista di dizionari
def generate_user_data(n_users):
    if n_users <= 0: # Verifica che il numero degli utenti sia maggiore di 0
        raise ValueError("Il numero di utenti deve essere maggiore di 0")
    
    user_list = []
    #Per ogni utente, genera un dizionario con UID, nome, cognome, email e telefono
    for _ in range(n_users):
        user = {
            'UID': generate_uid(),
            'Nome': FAKER.first_name(), # Nome casuale
            'Cognome': FAKER.last_name(), # Cognome casuale
            'Email': FAKER.email(), # Email casuale
            'Telefono': FAKER.phone_number() # Numero di telefono casuale
        }
        user_list.append(user)
    return user_list

# Salva i dati in un file Excel; Se il file esiste già, aggiunge i nuovi dati a quelli esistenti
def save_data_to_excel(data, filename):

    # Verifica che 'data' non sia una lista vuota
    if not isinstance(data, list) or not data:
        raise ValueError("Dati non validi per il salvataggio")
    
    # Crea un dataFrame con i nuovi dati
    new_df = pd.DataFrame(data)
    
    # Se il file esiste già, legge i dati esistenti e unisce i nuovi
    if os.path.exists(filename):
        try:
            df_existing = pd.read_excel(filename)
            df_combined = pd.concat([df_existing, new_df], ignore_index=True)
        except Exception as e:
            raise Exception(f"Errore durante la lettura del file Excel esistente: {e}")
    else:
        df_combined = new_df # Altrimenti salva solo i nuovi dati 

    # Salva il dataframe nel file excel 
    try:
        df_combined.to_excel(filename, index=False)
    except Exception as e:
        raise Exception(f"Errore durante il salvataggio dei dati in Excel: {e}")
    
# Visualizza i dati contenuti nel file Excel in formato tabellare
def display_excel_data(filename):
    try:
        df = read_data_from_excel(filename) # Legge i dati dal file excel
        if df.empty:
            print("Nessun dato presente nel file Excel.")
        else:
            print(" ---------- Dati in 'utenti.xlsx' ---------- ")
            print(df.to_string(index=False)) # 
    except Exception as e:
        print("Errore durante la visualizzazione dei dati dal file Excel:", e)    
    
# Genera dati casuali per N_USERS e li salva in un file excel 
def main():
    try:
        # Genera i dati per N_USERS utenti
        dati_utenti = generate_user_data(N_USERS)
        # Salva i dati generati nel file Excel
        save_data_to_excel(dati_utenti, EXCEL_PATH)
        print("Dati generati e salvati in 'utenti.xlsx'.")
    except Exception as e:
        print("Errore durante la generazione e il caricamento dei dati:", e)

if __name__ == '__main__':
    main()