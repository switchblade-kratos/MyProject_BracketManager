import pygame

class Block:
    def __init__(self, x, y, width, height, color, speed=0):
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.color = color
        self.speed = speed
        self.direction = 1

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))

    def update(self, screen_width):
        if self.speed == 0:
            return

        self.x += self.speed * self.direction
        if self.x <= 20:
            self.x = 20
            self.direction = 1
        elif self.x + self.width >= screen_width - 20:
            self.x = screen_width - 20 - self.width
            self.direction = -1

    def render(self, surface):
        draw_rect = self.rect
        pygame.draw.rect(surface, self.color, draw_rect, border_radius=4)
        pygame.draw.rect(surface, (245, 245, 250), draw_rect, width=2, border_radius=4)

class Debris:
    """A trimmed-off block section that falls and spins out of the arena."""

    def __init__(self, x, y, width, height, color, direction):
        self.x = float(x)
        self.y = float(y)
        self.width = max(1.0, float(width))
        self.height = float(height)
        self.color = color
        self.vx = 1.5 * direction       # drift away from the tower
        self.vy = -1.5                  # small upward pop before falling
        self.angle = 0.0
        self.spin = 4.0 * direction
        self.gravity = 0.45

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.angle += self.spin

    def is_off_screen(self, screen_height):
        return self.y > screen_height + 100

    def render(self, surface):
        piece = pygame.Surface((int(self.width), int(self.height)), pygame.SRCALPHA)
        piece.fill(self.color)
        pygame.draw.rect(piece, (245, 245, 250), piece.get_rect(), width=2)
        rotated = pygame.transform.rotate(piece, self.angle)
        center = (self.x + self.width / 2, self.y + self.height / 2)
        surface.blit(rotated, rotated.get_rect(center=center))
