import os
import keyboard
import time
import random
import sys
import subprocess
from colorama import Fore, Style, init

# Intentar importar librerías para limpiar el búfer según el SO
if os.name == 'nt':
    import msvcrt
else:
    import termios

# Inicializa Colorama
init(autoreset=True)

# --- CONFIGURACIÓN ---
ANCHO = 32
ALTO = 16
OFFSET_Y = 5 

# --- SÍMBOLOS ---
S_BORDE_H = "═"
S_BORDE_V = "║"
S_ESQUINA_UL = "╔"
S_ESQUINA_UR = "╗"
S_ESQUINA_DL = "╚"
S_ESQUINA_DR = "╝"

S_SERP_CABEZA = Fore.GREEN + "●"
S_SERP_CUERPO = Fore.GREEN + "○"
S_MANZANA = Fore.RED + "#"
S_VACIO = " "

subprocess.run(['cmd', '/c', 'cls'])


def limpiar_buffer():
    """Elimina las teclas acumuladas en la terminal para que no aparezcan al salir."""
    if os.name == 'nt':
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def mover_cursor(y, x):
    print(f"\033[{y};{x}H", end="")

def dibujar_interfaz_estatica():    # Letrero superior
    print(Fore.CYAN + S_ESQUINA_UL + S_BORDE_H * (ANCHO) + S_ESQUINA_UR)
    print(Fore.CYAN + S_BORDE_V + f"  SNAKE GAME - MANZANAS: 000  ".center(ANCHO) + S_BORDE_V)
    print(Fore.CYAN + S_ESQUINA_DL + S_BORDE_H * (ANCHO) + S_ESQUINA_DR)
    
    # Campo de juego (Bordes)
    mover_cursor(OFFSET_Y, 1)
    print(Fore.WHITE + S_ESQUINA_UL + S_BORDE_H * ANCHO + S_ESQUINA_UR)
    for i in range(1, ALTO + 1):
        mover_cursor(OFFSET_Y + i, 1)
        print(Fore.WHITE + S_BORDE_V + S_VACIO * ANCHO + S_BORDE_V)
    mover_cursor(OFFSET_Y + ALTO + 1, 1)
    print(Fore.WHITE + S_ESQUINA_DL + S_BORDE_H * ANCHO + S_ESQUINA_DR)

def actualizar_puntos(puntos):
    mover_cursor(2, 26)
    print(Fore.YELLOW + str(puntos).zfill(3))

def main():
    serpiente = [[10, 15], [10, 14], [10, 13]]
    direccion = [0, 1] 
    manzana = [random.randint(1, ALTO), random.randint(1, ANCHO)]
    puntos = 0
    
    dibujar_interfaz_estatica()

    try:
        while True:
            # 1. Controles
            if keyboard.is_pressed('w') and direccion != [1, 0]: direccion = [-1, 0]
            elif keyboard.is_pressed('s') and direccion != [-1, 0]: direccion = [1, 0]
            elif keyboard.is_pressed('a') and direccion != [0, 1]: direccion = [0, -1]
            elif keyboard.is_pressed('d') and direccion != [0, -1]: direccion = [0, 1]
            elif keyboard.is_pressed('q'): 
                break

            # 2. Lógica de movimiento
            nueva_cabeza = [serpiente[0][0] + direccion[0], serpiente[0][1] + direccion[1]]

            # Colisión Bordes o Cuerpo
            if (nueva_cabeza[0] < 1 or nueva_cabeza[0] > ALTO or 
                nueva_cabeza[1] < 1 or nueva_cabeza[1] > ANCHO or 
                nueva_cabeza in serpiente):
                mover_cursor(OFFSET_Y + ALTO + 3, 1)
                print(Fore.RED + f" ¡FIN DEL JUEGO! Puntos: {puntos} ".center(ANCHO + 2))
                break

            serpiente.insert(0, nueva_cabeza)

            # 3. Comida
            if nueva_cabeza == manzana:
                puntos += 1
                actualizar_puntos(puntos)
                while True:
                    manzana = [random.randint(1, ALTO), random.randint(1, ANCHO)]
                    if manzana not in serpiente: break
            else:
                cola = serpiente.pop()
                mover_cursor(OFFSET_Y + cola[0], cola[1] + 1)
                print(S_VACIO)

            # 4. Dibujar
            mover_cursor(OFFSET_Y + manzana[0], manzana[1] + 1)
            print(S_MANZANA)
            mover_cursor(OFFSET_Y + serpiente[0][0], serpiente[0][1] + 1)
            print(S_SERP_CABEZA)
            if len(serpiente) > 1:
                mover_cursor(OFFSET_Y + serpiente[1][0], serpiente[1][1] + 1)
                print(S_SERP_CUERPO)

            time.sleep(0.1)

    finally:
        # Esto se ejecuta SIEMPRE al salir (por Q, Game Over o error)
        time.sleep(0.2) # Pausa mínima para que keyboard suelte el hilo
        limpiar_buffer()
        mover_cursor(OFFSET_Y + ALTO + 4, 1)
        print(Style.RESET_ALL + "Terminal restaurada. ¡Gracias por jugar!")

if __name__ == "__main__":
    main()