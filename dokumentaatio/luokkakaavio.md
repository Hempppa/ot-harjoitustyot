```mermaid
   classDiagram
	Menu "1" -- "1" StartMenu
	Menu "1" -- "1" DifficultySelection
	Menu "1" -- "0..1" GameLoop
	DefaultLoop --|> StartMenu
	DefaultLoop --|> DifficultySelection
	DefaultLoop --|> GameLoop
	Menu "1" -- "1" Clock
	Menu "1" -- "1" EventQueue
	Menu ..> Level
	Menu ..> MapGen
	StartMenu "1" -- "1" Clock
	DifficultySelection "1" -- "1" Clock
	GameLoop "1" -- "1" Clock
	StartMenu "1" -- "1" EventQueue
	DifficultySelection "1" -- "1" EventQueue
	GameLoop "1" -- "1" EventQueue
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
	class Sprites{
	}
```
