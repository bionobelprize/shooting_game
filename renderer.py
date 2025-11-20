"""Rendering utilities for HUD and sprites"""

import pygame
import math
from config import *


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def render_hud(self, player, enemies_alive):
        """Render game HUD"""
        # Health bar
        health_text = self.small_font.render(f"Health: {player.health}", True, WHITE)
        self.screen.blit(health_text, (10, SCREEN_HEIGHT - 70))
        
        # Health bar graphic
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = SCREEN_HEIGHT - 45
        
        # Background
        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # Current health
        health_width = int(bar_width * (player.health / PLAYER_HEALTH))
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        # Border
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Ammo
        ammo_text = self.small_font.render(f"Ammo: {player.ammo}", True, WHITE)
        self.screen.blit(ammo_text, (10, SCREEN_HEIGHT - 100))
        
        # Enemies remaining
        enemies_text = self.small_font.render(f"Enemies: {enemies_alive}", True, WHITE)
        self.screen.blit(enemies_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 70))
        
        # Crosshair
        self.draw_crosshair()
        
    def draw_crosshair(self):
        """Draw crosshair in center of screen"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        size = 10
        thickness = 2
        
        # Horizontal line
        pygame.draw.line(self.screen, YELLOW, 
                        (center_x - size, center_y), 
                        (center_x + size, center_y), thickness)
        # Vertical line
        pygame.draw.line(self.screen, YELLOW, 
                        (center_x, center_y - size), 
                        (center_x, center_y + size), thickness)
        # Center dot
        pygame.draw.circle(self.screen, YELLOW, (center_x, center_y), 2)
        
    def render_enemies(self, player, enemies, walls):
        """Render enemies as sprites"""
        visible_enemies = []
        
        for enemy in enemies:
            if not enemy.alive:
                continue
                
            # Calculate enemy position relative to player
            dx = enemy.x - player.x
            dy = enemy.y - player.y
            distance = math.sqrt(dx * dx + dy * dy)
            
            # Get angle to enemy
            enemy_angle = math.atan2(dy, dx)
            angle_diff = enemy_angle - player.angle
            
            # Normalize angle
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
                
            # Check if enemy is in FOV
            half_fov_rad = math.radians(HALF_FOV)
            if abs(angle_diff) < half_fov_rad:
                # Check if enemy is blocked by wall
                blocked = False
                for wall_dist, _, _ in walls:
                    if wall_dist and wall_dist < distance:
                        # Simple occlusion test
                        pass
                        
                if not blocked:
                    visible_enemies.append((distance, angle_diff, enemy))
                    
        # Sort by distance (far to near) for proper rendering
        visible_enemies.sort(reverse=True)
        
        # Render each visible enemy
        for distance, angle_diff, enemy in visible_enemies:
            # Calculate screen position
            screen_x = SCREEN_WIDTH / 2 + (angle_diff / math.radians(HALF_FOV)) * (SCREEN_WIDTH / 2)
            
            # Calculate size based on distance
            sprite_height = min(SCREEN_HEIGHT, (SCREEN_HEIGHT / (distance + 0.0001)) * 0.5)
            sprite_width = sprite_height * 0.8
            
            # Draw simple enemy sprite (rectangle for now)
            sprite_y = (SCREEN_HEIGHT - sprite_height) / 2
            sprite_x = screen_x - sprite_width / 2
            
            # Draw enemy body
            pygame.draw.rect(self.screen, enemy.color, 
                           (sprite_x, sprite_y, sprite_width, sprite_height))
            pygame.draw.rect(self.screen, BLACK, 
                           (sprite_x, sprite_y, sprite_width, sprite_height), 2)
                           
    def render_menu(self, title, options, selected):
        """Render menu screen"""
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font.render(title, True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Options
        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            option_text = self.small_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 50))
            self.screen.blit(option_text, option_rect)
            
    def render_game_over(self, won):
        """Render game over screen"""
        message = "Victory!" if won else "Game Over"
        color = GREEN if won else RED
        
        text = self.font.render(message, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        self.screen.blit(text, text_rect)
        
        # Instructions
        instruction = self.small_font.render("Press ESC for menu", True, WHITE)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(instruction, instruction_rect)
