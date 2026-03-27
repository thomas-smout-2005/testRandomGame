import turtle
import time
import random
import math

# ==========================================
# 1. CORE ENGINE & MANAGERS
# ==========================================
pots = [
    {"x": -200, "width": 100, "points": 25, "color": "blue"},
    {"x": 0,    "width": 120, "points": 100, "color": "gold"},
    {"x": 200,  "width": 100, "points": 25, "color": "blue"}
]

class GameManager:
    def __init__(self):
        self.state = "PLAYING" 
        self.level = 1
        self.score = 0
        self.attempts_left = 10
        self.ball_value_multiplier = 1
        self.screen_width = 800
        self.screen_height = 600
        
        self.ui = turtle.Turtle()
        self.ui.hideturtle()
        self.ui.color("white")
        self.ui.penup()
        
        self.pot_drawer = turtle.Turtle()
        self.pot_drawer.hideturtle()
        self.pot_drawer.speed(0)
        
    def draw_pots(self):
        self.pot_drawer.clear()
        floor_y = -(self.screen_height / 2)
        
        for pot in pots:
            self.pot_drawer.penup()
            self.pot_drawer.goto(pot["x"] - pot["width"]/2, floor_y)
            self.pot_drawer.color(pot["color"])
            self.pot_drawer.pendown()
            self.pot_drawer.begin_fill()
            for _ in range(2):
                self.pot_drawer.forward(pot["width"])
                self.pot_drawer.left(90)
                self.pot_drawer.forward(30)
                self.pot_drawer.left(90)
            self.pot_drawer.end_fill()
            self.pot_drawer.penup()
            
            self.pot_drawer.goto(pot["x"], floor_y + 5)
            self.pot_drawer.color("white")
            self.pot_drawer.write(f"{pot['points']}", align="center", font=("Arial", 14, "bold"))

    def load_level(self):
        global obstacles, pegs, black_holes, all_balls, particles
        
        for ball in all_balls: 
            ball.shape.hideturtle()
            ball.trail_pen.clear()
        for p in particles: p.shape.hideturtle()
        for obs in obstacles: obs.shape.hideturtle()
        for peg in pegs: peg.shape.hideturtle()
        for bh in black_holes: bh.shape.hideturtle()
        
        all_balls.clear()
        particles.clear()
        obstacles.clear()
        pegs.clear()
        black_holes.clear()
        
        if self.level == 5:
            self.screen_width = 1000
            self.screen_height = 800
            screen.setup(width=self.screen_width, height=self.screen_height)
            
        self.draw_pots()
            
        if self.level == 1:
            obstacles.append(MovingObstacle(100, 3, 6))
        elif self.level == 2:
            pegs.append(Peg(0, 50, 20))
            pegs.append(Peg(-100, 100, 20))
            pegs.append(Peg(100, 100, 20))
        elif self.level == 3:
            obstacles.append(MovingObstacle(150, 4, 5))
            pegs.append(Peg(0, 0, 30))
        elif self.level == 4:
            black_holes.append(BlackHole(0, 100, 3500))  
            black_holes.append(BlackHole(-150, -50, 2500)) 
        elif self.level == 5:
            obstacles.append(MovingObstacle(200, 5, 8))
            pegs.append(Peg(-200, 0, 40))
            pegs.append(Peg(200, 0, 40))
            black_holes.append(BlackHole(0, -100, 6000)) 
            
        self.update_ui()

    def update_ui(self):
        self.ui.clear()
        if self.state == "PLAYING":
            self.ui.goto(0, self.screen_height/2 - 40)
            self.ui.write(f"LEVEL {self.level} | SCORE: {self.score} | BALLS: {self.attempts_left}", align="center", font=("Arial", 16, "bold"))
        elif self.state == "SHOP":
            
            self.ui.goto(0, 0)
            self.ui.write(f"SHOP (Score: {self.score})\n\n1: Buy +3 Extra Balls (50 pts)\n2: Upgrade Score Multiplier (100 pts)\n3: Next Level", align="center", font=("Arial", 20, "bold"))

