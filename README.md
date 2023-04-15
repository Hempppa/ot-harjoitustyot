# Miinaharava
Sovellus toimii kuin klassinen miinaharavapeli. Pelaajan tarkoitus on siis, osumatta miinoihin, tyhjentää kenttä kaikista muista ruuduista. Tähän avustukseksi "tyhjät" ruudut ilmoittavat miinojen lukeman 3x3 ruudukossa niiden ympäriltä. Oikeasti tyhjät ruudut avaavat automaattisesti koko ko. alueen. Ruutuja voi myös liputtaa miinoiksi, jotta niitä olisi helpompi seurata.
## Dokumentaatio
- [vaatimusmäärittely](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/vaatimusmaarittely.md)
- [tuntikirjanpito](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/tuntikirjanpano.md)
- [Changelog](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/changelog.md)
- [Luokkakaavio](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/luokkakaavio.md) (Sprites = monet pienet "Sprites" luokat)

## Komentorivitoiminnot
Tällä hetkellä alkuun pääsemiseen riittää pelkkä riippuvuuksien asentaminen
```bash
poetry install
```
Tämän jälkeen peliä voi pelata komennolla:
```bash
poetry run invoke start
```
### Testaus
Pytest testit voi suorittaa
```bash
poetry run invoke test
```

Ja testikattavuus (index.html tallennetaan htmlcov-hakemistoon)
```bash
poetry run invoke coverage-report
```

Myös ohjelman siisteyttä voi arvioida pylintillä
```bash
poetry run invoke lint
```
