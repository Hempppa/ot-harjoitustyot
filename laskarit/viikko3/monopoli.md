```mermaid
 classDiagram
      Pelilauta "1" --> "40" Ruutu
      Pelilauta "1" --> "2..8" Pelaaja
      Pelilauta "1" --> "2" Noppa
      Ruutu "1" --> "1" Ruutu : Seuraava Ruutu
      Pelaaja "1" --> "1" Pelinappula
      Pelinappula "1" --> "1" Ruutu
      class Pelilauta{
      }
      class Noppa{
      }
      class Pelaaja{
      }
      class Ruutu{
      }
      class Pelinappula{
      }
```
