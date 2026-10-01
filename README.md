# Sandertunet 27, Ski – nettside for boligsalget

En rask, SEO-optimalisert nettside for 3-roms hageleiligheten i Sandertunet 27, 1400 Ski
(FINN-kode [477552206](https://www.finn.no/realestate/homes/ad.html?finnkode=477552206)).

Hele nettsiden ligger i `site/` og er ren HTML/CSS med litt JavaScript. Den trenger ingen
byggesteg og kan legges på hvilken som helst statisk webserver.

## Publisere med GitHub Pages (gratis)

1. Slå sammen denne grenen til `main`.
2. Gå til **Settings → Pages** i repoet og velg **Source: GitHub Actions**.
3. Arbeidsflyten `.github/workflows/pages.yml` publiserer `site/` automatisk ved hver endring.
   Siden blir liggende på `https://andersmathisen7-design.github.io/hus/`.

GitHub Pages krever offentlig repo, eller et betalt GitHub-abonnement for private repoer.

## Anbefalt: eget domene

Et eget domene (f.eks. `sandertunet27.no`) gir bedre synlighet i søk og en adresse som er lett å
dele. Slik bytter du:

```bash
python3 tools/render.py --site-url https://sandertunet27.no/
```

Kommandoen oppdaterer canonical-adresse, delingsbilder, strukturerte data, `sitemap.xml` og
`robots.txt`. Legg deretter inn domenet under **Settings → Pages → Custom domain**, og pek
DNS-en til GitHub Pages som beskrevet der.

## Få siden inn i Google

1. Legg til siden i [Google Search Console](https://search.google.com/search-console).
2. Send inn `sitemap.xml` (f.eks. `https://andersmathisen7-design.github.io/hus/sitemap.xml`).
3. Bruk **URL-inspeksjon → Be om indeksering** på forsiden.
4. Gjør det samme i [Bing Webmaster Tools](https://www.bing.com/webmasters) (Bing brukes også av
   flere KI-søketjenester).
5. Del lenken i lokale Facebook-grupper for Ski og Follo – lenker og trafikk hjelper siden å bli
   funnet raskere.

`robots.txt` virker bare når siden ligger på roten av et domene. På `github.io/hus/` må du
derfor sende inn sitemap i Search Console.

## Hva som er gjort for SEO

- **Søkeord:** tittel, beskrivelse, overskrifter og tekst er skrevet for søk som
  «hageleilighet Ski», «3-roms leilighet til salgs Ski», «Sandertunet 27» og
  «leilighet nær Ski stasjon».
- **Eget innhold:** teksten er skrevet på nytt og ikke kopiert fra FINN, slik at Google ikke
  ser siden som et duplikat.
- **Strukturerte data (JSON-LD):** `RealEstateListing`, `Apartment` (adresse, koordinater,
  areal, rom, byggeår, fasiliteter), `Offer` (pris), `Event` (visning), `FAQPage` og
  `RealEstateAgent`.
- **Bilder:** 25 bilder i WebP i fire størrelser (`srcset`), beskrivende filnavn og alt-tekster,
  lat innlasting og et bildekart i `sitemap.xml`.
- **Hastighet:** kritisk CSS inline, egen font (28 KB, `font-display: swap`), hovedbildet
  forhåndslastes, ingen tredjepartsskript og ingen informasjonskapsler.
- **Deling:** Open Graph og Twitter Card med eget bilde på 1200 × 630 piksler, for
  Facebook, Messenger, iMessage, Slack og LinkedIn.
- **Mobil:** responsiv layout, fast handlingslinje nederst («Ring megler» / «Visning») og
  bildegalleri med sveip.
- **Tilgjengelighet:** semantisk HTML, «hopp til innhold»-lenke, synlig fokus og tastaturstyrt
  galleri.
- **Lokal SEO:** geo-metadata, OpenStreetMap-kart, veibeskrivelse og avstander til skoler,
  stasjon og butikker.

## Vedlikehold

- **Etter visningen** skjuler siden visningsinfoen automatisk og ber i stedet folk ta kontakt for
  privat visning.
- **Ny visning:** oppdater datoen i `index.html` (seksjonen `#visning`, `Event` i JSON-LD og FAQ)
  og i `visning.ics`.
- **Når boligen er solgt:** endre `"availability": "https://schema.org/InStock"` til
  `"https://schema.org/SoldOut"` og legg inn en «Solgt»-melding, eller ta siden ned.
- **Bilder:** `tools/build_images.py` lager alle bildestørrelser fra originalene.
  Alt-tekster og filnavn ligger i `tools/images.json`. Kjør `python3 tools/render.py` etterpå
  for å oppdatere galleriet og sitemap.

## Rettigheter

Bildene er tatt av meglerens fotograf i forbindelse med salget. Avklar med PrivatMegleren at de
kan brukes på denne siden. Fonten Fraunces er lisensiert under SIL Open Font License.
Kartet er © OpenStreetMap-bidragsytere.
