```mermaid
   classDiagram
	Menu "1" -- "0..1" StartMenu
	Menu "1" -- "0..1" DifficultySelection
	Menu "1" -- "0..1" GameLoop
	DefaultLoop --|> StartMenu
	DefaultLoop --|> DifficultySelection
	DefaultLoop --|> GameLoop
	StartMenu "1" -- "1" Clock
	DifficultySelection "1" -- "1" Clock
	GameLoop "1" -- "1" Clock
	StartMenu "1" -- "1" EventQueue
	DifficultySelection "1" -- "1" EventQueue
	GameLoop "1" -- "1" EventQueue
	StartMenu "1" -- "1" ui
	DifficultySelection "1" -- "1" ui
	GameLoop "1" -- "1" ui
	MapGen "1" -- "1" Level
	Level "1" -- "1" GameLoop
	Level "1" -- "0..*" Sprites
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
