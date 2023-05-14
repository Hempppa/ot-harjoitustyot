# Vaatimusmäärittely

## Sovelluksen tarkoitus

 Klassinen miinaharava peli. Pelissä on kolme valmiiksi määrättyä vaikeustasoa ja mahdollisuus luoda haluamansa mukainen pelikenttä. Tulostauluun tallennetaan kymmenen parasta aikaa jokaista neljää vaikeustasoa kohti (kolme valmista ja itse luodut).

## Perusversion tarjoama toiminnallisuus

### Alkunäkymä

 - Tämä näkymä avautuu pelin käynnistyttyä
 - Alkunäkymästä voi siirtyä kolmeen eri vaihtoehtoon, joista pääsee peliin tai tulostauluun
   - "Default Dífficulties" Avaa valikon ennalta määrättyjä miinakenttiä
   - "Custom Difficulty" Avaa näkymän, jossa voi syöttää omia arvoja kentän luomiseen
   - "Leaderboard" Avaa tulostaulun, johon on tallennettu tuloksia eri vaikeustasoista

### "Default Difficulties"

  - Näkymässä on kolme vaihtoehtoa miinakentän koolle ja miinojen määrälle
  - Pelin kenttä generoidaan valinnan mukaan
  - Näkymästä voi myös palata alkunäkymään ESCillä
  - Valittu vaikeus myös tallennetaan tulostauluun

### "Custom Difficulties"

  - Näkymässä on kolme kenttää joiden arvojen mukaan pelin kenttä generoidaan
  - Näkymästä voi myös palata alkunäkymään ESCillä
  - Klikkaamalla kenttiä ne aktivoidaan jonka jälkeen kenttään voi syöttää numeroita
  - "Width" ja "Height" määräävät kentän koon ja "Mines" miinojen määrän
  - Lukuja rajoitetaan ilmoitettujen rajojen sisälle, esim. "Height (1-18)"
    - Lisäksi miinoja on korkeintaan kentän koon verran

### Pelinäkymä

 - Peliä pelataan tavallisen miinaharavan tyyliin:
   - Pelin tavoite on avata kaikki miinattomat ruudut
   - Jos avataan miinan sisältävä ruutu, peli päättyy
   - Kukin avattu miinaton ruutu kertoo numerolla montako miinaa sen viereisistä ruuduista (1-8kpl) löytyy
   - Epäiltyjä miinoja voi liputtaa, joka helpottaa miinojen seuraamista
     - Liputettua ruutua ei voida avata, lipun voi myös poistaa
 - Näkymästä poistutaan joko häviämällä tai voittamalla
   - Häviöstä palataan suoraan alkunäkymään
   - Voistosta siirrytään "voittoruutuun"

### Voittoruutu

 - Täällä tallennetaan pelisuoritus, eli pelaajan syöttämä nimi, pelattu vaikeustaso ja peliin kestänyt aika 
 - Nimikenttä toimii kuin "CustomDifficulties" kentät, mutta hyväksyy kaikkia unicode merkkejä, kuitenkin max 8 merkkiä
 - Näkymästä poistutaan joko ESCillä tai enterillä
   - Enterillä tulos tallennetaan annetulla nimellä, siirrytään tauluun johon tulos tallennettiin
   - ESCillä palataan alkunäkymään tallentamatta mitään

### "Leaderboard"

 - Viimeinen näkymä, johon alkunäkymästä pääsee. Toinen tapa, josta päätyy tulostauluun
 - Valikko jossa valitaan vaikeustaso, jonka tulokset näytetään
 - Näkymästä voi myös palata alkunäkymään ESCillä
 - Vaihtoehtoja on neljä, joista kolme vastaa "Default Difficulties" vaikeuksia ja neljäs näyttää kaikki tulokset

### Tulostaulu

 - Tähän päädytään, joko "Leaderboard" valikosta tai voittoruudusta.
 - Näyttää yhden, valitun vaikeustason kymmenen parasta aikaa
 - Täältä voi vain palata ESCillä
   - Voittoruudun sijaan palataan alkunäkymään
   - Muuten palataan "Leaderboard" valikkoon

## Jatkokehitysideoita

 Ideoita pelikokemuksen laajentamiseen

### Resoluution säätö

 - Peli osaa itse tai ainakin pelaajan avustamana säätää halutun resoluution
   - Hetkellä jää paljon tyhjää tilaa tai menee näytön ulkopuolelle
   - Myös kentän koko rajottuu 38x18, kun näytölle (1920x1080) ei mahdu enempää 50x50 pikseli ruutuja
 - Useampia eri kokosia assetteja
   - Suuremmille kentille voisi ladata pienempiä ruutuja.
