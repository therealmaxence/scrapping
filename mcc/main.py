from spider.mcc_spyder import MCC_Spyder
from utils.db import DB


db = DB("./db/", "database.db")
if input("Do you want to reset/create the database ? (y/n) ") == 'y':
    db.executeFile("./db/schema.sql")

db.connect()
request = """INSERT INTO Topic (name) VALUES (?)"""
db.execute(request, ("Informatique",))
request = """INSERT INTO Certification (name) VALUES (?)"""
db.execute(request, ("IUT",))
db.conn.commit()
db.close()

db.connect()
spider = MCC_Spyder()
degrees = spider.getall_degree()
for degree in degrees:
    # Insert the degree into the database
    request = """INSERT INTO Degree (name, description, id_certification, id_topic) VALUES (?, ?, ?, ?)"""
    db.execute(request, (degree['formation'], "HOP", 1, 1),)
    # try:
    #     degree['mcc'] = spider.get_mcc_degree(degree['link'])
    # except Exception as e:
    #     print(f"Erreur lors de la récupération des données MCC pour {degree['formation']}: {e}")
    #     degree['mcc'] = None
db.conn.commit()
db.close()

# # Définir le chemin du dossier et du fichier
# dossier = "./mcc/result"
# fichier = os.path.join(dossier, "data.json")
# # Vérifier si le dossier existe, sinon le créer
# os.makedirs(dossier, exist_ok=True)
# # Écrire les données dans le fichier JSON
# with open(fichier, "w", encoding="utf-8") as f:
#     json.dump(degrees, f, ensure_ascii=False, indent=4)

# print(f"Fichier JSON créé : {fichier}")