# ==========================================
# 2. ENTITY CLASSES (Blueprints)
# ==========================================
class Particle:
    def __init__(self, x, y, color):
        self.shape = turtle.Turtle()
        self.shape.shape("circle")
        self.shape.shapesize(0.2, 0.2)
        self.shape.color(color)
        self.shape.penup()
        self.shape.goto(x, y)
        self.speed_x = random.uniform(-5, 5)
        self.speed_y = random.uniform(-5, 5)
        self.life = 20 

    def move(self):
        self.shape.goto(self.shape.xcor() + self.speed_x, self.shape.ycor() + self.speed_y)
        self.life -= 1

class Peg:
    def __init__(self, x, y, radius):
        self.shape = turtle.Turtle()
        self.shape.shape("circle")
        self.shape.color("purple")
        self.shape.shapesize(radius / 10, radius / 10)
        self.shape.penup()
        self.shape.goto(x, y)
        self.radius = radius

class BlackHole:
    def __init__(self, x, y, strength):
        self.shape = turtle.Turtle()
        self.shape.shape("circle")
        self.shape.color("dark red")
        self.shape.shapesize(2, 2)
        self.shape.penup()
        self.shape.goto(x, y)
        self.strength = strength 

class MovingObstacle:
    def __init__(self, start_y, speed_x, width_stretch):
        self.shape = turtle.Turtle()
        self.shape.shape("square")
        self.shape.color("white")
        self.shape.shapesize(stretch_wid=1, stretch_len=width_stretch) 
        self.shape.penup()
        self.shape.goto(0, start_y)
        self.speed_x = speed_x
        self.width = width_stretch * 20
        self.height = 20

    def move(self, screen_width):
        new_x = self.shape.xcor() + self.speed_x
        self.shape.setx(new_x)
        if new_x > (screen_width / 2 - self.width / 2) or new_x < -(screen_width / 2 - self.width / 2):
            self.speed_x *= -1

class BouncyBall:
    def __init__(self, color, start_x, start_y, speed_x, speed_y):
        self.shape = turtle.Turtle()
        self.shape.shape("circle")
        self.r, self.g, self.b = color
        self.base_color = color
        self.shape.color(self.base_color)
        self.shape.penup()
        self.shape.goto(start_x, start_y)
        
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = 15
        self.is_dead = False 
        
        self.history = []
        self.trail_pen = turtle.Turtle()
        self.trail_pen.hideturtle()
        self.trail_pen.pensize(3)

    def draw_trail(self):
        self.trail_pen.clear()
        self.history.append((self.shape.xcor(), self.shape.ycor()))
        if len(self.history) > 8:
            self.history.pop(0)
            
        for i in range(len(self.history) - 1):
            fade_factor = (i + 1) / len(self.history)
            r = int(self.r * fade_factor)
            g = int(self.g * fade_factor)
            b = int(self.b * fade_factor)
            
            self.trail_pen.color((r, g, b))
            self.trail_pen.penup()
            self.trail_pen.goto(self.history[i])
            self.trail_pen.pendown()
            self.trail_pen.goto(self.history[i+1])

    def explode(self):
        for _ in range(12):
            particles.append(Particle(self.shape.xcor(), self.shape.ycor(), self.base_color))

    def move(self, screen_width, screen_height):
        self.speed_y -= 0.3
        
        for hole in black_holes:
            dx = hole.shape.xcor() - self.shape.xcor()
            dy = hole.shape.ycor() - self.shape.ycor()
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 10: 
                force = hole.strength / (dist**2)
                self.speed_x += (dx / dist) * force
                self.speed_y += (dy / dist) * force

        new_x = self.shape.xcor() + self.speed_x
        new_y = self.shape.ycor() + self.speed_y
        self.shape.goto(new_x, new_y)
        self.draw_trail()
        
        if new_x > (screen_width / 2 - self.radius) or new_x < -(screen_width / 2 - self.radius):
            self.speed_x *= -1

        floor_level = -(screen_height / 2 - self.radius)
        
        over_pot = False
        for pot in pots:
            if abs(self.shape.xcor() - pot["x"]) < (pot["width"] / 2):
                over_pot = True
                break

        if self.shape.ycor() < floor_level:
            if over_pot:
                if self.shape.ycor() < floor_level - 20:
                    for pot in pots:
                        if abs(self.shape.xcor() - pot["x"]) < (pot["width"] / 2):
                            health_multiplier = self.radius / 15.0 
                            base_pts = pot["points"] * health_multiplier
                            final_pts = int(base_pts * game.ball_value_multiplier) 
                            
                            game.score += max(1, final_pts) 
                            self.explode()
                            self.is_dead = True
                            game.update_ui()
                            break
            else:
                self.shape.sety(floor_level)
                self.speed_y *= -0.8 
                self.speed_x *= 0.95 
                
                if abs(self.speed_y) < 0.6:
                    self.speed_y = 0
                    self.speed_x *= 0.9
                    if abs(self.speed_x) < 0.1:
                        self.speed_x = 0
                        
                        self.is_dead = True

    def collide_with_peg(self, peg):
        dx = self.shape.xcor() - peg.shape.xcor()
        dy = self.shape.ycor() - peg.shape.ycor()
        dist = math.sqrt(dx**2 + dy**2)
        if dist < (self.radius + peg.radius):
            overlap = (self.radius + peg.radius) - dist
            self.shape.setx(self.shape.xcor() + (dx/dist) * overlap)
            self.shape.sety(self.shape.ycor() + (dy/dist) * overlap)
            self.speed_x = (dx / dist) * 5
            self.speed_y = (dy / dist) * 5

    def collide_with_obstacle(self, obs):
        dx = self.shape.xcor() - obs.shape.xcor()
        dy = self.shape.ycor() - obs.shape.ycor()
        
        if abs(dx) < (obs.width / 2 + self.radius) and abs(dy) < (obs.height / 2 + self.radius):
            self.speed_y *= -1
            if dy > 0:
                self.shape.sety(obs.shape.ycor() + obs.height / 2 + self.radius)
            else:
                self.shape.sety(obs.shape.ycor() - obs.height / 2 - self.radius)

