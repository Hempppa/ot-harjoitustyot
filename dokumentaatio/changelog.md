## Viikko 3

- Pelin perustoiminnallisuus: main.py alustaa ja käynistää
   - mapGen luokka generoi kartan ja miinat
   - Level käsittelee spritejä/toimintoja, alustaa ja hoitaa ruutujen avaamisen gameloopin kautta
       - Assetteja ja Sprite luokkia graafiseen käyttöliittymään, näitä voi myös parannella
   - Viimeiseksi gameloop hoitaa pelaajan syötteiden lukemisen, jotkun toiminnallisuudet ulkoistettu clock.py, event_queue.py ja renderer.py testaamisen helpottamiseksi
- Ensimmäiset alustavat testit, vain luokille mapGen ja Level
- Peliä on siis mahdollista pelaa, se "jäätyy" kolmeksi sekunniksi, häviön tai voiton takia ja sulkee itsensä. Liputus toiminta puuttuu vielä

## Viikko 4

- Peliin liputus mekaniikka
   - Toimii niin kuin pitäisi, eli lippuja vain miinojen verran ja liputettua ruutua ei saa avattua
- Muita näkymiä peliin
   - Aloitusruutu; Hetkellä vain välivaihe, mutta myöhemmin valikko täydentyy
   - Vaikeustaso valikoima; Nyt pelissä voi valita kolmen vaikeustason välillä 
- pylint käyttöön


## Viikko 5

- Aloitusruudun custom vaikeudet käyttöön
   - Tällä valinnalla pelaaja voi syöttää haluamansa kentän koon (leveys 1--38, korkeus 1--18)
       - Jos lisään peliin resoluution muuttamisen, niin mahdollinen kentän koko saattaa kasvaa
   - Myös miinojen määrän saa valita (1--kentänkoko eli max 798)
- Pelin loppuessa aiheutuvan hiiribugin korjaus (m1 nappi pysyi pohjaan painettuna)
- src kansion kattaus (vko4 unohtui päivittää): 
   - MapGen ja Level sekä Clock ja Eventqueue säilyneet samana
   - GameEngine(main.py), vastaa koko pelin toiminnasta luokkien välillä
   - input_handlers.py tiedosto sisältää valtaosan sovelluslogiikasta
       - DefaultLoop, pohja sovelluslogiikka luokille
           - StartMenu ja DifficultySelection valikot tämän muotoisia
       - GameLoop, muodostaa varsinaisen pelilogiikan Level luokan kanssa
       - CustomDifficulty, vastaa muokatun vaikeustason valikosta
   - UI kansiossa ovat valikkoja ja peliä vastaavat Käyttöliittymät (-rendererit)
   - Assets kansiossa ovat pelin käyttämät kuvatiedostot 
   - Sprites kansiossa ovat asseteista luokat joita Level käyttää
