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
# vitesses de translation, de rotation. Facteur multiplicatif du mode "flash"
Vt, Vr, facteur_flash = 2.0, pi/48, 2

keys = {"avancer":False, "reculer":False,
        "tourner_gauche":False, "tourner_droite":False,
        "strafe_gauche": False, "strafe_droite": False,
        "strafe":False, "flash":False}

# "batch" du joueur
joueur = pg.graphics.Batch()
# détection d'un touche pressée au clavier
@window2d.event
def on_key_press(symbol, modifiers):
  global x, y, a, r, keys
  print("Touche pressée n°", symbol)
  # shift pour changer de mode de déplacement joueur
  if symbol == pg.window.key.LSHIFT: keys["flash"] = True
  keys["strafe"] = (pg.window.key.Q or pg.window.key.D or pg.window.LCTRL)
  # touches de déplacement
  if symbol == pg.window.key.DOWN or symbol == pg.window.key.S: # reculer
      keys["reculer"] = True
  if symbol == pg.window.key.UP or symbol == pg.window.key.Z: # avancer
      keys["avancer"] = True
  # touches pour pivoter
  if symbol == pg.window.key.LEFT or symbol == pg.window.key.Q:
      keys["tourner_gauche"] = True
  if symbol == pg.window.key.RIGHT or symbol == pg.window.key.D:
      keys["tourner_droite"] = True
    
    

# détection d'un touche relâchée au clavier
@window2d.event
def on_key_release(symbol, modifiers):
    global keys
    print("Touche relâchée n°", symbol)
    keys["strafe"] = not (pg.window.key.Q or pg.window.key.D or pg.window.LCTRL)
    if symbol == pg.window.key.LSHIFT: keys["flash"] = False
    if symbol == pg.window.key.UP or symbol == pg.window.key.Z:
        keys["avancer"] = False
    if symbol == pg.window.key.DOWN or symbol == pg.window.key.S:
        keys["reculer"] = False
    if symbol == pg.window.key.LEFT or symbol == pg.window.key.Q:
        keys["tourner_gauche"] = False
    if symbol == pg.window.key.RIGHT or symbol == pg.window.key.D:
        keys["tourner_droite"] = False
    


# évènement principal : rendu graphique
@window2d.event
def on_draw():
    global x, y, a, Vt, Vr, facteur_flash
    Dx, Dy, Da, F = 0, 0, 0, 1
    if keys["flash"]: F = facteur_flash
    if keys["avancer"]:
        Dx, Dy = Vt*cos(a), Vt*sin(a)
    if keys["reculer"]:
        Dx, Dy = -Vt*cos(a), -Vt*sin(a)
    if keys["strafe"] or keys["strafe_gauche"] or keys["strafe_droite"]:
        if keys["tourner_gauche"]: Dx, Dy = -Vt*sin(a), Vt*cos(a)
        if keys['tourner_droite']: Dx, Dy = Vt*sin(a), -Vt*cos(a)
    elif keys["tourner_gauche"]: Da = Vr
    elif keys["tourner_droite"]: Da = -Vr
    x += Dx*F
    y += Dy*F
    a += Da*F
    window2d.clear()
    # le joueur comme un cercle
    circle = pg.shapes.Circle(x, y, 10, color =(50, 225, 30), batch = joueur)
    # segment "vecteur vitesse" qui pointe vers la direction de visée
    visée = pg.shapes.Line(x, y, x + 20*cos(a), y + 20*sin(a), width=5, batch = joueur)
    # on dessine le "batch"
    joueur.draw()

    
# lancement du jeu
pg.app.run()