# ==========================================
# SETUP & INPUTS
# ==========================================
screen = turtle.Screen()
screen.title("Physics Game Engine")
screen.bgcolor("black")
screen.colormode(255)
screen.tracer(0)

game = GameManager()
all_balls = []
particles = []
obstacles = []
pegs = []
black_holes = []

def spawn_ball(x, y):
    if game.state == "PLAYING" and game.attempts_left > 0 and y > 0:
        colors = [(255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 0)]
        all_balls.append(BouncyBall(random.choice(colors), x, y, random.randint(-4, 4), 0))
        game.attempts_left -= 1
        game.update_ui()

def shop_buy_balls():
    if game.state == "SHOP" and game.score >= 50:
        game.score -= 50
        game.attempts_left += 3
        game.update_ui()

def shop_buy_multiplier():
    if game.state == "SHOP" and game.score >= 100:
        game.score -= 100
        game.ball_value_multiplier += 0.5
        game.update_ui()

def shop_next_level():
    if game.state == "SHOP":
        game.level += 1
        game.attempts_left += 10 
        game.state = "PLAYING"
        game.load_level()

screen.onclick(spawn_ball)
screen.onkeypress(shop_buy_balls, "1")
screen.onkeypress(shop_buy_multiplier, "2")
screen.onkeypress(shop_next_level, "3")
screen.listen()

game.load_level()

# ==========================================
# MAIN LOOP
# ==========================================
try:
    while True:
        if game.state == "PLAYING":
            for obs in obstacles:
                obs.move(game.screen_width)
            
            for p in particles[:]:
                p.move()
                if p.life <= 0:
                    p.shape.hideturtle()
                    particles.remove(p)

            for ball in all_balls:
                ball.move(game.screen_width, game.screen_height)
                for peg in pegs:
                    ball.collide_with_peg(peg)
                for obs in obstacles:
                    ball.collide_with_obstacle(obs)

            for ball in all_balls[:]:
                if ball.is_dead:
                    ball.shape.hideturtle()
                    ball.trail_pen.clear()
                    all_balls.remove(ball)
            
            if game.attempts_left <= 0 and len(all_balls) == 0:
                if game.level < 5:
                    game.state = "SHOP"
                    game.update_ui()
                else:
                    game.state = "GAME_OVER"
                    game.ui.clear()
                    game.ui.goto(0,0)
                    game.ui.write(f"YOU BEAT THE GAME!\nFinal Score: {game.score}", align="center", font=("Arial", 24, "bold"))
            
        screen.update()
        time.sleep(0.01)
except turtle.Terminator:
    pass