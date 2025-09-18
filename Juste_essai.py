import csv
import json
import os
import uuid
from datetime import datetime

# ---------------------------
# Utilitaires
# ---------------------------

def now_iso():
    """Retourne la date et l'heure actuelle au format ISO."""
    return datetime.utcnow().isoformat()

def gen_id():
    """Génère un identifiant unique."""
    return str(uuid.uuid4())

def safe_read_json(path):
    """Charge un fichier JSON de manière sécurisée."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print(f"Impossible de lire le fichier JSON : {path} .")
        return []

def safe_write_json(path, data):
    """Crée un fichier JSON de manière sécurisée."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError:
        print(f"Échec d'écriture du fichier JSON : {path}")

def safe_read_csv(path, fieldnames):
    """Charge un fichier CSV de manière sécurisée."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            result = []
            for row in reader:
                r = {k: row.get(k, "") for k in fieldnames}
                result.append(r)
            return result
    except Exception as e:
        print(f"Impossible de lire le fichier CSV {path}, l'erreur : {e}")
        return []

def safe_write_csv(path, fieldnames, rows):
    """Crée un fichier CSV de manière sécurisée."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except Exception as e:
        print(f"Impossible d'écrire le CSV {path} : {e}")

def to_int(val, default=0):
    """Convertit une valeur en entier ou retourne une valeur par défaut."""
    try:
        return int(val)
    except Exception:
        return default

def to_float(val, default=0.0):
    """Convertit une valeur en flottant ou retourne une valeur par défaut."""
    try:
        return float(val)
    except Exception:
        return default

# ---------------------------
# Classes
# ---------------------------

class Category:
    JSON_FILE = "les_categories.json"

    def __init__(self, id=None, name="", description="", created_at=None):
        self.id = id or gen_id()
        self.name = name
        self.description = description
        self.created_at = created_at or now_iso()

    @staticmethod
    def _charger_categories():
        return safe_read_json(Category.JSON_FILE)

    @staticmethod
    def categorie_existe(category_id_or_name):
        categories = Category._charger_categories()
        for cat in categories:
            if (cat.get("ID", "").strip().lower() == category_id_or_name.strip().lower() or
                cat.get("name", "").strip().lower() == category_id_or_name.strip().lower()):
                return True
        return False

    def ajouter_categorie(self):
        if not self.name:
            print("L'ajout nécessite au minimum un nom de catégorie.")
            return
        categories = Category._charger_categories()
        for c in categories:
            if c.get("ID", "").strip().lower() == self.id.strip().lower() or \
                c.get("name", "").strip().lower() == self.name.strip().lower():
                print("Cette catégorie existe déjà.")
                return
        categories.append({
            "ID": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at
        })
        safe_write_json(Category.JSON_FILE, categories)
        print("Catégorie ajoutée avec succès.")

    @staticmethod
    def lecture_categories():
        categories = Category._charger_categories()
        if not categories:
            print("Aucune catégorie enregistrée.")
            return
        print("\nListe des catégories :")
        for c in categories:
            print(c)

    @staticmethod
    def modifier_categorie(nom, **modifications):
        categories = Category._charger_categories()
        modifie = False
        for c in categories:
            if c.get("name", "").strip().lower() == nom.strip().lower():
                for champ, valeur in modifications.items():
                    if champ in c:
                        c[champ] = str(valeur)
                        modifie = True
        if modifie:
            safe_write_json(Category.JSON_FILE, categories)
            print(f"Catégorie '{nom}' modifiée avec succès.")
        else:
            print(f"Aucun champ valide modifié pour la catégorie '{nom}'.")

    @staticmethod
    def supprimer_categorie(nom_categorie):
        categories = Category._charger_categories()
        nouvelle_liste = [c for c in categories if c.get("name", "").strip().lower() != nom_categorie.strip().lower()]
        if len(categories) == len(nouvelle_liste):
            print(f"La catégorie '{nom_categorie}' n'existe pas.")
            return
        safe_write_json(Category.JSON_FILE, nouvelle_liste)
        print(f"Catégorie '{nom_categorie}' supprimée avec succès.")

