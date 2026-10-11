import random
import pygame
from game.block import Block, Debris


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_height = 28
        self.base_width = 180

        # Perfect placement tuning
        self.perfect_tolerance = 6      # max pixel offset that still counts as "perfect"
        self.perfect_bonus = 2          # extra points awarded for a perfect drop
        self.restore_amount = 10        # width regained per perfect drop once a streak is going

        # Atmospheric sky stages as (top color, bottom color), from ground level to space
        self.sky_stages = [
            ((70, 130, 190), (150, 195, 230)),   # Daytime
            ((220, 110, 90), (250, 180, 110)),   # Sunset
            ((80, 50, 120), (190, 90, 120)),     # Twilight
            ((15, 20, 55), (40, 50, 100)),       # Night
            ((2, 2, 10), (15, 10, 35)),          # Upper atmosphere / space
        ]
        self.floors_per_stage = 8

        self.font_title = pygame.font.SysFont(None, 38)
        self.font_hud = pygame.font.SysFont(None, 28)
        self.font_big = pygame.font.SysFont(None, 46)

        self.reset()

    def get_color(self, index):
        palette = [
            (230, 75, 75),   # Crimson
            (240, 140, 45),  # Orange
            (245, 210, 50),  # Gold
            (60, 195, 110),  # Green
            (50, 150, 240),  # Blue
            (165, 80, 225),  # Purple
        ]
        return palette[index % len(palette)]

    def reset(self):
        self.score = 0
        self.game_over = False
        self.perfect_streak = 0
        self.perfect_timer = 0
        self.debris = []
        self.sky_progress = 0.0

        base_x = (self.width - self.base_width) // 2
        base_y = self.height - 60
        base_block = Block(base_x, base_y, self.base_width, self.block_height, self.get_color(0), speed=0)
        self.stack = [base_block]

        self.spawn_active_block()

    def spawn_active_block(self):
        top_block = self.stack[-1]
        next_y = top_block.y - self.block_height - 4
        speed = min(10.0, 4.5 + (len(self.stack) * 0.35))
        color = self.get_color(len(self.stack))

        start_x = 25 if random.choice([True, False]) else self.width - 25 - top_block.width
        self.active_block = Block(start_x, next_y, top_block.width, self.block_height, color, speed=speed)

    def drop_block(self):
        if self.game_over:
            return

        top_block = self.stack[-1]
        act = self.active_block

        left = max(act.x, top_block.x)
        right = min(act.x + act.width, top_block.x + top_block.width)
        overlap = right - left
        
        is_successful_drop = overlap > 0
        
        if is_successful_drop:
            is_perfect = abs(act.x - top_block.x) <= self.perfect_tolerance

            if is_perfect:
                # Snap flush onto the tower without trimming
                self.perfect_streak += 1
                new_x = top_block.x
                new_width = top_block.width

                # Two or more perfects in a row slowly restore lost width
                if self.perfect_streak >= 2 and new_width < self.base_width:
                    grow = min(self.restore_amount, self.base_width - new_width)
                    new_width += grow
                    new_x -= grow / 2
                    new_x = max(20.0, min(new_x, self.width - 20 - new_width))

                new_block = Block(new_x, act.y, new_width, self.block_height, act.color, speed=0)
                self.score += 1 + self.perfect_bonus
                self.perfect_timer = 60  # show the prompt for ~1 second
            else:
                self.perfect_streak = 0
                trimmed_width = max(10.0, overlap)
                new_block = Block(left, act.y, trimmed_width, self.block_height, act.color, speed=0)
                self.score += 1

                # Spawn falling debris for whichever side(s) hung over the edge
                if act.x < left:
                    self.debris.append(Debris(act.x, act.y, left - act.x, self.block_height, act.color, -1))
                act_right = act.x + act.width
                if act_right > right:
                    self.debris.append(Debris(right, act.y, act_right - right, self.block_height, act.color, 1))

            self.stack.append(new_block)

            if new_block.y < 180:
                shift_amount = self.block_height + 4
                for b in self.stack:
                    b.y += shift_amount
                for d in self.debris:
                    d.y += shift_amount

            self.spawn_active_block()
        else:
            self.game_over = True

    def handle_event(self, event):
        if self.game_over:
            if (event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_r)) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                self.reset()
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.drop_block()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.drop_block()

    def update(self):
        if not self.game_over:
            self.active_block.update(self.width)

        if self.perfect_timer > 0:
            self.perfect_timer -= 1

        for d in self.debris:
            d.update()
        self.debris = [d for d in self.debris if not d.is_off_screen(self.height)]

        # Ease the sky toward the stage matching the current tower height
        target = min((len(self.stack) - 1) / self.floors_per_stage, len(self.sky_stages) - 1)
        self.sky_progress += (target - self.sky_progress) * 0.03

    @staticmethod
    def lerp_color(a, b, t):
        return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

    def draw_sky(self, screen):
        stage = min(int(self.sky_progress), len(self.sky_stages) - 2)
        t = self.sky_progress - stage
        top_a, bottom_a = self.sky_stages[stage]
        top_b, bottom_b = self.sky_stages[stage + 1]
        top = self.lerp_color(top_a, top_b, t)
        bottom = self.lerp_color(bottom_a, bottom_b, t)

        for y in range(self.height):
            pygame.draw.line(screen, self.lerp_color(top, bottom, y / self.height), (0, y), (self.width, y))

    def render(self, screen):
        self.draw_sky(screen)

        title_surf = self.font_title.render("Skyscraper Stack", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 16))

        tower_height = len(self.stack) - 1
        score_surf = self.font_hud.render(f"Height: {tower_height}   Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 54))

        for b in self.stack:
            b.render(screen)

        for d in self.debris:
            d.render(screen)

        if not self.game_over:
            self.active_block.render(screen)

        if self.perfect_timer > 0 and not self.game_over:
            label = f"PERFECT! +{self.perfect_bonus}"
            if self.perfect_streak >= 2:
                label += f"  x{self.perfect_streak}"
            perfect_surf = self.font_big.render(label, True, (255, 240, 120))
            perfect_surf.set_alpha(min(255, self.perfect_timer * 8))
            rise = (60 - self.perfect_timer) // 3
            screen.blit(perfect_surf, (self.width // 2 - perfect_surf.get_width() // 2, 100 - rise))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 195))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render("TOWER COLLAPSED!", True, (240, 75, 75))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 40))

            final_surf = self.font_hud.render(f"Final Height: {tower_height}   Score: {self.score}", True, (255, 255, 255))
            screen.blit(final_surf, (self.width // 2 - final_surf.get_width() // 2, self.height // 2 + 10))

            restart_surf = self.font_hud.render("Press [Space] or [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))
