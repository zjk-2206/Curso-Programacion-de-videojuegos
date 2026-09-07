# Curso Programacion de videojuegos
 curso de programacion de videojuegos de la universidad de los andes
 
 # 🎮 Colección de Juegos Arcade en Pygame

Este repositorio contiene una colección de juegos 2D clásicos (Pong y Flappy Bird) desarrollados en Python utilizando **Pygame** y **GALE**. 

El proyecto destaca por su enfoque en la **arquitectura limpia y principios de Ingeniería de Software**, aplicando conceptos del diseño orientado a objetos (OOP) fuertemente tipado en un entorno de Python.

## 🏗️ Arquitectura y Patrones de Diseño

El motor de los juegos está construido con una separación estricta de responsabilidades:
* **Patrón Strategy:** Implementado para la gestión dinámica de la dificultad (`GameModeNormal`, `GameModeHard`). Las mecánicas de generación procedural y físicas se inyectan en tiempo de ejecución sin alterar el núcleo del juego.
* **Máquina de Estados (State Pattern):** Gestión del flujo del juego mediante estados independientes (ej. `PlayingState`, `MenuState`).
* **Factory Pattern:** Utilizado para la instanciación eficiente de obstáculos (`Factory(LogPair)`).
* **Gestor de Audio Aislado:** Control dinámico de *streams* de música en formato `.ogg` con ajustes de volumen independientes de los efectos de sonido puntuales (SFX).

## ⚙️ Requisitos e Instalación

Es altamente recomendable ejecutar este proyecto dentro de un entorno virtual para evitar conflictos de dependencias en el sistema.
Es necesario la instalacion de Gale creado por Alejandro Mujica:
`https://github.com/R3mmurd/Gale`

## Referencias

Curso dado por el profesor Alejandro Mujica y Gerardo Rosetti de la asignatura ***Programacion de Videojuegos*** cuyo repositorio creado y utilizado para el curso es:
`https://github.com/R3mmurd/VideoGameProgrammingI`

## Instrucciones Para la Instalacion y Ejecucion de los Programas
### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio
```
### 2. Crear y activar el entorno virtual

**En Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

 **En Window**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalacion de Dependencias

Con el entorno virtual activado instala Pygame y Gale:

```bash
pip install pygame
pip install Gale
```

### 4. Ejecucion del Programa

Con el entorno virtual aun activo ejecuta:
Para el pong:
```bash
python 01-pong/main.py
```

Para el flappy bird:
```bash
python 02-flappy_bird/main.py
```

## Mecanicas

### 1. Pong

Juego clasico de pong de 1 jugador vs la IA creada como tarea del curso

#### Instrucciones para jugarlo

Se utiliza las teclas **W** y **S** para mover la tabla hacia arriba y abajo respectivamente y ganas cuando la pelota toque la pared izquierda atras del jugador contrario controlado por la IA

### 2. Flappy bird

juego clasico de flappy bird con modificaciones para elegir la dificultad, powerup y un sistema de pause creado como tarea del curso

#### Instrucciones para jugarlo

En el modo normal se utiliza espacio para saltar y se juega como el clasico flappy bird, mientras que en el modo dificil se utiliza el espacio y flechas izquierda y derecha para moverte, tambien en el modo dificil viene incluido un powerup que te hace invencible durante 6 segundos y un sistema de cambio de apertura de los troncos generados. En ambos modos se utiliza el tab(tabulador) para pausar el juego que en el momento de quitarlo empieza de inmediato.

### 3. Breackout

juego clasico de breackout con modificaciones para los powerup que te pueden salir

#### Instrucciones para jugarlo

El juego consiste en obtener la mayor cantidad de puntos al pasar los niveles, se utiliza las flechas izquierda y derecha para mover la paleta, el espacio para activar el modificador de captureballs que te permite pegar una o varias pelotas a la paleta por 5 segundos y lanzarlas, la **M** para el powerup de rocketup que genera 2 pelotas y las lanza hacia el frente y por ultimo un powerup personalizado que le quita uno de vida a todos los ladrillos de la partida, este ultimo aparece menos que los demas y te permite avanzar mas rapido por los niveles, pero no te suma puntaje ni tampoco te da alguna otra ventaja aparte de ya dicha.

### 4. match3

juego con tematica de candy-crush pero con powerups y mas colores

#### Intrucciones para jugarlo

Al igual que candy-crush se desea pasar de niveles, solo que aqui se hace al alcanzar un minimo de puntos, se tienen 2 powerups que se activan al darle clic o hacer match, para cuando se hace un match de 4 que destruye todas las casillas horizontal y verticalmente al activarse y al hacer un match de 5 se crea un powerup que destruye todas las piezas del mismo color

 
