Clock ja EventQueue sekä tietenkin UI jätetty pois

```mermaid
   classDiagram
	GameEngine "1" -- "1" StartMenu
	GameEngine "1" -- "1" DifficultySelection
	GameEngine "1" -- "1" CustomDifficulty
	GameEngine "1" -- "0..1" GameLoop
	DefaultLoop --|> StartMenu
	DefaultLoop --|> DifficultySelection
	DefaultLoop --|> GameLoop
	DefaultLoop --|> CustomDifficulty
	GameEngine ..> Level
	GameEngine ..> MapGen
	MapGen "1" -- "1" Level
	Level "1" -- "1" GameLoop
	Level "1" -- "0..*" Sprites
	class GameEngine{
	}
	class StartMenu{
	}
	class MapGen{
	}
	class DefaultLoop{
	}
	class DifficultySelection{
	}
	class CustomDifficulty{
	}
	class GameLoop{
	}
	class Level{
	}	
	class Sprites{
	}
```

Sovellus käynnistetään sen jälkeen kun GameEngine on luotu, valitaan valmiiksi asetetuista vaikeuksista keskivaikea, avataan ruutu ja poistutaan pelistä.
(selvyyden vuoksi Clock, Eventqueue, spritet sekä rendererit jätetty pois)

```mermaid
sequenceDiagram
  actor User
  participant GameEngine
  participant StartMenu
  participant DifficultySelection
  participant MapGen
  participant Level
  participant GameLoop
  User->>GameEngine: käynnistää main()
  GameEngine->>StartMenu: siirtyy valikkoon start(MenuRenderer())
  StartMenu->>StartMenu: piirtää näkymän render()
  User->>StartMenu: painaa "Default difficulties" nappia
  StartMenu-->>GameEngine: palauttaa vastaavan arvon 0
  GameEngine->>DifficultySelection: siirtyy valikkon start(DiffRenderer())
  DifficultySelection->>DifficultySelection: render()
  User->>DifficultySelection: valitsee "medium" vaikeustason
  DifficultySelection-->>GameEngine: palauttaa vastaavan arvon 1
  GameEngine->>MapGen: luo kentän MapGen(16,16,40)
  MapGen-->>GameEngine: palauttaa kentän numero esityksen
  GameEngine->>Level: Level(MapGen(16,16,40))
  GameEngine->>GameLoop: start(Level, LevelRenderer(Level))
  GameLoop->>GameLoop: render()
  User->>GameLoop: painaa m1 kohdassa (21,38)
  GameLoop->>Level: ilmoittaa painalluksesta cellClicked((True, False, False), (21,38)) 
  Level-->>GameLoop: peli jatkuu, palauttaa 10
  GameLoop->>GameLoop: render()
  User->>GameLoop: painaa raksista
  GameLoop-->>GameEngine: -1
```
