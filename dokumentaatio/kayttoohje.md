# Käyttöohje

Projektin viimeisimmän version voi ladata 

## Konfigurointi

Sovelluksen käyttämiä tiedostonnimiä voi muuttaa, ne löytyvät .env tiedostosta, mutta en suosittele kuvatiedostojen muuttamista, sillä jos sovellus ei niitä löydä se ei toimi. Tietokannan nimen voi vaihtaa (lukuunottamatta .db päätettä) ja se vain luo uuden sillä nimellä jos semmoista ei löydy. Tietokannan nimi on kohdassa:
```
LEADERBOARD_REPO=leaderboard.db
```

## Käynnistäminen
Alkuun pääsee kun ensin asentaa riippuvaisuudet
```bash
poetry install
```
ja sen jälkeen vielä alustaa tietokannan 
```bash
poetry run invoke build
```
Tämän jälkeen peliä voi pelata komennolla:
```bash
poetry run invoke start
```
## Alkunäkymästä peliin
