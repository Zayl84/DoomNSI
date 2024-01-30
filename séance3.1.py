# Séance 2 du 16/01/2024
# Dessin et déplacement 2d du joueur

# module pyglet principal (qu'on nenomme en pg pour plus de simplicité)
import pyglet as pg
# import des fonctions trigo du module math
from math import cos, sin, pi
from pyglet.window import key
# création de la fenêtre pour le plan 2D
# résolution : 320x200 (comme le Doom de l'époque)
window2d = pg.window.Window(1000, 700, "Plan 2D", vsync=False)

# variables globales 
x, y, a = 160, 100, 0 # position et angle du joueur
# vitesses de translation, de rotation. Facteur multiplicatif du mode "flash"
Vt, Vr, facteur_flash = 4.0, pi/48, 25

keys = {"avancer":False, "reculer":False,
        "tourner_gauche":False, "tourner_droite":False,
        "strafe_gauche": False, "strafe_droite": False,
        "strafe":False, "flash":False}

# "batch" du joueur
joueur = pg.graphics.Batch()
# détection d'un touche pressée au clavier
@window2d.event
def on_key_press(symbol, modifiers):
    global keys
    print("Touche pressée n°", symbol)
    # shift pour changer de mode de déplacement joueur
    if symbol == pg.window.key.LSHIFT: keys["flash"] = True
    if symbol == pg.window.key.LCTRL: keys["strafe"] = True
    # touches de déplacement
    if symbol == pg.window.key.DOWN or symbol == pg.window.key.S: # reculer
        keys["reculer"] = True
    if symbol == pg.window.key.UP or symbol == pg.window.key.Z: # avancer
        keys["avancer"] = True
    # touches pour pivoter
    if symbol == pg.window.key.LEFT:
        keys["tourner_gauche"] = True
    if symbol == pg.window.key.RIGHT:
        keys["tourner_droite"] = True
    if symbol == pg.window.key.Q:
        keys["strafe_gauche"] = True
    if symbol == pg.window.key.D:
        keys["strafe_droite"] = True
    
    

# détection d'un touche relâchée au clavier
@window2d.event
def on_key_release(symbol, modifiers):
    global keys
    print("Touche relâchée n°", symbol)
    if symbol == pg.window.key.LCTRL: keys["strafe"] = False
    if symbol == pg.window.key.LSHIFT: keys["flash"] = False
    if symbol == pg.window.key.UP or symbol == pg.window.key.Z:
        keys["avancer"] = False
    if symbol == pg.window.key.DOWN or symbol == pg.window.key.S:
        keys["reculer"] = False
    if symbol == pg.window.key.LEFT:
        keys["tourner_gauche"] = False
    if symbol == pg.window.key.RIGHT:
        keys["tourner_droite"] = False
    if symbol == pg.window.key.Q:
        keys["strafe_gauche"] = False
    if symbol == pg.window.key.D:
        keys["strafe_droite"] = False  


# évènement principal : rendu graphique
@window2d.event
def on_draw():
    window2d.clear()
    # le joueur comme un cercle
    circle = pg.shapes.Circle(x, y, 10, color =(50, 225, 30), batch = joueur)
    # segment "vecteur vitesse" qui pointe vers la direction de visée
    visée = pg.shapes.Line(x, y, x + 20*cos(a), y + 20*sin(a), width=5, batch = joueur)
    # on dessine le "batch"
    joueur.draw()

def update(dt):
    global x, y, a, Vt, Vr, facteur_flash, keys
    Dx, Dy, Da, F = 0, 0, 0, 1
    if keys["flash"]: F = facteur_flash
    if keys["avancer"]:
        Dx, Dy = Vt*cos(a), Vt*sin(a)
        y += Dy*F
        x += Dx*F
    if keys["reculer"]:
        Dx, Dy = -Vt*cos(a), -Vt*sin(a)
        y += Dy*F
        x += Dx*F
    if keys["strafe"]:
        if keys["tourner_gauche"]:
            Dx, Dy = -Vt*sin(a), Vt*cos(a)
            y += Dy*F
            x += Dx*F
        if keys['tourner_droite']:
            Dx, Dy = Vt*sin(a), -Vt*cos(a)
            y += Dy*F
            x += Dx*F
    elif keys["tourner_gauche"]:
        Da = Vr
        a += Da*F
    elif keys["tourner_droite"]:
        Da = -Vr
        a += Da*F
    if keys["strafe_gauche"]:
        Dx, Dy = -Vt*sin(a), Vt*cos(a)
        y += Dy*F
        x += Dx*F
    if keys["strafe_droite"]:
        Dx, Dy = Vt*sin(a), -Vt*cos(a)
        y += Dy*F
        x += Dx*F
pg.clock.schedule_interval(update, 1/30.0)
    
# lancement du jeu
pg.app.run()