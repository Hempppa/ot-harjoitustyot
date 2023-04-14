```mermaid
   classDiagram
	Menu "1" -- "0..1" StartMenu
	Menu "1" -- "0..1" DifficultySelection
	Menu "1" -- "0..1" GameLoop
	DefaulLoop --|> StartMenu
	DefaulLoop --|> DifficultySelection
	DefaulLoop --|> GameLoop
	StartMenu "1" -- "1" Clock
	DifficultySelection "1" -- "1" Clock
	GameLoop "1" -- "1" Clock
	StartMenu "1" -- "1" EventQueue
	DifficultySelection "1" -- "1" EventQueue
	GameLoop "1" -- "1" EventQueue
	MapGen "1" -- "1" Level
	Level "1" -- "1" GameLoop
	Level "1" -- "0..*" CellZero
	Level "1" -- "0..*" CellOne
	Level "1" -- "0..*" CellTwo
	Level "1" -- "0..*" CellThree
	Level "1" -- "0..*" CellFour
	Level "1" -- "0..*" CellFive
	Level "1" -- "0..*" CellSix
	Level "1" -- "0..*" CellSeven
	Level "1" -- "0..*" CellEight
	Level "1" -- "0..*" CellNine
	Level "1" -- "0..*" Flag
	Level "1" -- "0..*" Highlight
	class Menu{
	}
	class StartMenu{
	}
	class Clock{
	}
	class EventQueue{
	}
	class ui {
	}
	class MapGen{
	}
	class DefaultLoop{
	}
	class DifficultySelection{
	}
	class GameLoop{
	}
	class Level{
	}	
```
