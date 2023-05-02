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

Peli avautuu vastaavanlaiseen näkymään


![alku](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/Screenshot%20from%202023-05-02%2020-22-02.png)


Peli toimii niin kuin voisi kuvitellakin, hiiren vasemmalla napilla voi siirtyä valikoissa, ESCillä palata niistä ja ruksia painamalla pääsee pois.

"Default difficulties" takana on vain toinen valikko, "Custom difficulty" valitsemalla pääsee itse säätämään vaikeutta.


![custom](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/Screenshot%20from%202023-05-02%2020-22-49.png)


Tässä haluamiaan arvoja voi syöttää ensin valitsemalla hiirellä taas ruudun ja sitten näpyttämällä haluamat numerot. Valitsemalla esim. 9x9/9 ruudukon avautuu peli ikkuna:


![peli](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/Screenshot%20from%202023-05-02%2020-22-17.png)

## Pelin eteneminen
Nyt peliä voi siis pelata kuin minesweeperiä, eli hiiren vasen painallus avaa ruudun ja oikea painallus liputtaa. Tavoitteena on siis avata kaikki muut ruudut osumatta miinoihin. Tältä voisi näyttää alkuvaiheissa oleva peli:


![kesken](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/Screenshot%20from%202023-05-02%2020-22-35.png)


Miinaan osuessa, peli pysähtyy kolmeksi sekunniksi ja palauttaa sitten alkunäkymään, voittaessa kuitenkin siirrytään seuraavaan näkymään:


![voitto](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/Screenshot%20from%202023-05-02%2020-26-58.png)


Tästä voi syöttää nimen, jolloin se kuluneen ajan kanssa sijoitetaan vaikeustasoa vastaavaan nopeuden mukaan järjestettyyn tulostauluun, joka taas näyttää tältä


![tulostaulu](https://github.com/Hempppa/ot-harjoitustyo/blob/master/dokumentaatio/kuvat/Screenshot%20from%202023-05-02%2020-26-37.png)


Kun on saanut pelistä tarpeeksi niin tietenkin voi poistua ruksia painamalla
