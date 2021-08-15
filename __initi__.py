#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame
import sys
import cv2

from pygame.locals import *

# ====================
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
# ====================


# Variables
WIDTH = 900
HEIGHT = 500
MposX = 300
MposY = 318

cont = 6
direc = True
i = 0
xixf = {}  # xinicial y xfinal
Rxixf = {}

parabola = {}
salto = False

salto_Par = False


# ===========================================================
# =================IMAGEM====================================

def imagem(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit
    image = image.convert()
    if transparent:
        cor = image.get_at((0, 0))
        image.set_colorkey(cor, RLEACCEL)
    return image


# ================================================================

# ======================TECLADO===================================
# ================================================================
def teclado(direcao):
    global MposX
    global cont, direc, salto, salto_Par

    tec_capturado = pygame.key.get_pressed()

    if tec_capturado[K_q] and tec_capturado[K_RIGHT] and salto_Par is False:
        salto_Par = True
    elif tec_capturado[K_q] and tec_capturado[K_LEFT] and salto_Par is False:
        salto_Par = True

    elif (tec_capturado[K_RIGHT] and salto is False and salto_Par is False) or direcao == 'direita':
        MposX += 2
        cont += 1
        direc = True
    elif (tec_capturado[K_LEFT] and salto is False and salto_Par is False) or direcao == 'esquerda':
        MposX -= 2
        cont += 1
        direc = False
    elif (tec_capturado[K_q] and salto is False and salto_Par is False) or direcao == 'pular':
        salto = True
    else:
        cont = 6

    return


def camera():
    # ==========================================
    ret, frame = video_capture.read()
    altura, largura = frame.shape[:2]  # NOVO
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(150, 150),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # ==========================================

    sprite()
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if x > 250:
            teclado(direcao='direita')
        if x < 200:
            teclado(direcao='esquerda')
        if y < 100:
            teclado(direcao='pular')
            # teclado()
            # novo ===========
    ponto = (0, 0)
    rotacao = cv2.getRotationMatrix2D(ponto, 0, 0.5)
    rotacionado = cv2.warpAffine(frame, rotacao, (largura, altura))
    cv2.imshow('Video', rotacionado)
    cv2.resizeWindow('Video', 320, 240)




# ===================SPRITE===============================
# ========================================================
def sprite():
    global cont

    xixf[0] = (0, 0, 20, 41)
    xixf[1] = (22, 0, 25, 41)
    xixf[2] = (47, 0, 25, 41)
    xixf[3] = (73, 0, 20, 41)
    xixf[4] = (93, 0, 27, 41)
    xixf[5] = (120, 0, 27, 41)

    Rxixf[0] = (122, 0, 22, 41)
    Rxixf[1] = (96, 0, 25, 41)
    Rxixf[2] = (74, 0, 22, 41)
    Rxixf[3] = (50, 0, 23, 41)
    Rxixf[4] = (24, 0, 26, 41)
    Rxixf[5] = (0, 0, 25, 41)

    p = 6

    global i

    if cont == p:
        i = 0

    if cont == p * 2:
        i = 1

    if cont == p * 3:
        i = 2

    if cont == p * 4:
        i = 3

    if cont == p * 5:
        i = 4

    if cont == p * 6:
        i = 5
        cont = 0

    return


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario")

    fundo = imagem("imagens/fundo.png")

    mario = imagem("imagens/sprites_mario.png", True)
    mario_inv = pygame.transform.flip(mario, True, False)

    clock = pygame.time.Clock()

    global salto_Par
    descida = False
    descida_parabolica = False
    # el bucle principal del juego
    while True:

        clock.tick(10)

        camera()

        global MposX, MposY, salto

        fundo = pygame.transform.scale(fundo, (1000, 400))

        screen.blit(fundo, (0, 0))

        if direc is True and salto is False:
            screen.blit(mario, (MposX, MposY), (xixf[i]))

        if direc is False and salto is False:
            screen.blit(mario_inv, (MposX, MposY), (Rxixf[i]))


            # salto normal
        if salto is True:

            if direc is True:
                screen.blit(mario, (MposX, MposY), (xixf[4]))
            if direc is False:
                screen.blit(mario_inv, (MposX, MposY), (Rxixf[4]))

            if descida is False:
                MposY -= 4

            if descida is True:
                MposY += 4

            if MposY == 186:
                descida = True

            if MposY == 318:
                descida = False
                salto = False
        # ==============================



        # SALTO PARABOLICO
        if salto_Par is True and direc is True:

            screen.blit(mario, (MposX, MposY), (xixf[4]))

            if descida_parabolica is False:
                MposY -= 3
                MposX += 2

            if descida_parabolica is True:
                MposY += 3
                MposX += 2

            if MposY == 246:
                descida_parabolica = True

            if MposY == 318:
                descida_parabolica = False
                salto_Par = False
        elif salto_Par is True and direc is False:

            screen.blit(mario_inv, (MposX, MposY), (Rxixf[4]))

            if descida_parabolica is False:
                MposY -= 3
                MposX -= 2

            if descida_parabolica is True:
                MposY += 3
                MposX -= 2

            if MposY == 246:
                descida_parabolica = True

            if MposY == 318:
                descida_parabolica = False
                salto_Par = False

        pygame.display.flip()

        # Cerrar la ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video_capture.release()
                cv2.destroyAllWindows()
                sys.exit()

if __name__ == '__main__':
    main()
