class Automata_Identificadores:
    def __init__(self):
        self.abecedario=['&','0','1','2','3','4','5','6','7','8','9','a','b','c','d','a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M','n','N',
                    'o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z','_']
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
                    if self.temp=='&':
                        estado=1
                    else:
                        estado=3
                elif estado==1:
                    if self.temp=='0' or self.temp=='1' or self.temp=='2' or self.temp=='3' or self.temp=='4'  or self.temp=='5' or self.temp=='6' or self.temp=='7' or self.temp=='8' or self.temp=='9' or self.temp=='&':
                        estado=3
                    else:
                        estado=2
                elif estado==2:
                    estado=estado
                else:
                    estado=estado
            else:
                estado=3
        
        if estado==0:
            return False
        elif estado==1:
            return False
        elif estado==2:
            return True
        elif estado==3:
            return False
        else:
            return False




if __name__=="__main__":
    atom=Automata_Identificadores()
    print('automata de identificadores')
    while(True):
        print('**********************')
        print("INGRESA UNA CADENA")
        cadena = input()
        valido = atom.automata(cadena)

        if valido:
            print('LA CADENA ES VALIDA')
        else:
            print('LA CADENA NO ES VALIDA') 