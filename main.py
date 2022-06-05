import sys
from time import sleep
from pygame import mixer

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard





class AllienInavasion:
    '''Загальний клас, що керує ресурсами та поведінкою гри'''

    def __init__(self):
        '''Ініціалізувати гру, створити ресурси гри'''

        pygame.init()
        pygame.mixer.music.load("music/background.wav")
        pygame.mixer.music.play(-1)
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Вторгнення прибульців")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Icon
        icon = pygame.image.load("icon2.png")
        pygame.display.set_icon(icon)

        # Створити кнопку play
        self.play_button = Button(self, "PLAY")


    def run_game(self):
        '''Розпочати основний цикл гри'''
        while True:
            self._check_events()
            self.ship.update()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Реагувати на натискання клавіш та подій миші"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Розпочати гру після натискання кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Анулювати ігрову статистику
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Позбавитися надлишку прибульців та куль
            self.aliens.empty()
            self.bullets.empty()

            # Створити новий флот та відцентрувати корабель
            self._create_fleet()
            self.center_ship()

            # Приховати курсор миші
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            bulletSound = mixer.Sound("music/laser.wav")
            bulletSound.play()



    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_alowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        # Наново перемалювати екран на кожній ітерації циклу
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        # Намалювати якщо гра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()


        pygame.display.flip()

    def _create_fleet(self):
        """Створити флот прибульців"""
        # Створити прибульця
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        aviable_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = aviable_space_x // (2 * alien_width)

        # Визначити, яка кількість рядів поміщається на екрані
        ship_height = self.ship.rect.height
        aviable_space_y = (self.settings.screen_height -
                           (3 * alien_height) - ship_height)
        number_rows = aviable_space_y // (2 * alien_height)

        # Створити повний флот прибульців
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                # Створити прибульця та поставити його в ряд
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Первірити, чи котрась із куль не влучила в прибульця
        #   Якщо влучила, позбавитися кулі і прибульця

        colisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)


        if colisions:

            for aliens in colisions.values():
                explosionSound = mixer.Sound("music/explosion.wav")
                explosionSound.play()
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()


        if not self.aliens:
            # Знищити наявні кулі та створити новий флот
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Збільшити рівень
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        # Шукати зіткнення прибульців з кораблем
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Шукати чи котрийсь з прибульців досяг нижнього краю екрана
        self._check_aliens_bottom()


    def center_ship(self):
        self.ship.midbottom = self.ship.screen_rect.midbottom
        self.x = float(self.ship.rect.x)

    def _ship_hit(self):
        """Реагувати на зіткнення прибульця з кораблем"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Позбавитися надлишку прибульців та куль
            self.aliens.empty()
            self.bullets.empty()

            # Створити новий флот і відцентрувати корабель
            self._create_fleet()
            self.center_ship()

            # Paused
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Перевірити чи не досяг якийсь пибудець низу екрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Реагувати так ніби корабель блуо підбито
                self._ship_hit()
                break




if __name__ == "__main__":
    '''Створити екземпляр гри та запустити її'''
    ai = AllienInavasion()
    ai.run_game()