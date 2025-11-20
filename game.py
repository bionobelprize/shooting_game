"""Main game class"""

import pygame
import math
from config import *
from player import Player
from enemy import Enemy
from raycaster import RayCaster
from renderer import Renderer
from map_data import ENEMY_POSITIONS


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pixel FPS Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game components
        self.raycaster = RayCaster(self.screen)
        self.renderer = Renderer(self.screen)
        
        # Game state
        self.state = "menu"  # menu, playing, game_over
        self.menu_selection = 0
        self.menu_options = ["Start Game", "Quit"]
        
        # Game objects
        self.player = None
        self.enemies = []
        
    def new_game(self):
        """Start a new game"""
        # Initialize player at starting position
        self.player = Player(2.5, 2.5, 0)
        
        # Initialize enemies
        self.enemies = []
        for x, y in ENEMY_POSITIONS:
            self.enemies.append(Enemy(x, y))
            
        self.state = "playing"
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    self.handle_menu_input(event.key)
                elif self.state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                    elif event.key == pygame.K_SPACE:
                        self.player_shoot()
                elif self.state == "game_over":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        
    def handle_menu_input(self, key):
        """Handle menu navigation"""
        if key == pygame.K_UP:
            self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
        elif key == pygame.K_DOWN:
            self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
        elif key == pygame.K_RETURN:
            if self.menu_selection == 0:  # Start Game
                self.new_game()
            elif self.menu_selection == 1:  # Quit
                self.running = False
                
    def player_shoot(self):
        """Handle player shooting"""
        current_time = pygame.time.get_ticks() / 1000.0
        if self.player.shoot(current_time):
            # Check if we hit an enemy
            self.check_hit()
            
    def check_hit(self):
        """Check if player's shot hit an enemy"""
        # Find enemy closest to crosshair
        closest_enemy = None
        closest_angle_diff = float('inf')
        
        for enemy in self.enemies:
            if not enemy.alive:
                continue
                
            if enemy.is_visible(self.player.x, self.player.y, self.player.angle):
                # Calculate angle difference
                enemy_angle = enemy.get_angle(self.player.x, self.player.y)
                angle_diff = abs(enemy_angle - self.player.angle)
                
                # Normalize
                while angle_diff > math.pi:
                    angle_diff -= 2 * math.pi
                angle_diff = abs(angle_diff)
                
                # Check if enemy is near center of screen (crosshair)
                if angle_diff < math.radians(5) and angle_diff < closest_angle_diff:
                    closest_enemy = enemy
                    closest_angle_diff = angle_diff
                    
        # Apply damage to closest enemy
        if closest_enemy:
            closest_enemy.take_damage(WEAPON_DAMAGE)
            
    def update(self, dt):
        """Update game state"""
        if self.state == "playing":
            # Update player
            keys = pygame.key.get_pressed()
            self.player.move(keys, dt)
            
            # Check game over conditions
            if not self.player.is_alive():
                self.state = "game_over"
                
            # Check victory condition
            enemies_alive = sum(1 for e in self.enemies if e.alive)
            if enemies_alive == 0:
                self.state = "game_over"
                
    def render(self):
        """Render game"""
        if self.state == "menu":
            self.renderer.render_menu("PIXEL FPS", self.menu_options, self.menu_selection)
            
        elif self.state == "playing":
            # Cast rays and get wall data
            walls = self.raycaster.cast_rays(self.player)
            
            # Render 3D view
            self.raycaster.render_3d(walls, self.player)
            
            # Render enemies
            self.renderer.render_enemies(self.player, self.enemies, walls)
            
            # Render 2D minimap
            self.raycaster.render_2d_minimap(self.player, self.enemies)
            
            # Render HUD
            enemies_alive = sum(1 for e in self.enemies if e.alive)
            self.renderer.render_hud(self.player, enemies_alive)
            
        elif self.state == "game_over":
            # Keep last frame visible
            enemies_alive = sum(1 for e in self.enemies if e.alive)
            won = enemies_alive == 0 and self.player.is_alive()
            self.renderer.render_game_over(won)
            
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS)
            
            self.handle_events()
            self.update(dt)
            self.render()
            
            pygame.display.flip()
            
        pygame.quit()
