# ImmoGest - Gestion Immobilière Simplifiée

Application web de gestion locative développée avec Flask. Permet aux bailleurs de gérer leurs biens, locataires, paiements et quittances de manière centralisée et sécurisée.

## Fonctionnalités Clés

*   **Tableau de Bord** : Statistiques en temps réel (taux d'occupation, revenus, alertes).
*   **Gestion des Biens** : Ajout, modification, photos, et suivi de l'état (Vacant/Occupé).
*   **Locataires** : Dossiers complets, assignation aux biens, et contacts d'urgence.
*   **Paiements & Quittances** : Enregistrement des loyers, génération PDF automatique des quittances, et export CSV pour la comptabilité.
*   **Alertes** : Notification automatique des loyers impayés du mois en cours.

## Prérequis Techniques

*   Python 3.11+
*   Git

## Installation Locale

1.  **Cloner le projet**
    ```bash
    git clone https://github.com/votre-user/gest-immo.git
    cd gest-immo
    ```

2.  **Créer un environnement virtuel**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Installer les dépendances**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurer l'environnement**
    Créer un fichier `.env` à la racine :
    ```env
    SECRET_KEY=votre_cle_secrete_tres_longue
    DATABASE_URL=sqlite:///gestimmo.db
    ```

5.  **Initialiser la base de données**
    ```bash
    flask db upgrade
    ```

6.  **Lancer l'application**
    ```bash
    python run.py
    ```
    Accédez à `http://127.0.0.1:5000`.

## Déploiement (Production)

Ce projet est prêt pour être déployé sur des plateformes comme **Render** ou **Heroku**.

### Fichiers de configuration inclus :
*   `Procfile` : Commande de lancement (`gunicorn run:app`).
*   `runtime.txt` : Version Python (`python-3.11.9`).
*   `requirements.txt` : Liste des dépendances incluant `gunicorn`.

### Étapes pour Render.com :
1.  Connectez votre dépôt GitHub à Render.
2.  Créez un **Web Service**.
3.  **Build Command** : `pip install -r requirements.txt`
4.  **Start Command** : `gunicorn run:app`
5.  Ajoutez les variables d'environnement (`SECRET_KEY`, `DATABASE_URL`) dans l'onglet "Environment".
    *   *Note : Pour la production, utilisez une base PostgreSQL externe.*

## Structure du Projet

```
gest-immo/
├── app/
│   ├── models/       # Modèles de base de données (User, Property, Tenant, Payment)
│   ├── routes/       # Logique des routes (Auth, Main, Property, Tenant, Payment)
│   ├── forms/        # Formulaires WTForms
│   ├── templates/    # Templates HTML (Jinja2) avec Tailwind CSS
│   └── utils/        # Utilitaires (Génération PDF)
├── migrations/       # Scripts de migration DB
├── run.py           # Point d'entrée
├── config.py        # Configuration Flask
└── requirements.txt # Dépendances
```

## Auteur
Développé avec ❤️ pour simplifier la gestion immobilière.