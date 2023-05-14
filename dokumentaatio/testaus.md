# Testausdokumentti

Ohjelmaa on testattu sekä automatisoiduin yksikkö- ja integraatiotestein unittestilla sekä manuaalisesti tapahtunein järjestelmätason testein.

## Yksikkö- ja integraatiotestaus

### Sovelluslogiikka

src/gamelogic/input-handlers.py tiedoston luokkien (MenuScreen/DefaultLoop, GameLoop, CustomDifficulty, LeaderboardInput) testaamisesta vastaa vastaavat Test* alkuiset luokat src/tests/input-handlers-test.py tiedostossa. Testit suoritettiin injektoimalla Clock, EvenQueue ja Renderer() olioiden sijaan Stub- versiot, jotka hoitivat luokkien toiminnallisuudet, kuitenkin siten että voidaan hallitusti syöttää tapahtumia ja ei piirretä mitään näkymää. GameFrame luokkaa testaa TestGameFrame luokka samalla periaatteella, injektoidiin Stub- versioita oikeista luokista ja pidettiin kirjaa näkymien vaihdoista StubRenderereillä, sekä tallennettiin StubRepolla muistiin, tietokannan pysyväistallennuksen sijaan. Viimeisenä TestWholeGame on sama testi kuin TestGameFrame, mutta input-handlerit sekä repository luokka ovat oikeita. Tässä käytettiin samankaltaisia Stub- luokkia kuin itse input-handlereiden testaamisessa.

### Repositorio-luokka

Repositorio-luokka `LeaderboardRepository` testataan ainoastaan testeissä käytössäolevilla tiedostolla. Tiedoston nimi on konfiguroitu _.env.test_-tiedostoon (vakiona testi.db). Luokkaa testataan TestLeaderboardRepository-testiluokalla (src/tests/database-test.py)

### Testauskattavuus

Testikattavuus, riippumatta mitä tiedostoja lasketaan mukaan, on yli 90%. Jos otetaan mukaan vain merkittävät tiedostot (leaderboard-repository.py, input-handlers.py, map-generator.py, level.py ja main.py) testikattavuus on 97% 

---

Testikattavuuden ulkopuolelle jäivät jotkut vaikeustaso valinnat ja joidenkin spritejen käyttö.

## Järjestelmätestaus

Sovelluksen järjestelmätestaus on suoritettu manuaalisesti.

### Asennus ja konfigurointi

Sovellus on haettu ja sitä on testattu [käyttöohjeen](./kayttoohje.md) kuvaamalla tavalla Linux-ympäristöön. Testauksessa konfiguraatioiden muokkaamisessa _.env_-tiedostossa, vain tietokannan nimen muokkaus on testattu. Todennäköisemmin saman kokoiset kuvatiedostot kuitenkin toimivat. Korvaavien tiedostojen täytyy sijaita samassa kansiossa. 

### Toiminnallisuudet

Kaikki [määrittelydokumentin](./vaatimusmaarittely.md#pelin-tarjoama-toiminnallisuus) ja käyttöohjeen listaamat toiminnallisuudet on käyty läpi. Kaikkien toiminnallisuuksien yhteydessä on syötekentät yritetty täyttää myös virheellisillä arvoilla.

## Sovellukseen jääneet laatuongelmat

Sovellus ei anna tällä hetkellä järkeviä virheilmoituksia, seuraavissa tilanteissa:

- Konfiguraation määrittelemiin tiedostoihin ei ole luku/kirjoitusoikeuksia
- Konfiguraatiossa määrittelemiä kuvatiedostoja ei löydy
- SQLite tietokantaa ei ole alustettu, eli `python -m poetry run invoke build`-komentoa ei ole suoritettu