# Classe Fournisseur

class Fournisseur:
    JSON_FILE = "les_fournisseurs.json"

    def __init__(self, id=None, name="", phone="", email="", address="", created_at=None):
        self.id = id or gen_id()
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.created_at = created_at or now_iso()

    @staticmethod
    def _charger_fournisseurs():
        return safe_read_json(Fournisseur.JSON_FILE)

    @staticmethod
    def fournisseur_existe(id_or_name):
        fournisseurs = Fournisseur._charger_fournisseurs()
        for f in fournisseurs:
            if (f.get("ID", "").strip().lower() == id_or_name.strip().lower() or
                f.get("name", "").strip().lower() == id_or_name.strip().lower()):
                return True
        return False

    def ajouter_fournisseur(self):
        if not self.name:
            print("L'ID et le nom du fournisseur sont requis (au moins le nom).")
            return
        fournisseurs = Fournisseur._charger_fournisseurs()
        for f in fournisseurs:
            if f.get("ID", "").strip().lower() == self.id.strip().lower() or \
                f.get("name", "").strip().lower() == self.name.strip().lower():
                print("Ce fournisseur existe déjà.")
                return
        fournisseurs.append({
            "ID": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "created_at": self.created_at
        })
        safe_write_json(Fournisseur.JSON_FILE, fournisseurs)
        print("Fournisseur ajouté avec succès.")

    @staticmethod
    def lecture_fournisseurs():
        fournisseurs = Fournisseur._charger_fournisseurs()
        if not fournisseurs:
            print("Aucun fournisseur enregistré.")
            return
        print("\nListe des fournisseurs :")
        for f in fournisseurs:
            print(f)

    @staticmethod
    def modifier_fournisseur(nom, **modifications):
        fournisseurs = Fournisseur._charger_fournisseurs()
        modifie = False
        for f in fournisseurs:
            if f.get("name", "").strip().lower() == nom.strip().lower() or \
               f.get("ID", "").strip().lower() == nom.strip().lower():
                for champ, valeur in modifications.items():
                    if champ in f:
                        f[champ] = str(valeur)
                        modifie = True
        if modifie:
            safe_write_json(Fournisseur.JSON_FILE, fournisseurs)
            print(f"Fournisseur '{nom}' modifié avec succès.")
        else:
            print(f"Aucun champ valide modifié pour le fournisseur '{nom}'.")

    @staticmethod
    def supprimer_fournisseur(nom_fournisseur):
        fournisseurs = Fournisseur._charger_fournisseurs()
        nouvelle_liste = [f for f in fournisseurs if f.get("name", "").strip().lower() != nom_fournisseur.strip().lower()]
        if len(fournisseurs) == len(nouvelle_liste):
            print(f"Le fournisseur '{nom_fournisseur}' n'existe pas.")
            return
        safe_write_json(Fournisseur.JSON_FILE, nouvelle_liste)
        print(f"Fournisseur '{nom_fournisseur}' supprimé avec succès.")

# Classe Product

