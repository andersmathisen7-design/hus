# Sandertunet 27, Ski – nettside for boligsalget

En rask, SEO-optimalisert nettside for 3-roms hageleiligheten i Sandertunet 27, 1400 Ski
(FINN-kode [477552206](https://www.finn.no/realestate/homes/ad.html?finnkode=477552206)).

Adresse: **https://andersmathisen7-design.github.io/hus/**

Hele nettsiden ligger i `site/` og er ren HTML/CSS med litt JavaScript. Den trenger ingen
byggesteg og kan legges på hvilken som helst statisk webserver.

## Slik publiseres siden

GitHub Pages serverer grenen `gh-pages`, som inneholder nøyaktig det som ligger i `site/`.
Arbeidsflyten `.github/workflows/pages.yml` oppdaterer `gh-pages` automatisk hver gang noe i
`site/` endres på standardgrenen. Du kan også kjøre den manuelt under **Actions → Publiser
nettside → Run workflow**.

**Første gang (må gjøres én gang av eieren av repoet):** gå til **Settings → Pages**, velg
**Deploy from a branch**, gren `gh-pages`, mappe `/ (root)`, og trykk **Save**. Etter et par
minutter ligger siden på adressen over.

## Anbefalt: eget domene

Et eget domene (f.eks. `sandertunet27.no`) gir bedre synlighet i søk, og gjør det mulig for
Google å vise husikonet og et eget nettstedsnavn i søkeresultatene – noe som ikke er mulig på en
undermappe av `github.io`. Slik bytter du:

```bash
python3 tools/render.py --site-url https://sandertunet27.no/
```

Kommandoen oppdaterer canonical-adresse, delingsbilder, strukturerte data, `sitemap.xml`,
`robots.txt` og lager filen `CNAME`. Legg deretter inn domenet under **Settings → Pages →
Custom domain**, og pek DNS-en til GitHub Pages som beskrevet der.

## Få siden inn i Google

1. Legg til siden i [Google Search Console](https://search.google.com/search-console)
   (velg «URL-prefiks» med adressen over).
2. Send inn `sitemap.xml` (`https://andersmathisen7-design.github.io/hus/sitemap.xml`).
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
- **Korrekte nøkkeltall i søk og deling:** beskrivelsen viser BRA-i, antall soverom,
  energimerke og totalpris, slik bransjen forventer i korte formater.
- **Strukturerte data (JSON-LD):** `RealEstateListing`, `Apartment` (adresse, koordinater,
  areal, rom, byggeår, fasiliteter), `Offer` med totalpris og priskomponenter, og megleren som
  `Organization`. Event- og FAQ-markering er bevisst utelatt: Google viser ikke FAQ-resultater
  lenger, og Event-resultater støttes ikke for Norge.
- **Bilder:** 25 bilder i WebP i fire størrelser (`srcset`), beskrivende filnavn og alt-tekster,
  lat innlasting og et bildekart i `sitemap.xml`.
- **Hastighet:** kritisk CSS inline, egen font (28 KB, `font-display: swap`), hovedbildet
  forhåndslastes, ingen tredjepartsskript og ingen informasjonskapsler. Kartet lastes først når
  noen klikker på det.
- **Deling:** Open Graph og Twitter Card med eget bilde på 1200 × 630 piksler, for
  Facebook, Messenger, iMessage, Slack og LinkedIn.
- **Mobil:** responsiv layout, fast handlingslinje nederst og bildegalleri med sveip.
- **Tilgjengelighet:** semantisk HTML, «hopp til innhold»-lenke, synlig fokus og tastaturstyrt
  galleri. Siden validerer uten feil i W3C-validatoren.
- **Lokal SEO:** geo-metadata, kart, veibeskrivelse og avstander til skoler, stasjon og butikker.

## Vedlikehold

Avslutt hver endring med `python3 tools/render.py --lastmod ÅÅÅÅ-MM-DD` (dagens dato), slik at
«Sist oppdatert», `dateModified` og `sitemap.xml` får riktig dato.

- **Etter visningen 11. oktober** bytter siden selv knappene «Meld deg på visning» ut med
  «Avtal visning med megler» / «Salgsoppgave», og FAQ-svaret om visning endres. Det som ikke
  kan endres automatisk, må endres for hånd: fjern «Visning søndag 11. oktober.» fra
  `og:description` og `twitter:description` i `index.html`.
- **Ny visning:** oppdater `data-viewing-end` og teksten i seksjonen `#visning`, datomerket,
  FAQ-svaret, `og:description`, `twitter:description` og `visning.ics`.
- **Når boligen er solgt:** endre `"availability": "https://schema.org/InStock"` til
  `"https://schema.org/SoldOut"` og legg inn en «Solgt»-melding, eller ta siden ned.
- **Bilder:** `tools/build_images.py` lager alle bildestørrelser fra originalene.
  Alt-tekster og filnavn ligger i `tools/images.json`. Kjør `python3 tools/render.py` etterpå
  for å oppdatere galleriet og sitemap.

## Rettigheter og personvern

- **Bildene og plantegningen** kommer fra salgsoppgaven til PrivatMegleren Ski & Ås (bildene er
  tatt av meglerens fotograf), og kilden er oppgitt i bunnteksten. Få en kort bekreftelse på
  e-post fra megleren om at fotografen og den som har laget plantegningen godtar bruken her, og
  spør hvordan de vil krediteres. Endre deretter linjen «Foto og plantegning …» i `index.html`.
- **Fonten** Fraunces er lisensiert under SIL Open Font License; lisensen ligger i
  `site/assets/fonts/OFL.txt`.
- **Kartet** er © OpenStreetMap-bidragsytere og lastes først når noen klikker på det.
- **Personvern:** siden setter ingen informasjonskapsler og har ingen sporing. GitHub logger
  IP-adresser for sikkerhetsformål, som for alle GitHub Pages-sider.
