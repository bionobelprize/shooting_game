"""Enemy class for the FPS game"""

import math
from config import *


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = ENEMY_HEALTH
        self.alive = True
        self.size = 0.3
        self.color = RED
        
    def get_distance(self, player_x, player_y):
        """Calculate distance from player"""
        dx = self.x - player_x
        dy = self.y - player_y
        return math.sqrt(dx * dx + dy * dy)
        
    def get_angle(self, player_x, player_y):
        """Calculate angle from player"""
        return math.atan2(self.y - player_y, self.x - player_x)
        
    def take_damage(self, damage):
        """Apply damage to enemy"""
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            
    def is_visible(self, player_x, player_y, player_angle):
        """Check if enemy is in player's view"""
        enemy_angle = self.get_angle(player_x, player_y)
        angle_diff = enemy_angle - player_angle
        
        # Normalize angle difference to -pi to pi
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi
            
        # Check if within FOV
        half_fov_rad = math.radians(HALF_FOV)
        return abs(angle_diff) < half_fov_rad
