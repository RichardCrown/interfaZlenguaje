class Automata_Numeros:
    def __init__(self):
        self.abecedario=['0','1','2','3','4','5','6','7','8','9','.']
        self.temp=None

    def buscar(self,letra):
        for tk in self.abecedario:
            if tk == letra:
                return True
        return False

    def automata(self,cadena):
            estado=0
            for iterator in range(len(cadena)):
                letter=(cadena[iterator])
                if self.buscar(letter):
                    self.temp=letter
                    if estado==0:
                        if self.temp=='.':
                            estado=4
                        else:
                            estado=1
                    elif estado==1:
                        if self.temp=='.':
                            estado=2
                        else:
                            estado=estado
                    elif estado==2:
                        if self.temp=='.':
                            estado=4
                        else:
                            estado=3
                    elif estado==3:
                        if self.temp=='.':
                            estado=4
                        else:
                            estado=estado
                    else:
                        estado=estado
                else:
                    estado=4
            
            if estado==0:
                return False
            elif estado==1:
                return True
            elif estado==2:
                return False
            elif estado==3:
                return True
            elif estado==4:
                return False            
            else:
                return False



if __name__=="__main__":
    atom=Automata_Numeros()
    print('automata de numeros')
    while(True):
        print('**********************')
        print("INGRESA UNA CADENA")
        cadena = input()
        valido = atom.automata(cadena)

        if valido:
            print('LA CADENA ES VALIDA')
        else:
            print('LA CADENA NO ES VALIDA')