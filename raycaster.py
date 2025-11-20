"""Raycasting engine for 3D rendering"""

import pygame
import math
from config import *
from map_data import GAME_MAP


class RayCaster:
    def __init__(self, screen):
        self.screen = screen
        
    def cast_rays(self, player):
        """Cast rays for 3D rendering"""
        walls = []
        
        # Starting angle for raycasting
        ray_angle = player.angle - math.radians(HALF_FOV)
        
        for ray in range(NUM_RAYS):
            # Cast single ray
            depth, side = self.cast_ray(player.x, player.y, ray_angle)
            
            # Calculate wall height based on distance
            if depth:
                # Fix fish-eye effect
                depth *= math.cos(player.angle - ray_angle)
                wall_height = min(SCREEN_HEIGHT, (SCREEN_HEIGHT / (depth + 0.0001)))
                
                walls.append((depth, wall_height, side))
            else:
                walls.append((MAX_DEPTH, 0, 0))
                
            ray_angle += math.radians(DELTA_ANGLE)
            
        return walls
        
    def cast_ray(self, ox, oy, angle):
        """Cast a single ray and return depth and side hit"""
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        
        # Raycasting
        for depth in range(1, int(MAX_DEPTH * 100)):
            depth_f = depth / 100.0
            target_x = ox + depth_f * cos_a
            target_y = oy + depth_f * sin_a
            
            col = int(target_x)
            row = int(target_y)
            
            # Check if ray hit a wall
            if 0 <= row < len(GAME_MAP) and 0 <= col < len(GAME_MAP[0]):
                if GAME_MAP[row][col] == 1:
                    # Determine which side was hit for shading
                    side = 0 if abs(target_x - col - 0.5) > abs(target_y - row - 0.5) else 1
                    return depth_f, side
                    
        return None, None
        
    def render_3d(self, walls, player):
        """Render 3D view using wall data"""
        # Draw ceiling
        pygame.draw.rect(self.screen, DARK_GRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        
        # Draw floor
        pygame.draw.rect(self.screen, GRAY, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        
        # Draw walls
        wall_width = SCREEN_WIDTH / NUM_RAYS
        
        for i, (depth, height, side) in enumerate(walls):
            if height > 0:
                # Calculate color based on depth
                color_index = min(4, int(depth / (MAX_DEPTH / 5)))
                base_color = WALL_COLORS[color_index]
                
                # Darken one side for better depth perception
                if side == 1:
                    color = tuple(max(0, c - 30) for c in base_color)
                else:
                    color = base_color
                
                # Draw wall slice
                x = i * wall_width
                y = (SCREEN_HEIGHT - height) / 2
                pygame.draw.rect(self.screen, color, (x, y, wall_width + 1, height))
                
    def render_2d_minimap(self, player, enemies):
        """Render 2D minimap"""
        minimap_scale = 20
        minimap_offset_x = 10
        minimap_offset_y = 10
        
        # Draw map
        for row in range(len(GAME_MAP)):
            for col in range(len(GAME_MAP[0])):
                color = WHITE if GAME_MAP[row][col] == 1 else BLACK
                x = minimap_offset_x + col * minimap_scale
                y = minimap_offset_y + row * minimap_scale
                pygame.draw.rect(self.screen, color, (x, y, minimap_scale - 1, minimap_scale - 1))
                
        # Draw enemies on minimap
        for enemy in enemies:
            if enemy.alive:
                ex = minimap_offset_x + int(enemy.x * minimap_scale)
                ey = minimap_offset_y + int(enemy.y * minimap_scale)
                pygame.draw.circle(self.screen, RED, (ex, ey), 3)
                
        # Draw player on minimap
        px = minimap_offset_x + int(player.x * minimap_scale)
        py = minimap_offset_y + int(player.y * minimap_scale)
        pygame.draw.circle(self.screen, GREEN, (px, py), 4)
        
        # Draw player direction
        dir_length = 15
        end_x = px + int(dir_length * math.cos(player.angle))
        end_y = py + int(dir_length * math.sin(player.angle))
        pygame.draw.line(self.screen, GREEN, (px, py), (end_x, end_y), 2)
