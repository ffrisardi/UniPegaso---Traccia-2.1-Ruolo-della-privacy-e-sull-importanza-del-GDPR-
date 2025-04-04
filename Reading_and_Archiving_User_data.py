import os
import sqlite3
import pandas as pd

# Path del file Excel in cui vengono salvati i dati degli utenti
EXCEL_PATH = 'utenti.xlsx'
# Path del file del database
DB_PATH = 'utenti.db'

# Legge i dati da un file excel e li restituisce come dataframe
def read_data_from_excel(filename):
    # verifica se il file esiste
    if not os.path.exists(filename):
        print(f"Il file {filename} non esiste.")
        return pd.DataFrame()  # restituisce un dataframe vuoto se il file non esiste
    try:
        df = pd.read_excel(filename) #legge il file 
        return df
    except Exception as e:
        print(f"Errore durante la lettura del file Excel: {e}")
        return pd.DataFrame() # restituisce un dataframe vuoto in caso di errore
       
# Crea la tabella SQL per l'archiviazione dei dati
def create_sql_table(connection):

    # Crea la connessione e crea la tabella
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS utenti (
                UID TEXT PRIMARY KEY,
                Nome TEXT,
                Cognome TEXT,
                Email TEXT,
                Telefono TEXT
            )
        ''')
        connection.commit() # Salva le modifiche nel DB
    except Exception as e:
        raise e

# Inserisci i dati del dataframe nel DB SQL
def insert_data_to_sql(connection, dataframe):

    # Controlla che il dataframe non sia vuoto
    if not isinstance(dataframe, pd.DataFrame) or dataframe.empty:
        raise ValueError("Dati non validi o vuoti per l'inserimento nel database SQL.")
    # Per ogni record nel df, inserisce i dati di ogni utente nella tabella
    try:
        cursor = connection.cursor() #connessione
        for _, row in dataframe.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO utenti (UID, Nome, Cognome, Email, Telefono)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['UID'], row['Nome'], row['Cognome'], row['Email'], row['Telefono']))
        connection.commit()  # Salva le modifiche nel DB
    except Exception as e:
        raise e

# Visualizza i dati presenti nel DB in formato tabellare 
def display_db_data(connection):
    try:
        df = pd.read_sql_query("SELECT * FROM utenti ORDER BY nome", connection) # Esegue una query per leggere e ordinare i dati per 'nome'
        if df.empty: # Se vengono trovati i dati, vengono visualizzati
            print("Nessun dato presente nel DB.") 
        else:
            print(" ---------- Dati in 'utenti.db' ---------- ")
            print(df.to_string(index=False))  
        connection.close()
    except Exception as e:
        print("Errore durante la visualizzazione dei dati dal DB:", e)

# Legge i dati dal file excel, li carica nel DB e li visualizza.
def main():
    try:
        conn = sqlite3.connect(DB_PATH) #Apre la connessione al DB 
        create_sql_table(conn) # Crea la tabella
        df = read_data_from_excel(EXCEL_PATH)  # Legge i dati dal file Excel
        insert_data_to_sql(conn, df) # Inserisce i dati nel DB
        print("Dati caricati con successo sul DB ('utenti.db').")
        display_db_data(conn) # Visualizza i dati inseriti
        conn.close() # Chiude la connessione
    except Exception as e:
        print("Errore durante il caricamento dei dati:", e)

if __name__ == '__main__':
    main()