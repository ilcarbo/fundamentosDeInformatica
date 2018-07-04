import re
from collections import Counter
from math import inf


class Elemento():
    def __init__(self,name,simbolo,num_atomico,neutrones,valencia):
        self._name = name
        self._simbolo = simbolo
        self._numAtomico = num_atomico
        self._protones = self._numAtomico
        self._neutrones = neutrones
        self._electrones = self._numAtomico
        self._pesoAtomico = self._protones + self._neutrones
        self._valencia = valencia

    def cantProtones(self):
        return self._protones

    def cantNeutrones(self):
        return self._neutrones

    def cantElectrones(self):
        return self._electrones

    def numeroAtomico(self):
        return self._numAtomico

    def pesoAtomico(self):
        return self._pesoAtomico

    def valencia(self):
        return self._valencia

    def simbolo(self):
        return self._simbolo

class TablaPeriodica():
    def __init__(self):
        self._tabla = []

    def agregarElemento(self,elemento):
            if elemento._simbolo not in [x[1] for x in self._tabla]:
                self._tabla.append((elemento,elemento._simbolo,elemento._numAtomico))
            else:
                print("Ese elemento ya está en la tabla.")

    def elementos(self):
        return [x[0] for x in self._tabla]

    def elementoS(self,simbolo):
        if simbolo not in [x[1] for x in self._tabla]:
            return None
        else:
            for elem in self._tabla:
                if elem[1] == simbolo:
                    return elem[0]

    def elementoN(self, numero):
        if numero not in [x[2] for x in self._tabla]:
            return None
        else:
            for elem in self._tabla:
                if elem[2] == numero:
                    return elem[0]

class Compuesto():
    def __init__(self,name):
        self._name = name
        self._atomos = []
        self._enlaces = []
        self._nombres = []
        self._elementos = []


    def agregarAtomo(self,elemento):
        AtomosDe = 1
        for elem in self._atomos:
            if elem[0] == elemento:
                AtomosDe +=1
        nombre = elemento._simbolo + str(AtomosDe)
        self._atomos.append((elemento, nombre))

    def cantAtomos(self):
        return len(self._atomos)

    def atomosDe(self,elemento):
        atomosDeElemento = []
        for elem in self._atomos:
            if elem[0] == elemento:
                atomosDeElemento.append(elem[1])
        return atomosDeElemento

    def atomosDeNum(self,elemento):
        self._elementos = [elem[0] for elem in self._atomos]
        cuentaAtom = 0
        for elem in self._elementos:
            if elem == elemento:
                cuentaAtom += 1
        return cuentaAtom

    def incluyeAtomo(self,nombre):
        self._nombres = [elem[1] for elem in self._atomos]
        return nombre in self._nombres

    def incluyeElemento(self,elemento):
        elementos = [elem[0] for elem in self._atomos]
        return elemento in elementos

    def elementosPresentes(self):
        elementosUnicos = []
        for elem in self._atomos:
            if elem[0] not in elementosUnicos:
                elementosUnicos.append(elem[0])
        return elementosUnicos

    def enlazar(self,atom1,atom2):
        self._enlaces.append((atom1,atom2))

    def cantEnlaces(self):
        return len(self._enlaces)

    def cantEnlacesAtomo(self,nombre):
        if self.incluyeAtomo(nombre) == False:
            print("Ese átomo no pertenece al compuesto!.")
            return None
        numEnlaces = 0
        for elem in self._enlaces:
            if elem[0] == nombre:
                numEnlaces += 1
            elif elem[1] == nombre:
                numEnlaces += 1
        return numEnlaces

    def masaMolar(self):
        masa = 0
        for elem in self._atomos:
            masa += elem[0]._pesoAtomico
        return masa

    def proporcionSobreMasa(self,elemento):
        if self.incluyeElemento(elemento) == True:
            return ((1 * ((self.atomosDeNum(elemento)) * elemento._pesoAtomico )) / self.masaMolar())
        elif self.incluyeElemento(elemento) == False:
            print("Este compuesto no contiene este elemento!")

    def agregarAtomos(self,elemento,cantidad):
        for i in range(0,cantidad):
            self.agregarAtomo(elemento)

    def enlazarConVarios(self,atom1,atoms):
        for elem in atoms:
            self.enlazar(atom1,elem)

    def enlacesOK(self):
        atomoEsta = True
        valenciaCorrecta = True
        for elem in self._enlaces:
            if (self.incluyeAtomo(elem[0]) and self.incluyeAtomo(elem[1])) == False:
                atomoEsta = False
        for elem in self._atomos:
            if elem[0]._valencia < self.cantEnlacesAtomo(elem[1]):
                valenciaCorrecta = False
        return (atomoEsta and valenciaCorrecta)

    def atomosConEnlacesSobrantes(self):
        conSobrantes = []
        for elem in self._atomos:
            if elem[0]._valencia < self.cantEnlacesAtomo(elem[1]):
                conSobrantes.append(elem[1])
        return conSobrantes

    def atomosConEnlacesDisponibles(self):
        conDisponibles = []
        for elem in self._atomos:
            if elem[0]._valencia > self.cantEnlacesAtomo(elem[1]):
                conDisponibles.append(elem[1])
        return conDisponibles

    def conQuienesEstaEnlazado(self,atomo):
        enlazadoCon = []
        for elem in self._enlaces:
            if elem[0] == atomo:
                enlazadoCon.append(elem[1])
            elif elem[1] == atomo:
                enlazadoCon.append(elem[0])
        return enlazadoCon

    def estanEnlazados(self,elem1,elem2):
        enlace_elem = (elem1,elem2)
        elementos1 = [elem2[0] for elem in [x[0] for x in self._enlaces] for elem2 in self._atomos if elem == elem2[1]]
        elementos2 = [elem2[0] for elem in [x[1] for x in self._enlaces] for elem2 in self._atomos if elem == elem2[1]]
        enlaces_elem1 = list(zip(elementos1,elementos2))
        enlaces_elem2 = list(zip(elementos2,elementos1))
        return (enlace_elem in enlaces_elem1) or (enlace_elem in enlaces_elem2)

