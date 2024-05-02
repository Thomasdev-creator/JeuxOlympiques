# Application des Jeux Olympiques

Bienvenue sur mon application. Ce projet dans le cadre de mes études vise à développer une application pour les Jeux Olympiques ! Cette application vous permet également d'acheter des billets pour les Jeux Olympiques.

## Technologies Utilisées

- **Backend** : Django, PostgreSQL, (TablePlus)
- **Frontend** : Tailwind CSS
- **ORM** : Django ORM

## Fonctionnalités Principales

- Consultation des sports olympiques
- Achat de billet, et reçu d'un QRCode
- Gestion du profil utilisateur
- Connexion, déconnexion, inscription

## Installation

Pour installer et exécuter l'application localement, suivez les étapes suivantes :

1. Cloner ce dépôt sur votre machine locale.
2. Assurez-vous d'avoir installé Python et PostgreSQL sur votre machine.
3. Créez un environnement virtuel et activez-le.
4. Installez les dépendances à l'aide de `pip install -r requirements.txt`.
5. Configurez les variables d'environnement, y compris les paramètres de base de données, dans un fichier `.env`.
6. Effectuez les migrations de la base de données à l'aide de `python manage.py migrate`.
7. Lancez le serveur de développement avec `python manage.py runserver`.
8. Executé la commande suivant en mode développement à la racine du projet pour écouter
les évènements Stripe et pour que la page de succès suite à l'achat fonctionne "stripe listen --forward-to 127.0.0.1:8000/stripe-webhook/"

9. Installez TablePlus pour avoir visualiser la base de données.

## Contribution

Les contributions à l'amélioration de l'application sont les bienvenues ! Si vous souhaitez contribuer, veuillez suivre ces étapes :

1. Fork ce dépôt.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/NomDeLaFonctionnalité`).
3. Commitez vos modifications (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`).
4. Poussez votre branche (`git push origin feature/NomDeLaFonctionnalité`).
5. Créez une nouvelle demande de tirage.

## Licence

Ce projet est sous licence [MIT](LICENSE).
