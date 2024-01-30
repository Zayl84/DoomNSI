# Séance 2 du 16/01/2024
# Dessin et déplacement 2d du joueur

# module pyglet principal (qu'on nenomme en pg pour plus de simplicité)
import pyglet as pg
# import des fonctions trigo du module math
from math import cos, sin, pi
from pyglet.window import key
# création de la fenêtre pour le plan 2D
# résolution : 320x200 (comme le Doom de l'époque)
window2d = pg.window.Window(320, 200, "Plan 2D", vsync=False)

# variables globales 
x, y, a = 160, 100, 0 # position et angle du joueur
# mode de déplacement du joueur: 0 = déplacement latéral, 1 = rotation
r = 1
keys = {"avancer":False, "reculer":False, "gauche":False, "droite":False}
# "batch" du joueur
joueur = pg.graphics.Batch()
# détection d'un touche pressée au clavier
@window2d.event
def on_key_press(symbol, modifiers):
  global x, y, a, r, keys
  print("Touche pressée n°", symbol)
  # shift pour changer de mode de déplacement joueur
  if symbol == pg.window.key.LSHIFT:
      if r == 0: r = 1
      else: r = 0
  # touches de déplacement
  if symbol == pg.window.key.DOWN or symbol == pg.window.key.S: # reculer
      keys["reculer"] = True
  if symbol == pg.window.key.UP or symbol == pg.window.key.Z: # avancer
      keys["avancer"] = True
  # touches pour pivoter
  if symbol == pg.window.key.LEFT or symbol == pg.window.key.Q:
      keys["gauche"] = True
  if symbol == pg.window.key.RIGHT or symbol == pg.window.key.D:
      keys["droite"] = True
    
    

# détection d'un touche relâchée au clavier
@window2d.event
def on_key_release(symbol, modifiers):
    global keys
    print("Touche relâchée n°", symbol)
    if symbol == pg.window.key.UP or symbol == pg.window.key.Z:
        keys["avancer"] = False
    if symbol == pg.window.key.DOWN or symbol == pg.window.key.S:
        keys["reculer"] = False
    if symbol == pg.window.key.LEFT or symbol == pg.window.key.Q:
        keys["gauche"] = False
    if symbol == pg.window.key.RIGHT or symbol == pg.window.key.D:
        keys["droite"] = False
    


# évènement principal : rendu graphique
@window2d.event
def on_draw():
    global x, y, a
    if keys["avancer"]:
            x += 2*cos(a)
            y += 2*sin(a)
    if keys["reculer"]:
        x -= 2*cos(a)
        y -= 2*sin(a)
    if keys["gauche"]:
       if r: a += pi/48
       else:
          x += 2*cos(a+(pi/2))
          y += 2*sin(a+(pi/2))
    if keys["droite"]:
       if r: a -= pi/48
       else:
          x -= 2*cos(a+(pi/2))
          y -= 2*sin(a+(pi/2))
    window2d.clear()
    # le joueur comme un cercle
    circle = pg.shapes.Circle(x, y, 10, color =(50, 225, 30), batch = joueur)
    # segment "vecteur vitesse" qui pointe vers la direction de visée
    visée = pg.shapes.Line(x, y, x + 20*cos(a), y + 20*sin(a), width=5, batch = joueur)
    # on dessine le "batch"
    joueur.draw()

    
# lancement du jeu
pg.app.run()