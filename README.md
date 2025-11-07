# 🧠 CoachAI_V1

CoachAI_V1 est une intelligence artificielle qui apprend de toi à travers tes parties de jeu vidéo.
Elle se base sur quatre facteurs principaux :

- 🎮 Le jeu choisi
- ⚡ La motivation (sur 5)
- 💤 La fatigue (sur 5)
- 🤝 Le mode duo (oui / non)

Grâce à un *apprentissage supervisé*, elle ajuste ses calculs après chaque partie pour *affiner ses prédictions.*
Son objectif : *prévoir si tu vas gagner ou non.*

## 🧩 Architecture

CoachAI_V1 est composée de :

- 4 neurones d’entrée
- 1 couche cachée de 3 neurones
- 1 neurone de sortie

Elle intègre un *système d’adaptation du taux d’apprentissage (learning rate)* permettant *d’accélérer* ou de *ralentir* son *apprentissage*, pour éviter le surapprentissage.

Un bouton de redémarrage permet d’intégrer des mises à jour sans perte des poids enregistrés.
Et si l’IA s’arrête, elle reprend automatiquement les derniers poids lors du redémarrage.

Le projet atteint ici sa limite logique : avec seulement 4 entrées, les prédictions restent simples.
Mais il remplit son rôle — comprendre comment créer une IA basique et fonctionnelle.

## 🚀 Utilisation
```bash
python3 main.py
```

## 🔭 Vision

Ce projet m’a permis de découvrir les fondements d’un perceptron simple puis d’un réseau multicouche (MLP).
Je poursuis maintenant vers une version plus ambitieuse : une IA capable de dialoguer et apprendre au fil des échanges, basée sur un réseau de neurones récurrent (RNN).