class Product:
    CSV_FILE = "gestion_inventaire.csv"
    FIELDNAMES = ["ID", "name", "description", "category_id", "supplier_id",
                "price", "cost", "quantity", "min_quantity", "SKU", "created_at", "updated_at"]

    def __init__(self, id=None, name="", description="", category_id="", supplier_id="", price=0.0, cost=0.0,
                quantity=0, min_quantity=0, SKU="", created_at=None, updated_at=None):
        self.id = id or gen_id()
        self.name = name
        self.description = description
        self.category_id = category_id
        self.supplier_id = supplier_id
        self.price = float(price) if price != "" else 0.0
        self.cost = float(cost) if cost != "" else 0.0
        self.quantity = int(quantity) if str(quantity).isdigit() else to_int(quantity, 0)
        self.min_quantity = int(min_quantity) if str(min_quantity).isdigit() else to_int(min_quantity, 0)
        self.SKU = SKU
        self.created_at = created_at or now_iso()
        self.updated_at = updated_at or now_iso()

    @staticmethod
    def _charger_produits():
        return safe_read_csv(Product.CSV_FILE, Product.FIELDNAMES)

    def ajouter_produit(self):
        """Ajoute un produit à la gestion de l'inventaire."""
        if not self.name:
            print("Le nom du produit est requis.")
            return
        if self.category_id and not Category.categorie_existe(self.category_id):
            print(f"La catégorie '{self.category_id}' n'existe pas. Ajoutez-la d'abord ou laissez vide.")
            return

        produits = Product._charger_produits()
        for p in produits:
            if p.get("ID", "").strip().lower() == self.id.strip().lower():
                print(f"Un produit avec l'ID '{self.id}' existe déjà.")
                return
            if p.get("SKU", "").strip().lower() == self.SKU.strip().lower() and self.SKU:
                print(f"Un produit avec le SKU '{self.SKU}' existe déjà.")
                return

        row = {
            "ID": self.id,
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id,
            "supplier_id": self.supplier_id,
            "price": str(self.price),
            "cost": str(self.cost),
            "quantity": str(self.quantity),
            "min_quantity": str(self.min_quantity),
            "SKU": self.SKU,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        produits.append(row)
        safe_write_csv(Product.CSV_FILE, Product.FIELDNAMES, produits)
        print("Produit ajouté avec succès ! (ID généré : {})".format(self.id))

    @staticmethod
    def lister_produits():
        """Liste tous les produits enregistrés."""
        produits = Product._charger_produits()
        if not produits:
            print("Aucun produit enregistré.")
            return
        print("\nListe des produits :")
        for i, ligne in enumerate(produits, start=1):
            print(f"{i}: {ligne}")

    @staticmethod
    def rechercher_produit(a_rechercher):
        """Recherche un produit par ID, nom ou SKU."""
        produits = Product._charger_produits()
        for ligne in produits:
            if (
                a_rechercher.strip().lower() == ligne.get("ID", "").strip().lower() or
                a_rechercher.strip().lower() == ligne.get("name", "").strip().lower() or
                a_rechercher.strip().lower() == ligne.get("SKU", "").strip().lower()
            ):
                print(f"Produit trouvé : {ligne}")
                return
        print("Aucun produit trouvé.")

    @staticmethod
    def modifier_produit(name_or_id, **modifications):
        """Modifie un produit existant."""
        produits = Product._charger_produits()
        modifie = False
        for ligne in produits:
            if (ligne.get("name", "").strip().lower() == name_or_id.strip().lower() or
                ligne.get("ID", "").strip().lower() == name_or_id.strip().lower()):
                for champ, valeur in modifications.items():
                    if champ in ligne:
                        if champ in ("quantity", "min_quantity"):
                            ligne[champ] = str(to_int(valeur, to_int(ligne[champ], 0)))
                        elif champ in ("price", "cost"):
                            ligne[champ] = str(to_float(valeur, to_float(ligne[champ], 0.0)))
                        else:
                            ligne[champ] = str(valeur)
                        modifie = True
                if modifie:
                    ligne["updated_at"] = now_iso()
        if modifie:
            safe_write_csv(Product.CSV_FILE, Product.FIELDNAMES, produits)
            print(f"Produit '{name_or_id}' modifié avec succès.")
        else:
            print(f"Aucun champ valide modifié pour le produit '{name_or_id}'.")

    @staticmethod
    def supprimer_produit(nom_produit):
        """Supprime un produit de l'inventaire."""
        produits = Product._charger_produits()
        nouvelle_liste = [p for p in produits if p.get("name", "").strip().lower() != nom_produit.strip().lower()]
        if len(produits) == len(nouvelle_liste):
            print(f"Produit '{nom_produit}' introuvable.")
            return
        safe_write_csv(Product.CSV_FILE, Product.FIELDNAMES, nouvelle_liste)
        print(f"Produit '{nom_produit}' supprimé avec succès.")

    @staticmethod
    def produits_par_categorie(category_name_or_id):
        """Affiche les produits d'une catégorie donnée."""
        produits = Product._charger_produits()
        if not produits:
            print("Aucun produit enregistré.")
            return
        trouve = False
        print(f"\nProduits de la catégorie '{category_name_or_id}' :")
        for ligne in produits:
            if ligne.get("category_id", "").strip().lower() == category_name_or_id.strip().lower():
                print(ligne)
                trouve = True
        if not trouve:
            print("Aucun produit trouvé dans cette catégorie.")

    @staticmethod
    def produits_par_fournisseur(fournisseur_name_or_id):
        """Affiche les produits d'un fournisseur donné."""
        produits = Product._charger_produits()
        if not produits:
            print("Aucun produit enregistré.")
            return

        fournisseurs = Fournisseur._charger_fournisseurs()
        fournisseur_id = fournisseur_name_or_id
        for f in fournisseurs:
            if f.get("name", "").strip().lower() == fournisseur_name_or_id.strip().lower():
                fournisseur_id = f.get("ID", "")
                break

        trouve = False
        print(f"\nProduits du fournisseur '{fournisseur_name_or_id}' :")
        for ligne in produits:
            if ligne.get("supplier_id", "").strip().lower() == fournisseur_id.strip().lower():
                print(ligne)
                trouve = True
        if not trouve:
            print("Aucun produit trouvé pour ce fournisseur.")

    @staticmethod
    def produits_stock_faible():
        """Affiche les produits en rupture ou avec un stock faible."""
        produits = Product._charger_produits()
        if not produits:
            print("Aucun produit enregistré.")
            return
        print("\nProduits en rupture ou stock faible :")
        trouve = False
        for ligne in produits:
            try:
                if int(ligne.get("quantity", "0")) <= int(ligne.get("min_quantity", "0")):
                    print(ligne)
                    trouve = True
            except ValueError:
                continue
        if not trouve:
            print("Aucun produit en rupture ou stock faible.")

# Classe StockManager

class StockManager:
    HISTORIQUE_FILE = "historique_mouvements.json"

    @staticmethod
    def _charger_historique():
        return safe_read_json(StockManager.HISTORIQUE_FILE)

    @staticmethod
    def _sauver_historique(historique):
        safe_write_json(StockManager.HISTORIQUE_FILE, historique)

    @staticmethod
    def mise_a_jour_stock(nom_produit_or_id, quantite, type_mouvement):
        """Met à jour le stock d'un produit."""
        produits = Product._charger_produits()
        modifie = False
        for p in produits:
            if (p.get("name", "").strip().lower() == nom_produit_or_id.strip().lower() or
                p.get("ID", "").strip().lower() == nom_produit_or_id.strip().lower()):
                try:
                    ancienne_qte = int(p.get("quantity", "0"))
                except ValueError:
                    ancienne_qte = 0
                q = to_int(quantite, 0)
                if type_mouvement == "ajout":
                    nouvelle_qte = ancienne_qte + q
                elif type_mouvement == "retrait":
                    nouvelle_qte = max(0, ancienne_qte - q)
                else:
                    print("Type de mouvement inconnu (ajout/retrait).")
                    return

                p["quantity"] = str(nouvelle_qte)
                p["updated_at"] = now_iso()
                historique = StockManager._charger_historique()
                historique.append({
                    "timestamp": now_iso(),
                    "produit": p.get("name", ""),
                    "produit_id": p.get("ID", ""),
                    "mouvement": type_mouvement,
                    "quantite": q,
                    "ancienne_qte": ancienne_qte,
                    "nouvelle_qte": nouvelle_qte
                })
                StockManager._sauver_historique(historique)
                modifie = True
        if modifie:
            safe_write_csv(Product.CSV_FILE, Product.FIELDNAMES, produits)
            print("Stock mis à jour avec succès.")
        else:
            print(f"Produit '{nom_produit_or_id}' introuvable.")

    @staticmethod
    def consulter_historique():
        """Consulte l'historique des mouvements de stock."""
        h = StockManager._charger_historique()
        if not h:
            print("Aucun mouvement enregistré.")
            return
        print("\nHistorique des mouvements :")
        for e in h:
            print(e)

    @staticmethod
    def valorisation_totale():
        """Calcule et affiche la valeur totale du stock."""
        produits = Product._charger_produits()
        total = 0.0
        for p in produits:
            try:
                total += int(p.get("quantity", "0")) * float(p.get("cost", "0.0"))
            except Exception:
                continue
        print(f"Valeur totale du stock : {total:.2f}")

# ---------------------------
# Menus
# ---------------------------

def menu_produits():
    while True:
        print("\n--- Gestion des Produits ---")
        print("1. Ajouter un produit")
        print("2. Lister les produits")
        print("3. Rechercher un produit")
        print("4. Modifier un produit")
        print("5. Supprimer un produit")
        print("6. Afficher les produits par catégorie")
        print("7. Afficher les produits par fournisseur")
        print("8. Afficher les produits en stock faible")
        print("0. Retour")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            name = input("Nom produit : ").strip()
            description = input("Description : ").strip()
            category_id = input("Catégorie (ID ou nom, laisser vide possible) : ").strip()
            supplier_id_or_name = input("Fournisseur (ID ou nom, laisser vide possible) : ").strip()

            supplier_id = ""
            if supplier_id_or_name:
                fournisseurs = Fournisseur._charger_fournisseurs()
                found = False
                for f in fournisseurs:
                    if f.get("name", "").strip().lower() == supplier_id_or_name.strip().lower() or \
                        f.get("ID", "").strip().lower() == supplier_id_or_name.strip().lower():
                        supplier_id = f.get("ID", "")
                        found = True
                        break
                if not found:
                    print("Fournisseur introuvable — laissez vide ou ajoutez le fournisseur d'abord.")
                    supplier_id = ""
            price = input("Prix : ").strip()
            cost = input("Coût : ").strip()
            quantity = input("Quantité : ").strip()
            min_quantity = input("Quantité minimale : ").strip()
            SKU = input("SKU : ").strip()
            produit = Product(name=name, description=description, category_id=category_id,
                            supplier_id=supplier_id, price=to_float(price, 0.0),
                            cost=to_float(cost, 0.0), quantity=to_int(quantity, 0),
                            min_quantity=to_int(min_quantity, 0), SKU=SKU)
            produit.ajouter_produit()

        elif choix == "2":
            Product.lister_produits()

        elif choix == "3":
            recherche = input("Nom, ID ou SKU du produit : ").strip()
            Product.rechercher_produit(recherche)

        elif choix == "4":
            nom = input("Nom ou ID du produit à modifier : ").strip()
            print("Champs modifiables :", Product.FIELDNAMES)
            champ = input("Champ à modifier : ").strip()
            valeur = input("Nouvelle valeur : ").strip()
            Product.modifier_produit(nom, **{champ: valeur})

        elif choix == "5":
            nom = input("Nom du produit à supprimer : ").strip()
            Product.supprimer_produit(nom)

        elif choix == "6":
            cat = input("Nom ou ID de la catégorie : ").strip()
            Product.produits_par_categorie(cat)

        elif choix == "7":
            f = input("Nom ou ID du fournisseur : ").strip()
            Product.produits_par_fournisseur(f)

        elif choix == "8":
            Product.produits_stock_faible()

        elif choix == "0":
            break
        else:
            print("Choix invalide.")

def menu_categories():
    while True:
        print("\n--- Gestion des Catégories ---")
        print("1. Ajouter une catégorie")
        print("2. Lister les catégories")
        print("3. Modifier une catégorie")
        print("4. Supprimer une catégorie")
        print("0. Retour")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            name = input("Nom catégorie : ").strip()
            description = input("Description : ").strip()
            categorie = Category(name=name, description=description)
            categorie.ajouter_categorie()

        elif choix == "2":
            Category.lecture_categories()

        elif choix == "3":
            nom = input("Nom de la catégorie à modifier : ").strip()
            print("Champs modifiables : ID, name, description, created_at")
            champ = input("Champ à modifier : ").strip()
            valeur = input("Nouvelle valeur : ").strip()
            Category.modifier_categorie(nom, **{champ: valeur})

        elif choix == "4":
            nom = input("Nom de la catégorie à supprimer : ").strip()
            Category.supprimer_categorie(nom)

        elif choix == "0":
            break
        else:
            print("Choix invalide.")

def menu_fournisseurs():
    while True:
        print("\n--- Gestion des Fournisseurs ---")
        print("1. Ajouter un fournisseur")
        print("2. Lister les fournisseurs")
        print("3. Modifier un fournisseur")
        print("4. Supprimer un fournisseur")
        print("5. Voir les produits d'un fournisseur")
        print("0. Retour")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            name = input("Nom fournisseur : ").strip()
            phone = input("Téléphone : ").strip()
            email = input("Email : ").strip()
            address = input("Adresse : ").strip()
            fournisseur = Fournisseur(name=name, phone=phone, email=email, address=address)
            fournisseur.ajouter_fournisseur()

        elif choix == "2":
            Fournisseur.lecture_fournisseurs()

        elif choix == "3":
            nom = input("Nom ou ID du fournisseur à modifier : ").strip()
            print("Champs modifiables : ID, name, phone, email, address, created_at")
            champ = input("Champ à modifier : ").strip()
            valeur = input("Nouvelle valeur : ").strip()
            Fournisseur.modifier_fournisseur(nom, **{champ: valeur})

        elif choix == "4":
            nom = input("Nom du fournisseur à supprimer : ").strip()
            Fournisseur.supprimer_fournisseur(nom)

        elif choix == "5":
            fournisseur = input("Nom ou ID du fournisseur : ").strip()
            Product.produits_par_fournisseur(fournisseur)

        elif choix == "0":
            break
        else:
            print("Choix invalide.")

def menu_stocks():
    while True:
        print("\n--- Outils de gestion des stocks ---")
        print("1. Mettre à jour le stock d'un produit")
        print("2. Afficher les alertes de stock faible")
        print("3. Consulter l'historique des mouvements")
        print("4. Valorisation du stock")
        print("0. Retour")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            nom = input("Nom ou ID du produit : ").strip()
            type_mvt = input("Type de mouvement (ajout/retrait) : ").strip().lower()
            qte = input("Quantité : ").strip()
            StockManager.mise_a_jour_stock(nom, qte, type_mvt)

        elif choix == "2":
            Product.produits_stock_faible()

        elif choix == "3":
            StockManager.consulter_historique()

        elif choix == "4":
            StockManager.valorisation_totale()

        elif choix == "0":
            break
        else:
            print("Choix invalide.")

def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Gestion des produits")
        print("2. Gestion des catégories")
        print("3. Gestion des fournisseurs")
        print("4. Outils de stock")
        print("0. Quitter")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            menu_produits()
        elif choix == "2":
            menu_categories()
        elif choix == "3":
            menu_fournisseurs()
        elif choix == "4":
            menu_stocks()
        elif choix == "0":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")

# ---------------------------
# Lancement
# ---------------------------

if __name__ == "__main__":
    # Vérification : créer fichiers vides si absent (pas obligatoire mais utile)
    if not os.path.exists(Category.JSON_FILE):
        safe_write_json(Category.JSON_FILE, [])
    if not os.path.exists(Fournisseur.JSON_FILE):
        safe_write_json(Fournisseur.JSON_FILE, [])
    if not os.path.exists(Product.CSV_FILE):
        safe_write_csv(Product.CSV_FILE, Product.FIELDNAMES, [])
    if not os.path.exists(StockManager.HISTORIQUE_FILE):
        safe_write_json(StockManager.HISTORIQUE_FILE, [])

    menu()
