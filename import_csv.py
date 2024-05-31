import mysql.connector
import csv
import logging
from datetime import datetime

db_config = {
    'host': "localhost",
    'user': "root",
    'password': "",
    'database': "wifi_analysis"
}

logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        logging.error(f"Erreur de connexion à la base de données : {err}")
        raise

def import_csv_to_db(csv_file):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        with open(csv_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            fieldnames = csv_reader.fieldnames
            print(f"Noms de colonnes trouvés : {fieldnames}")
            for row in csv_reader:
                try:
                   
                    session_associated_time = datetime.strptime(row['Session Associated Time'], '%d/%m/%Y %H:%M')
                    session_duration = int(row['Session Duration'].replace(',', ''))
                    client_mac = row['Client MAC Address']
                    host_name = row['Host Name']
                    device = row['Device']
                    os_type = row['OS Type']
                    upstream_transferred = int(row['Upstream Transferred (Bytes)'].replace(',', ''))
                    downstream_transferred = int(row['Downstream Transferred (Bytes)'].replace(',', ''))
                    ap_name = row['Connected AP Name']

                   
                    cursor.execute("INSERT INTO APs (ap_name) VALUES (%s) ON DUPLICATE KEY UPDATE ap_name=ap_name", (ap_name,))
                    cursor.execute("SELECT id FROM APs WHERE ap_name = %s", (ap_name,))
                    ap_id = cursor.fetchone()[0]

                    
                    cursor.execute("""
                        INSERT INTO Clients (client_mac, host_name, device, os_type)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            host_name = VALUES(host_name),
                            device = VALUES(device),
                            os_type = VALUES(os_type)
                    """, (client_mac, host_name, device, os_type))
                    cursor.execute("SELECT id FROM Clients WHERE client_mac = %s", (client_mac,))
                    client_id = cursor.fetchone()[0]

                    
                    cursor.execute("""
                        INSERT INTO Connections (
                            session_associated_time, session_duration, upstream_transferred,
                            downstream_transferred, ap_id, client_id
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """, (session_associated_time, session_duration, upstream_transferred, downstream_transferred, ap_id, client_id))

                except KeyError as e:
                    logging.error(f"Clé manquante dans le fichier CSV: {e}")
                    continue  
                except mysql.connector.Error as err:
                    logging.error(f"Erreur lors de l'insertion des données : {err}")
                    continue  

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Erreur lors de l'importation des données CSV : {e}")
        raise

import_csv_to_db('log_wifi_red_hot.csv')
