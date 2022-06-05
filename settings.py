class Settings:
    """Клас для збереження налаштувань"""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (11,40,82)



        # Налаштування кулі
        self.bullet_width = 5
        self.bullet_height = 5
        self.bullet_color = (255, 0, 0)
        self.bullets_alowed = 10

        # Налаштування корабля
        self.ship_limit = 3

        # Налаштування прибульця
        self.fleet_direction = 1

        # Як швидко гра має прискорюватись
        self.speedup_scale = 1.1

        # Як швидко збільшується вартість прибудбців
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Ініціалізація змінних налаштувань"""
        self.bullet_speed = 2.0
        self.ship_speed = 1.5
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10

        #Scoring
        self.alien_points = 50


    def increase_speed(self):
        """Збільшення налаштувань швидкості"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.aliens_points = int(self.alien_points * self.score_scale)
        print(self.aliens_points)







