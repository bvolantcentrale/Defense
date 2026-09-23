# Conversion native du PowerPoint

Cette version ne contient plus de captures de diapositives complètes.

- SVG / PNG / JPEG : extraits directement du `.pptx`
- texte : converti en texte HTML modifiable
- tableaux : convertis en HTML
- SmartArt / groupes / graphiques / formes PowerPoint : exportés individuellement en SVG vectoriel

Les annexes sont placées après « Merci » et n'ont pas de `data-part`. Elles sont donc absentes du plan et du compteur de progression.

Lancer :
```bash
quarto preview presentation.qmd
```

## Palette pour les modifications futures

Pour toute demande de couleur, utiliser uniquement le noir, ses nuances, ou les quatre couleurs des titres de parties : `#440F76`, `#942C80`, `#E44F64`, `#FEA973` (variables CSS `--part-1` à `--part-4`). Les fonds peuvent utiliser ces mêmes couleurs avec une faible opacité. Ne pas introduire d’autre teinte sans demande explicite. Conserver les couleurs des données importées lorsqu’elles doivent reproduire une source.

Dans le tableau modulaire : Scénarios en noir ; alimentation embarquée en couleur de partie 1 ; production d’énergie en couleur de partie 2 ; infrastructure en couleur de partie 3.

## Sous-titre optionnel

Conserver le format discret à côté du titre : 11 px, couleur atténuée, graisse normale, espacement des lettres de 0,05 em et marge gauche de 12 px. Utiliser la classe `slide-subtitle` pour tout futur sous-titre :

```html
<div class="slide-title">Titre <span class="slide-subtitle">Sous-titre</span></div>
```

## Placement des images

Lors d’une conversion ou d’un remplacement d’image, conserver strictement les positions et dimensions du QMD (left, top, width, height). Modifier uniquement le chemin src, sauf demande explicite de changement de mise en page.

## Tailles du contenu

Le contenu HTML utilise `--content-size: 18px` et les titres internes `--content-title-size: 24px`, centralises dans `custom.css`. Les titres principaux et la navigation conservent leurs styles propres. Le texte integre aux images reste dans les fichiers sources.

## Références par grande partie

Définir chaque source une seule fois dans `references.yml` :

```yaml
part-references:
  bloch-2023:
    short: "Bloch et al. (2023)"
    full: "Bloch, F., Jackson, M. O., & Tebaldi, P. (2023). Centrality measures in networks. Social Choice and Welfare, 61(2), 413–453."
```

Ajouter ensuite `refs="bloch-2023"` dans les accolades du titre de la diapo :

```markdown
## Mon titre {.editorial data-part="2" data-subpart="1" refs="bloch-2023"}
```

Pour plusieurs sources : `refs="bolla-2011,li-2023"`. Réutiliser le même identifiant conserve le même numéro dans la partie. L'ordre de première citation définit les numéros, qui recommencent à 1 pour chaque `data-part`.

Le filtre `part-references.lua` affiche le champ `full` de chaque référence en bas de la diapo (16 px, gris, une notice par bloc), puis les notices complètes en fin de partie (26 px, dix références par page). `navigation.html` ajuste l’espace réservé en bas du canevas à la hauteur réelle des notices pour éviter les chevauchements. Les citations sont cliquables vers leur récapitulatif. Les récapitulatifs apparaissent avant la partie suivante, ou avant « Merci » pour la dernière partie ; une partie sans citation ne reçoit pas de page vide. Ils font partie du compteur et de la progression, et sont présents dans l'export PDF.

Exception pour l’introduction (`data-part="1"`) : les notices restent en pied de page, sans lien ni diapositive récapitulative en fin de partie. Cette exception est définie dans `FOOTER_ONLY_PARTS` du filtre Lua.

Ne pas écrire les diapositives de références à la main. Lancer `quarto render presentation.qmd` après modification. Un identifiant inconnu ou une notice sans `short` / `full` provoque une erreur explicite au rendu.

Les références initiales sont reprises du document existant sans validation bibliographique. Les six entrées `literature-*` n'ont que les auteurs, l'année et l'approche citée : compléter `full` avec les notices bibliographiques exactes.

## Langue de la présentation

Traduire systématiquement en français les nouveaux textes, tableaux et figures, y compris les ressources importées. Conserver les exceptions demandées explicitement : le titre de tableau « LCA type » reste en anglais.

La figure d’incertitude est adaptée de `../LCA/examples/schema_bloc/incertitude_variabilite_fig.py`. Régénérer ses deux états avec `python figures/incertitude_variabilite_fig.py`, puis rendre la présentation avec Quarto.

Le schéma LCIA ReCiPe est traduit depuis `../LCA/examples/schema_bloc/recipe_impact_fig.py`. Régénérer la version locale avec `python figures/recipe_impact_fig.py`.
