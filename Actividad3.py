import numpy as np
import pygame
from random import randint as r
import random



lados = 8
celdas = []
alpha = 0.05
gamma = 0.95
celda_actual = [0, 0]
epsilon = 0.2
min_epsilon = 0.05
tabla_recompensa = np.full((lados, lados), 0)
colores = [(224, 224, 224) for i in range(lados**2)]
acciones = {"arriba": 0, "abajo": 1, "izquierda": 2, "derecha": 3, "topLeft": 4, "topRight": 5, "botLeft": 6, "botRight": 7}
estados = {}
tabla_Q = np.zeros((lados**2,8))


def crear_ambiente():
    obstaculos = int(lados*0.8)
    while obstaculos != 0:
        i = r(0,lados-1)
        j = r(0,lados-1)
        if tabla_recompensa[i,j] == 0 and [i,j] != [0,0] and [i,j] != [lados-1,lados-1]:
            tabla_recompensa[i,j] = -100
            obstaculos-= 1
            colores[lados*i+j] = (10,10,10)
            celdas.append(lados*i+j)

    tabla_recompensa[lados-1,lados-1] = 100
    colores[lados**2 - 1] = (232,63,111)
    celdas.append(lados**2 - 1) 
    contador = 0
    for i in range(lados):
        for j in range(lados):
            estados[(i,j)] = contador
            contador+=1


def escoger_accion(estado_actual):
    global celda_actual,epsilon
    acciones_disponibles = []
    cambios_evaluados = []
    if epsilon >= min_epsilon:
        if celda_actual[0] != 0:
            if celda_actual[1] != 0:
                acciones_disponibles.append("topLeft")
            elif celda_actual[1] != lados-1:
                acciones_disponibles.append("topRight")
            else:
                acciones_disponibles.append("arriba")

        if celda_actual[0] != lados-1:
            if celda_actual[1] != 0:
                acciones_disponibles.append("botLeft")
            elif celda_actual[1] != lados-1:
                acciones_disponibles.append("botRight")
            else:
                acciones_disponibles.append("abajo")
        if celda_actual[1] != 0:
            acciones_disponibles.append("izquierda")
        if celda_actual[1] != lados-1:
            acciones_disponibles.append("derecha")
        accion = acciones[acciones_disponibles[r(0,len(acciones_disponibles) - 1)]]
    elif np.random.uniform() <= epsilon:
        if celda_actual[0] != 0:
            if celda_actual[1] != 0:
                acciones_disponibles.append("topLeft")
            elif celda_actual[1] != lados - 1:
                acciones_disponibles.append("topRight")
            else:
                acciones_disponibles.append("arriba")

        if celda_actual[0] != lados - 1:
            if celda_actual[1] != 0:
                acciones_disponibles.append("botLeft")
            elif celda_actual[1] != lados - 1:
                acciones_disponibles.append("botRight")
            else:
                acciones_disponibles.append("abajo")
        if celda_actual[1] != 0:
            acciones_disponibles.append("izquierda")
        if celda_actual[1] != lados - 1:
            acciones_disponibles.append("derecha")
        accion = acciones[acciones_disponibles[r(0,len(acciones_disponibles) - 1)]]
    else:
        if celda_actual[0] != 0:
            if celda_actual[1] != 0:
                acciones_disponibles.append(tabla_Q[estado_actual, 4])
                cambios_evaluados.append(4)
            elif celda_actual[1] != lados - 1:
                acciones_disponibles.append(tabla_Q[estado_actual, 5])
                cambios_evaluados.append(5)
            else:
                acciones_disponibles.append(tabla_Q[estado_actual, 0])
                cambios_evaluados.append(0)

        if celda_actual[0] != lados - 1:
            if celda_actual[1] != 0:
                acciones_disponibles.append(tabla_Q[estado_actual, 6])
                cambios_evaluados.append(6)
            elif celda_actual[1] != lados - 1:
                acciones_disponibles.append(tabla_Q[estado_actual, 7])
                cambios_evaluados.append(7)
            else:
                acciones_disponibles.append(tabla_Q[estado_actual, 1])
                cambios_evaluados.append(1)

        if celda_actual[1] != 0: 
            acciones_disponibles.append(tabla_Q[estado_actual,2])
            cambios_evaluados.append(2)
        if celda_actual[1] != lados-1: 
            acciones_disponibles.append(tabla_Q[estado_actual,3])
            cambios_evaluados.append(3)
        accion = cambios_evaluados[random.choice([i for i,a in enumerate(acciones_disponibles) if a == max(acciones_disponibles)])]
    return accion
      
      
def iteracion():
    global celda_actual,epsilon
    estado_actual = estados[(celda_actual[0],celda_actual[1])]
    accion = escoger_accion(estado_actual)
    if accion == 0: 
        celda_actual[0] -= 1
    elif accion == 1: 
        celda_actual[0] += 1
    elif accion == 2: 
        celda_actual[1] -= 1
    elif accion == 3: 
        celda_actual[1] += 1
    elif accion == 4:
        celda_actual[0] -= 1
        celda_actual[1] -= 1
    elif accion == 5:
        celda_actual[0] += 1
        celda_actual[1] -= 1
    elif accion == 6:
        celda_actual[0] -= 1
        celda_actual[1] += 1
    elif accion == 7:
        celda_actual[0] += 1
        celda_actual[1] += 1
    proximo_estado = estados[(celda_actual[0],celda_actual[1])]
    if proximo_estado not in celdas:
        tabla_Q[estado_actual,accion] += alpha*(tabla_recompensa[celda_actual[0],celda_actual[1]] + gamma*(np.max(tabla_Q[proximo_estado])) - tabla_Q[estado_actual,accion])
    else:
        tabla_Q[estado_actual,accion] += alpha*(tabla_recompensa[celda_actual[0],celda_actual[1]] - tabla_Q[estado_actual,accion])
        print(epsilon)
        celda_actual = [0,0]
        if epsilon > min_epsilon:
            epsilon -= 5e-4 
            
              
def distribucion():
    color = 0
    scrx = lados*100
    scry = lados*100
    screen = pygame.display.set_mode((1300, 800))
    screen.fill((255, 255, 255))
    for i in range(0, scrx, 100):
        for j in range(500, 1300, 100):
            rect1 = pygame.Rect(j, i, j+100, i+100)
            pygame.draw.rect(screen, (0, 0, 0), rect1)
            rect2 = pygame.Rect(j+3, i+3, j+95, i+95)
            pygame.draw.rect(screen, colores[color], rect2)
            color += 1
            agent = pygame.Rect(500+(celda_actual[1]*100), (celda_actual[0]*100), 100, 100)
            pygame.draw.rect(screen, (34, 116, 165), agent)

    pygame.font.init()
    fuente = pygame.font.Font("RobotoMono-Light.ttf", int(scry/64))

    for i in range(64):
        texto = fuente.render(str(tabla_Q[i]), 1, (0, 0, 0))
        screen.blit(texto, (10, int(i*scry/64)))
    pygame.display.flip()
    

def main():
    crear_ambiente()
    run = True
    while run:
        distribucion()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.flip()
        iteracion()
    pygame.quit()
    print(tabla_Q)


main()