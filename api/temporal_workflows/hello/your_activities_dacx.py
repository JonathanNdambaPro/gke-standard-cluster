"""
DESIGN PATTERN : Pydantic Service Class for Temporal Activities
---------------------------------------------------------------
Ce pattern a été choisi pour structurer les activités Temporal en tant que
'Dependency Injection Container'.

POURQUOI CE CHOIX PLUTÔT QUE LES ALTERNATIVES ?

1. VS PROCÉDURAL / FONCTIONNEL (Globales & Closures) :
   - Évite les variables globales qui rendent les tests parallèles impossibles.
   - Évite l'enfer des 'Factories' de fonctions (closures) difficiles à debugger.
   - Offre un cadre rigide : les outils sont dans 'self', les données dans 'args'.

2. VS CLASSE CLASSIQUE (Vanilla Python) :
   - ZÉRO BOILERPLATE : Pas de `__init__(self, a, b...)` répétitif et verbeux.
   - VALIDATION AUTO : Pydantic vérifie les types à l'instanciation. Une classe
     classique accepterait un `None` silencieusement, causant un crash plus tard.
   - IMMUABILITÉ : Avec `frozen=True`, on garantit que personne ne modifie
     les dépendances (ex: changer l'URL de l'API) pendant l'exécution.

3. ROBUSTESSE 'FAIL-FAST' :
   - Le Worker crash IMMÉDIATEMENT au démarrage si une dépendance est mal
     configurée. C'est une sécurité critique pour éviter les erreurs de
     production 'à retardement' (Runtime Errors).

4. TESTABILITÉ INDUSTRIELLE :
   - Chaque test instancie sa propre version de la classe avec des Mocks.
     Zéro collision latérale. Isolation totale garantie.

5. SÉPARATION DES PRÉOCCUPATIONS (Concerns) :
   - LA CLASSE (self) : L'Infrastructure (Comment on accède aux données).
   - LA MÉTHODE (args) : Le Domaine (Quelles données on traite).

RÈGLES D'OR POUR L'ÉQUIPE :
- Interdiction de stocker un état mutable dans `self` (La classe est Stateless).
- Tout client externe (DB, API, S3) DOIT passer par le modèle Pydantic.
- Si une activité dépasse 15-20 lignes, extraire la logique pure dans une
  fonction privée ou un module métier dédié.
"""

from pydantic import BaseModel, ConfigDict
from temporalio import activity

from api.models.events import EventModelV1
from api.temporal_workflows.hello.config_excution_temporal import config_temporal_hello


class HelloActivities(BaseModel):
    # ICI : Ce qui est FIXE (Dépendances)
    # Exemple : prefix_message: str = "Hello"

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @activity.defn(name=config_temporal_hello.activity_name)
    async def your_activity(self, input_hello: EventModelV1) -> str:
        # ICI : Ce qui est VARIABLE (Données d'entrée)
        return f"hello {input_hello.name}, {input_hello.lastname}!"


class HelloActivitiesMultiStep(BaseModel):
    # ICI : Ce qui est FIXE (Dépendances)
    # Exemple : prefix_message: str = "Hello"

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @activity.defn(name=f"{config_temporal_hello.activity_name}_name")
    async def your_activity_name(self, input_hello: EventModelV1) -> str:
        # ICI : Ce qui est VARIABLE (Données d'entrée)
        return f"hello {input_hello.name}, "

    @activity.defn(name=f"{config_temporal_hello.activity_name}_lastname")
    async def your_activity_lastname(self, input_hello: EventModelV1, prefix: str) -> str:
        # ICI : Ce qui est VARIABLE (Données d'entrée)
        return prefix + f"{input_hello.lastname}!"
