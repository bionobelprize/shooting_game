"""Player class for the FPS game"""

import pygame
import math
from config import *
from map_data import GAME_MAP


class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.health = PLAYER_HEALTH
        self.ammo = 100
        self.last_shot_time = 0
        
    def move(self, keys, dt):
        """Handle player movement"""
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        
        dx, dy = 0, 0
        speed = PLAYER_SPEED * dt
        
        # Forward/backward movement
        if keys[pygame.K_w]:
            dx += speed * cos_a
            dy += speed * sin_a
        if keys[pygame.K_s]:
            dx -= speed * cos_a
            dy -= speed * sin_a
            
        # Strafe left/right
        if keys[pygame.K_a]:
            dx += speed * sin_a
            dy -= speed * cos_a
        if keys[pygame.K_d]:
            dx -= speed * sin_a
            dy += speed * cos_a
            
        # Check collision before moving
        self.check_wall_collision(dx, dy)
        
        # Rotation
        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * dt
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * dt
            
    def check_wall_collision(self, dx, dy):
        """Check if player can move to new position"""
        scale = PLAYER_SIZE / 2
        
        # Check new position
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check if new position is within map bounds and not a wall
        if self.check_pos(new_x, new_y):
            # Check corners for smoother collision
            if (self.check_pos(new_x + scale, new_y + scale) and
                self.check_pos(new_x - scale, new_y + scale) and
                self.check_pos(new_x + scale, new_y - scale) and
                self.check_pos(new_x - scale, new_y - scale)):
                self.x = new_x
                self.y = new_y
                
    def check_pos(self, x, y):
        """Check if position is valid (not a wall)"""
        map_x = int(x)
        map_y = int(y)
        
        if 0 <= map_y < len(GAME_MAP) and 0 <= map_x < len(GAME_MAP[0]):
            return GAME_MAP[map_y][map_x] == 0
        return False
        
    def shoot(self, current_time):
        """Handle shooting"""
        if self.ammo > 0 and (current_time - self.last_shot_time) > WEAPON_FIRE_RATE:
            self.ammo -= 1
            self.last_shot_time = current_time
            return True
        return False
        
    def take_damage(self, damage):
        """Apply damage to player"""
        self.health = max(0, self.health - damage)
        
    def is_alive(self):
        """Check if player is alive"""
        return self.health > 0
