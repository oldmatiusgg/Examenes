'''
CLASE Pptlsge: Piedra-pape-tigera-lagarto-spock-garrafa-edans
'''

# Importamos librerias que nos ayudaran en la clase
import os
import random
import time


class Pptlsge():

    OPCIONES = {

    0: '{{ url_for(\'static\', filename=\'img/piedra.jpg\')}}',
    1: '{{ url_for(\'static\', filename=\'img/papel.jpg\')}}',
    2: '{{ url_for(\'static\', filename=\'img/tijera.jpg\')}}',
    3: '{{ url_for(\'static\', filename=\'img/lagarto.jpg\')}}',
    4: '{{ url_for(\'static\', filename=\'img/spock.png\')}}',
    5: '{{ url_for(\'static\', filename=\'img/garrafa.png\')}}',
    6: '{{ url_for(\'static\', filename=\'img/edans.jpg\')}}'

}

    REGLAS = {

        'piedra': [OPCIONES[2], OPCIONES[3], OPCIONES[5]],
        # 'papel': [OPCIONES[]]
    }

    

    def __init__(self):

        
        self.papel = False
        self.tijera = False
        self.lagarto = False
        self.spock = False
        self.garrafa = False
        self.edans = False
        self.aleatorio = random.choice(self.OPCIONES)
        


    def piedra(self):

        opcionYmensaje = []

        piedra = self.OPCIONES[0]

        if piedra == self.aleatorio:

            opcionYmensaje.append(self.aleatorio)
            opcionYmensaje.append('<h1> Has empatado </h1>')

            return opcionYmensaje
        
        elif self.aleatorio == self.OPCIONES[2] or self.aleatorio == self.OPCIONES[3] or self.aleatorio == self.OPCIONES[5]:

            opcionYmensaje.append(self.aleatorio)
            opcionYmensaje.append('<h1> Has ganado </h1>')

            return opcionYmensaje

        elif self.aleatorio == self.OPCIONES[1] or self.aleatorio == self.OPCIONES[4] or self.aleatorio == self.OPCIONES[6]:

            opcionYmensaje.append(self.aleatorio)
            opcionYmensaje.append('<h1> Has perdido </h1>')

            return opcionYmensaje


        # for llave, valor in self.OPCIONES.items():

                

        #     if piedra != valor:

        #         for llaveRegla, valorRegla in self.REGLAS.items():

        #             for i in valorRegla:

        #                 if self.aleatorio == i:

        #                     opcionYmensaje.append(self.aleatorio)
        #                     opcionYmensaje.append('<h1> Has ganado </h1>')

        #                     return opcionYmensaje

        #                 else:

        #                     opcionYmensaje.append(self.aleatorio)
        #                     opcionYmensaje.append('<h1> Has perdido </h1>')

        #                     return opcionYmensaje
            

            # elif piedra == valor:

            #     opcionYmensaje.append(piedra)
            #     opcionYmensaje.append('<h1> Has igualado </h1>')

            #     return opcionYmensaje
                



            
            



    # def resultado(self, inputOpcion):

    #     resultado = {

    #         'piedra': self.piedra()
    #     }

    #     for llave, valor in resultado.items():

    #         if inputOpcion == llave:

    #             return valor



        