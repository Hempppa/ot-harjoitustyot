import pygame

class LevelRenderer:
    """Piirtää varsinaisen pelinäkymän

    Attributes:
        _display: ikkuna johon näkymä piirretään
        _level: Level Luokan olio, joka sisältää kaikki piirrettävät Spritet
    """
    def __init__(self, display, level):
        """Vain levelin Spritet ja display tarvitaan

        Args:
            display: ikkuna johon näkymä piirretään
            level: Level olio
        """
        self._display = display
        self._level = level

    def get_level(self):
        """input_handleri set_rendererin mukana pyytää leveliä johon muutokset tehdään

        Returns:
            level: palauttaa rendererin käyttämän levelin
        """
        return self._level

    def render(self):
        """Piirtää kaikki _display ikkunaan kaikki levelin spritet
        """
        self._level.all_cells.draw(self._display)
        self._level.cell_covers.draw(self._display)
        self._level.flags.draw(self._display)
        pygame.display.update()
