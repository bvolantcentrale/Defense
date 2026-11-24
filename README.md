# Soutenance de thèse Benoît Volant

Présentation de la défense de thèse "Organisation des Parties Prenantes et Recommandation de Substitution Technologique Respectueuse de l’Environnement : Application à la Décarbonation Ferroviaire Régionale".


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
