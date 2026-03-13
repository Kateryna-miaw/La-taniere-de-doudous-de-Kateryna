# La Tanière des Doudous de Kateryna

Une simulation comportementale construite avec Streamlit. Le joueur gère trois peluches, Zaïtchyk (un lièvre), Jean-Jacques (un ours) et Frédéric (un cochon), sur 10 jours. Ce sont les vraies peluches de Kateryna, celles qui traînent sur son lit depuis toujours. L'objectif est d'atteindre 100 % d'affection avec chacune d'entre elles en choisissant les bonnes actions et, surtout, les bons *mots*.

C'est à la fois un jeu, une expérience de linguistique, et un outil d'analyse de données.

Vous pouvez y jouer sur : 
https://la-taniere-de-doudous-de-kateryna-rhyjcfq3z5ptu6fgn6vy3u.streamlit.app

---

## De quoi il s'agit

En surface, c'est un jeu de gestion de ressources. Chaque peluche a des stats d'énergie, de stress et d'affection. On choisit une action par peluche chaque jour (dormir, jouer, parler, les faire discuter entre elles), on résout les effets, et on passe au jour suivant. La nuit, il y a 15 % de chances que Calamar, un calamar géant, débarque et terrorise tout le monde, faisant exploser le stress de chaque peluche.

Mais la vraie mécanique, c'est le langage. Chaque peluche a un type de personnalité (extraverti, introverti, équilibré) et un registre de communication idéal (enthousiaste, empathique, factuel). Quand on choisit de parler à une peluche, on se retrouve face à trois répliques, une par registre. Si on tombe sur le bon registre, on gagne de l'affection. Si on se trompe, on se fait rejeter, le stress monte, et on a perdu un tour.

Ça repose sur la pragmatique linguistique : l'idée que ce qu'on dit compte moins que *comment* on le dit et *à qui* on le dit. Même intention, formulation différente, résultat complètement différent. Le jeu rend ça concret.

---

## Pourquoi ce projet

Il se situe au croisement de plusieurs disciplines et a été conçu pour montrer comment elles se rejoignent en pratique.

**Pragmatique linguistique.** La boucle de jeu oblige le joueur à réfléchir à l'adaptation du registre. On ne peut pas forcer l'affection, il faut lire le profil de chaque personnage et ajuster son langage en conséquence. Les sets de dialogues changent chaque jour (10 thèmes narratifs uniques sur la partie, plus un set de crise dédié aux apparitions de Calamar), donc ce n'est pas juste de la mémorisation.

**Psychologie comportementale.** Le système de traits (extraverti/introverti/équilibré) influence la réaction de chaque peluche à chaque action. Jouer motive Zaïtchyk mais stresse Jean-Jacques. Dormir est deux fois plus efficace pour les introvertis. Les discussions croisées entre peluches créent des synergies ou des tensions selon l'appariement des traits. La crise Calamar teste la capacité du joueur à gérer une situation de haute pression où seul le bon registre peut désamorcer la panique.

**Mathématiques appliquées.** L'écran de résultats calcule le coefficient de corrélation de Pearson entre le stress et l'affection de chaque peluche, implémenté à la main sans NumPy ni SciPy. Détails plus bas.

**Science des données.** Chaque action, chaque variation de stat, chaque choix de registre est enregistré dans un dataset structuré. En fin de partie, on obtient des courbes d'évolution, un scatter plot, un export CSV complet, et une analyse de biais qui mesure si le joueur a traité les trois peluches équitablement ou s'il a joué les favoris.

---

## Les maths

### Corrélation de Pearson

Une fois la partie terminée, l'application calcule le coefficient r de Pearson entre stress et affection, par peluche et globalement. L'implémentation est manuelle :

```
r = Σ(xi - x̄)(yi - ȳ) / √[Σ(xi - x̄)² · Σ(yi - ȳ)²]
```

x représente le stress et y l'affection à chaque jour enregistré. r varie entre -1 et +1. Un bon joueur devrait obtenir une corrélation négative (stress bas = affection haute). Une valeur proche de zéro signifie que les deux variables ont évolué indépendamment. Une corrélation positive indiquerait une partie chaotique, stress et affection qui montent ensemble, probablement sous pression constante de Calamar.

L'intérêt n'est pas juste d'afficher un chiffre. C'est de donner au joueur une mesure concrète et interprétable de l'impact de ses choix sur la durée, en utilisant un outil statistique fondamental.

### Score d'équité

L'onglet d'analyse des biais calcule un score d'équité basé sur l'écart-type des valeurs d'affection finales entre les trois peluches :

```
équité = 100 - σ(affection_finale)
```

Un score de 100 signifie un traitement parfaitement égal. Plus il descend, plus le joueur a favorisé certaines peluches au détriment des autres. L'application détecte aussi le favoritisme en comparant le nombre d'actions par peluche à la moyenne, suit la précision linguistique (proportion de bons registres pour chaque peluche), et calcule un taux de réussite en situation de crise Calamar.

---

## Fonctionnement technique

L'application est un fichier Streamlit unique. La gestion d'état passe entièrement par `st.session_state`, puisque Streamlit relance le script à chaque interaction.

La partie la plus casse-tête a été l'audio. Streamlit exécute ses composants dans des iframes isolées, donc impossible de créer un objet `Audio` et de le connecter au DOM de la page. La solution a été d'injecter tout le moteur audio dans `window.parent` via `st.components.v1.html`, puis d'utiliser un `MutationObserver` pour réattacher automatiquement les effets sonores (survol, clic) aux nouveaux boutons et éléments peluche après chaque rerun Streamlit. La musique de fond, le bouton mute, et la bande-son de crise Calamar vivent tous dans la fenêtre parente.

Côté visuel, le design utilise du glassmorphism (cartes translucides avec backdrop blur), la police Pixelify Sans pour un rendu pixel-art, et des animations CSS keyframe pour les humeurs des peluches : rebond pour heureux, tremblement pour effrayé, pulsation lente pour triste, éclat heartbeat pour les gagnantes.

Chaque peluche a des sprites PNG par état émotionnel (happy, sad, scared, tired, super_happy) qui changent dynamiquement en fonction de l'humeur et des événements récents.

---

## Dataset généré

Chaque partie produit un CSV téléchargeable avec une ligne par peluche et par jour. Colonnes : numéro du jour, nom du personnage, énergie, stress, affection, action choisie, registre linguistique utilisé, si Calamar était actif ou non, et partenaire de discussion le cas échéant. Ce dataset peut servir pour des analyses complémentaires ou comme support pédagogique.

---

## Licence

Tous droits réservés.