class Medio():
    def __init__(self):
        self._componentes = {}

    def agregarComponente(self,componente,cantidad):
        if componente not in self._componentes:
            self._componentes[componente] = cantidad
        elif componente in self._componentes:
            self._componentes[componente] += cantidad

    def masaTotal(self):
        masa = 0
        for elem in list(self._componentes.items()):
            masa += (elem[0].masaMolar() * elem[1])
        return masa

    def elementosPresentes(self):
        elementos = []
        elementosPorCompuesto = ()
        for elem in self._componentes.keys():
            elementosPorCompuesto = elem.elementosPresentes()
            for elem in elementosPorCompuesto:
                if elem not in elementos:
                    elementos.append(elem)
            elementosPorCompuesto = ()
        return elementos

    def compuestosPresentes(self):
        return list(self._componentes.keys())

    def cantMolesElemento(self,elemento):
        molesAtom = 0
        for elem in list(self._componentes.items()):
            molesAtom += (elem[0].atomosDeNum(elemento) * elem[1])
        return molesAtom

    def masaDeCompuesto(self,comp):
        if comp not in self.compuestosPresentes():
            return 0
        elif comp in self.compuestosPresentes():
            return (self._componentes[comp] * comp.masaMolar())

    def masaDeElemento(self,elem):
        if elem not in self.elementosPresentes():
            return 0
        elif elem in self.elementosPresentes():
            return self.cantMolesElemento(elem) * elem._pesoAtomico

    def proporcionElementoSobreMasa(self,elem):
        return ((1 * self.masaDeElemento(elem)) / self.masaTotal())

    def proporcionCompuestoSobreMasa(self,comp):
        return ((1 * self.masaDeCompuesto(comp)) / self.masaTotal())

    def escalar(self,numero):
        for key in self._componentes:
            self._componentes[key] *= numero

    def incorporarMedio(self,medio2):
        self._componentes = Counter(self._componentes) + Counter(medio2._componentes)

    def masMedio(self,medio2):
        medionuevo = Medio()
        medionuevo._componentes = Counter(self._componentes) + Counter(medio2._componentes)
        return medionuevo

