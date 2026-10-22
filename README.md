# Soutenance de thèse — Benoît Volant

Présentation finale sur l’organisation des parties prenantes et la décarbonation ferroviaire régionale.

## Diffusion

Ouvrir ou partager `presentation.html` : ce fichier autonome contient les styles, les images et les bibliothèques nécessaires à la présentation. Il peut être consulté hors connexion dans un navigateur récent.

Les deux publications liées depuis les diapositives restent des fichiers séparés : pour conserver leur accès, joindre le dossier `figures/` au HTML en respectant son emplacement relatif.

## Génération

Installer [Quarto](https://quarto.org/), puis exécuter à la racine du dépôt :

```sh
quarto render presentation.qmd
```

Pour prévisualiser les modifications :

```sh
quarto preview presentation.qmd
```

## Contenu du dépôt

- `presentation.qmd` : contenu final des diapositives et annexes.
- `presentation.css` : mise en page et styles.
- `navigation.html` : navigation et interactions.
- `references.yml` et `part-references.lua` : références bibliographiques par partie.
- `figures/` et `assets/` : seules ressources utilisées par la présentation.
- `presentation.html` : version générée pour la diffusion, à régénérer après toute modification.

Les annexes suivent la diapositive « Merci » et sont exclues du plan des grandes parties. Les citations dans le contenu utilisent `<span data-cite="identifiant"></span>` et doivent également être déclarées dans l’attribut `refs` de la diapositive.
