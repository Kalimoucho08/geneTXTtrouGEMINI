# Générateur de Texte à Trous

Ce projet est une application Python qui permet de générer des textes à trous à partir d'un texte source. Vous pouvez coller, ouvrir un fichier, ou utiliser l'API Gemini pour générer le texte source. L'application offre la possibilité de configurer le nombre et le type de mots à supprimer, ainsi que la position du texte original.

## Fonctionnalités

*   **Sources de Texte Multiples :**
    *   Coller du texte directement dans l'application.
    *   Ouvrir un fichier texte (``.txt``) existant.
    *   Générer du texte à l'aide de l'API Gemini (nécessite une clé API).
*   **Configuration du Texte à Trous :**
    *   Spécifier le nombre de mots à supprimer.
    *   Choisir les types de mots à supprimer (Noms, Verbes, Adjectifs, etc.).
    *   Option pour afficher la liste des mots supprimés.
    *   Option pour ajouter le texte original (avant, après, ou non).
    *   Option pour activer ou désactiver la répartition harmonieuse des trous dans le texte.
*   **Options Gemini:**
    *   Possibilité d'enregistrer votre clé API pour une utilisation future. L'application reste fonctionnelle même sans clé API (la fonctionnalité Gemini sera grisée).
*   **Interface Simple :**
    *   Interface graphique intuitive et facile à utiliser.
    *   Fenêtre dédiée pour l'affichage du texte à trous.
    *   Bouton pour copier le texte généré.
*   **Sauvegarde :**
    *   Sauvegarde du texte généré en format texte brut (.txt).

## Installation et Utilisation

### Prérequis

1.  **Python 3.6+** installé sur votre système.
2.  Les bibliothèques Python suivantes :
    *   `tkinter` (normalement inclus avec Python)
    *   `spacy`
    *   `google-generativeai`
    *   `odfpy`
    *   `reportlab`

    Vous pouvez installer ces bibliothèques avec pip :

    ```bash    pip install spacy google-generativeai odfpy reportlab    ```
3.  Modèle spaCy pour le français:
    ```bash    python -m spacy download fr_core_news_sm    ```
4.  (Optionnel) Une clé API Google Gemini si vous souhaitez utiliser la génération de texte.

### Utilisation

1.  **Téléchargez** le fichier ``.py`` (par exemple, `texte_a_trous.py`) de ce dépôt.
2.  **Exécutez** le fichier Python :

    ```bash    python texte_a_trous.py    ```
3.  **Interface Graphique :**
    *   **Source du Texte :** Choisissez votre source de texte (coller, ouvrir un fichier ou Gemini).
    *   **Options du Texte à Trous :** Définissez le nombre de mots à supprimer, les types de mots et les options d'affichage.
    *   **Générer :** Cliquez sur le bouton "Générer" pour créer le texte à trous.
    *   **Résultat :** Une nouvelle fenêtre affichera le texte à trous généré.
    *   **Copier :** Vous pouvez copier le texte généré avec le bouton "Copier le texte".
    *   **Sauvegarder :** Enregistrez le texte généré en cliquant sur "Sauvegarder Texte".
   
4.  **API Key (Optionnel) :**
    *   Si vous souhaitez utiliser Gemini, entrez votre clé API dans la zone prévue à cet effet et cliquez sur Sauvegarder. La clé sera sauvegardée pour les utilisations futures, mais elle restera invisible dans la zone de saisie.

## Captures d'écran

Vous pouvez inclure ici une ou plusieurs captures d'écran de l'application en action pour donner un aperçu visuel.

## Notes

*   L'API key n'est pas obligatoire pour utiliser l'application, vous pouvez générer un texte avec ou sans l'API Gemini.

## Contributions

Les contributions sont les bienvenues ! Si vous avez des suggestions d'amélioration, des corrections de bugs ou des nouvelles fonctionnalités, n'hésitez pas à soumettre une Pull Request.

## Licence

Ce projet est sous licence [MIT](https://opensource.org/licenses/MIT).

## Auteur

Kalimoucho08
