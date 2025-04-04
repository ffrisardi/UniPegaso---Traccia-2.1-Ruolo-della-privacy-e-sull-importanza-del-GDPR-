# Import librerie
import sqlite3
import pandas as pd
from Reading_and_Archiving_User_data import create_sql_table
from Users_Data_Generator import generate_uid

# Nome del file del database
DB_PATH = 'utenti.db'


# Chiede all'utente un input numerico,  lo richiede nuovamente se non viene inserito un numero. Se valid_range è specificato, accetta solo valori in quell'intervallo
def get_numeric_input(prompt, valid_range):
    while True:
        scelta = input(prompt)
        try:
            scelta = int(scelta)
            if valid_range and scelta not in valid_range:
                print("Selezione non valida. Riprova.")
                continue
            return scelta
        except ValueError:
            print("Inserire un numero valido.")


# Inserisce un nuovo utente (record) all'interno del DB
def insert_user(connection):
    try:
        # Richiede all'utente i dati necessari per creare un nuovo utente
        nome = input("Inserisci il nome: ").strip()
        cognome = input("Inserisci il cognome: ").strip()
        email = input("Inserisci l'email: ").strip()
        telefono = input("Inserisci il telefono: ").strip()
        new_user = {        
                    'UID': generate_uid(), #Genera un UID
                    'Nome': nome,
                    'Cognome': cognome,
                    'Email': email,
                    'Telefono': telefono
                } 
        create_sql_table(connection) #Assicura che la tabella 'utenti' esista
        cursor = connection.cursor()
        # Inserisce il record dell'utente nel database
        cursor.execute('''  
            INSERT OR REPLACE INTO utenti (UID, Nome, Cognome, Email, Telefono)
            VALUES (?, ?, ?, ?, ?)
        ''', (new_user['UID'], new_user['Nome'], new_user['Cognome'], new_user['Email'], new_user['Telefono']))
        connection.commit() # Salva le modifiche
        sync_excel_with_db()  # Aggiorna il file Excel per mantenere i dati sincronizzati
        print("Nuovo utente inserito.")
    except Exception as e:
        print("Errore nell'inserimento del nuovo utente:", e)

# Aggiorna i dati di un utente già presente nel DB
def update_user(connection):
    try:
        cursor = connection.cursor()
        # Controlla che il record esiste
        uid = input("Inserisci l'UID dell'utente da modificare: ").strip()
        cursor.execute("SELECT COUNT(*) FROM utenti WHERE UID = ?", (uid,))
        if cursor.fetchone()[0] == 0:
           raise ValueError("User id non trovato.")
        # Richiede all'utente i dati da aggiornare
        print("Lasciare vuoto il campo se non si vuole modificarlo.") # Se il campo non deve essere aggiornato deve essere lasciato vuoto
        nuovo_nome = input("Nuovo nome: ").strip()
        nuovo_cognome = input("Nuovo cognome: ").strip()
        nuova_email = input("Nuova email: ").strip()
        nuovo_telefono = input("Nuovo telefono: ").strip()
        new_data = {}
        if nuovo_nome:
           new_data['Nome'] = nuovo_nome
        if nuovo_cognome:
            new_data['Cognome'] = nuovo_cognome
        if nuova_email:
            new_data['Email'] = nuova_email
        if nuovo_telefono:
             new_data['Telefono'] = nuovo_telefono
        if new_data:
            # Aggiorna i campi specificati
            for key, value in new_data.items():
                cursor.execute(f"UPDATE utenti SET {key} = ? WHERE UID = ?", (value, uid))
            connection.commit()
            print("Dati dell'utente aggiornati.")
            sync_excel_with_db() 
        else:
            print("Nessun dato da aggiornare.")
    except Exception as e:
        print("Errore nell'aggiornamento dei dati:", e)

def delete_user(connection):
    try:
        uid = input("Inserisci l'UID dell'utente da cancellare: ").strip()
        cursor = connection.cursor()
        # Verifica che il record esiste
        cursor.execute("SELECT COUNT(*) FROM utenti WHERE UID = ?", (uid,))
        if cursor.fetchone()[0] == 0:
            raise ValueError("User id non trovato.")
        # Esegue la cancellazione
        cursor.execute("DELETE FROM utenti WHERE UID = ?", (uid,))
        connection.commit()
        connection.close()
        sync_excel_with_db()
        print("Utente cancellato.")
    except Exception as e:
        print("Errore nella cancellazione dell'utente:", e)

# Esporta i dati dell'utente identificato da user_id in un file .csv
def export_user_data(connection):
    try:
        uid = input("Inserisci l'UID dell'utente da esportare: ").strip()
        output_csv = input("Inserisci il nome del file CSV di output (es. utente.csv): ").strip()
        df = pd.read_sql_query("SELECT * FROM utenti WHERE UID = ?", connection, params=(uid,))
        if df.empty:
            raise ValueError("User id non trovato.")
        df.to_csv(output_csv, index=False)
        connection.close()
        print(f"Dati esportati correttamente in {output_csv}")
    except Exception as e:
        print("Errore durante l'export dei dati:", e)


# Sincronizza il file excel con i dati presenti nel DB
def sync_excel_with_db(connection,filename):
    try:
        # Legge tutti i dati dalla tabella 'utenti'
        df = pd.read_sql_query("SELECT * FROM utenti", connection) 
        # Scrive i dati letti nel file excel, sovrascrivendo il contenuto esistente
        df.to_excel(filename, index=False) 
        print("Il file Excel è stato aggiornato dal DB.")
    except Exception as e:
        print("Errore durante la sincronizzazione da DB a Excel:", e)

    
# Menu relativo alla gestione dei dati del DB che consentono operazioni di Inserimento, Modifica, Cancellazione, Esportazione
def data_management_menu():
    while True:
        print("\n--- Gestione Dati Utente ---")
        print("1. Inserisci nuovo utente")
        print("2. Modifica utente")
        print("3. Cancella utente")
        print("4. Esporta dati utente in .csv")
        print("5. Esci")
        scelta = get_numeric_input("Inserire scelta: ", valid_range=range(1, 6))
        
        if scelta == 1:
            try:
                conn = sqlite3.connect(DB_PATH) #Apre la connessione al DB 
                insert_user(conn) 
                conn.close() # Chiude la connessione          
            except Exception as e:
                print("Errore nell'inserimento del nuovo utente:", e)
        elif scelta == 2:
            try:
                conn = sqlite3.connect(DB_PATH) #Apre la connessione al DB 
                update_user(conn)
                conn.close() # Chiude la connessione
            except Exception as e:
                print("Errore nell'aggiornamento dei dati:", e) 
        elif scelta == 3:
            try: 
                conn = sqlite3.connect(DB_PATH) #Apre la connessione al DB 
                delete_user(conn)
                conn.close() # Chiude la connessione
            except Exception as e:
                print("Errore nella cancellazione dell'utente:", e)
        elif scelta == 4:
            try:
                conn = sqlite3.connect(DB_PATH) #Apre la connessione al DB 
                export_user_data(conn)
                conn.close() # Chiude la connessione
            except Exception as e:
                print("Errore durante l'export dei dati:", e)
        elif scelta == 5:
            print("Uscita dall'applicazione.")
            break

# MAIN
def main():
    data_management_menu()
      
if __name__ == '__main__':
    main()
