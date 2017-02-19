import pygame

from level import dir_vectors, TILE_W, TILE_H

class Character(pygame.sprite.DirtySprite):
    def __init__(self, level, frames, containers, pos=(0, 0)):
        # frames: 6 images (front, back, left, run front, run back, run left)
        # containers: list of sprite groups to join
        pygame.sprite.DirtySprite.__init__(self, *containers)
        self.x, self.y = pos
        self.level = level
        self.moving_delta = None  # non null = moving
        self.moving_from = None
        self.move_speed = 1.0 # duration of move_player animation, in seconds
        self.dir = 'S'
        self.standing_frames = {
            'S': [frames[0]],
            'N': [frames[1]],
            'W': [frames[2]],
            'E': [pygame.transform.flip(frames[2], True, False)]
            }
        self.moving_frames = {
            'S': [frames[3], pygame.transform.flip(frames[3], True, False)],
            'N': [frames[4], pygame.transform.flip(frames[4], True, False)],
            'W': [frames[5]],
            'E': [pygame.transform.flip(frames[5], True, False)]
            }
        self.image = self.standing_frames[self.dir][0]
        self.rect = pygame.Rect(pos[0] * TILE_W, pos[1] * TILE_H, TILE_W, TILE_H)
        self.animation_index = 0
    
    def try_moving_towards(self, direction):
        x, y = self.x, self.y
        if(self.level.is_walkable(x, y, direction) and not self.moving_delta):
            self.move_towards(direction)    

    def move_towards(self, direction):
        self.dir = direction
        dx, dy = dir_vectors[direction]
        self.moving_from = self.x, self.y
        self.moving_delta = dx, dy
        self.x += dx
        self.y += dy
        self.animation_index = 0
        
        
    def update(self, fps):
        if self.moving_delta:
            dx, dy = self.moving_delta
            if self.animation_index >= int(fps * self.move_speed): # animation is over
                self.animation_index = 0
                self.moving_delta = None
                self.moving_from = None
            else: # animation is not over yet
                if self.animation_index == 0:
                    self.image = self.standing_frames[self.dir][0]
                elif self.animation_index == int(fps * self.move_speed / 4):
                    # alternate legs/arms when moving N or S
                    if len(self.moving_frames[self.dir]) > 1:
                        self.image = self.moving_frames[self.dir][self.y % 2]
                    else:
                        self.image = self.moving_frames[self.dir][0]
                elif self.animation_index == int(fps * self.move_speed * 3 / 4):
                    self.image = self.standing_frames[self.dir][0]
                self.animation_index += 1
                
                old_x, old_y = self.moving_from
                xx = old_x + dx * float(self.animation_index) / fps / self.move_speed
                yy = old_y + dy * float(self.animation_index) / fps / self.move_speed
                self.rect.x = int(xx * TILE_W)
                self.rect.y = int(yy * TILE_H)
            
