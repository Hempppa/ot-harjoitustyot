# Miinaharava
Sovellus toimii kuin "suoraviivaisempi" miinaharavapeli. Pelaajan tarkoitus on siis, osumatta miinoihin, tyhjentää kenttä kaikista muista ruuduista. Tähän avustukseksi "tyhjät" ruudut ilmoittavat miinojen lukeman 3x3 ruudukossa niiden ympäriltä. OIkeasti tyhjät ruudut avaavat automaattisesti koko ko. alueen.
## Dokumentaatio
- [vaatimusmäärittely](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/vaatimusmaarittely.md)
- [tuntikirjanpito](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/tuntikirjanpano.md)
- [Changelog](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/changelog.md)

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
(Testit ovat hetkellä hyvin vaiheessa)
Pytest testit voi kuitenkin suorittaa
```bash
poetry run invoke test
```
Ja testikattavuus
```bash
poetry run invoke coverage-report
```
index.html tallennetaan htmlcov-hakemistoon
