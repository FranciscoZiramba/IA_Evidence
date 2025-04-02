#Francisco Benjamín Ziramba Lucas
#Modelado de Red Neuronal
  ##Características necesarias para la red neuronal:
    1, Definir el tipo de red neuronal y describir cada una de sus partes
    2. Definir patrones a utilizar
    3. Definir qué función de activación es necesaria para el problema
    4.  Definir el valor máximo de entradas
    5. ¿Qué valores a la salida de la red se podrían esperar?
    6. ¿Cuáles son los valores máximos que puede tener el bias?
    ###Desarrollo de solución
    1. Una red neuronal convolucional creo que puede ser la ideal ya que el problema por si mismo y las posibilidades del tablero no parecen linealmente separables por la cantidad de variables.
    Las partes que necesitaría sería una entrada en la que se establezca el contexto del problema, pudiendo ser:
        - Entrada (una entrada que defina el tamaño del tablero opcionalmente ya que siempre será del mismo tamaño, en dicha entrada puede indicarse también datos importantes como el turno de juego)
        - Capas convolucionales 
        - Kernel (lo más ideal creo sería poner uno de 5x5 para que pueda tener mejor contexto)
        - Capas de agrupación
        - Capa de salida para recomendar un movimiento o evaluación de un estado determinado
    2. Orientación de lineas de fichas y su número, por ejemplo 2 horizontal, 4 diagonal, etc. Oportunidades de ganar al tener 4 fichas, patrones de defensa para los movimientos del rival, espacios estratégicos.
    3. ReLU
    4. El valor máximo de entradas serían 3, una para el tamaño del tablero, la segunda para informacion del turno y una tercera para por ejemplo contexto de casillas disponibles u ocupadas por el rival.
    5. El mejor movimiento o un movimiento recomendado basado en el aprendizaje logrado de las posibilidades jugadas.
    6. Iniciarla en 0.1