class descripcionMedio():
    def __init__(self,medio):
        self._medio = medio

    def apareceCompuesto(self,comp):
        return (re.search("\[" + comp._name + "\]",self._medio) is not None)

    def molesCompuesto(self,comp):
        return len(re.findall(comp._name,self._medio))

    def quienesAparecen(self,compuestos):
        elem_en_medio = []
        for elem in compuestos:
            if self.apareceCompuesto(elem) == True:
                elem_en_medio.append(elem)
        return elem_en_medio

    def agregarAMedio(self,medio,comp):
        medio.agregarComponente(comp,self.molesCompuesto(comp))

    def compuestosDesconocidos(self,listascompuestos):
        _compuestosDesconocidos = []
        for elem in listascompuestos:
            if self.apareceCompuesto(elem) == False:
                _compuestosDesconocidos.append(elem)
        return _compuestosDesconocidos

    def agregarTodosAMedio(self,medio,listaCompuestos):
        for elem in listaCompuestos:
            if self.apareceCompuesto(elem) == True:
                self.agregarAMedio(medio,elem)

    def agregarTodosAMedioConEscala(self,medio,listaCompuestos,escala):
        for elem in listaCompuestos:
            if self.apareceCompuesto(elem) == True:
                cant = (self.molesCompuesto(elem) * escala)
                medio.agregarComponente(elem,cant)

class descripcionesConCantidades(descripcionMedio):
    def __init__(self,medio):
        super().__init__(medio)

    def molesCompuesto(self, comp):
        if self.apareceCompuesto(comp) == True:
            cantidad = int((re.search("\[" + comp._name + "\]\((.*?)\)",self._medio).group(1)))
        elif self.apareceCompuesto(comp) == False:
            cantidad = 0
        return cantidad

class reaccionQuimica():
    def __init__(self,reactivos,productos):
        self._reactivos = reactivos
        self._productos = productos

    def sePuedeAplicar(self,medio):
        estan = []
        for elem in self._reactivos:
            if elem in medio.compuestosPresentes() and medio._componentes[elem] > 0:
                estan.append(True)
            elif elem not in medio.compuestosPresentes() or medio._componentes[elem] <= 0:
                estan.append(False)
        return all(estan)

    def maximoMoles(self,medio):
        if self.sePuedeAplicar(medio) == True:
            cant_limitante = inf
            for elem in self._reactivos:
                if medio._componentes[elem] < cant_limitante:
                    cant_limitante = medio._componentes[elem]
            return cant_limitante
        elif self.sePuedeAplicar(medio) == False:
            print("Esta reacción no se puede aplicar a este medio!")

    def aplicar(self,medio,proporcion):
        if self.sePuedeAplicar(medio) == True:
            cant_reaccion = self.maximoMoles(medio) * proporcion
            for elem in self._reactivos:
                medio._componentes[elem] -= cant_reaccion
                if medio._componentes[elem] == 0:
                    del medio._componentes[elem]
            for elem in self._productos:
                if elem not in medio._componentes:
                    medio.agregarComponente(elem,cant_reaccion)
                elif elem in medio._componentes:
                    medio._componentes[elem] += cant_reaccion
        elif self.sePuedeAplicar(medio) == False:
            print("Esta reacción no se puede aplicar a este medio!")




oxigeno = Elemento("Oxigeno", "O", 8, 8, 4)
hidrogeno = Elemento("Hidrogeno", "H", 1, 0, 1)
nitrogeno = Elemento("Nitrogeno", "N", 7, 7, 5)
carbono = Elemento("Carbono", "C", 6, 6, 4)
tabla = TablaPeriodica()
tabla.agregarElemento(oxigeno)
tabla.agregarElemento(hidrogeno)
tabla.agregarElemento(nitrogeno)
tabla.agregarElemento(carbono)
amoniaco = Compuesto("NH3")
amoniaco.agregarAtomo(tabla.elementoS("N"))
amoniaco.agregarAtomos(tabla.elementoS("H"), 3)
amoniaco.enlazarConVarios("N1", ["H1", "H2", "H3"])
agua = Compuesto("H2O")
agua.agregarAtomo(oxigeno)
agua.agregarAtomos(hidrogeno,2)
agua.enlazarConVarios("O1", ["H1", "H2"])
metano = Compuesto("CH4")
metano.agregarAtomo(carbono)
metano.agregarAtomos(hidrogeno,4)
metano.enlazarConVarios("C1", ["H1", "H2", "H3", "H4"])
dioxidoC = Compuesto("CO2")
dioxidoC.agregarAtomo(carbono)
dioxidoC.agregarAtomos(oxigeno,2)
dioxidoC.enlazarConVarios("C1", ["O1", "O2"])
dioxidoC.enlazarConVarios("C1", ["O1", "O2"])