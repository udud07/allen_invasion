class GameStats:
    """Відстежування статистики гри"""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # Розпочати гру в неактивному стані
        self.game_active = False

        # Рекорд не анульовується
        self.high_score = 0

    def reset_stats(self):
        """"Ініціалізація статистики, що може змінюватися впродовж гри"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1