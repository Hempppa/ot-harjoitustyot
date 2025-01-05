# Miinaharava
Sovellus toimii kuin klassinen miinaharavapeli. Pelaajan tarkoitus on siis, osumatta miinoihin, tyhjentää kenttä kaikista muista ruuduista. Tähän avustukseksi "tyhjät" ruudut ilmoittavat miinojen lukeman 3x3 ruudukossa niiden ympäriltä. Oikeasti tyhjät ruudut avaavat automaattisesti koko ko. alueen. Ruutuja voi myös liputtaa miinoiksi, jotta niitä olisi helpompi seurata. Parhaat tulokset tallennetaan tulostauluun.

## Dokumentaatio
- [käyttöohje](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/kayttoohje.md)
- [Vaatimusmäärittely](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/vaatimusmaarittely.md)
- [Tuntikirjanpito](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/tuntikirjanpano.md)
- [Changelog](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/changelog.md)
- [Arkkitehtuuri](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/luokkakaavio.md)
- [Testausdokumentti](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/testaus.md)

## Komentorivitoiminnot
Sovelluksen asentamiseen tarvitsee docker olla asennettuna
### Imagen asentaminen
#### Githubista kloonaamisen jälkeen
```
docker build . -t hempppa/devops-w-docker-exercise-1-15
```

#### Vaihtoehtoisesti imagen lataaminen Dockerhubista 
```
docker pull hempppa/devops-w-docker-exercise-1-15
```
### Sovelluksen käynnistäminen
Sovelluksen pitäisi käynnistyä linux järjestelmällä komennolla
```
docker run -it -v "/tmp/.X11-unix:/tmp/.X11-unix" -e DISPLAY=${DISPLAY} hempppa/devops-w-docker-exercise-1-15
```
