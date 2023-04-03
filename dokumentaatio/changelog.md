## Viikko 3

- Pelin perustoiminnallisuus: main.py alustaa ja käynistää
   - mapGen luokka generoi kartan ja miinat
   - Level käsittelee spritejä/toimintoja, alustaa ja hoitaa ruutujen avaamisen gameloopin kautta
       - Assetteja ja Sprite luokkia graafiseen käyttöliittymään, näitä voi myös parannella
   - Viimeiseksi gameloop hoitaa pelaajan syötteiden lukemisen, jotkun toiminnallisuudet ulkoistettu clock.py, event_queue.py ja renderer.py testaamisen helpottamiseksi
- Ensimmäiset alustavat testit, vain luokille mapGen ja Level
- Peliä on siis mahdollista pelaa, se "jäätyy" kolmeksi sekunniksi, häviön tai voiton takia ja sulkee itsensä. Liputus toiminta puuttuu vielä
