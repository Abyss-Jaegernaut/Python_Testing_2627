# Intro

```
Hey,

Je viens de recevoir le rapport de QA pour la phase 1 du projet. Il y a plusieurs bogues, dont un qui fait planter l'application ! 
Malheureusement, je ne suis pas au bureau pour les prochains jours (un de mes enfants est tombé malade ce week-end). 
Je ne sais pas encore quand je pourrai être là dans la semaine. Pourriez-vous prendre en charge la mise en œuvre du projet ? 
Vous devrez régler les bogues de la phase 1 et mettre en œuvre les éléments de la phase 2 (j'ai ajouté le travail de la phase 2 et les bogues de la section “issues” du repo). 

Vous devrez cloner et forker le repo et le mettre en place sur votre machine locale (tout ce dont vous avez besoin se trouve dans le fichier README). 
Ensuite, passez en revue les bogues dans la section des problèmes, puis essayez de reproduire les problèmes sur votre machine locale pour résoudre les bogues et ajouter la gestion des erreurs. 
Pour gagner du temps de configuration, nous utilisons Flask et JSON pour éviter d'utiliser une base de données. 
La plupart des outils dont vous aurez besoin se trouvent dans le fichier requirements.txt dans le repo, 
mais vous devrez installer Flask et notre framework de test préféré, pytest, ainsi que notre outil de test de performance, Locust. 

Vous devrez également préparer un rapport de test et un rapport de performances, 
conformément au guide de développement à la fin des spécifications fonctionnelles ci-jointes. 
Veillez à suivre toutes les directives, car le QA nous reproche de ne pas respecter les normes. 
Vous devez tester de manière approfondie les résultats requis (à la fois les happy paths et les sad paths) pour toutes les fonctionnalités de l'application.  
Je vous encourage également à adopter une approche de TDD, car cela vous aidera à rationaliser votre travail. 

Une fois que vous aurez terminé, nous ferons un examen de ce que vous avez dans la branche QA du code. 
Nous examinerons les rapports et la manière dont vous avez résolu les problèmes, 
nous examinerons votre code et nous testerons la couverture de la nouvelle fonctionnalité. 

Merci !
```

1. Why

   This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.
2. Getting Started

   This project uses the following technologies:

   * Python v3.10
   * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

     Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need.
   * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

     This ensures you'll be able to install the correct packages without interfering with Python on your machine.

     Before you begin, please ensure you have this installed globally.
3. Installation

   - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.
   - Next, type <code>venv\Scripts\activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>
   - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>
   - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details
   - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.
4. Current Setup

   The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:

   * competitions.json - list of competitions
   * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.
5. Testing & Code Coverage

   Nous utilisons **pytest** et **pytest-cov** pour valider l'ensemble des règles métier et fonctionnalités.

   Pour exécuter tous les tests et générer le rapport de couverture :

   ```bash
   pytest --cov=server --cov-report=term-missing --cov-report=html
   ```
   * **Taux de couverture atteint : 97%** (objectif initial : minimum 60%).
   * Le rapport HTML interactif complet est généré dans le dossier `htmlcov/`.
6. Flake8 Report

   Pour vérifier la conformité PEP 8 du code et générer le rapport HTML :

   ```bash
   flake8 --format=html --htmldir=flake8_report server.py tests/
   ```
   Le rapport est consultable dans `flake8_report/index.html`.
7. Tests de Performance (Locust)

   Pour évaluer la charge avec 6 utilisateurs simultanés (exigence : chargement < 5s, mise à jour < 2s) :

   ```bash
   python -m locust -f tests/locustfile.py --headless -u 6 -r 2 --run-time 20s --host http://127.0.0.1:5000
   ```
   * Résultats obtenus : temps de réponse moyen de **10 ms**, temps max de **47 ms**, et **0% d'échec**.
