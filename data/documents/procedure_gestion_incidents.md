# Procédure de gestion des incidents de sécurité — NovaTech Solutions

**Référence** : PROC-SEC-004
**Version** : 2.1
**Dernière mise à jour** : 03 février 2026
**Propriétaire** : Équipe Sécurité (SOC)
**Public concerné** : Tous les employés

## 1. Objectif

Cette procédure décrit les étapes à suivre pour signaler et traiter un incident de sécurité informatique (compromission de compte, malware, fuite de données, comportement suspect sur le réseau, etc.).

## 2. Qu'est-ce qu'un incident de sécurité ?

Un incident de sécurité est tout événement pouvant compromettre la confidentialité, l'intégrité ou la disponibilité des systèmes ou des données de l'entreprise. Exemples : e-mail de phishing sur lequel vous avez cliqué, ordinateur qui affiche un comportement anormal (ralentissements, fenêtres suspectes), perte d'un accès (compte verrouillé de façon inattendue), envoi accidentel d'un fichier confidentiel à la mauvaise personne.

**En cas de doute, signalez.** Il vaut mieux un faux positif qu'un incident non traité.

## 3. Niveaux de gravité et délais de prise en charge

| Gravité | Exemple | Délai de première réponse |
|---|---|---|
| Critique | Fuite de données clients, ransomware actif | 30 minutes, 24h/24 |
| Élevée | Compte compromis, malware détecté | 2 heures ouvrées |
| Moyenne | E-mail de phishing cliqué sans conséquence visible | 1 jour ouvré |
| Faible | Doute sur un e-mail, question générale | 3 jours ouvrés |

## 4. Étapes à suivre

1. **Isoler** : si votre poste semble compromis, déconnectez-le du réseau (débranchez le câble Ethernet ou désactivez le Wi-Fi) sans l'éteindre.
2. **Signaler immédiatement** au SOC via :
   - Le numéro d'urgence sécurité : poste **4444** (disponible 24h/24 pour les incidents critiques).
   - Le ticket interne, catégorie "Incident de sécurité", pour les cas non critiques.
3. **Ne pas tenter de corriger vous-même** (ne pas désinstaller, ne pas reformater, ne pas supprimer de fichiers) : cela peut détruire des preuves nécessaires à l'analyse.
4. **Documenter** ce que vous avez observé : heure, ce que vous avez fait juste avant, captures d'écran si possible.
5. Le SOC prend le relais, qualifie la gravité réelle, et vous tient informé de la suite.

## 5. Après l'incident

Une fois l'incident clos, le SOC peut vous demander de participer à un retour d'expérience (post-mortem) si l'incident était critique. Aucune sanction n'est appliquée pour un signalement de bonne foi, même si l'incident s'avère être une fausse alerte.

## 6. Contact

- Urgence sécurité (24h/24) : poste **4444**
- Ticket non urgent : catégorie "Incident de sécurité" sur le portail interne
- E-mail : soc@novatech-solutions.example
