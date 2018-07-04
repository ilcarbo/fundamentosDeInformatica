import unittest
import TPlimpio

oxigeno = TPlimpio.oxigeno
hidrogeno = TPlimpio.hidrogeno
nitrogeno = TPlimpio.nitrogeno
carbono = TPlimpio.carbono
tabla = TPlimpio.tabla
amoniaco = TPlimpio.amoniaco
agua = TPlimpio.agua
metano = TPlimpio.metano
dioxidoC = TPlimpio.dioxidoC

def crearMedioReaccion():
    medioParaReaccion = TPlimpio.Medio()
    medioParaReaccion.agregarComponente(agua, 100)
    medioParaReaccion.agregarComponente(metano, 50)
    medioParaReaccion.agregarComponente(amoniaco, 20)
    return medioParaReaccion

def crearMedioEscalable():
    medioEscalable = TPlimpio.Medio()
    medioEscalable.agregarComponente(agua, 20)
    medioEscalable.agregarComponente(amoniaco, 1)
    return medioEscalable

def crearMedioRaro():
    medioRaro = TPlimpio.Medio()
    medioRaro.agregarComponente(agua, 100)
    medioRaro.agregarComponente(amoniaco, 6)
    medioRaro.agregarComponente(metano, 20)
    medioRaro.agregarComponente(dioxidoC, 14)
    medioRaro.agregarComponente(amoniaco, 15)
    return medioRaro

def crearDescripcion():
    Descripcion = TPlimpio.descripcionMedio("[H2O][CO2][H2O][CH4]")
    return Descripcion

def crearDescripcionCant():
    DescripcionCant = TPlimpio.descripcionesConCantidades("[H2O](1000)[CO2](50)[CH4](25)")
    return DescripcionCant

def crearReaccion():
    reaccion = TPlimpio.reaccionQuimica([agua,metano,amoniaco],[dioxidoC,agua])
    return reaccion

class AtomosTest(unittest.TestCase):
    def test_creacion(self):
        self.assertEqual(8, oxigeno.cantProtones())
        self.assertEqual(8, oxigeno.cantNeutrones())
        self.assertEqual(8, oxigeno.cantElectrones())
        self.assertEqual(8, oxigeno.numeroAtomico())
        self.assertEqual(16, oxigeno.pesoAtomico())
        self.assertEqual(4, oxigeno.valencia())
        self.assertEqual("O", oxigeno.simbolo())
        self.assertEqual(1, hidrogeno.cantProtones())
        self.assertEqual(0, hidrogeno.cantNeutrones())
        self.assertEqual(1, hidrogeno.cantElectrones())
        self.assertEqual(1, hidrogeno.numeroAtomico())
        self.assertEqual(1, hidrogeno.pesoAtomico())
        self.assertEqual(1, hidrogeno.valencia())
        self.assertEqual("H", hidrogeno.simbolo())

class TablasTest(unittest.TestCase):
    def test_tabla(self):
        self.assertEqual(4, len(tabla.elementos()))
        self.assertEqual(6, tabla.elementoS("C").numeroAtomico())
        self.assertEqual(14, tabla.elementoN(7).pesoAtomico())

class CompuestosTests(unittest.TestCase): #cambiarTest en funcion de nueva definición de agregar atomo.
    def test_compuesto(self):
        self.assertEqual(4, amoniaco.cantAtomos())
        self.assertEqual(["H1", "H2", "H3"], amoniaco.atomosDe(tabla.elementoS("H")))
        self.assertEqual(True, amoniaco.incluyeAtomo("N1"))
        self.assertEqual(False, amoniaco.incluyeAtomo("H4"))
        self.assertEqual(True, amoniaco.incluyeElemento(tabla.elementoS("N")))
        self.assertEqual(False, amoniaco.incluyeElemento(tabla.elementoS("O")))
        self.assertEqual(["N", "H"], [elem.simbolo() for elem in amoniaco.elementosPresentes()])
        self.assertEqual(3, amoniaco.cantEnlaces())
        self.assertEqual(1, amoniaco.cantEnlacesAtomo("H2"))
        self.assertEqual(17, amoniaco.masaMolar())
        self.assertAlmostEqual(0.8235, amoniaco.proporcionSobreMasa(tabla.elementoS("N")), places= 4) #hacer almost equal?SI,
        self.assertEqual(True, amoniaco.enlacesOK())
        self.assertEqual([], amoniaco.atomosConEnlacesSobrantes())
        self.assertEqual(["N1"], amoniaco.atomosConEnlacesDisponibles())
        self.assertEqual(["H1", "H2", "H3"], amoniaco.conQuienesEstaEnlazado("N1"))
        self.assertEqual(["N1"], amoniaco.conQuienesEstaEnlazado("H2"))
        self.assertEqual(True, amoniaco.estanEnlazados(nitrogeno,hidrogeno))

class medioTests(unittest.TestCase):
    def test_Medio(self):
        medioRaro = crearMedioRaro()
        self.assertEqual(3093, medioRaro.masaTotal())
        self.assertCountEqual([hidrogeno, oxigeno, nitrogeno, carbono], medioRaro.elementosPresentes())
        self.assertCountEqual([agua,amoniaco,metano,dioxidoC], medioRaro.compuestosPresentes())
        self.assertEqual(128, medioRaro.cantMolesElemento(oxigeno))
        self.assertEqual(343, medioRaro.cantMolesElemento(hidrogeno))
        self.assertEqual(1800, medioRaro.masaDeCompuesto(agua))
        self.assertEqual(357, medioRaro.masaDeCompuesto(amoniaco))
        self.assertEqual(2048, medioRaro.masaDeElemento(oxigeno))
        self.assertEqual(408, medioRaro.masaDeElemento(carbono))
        self.assertAlmostEqual(0.5819, medioRaro.proporcionCompuestoSobreMasa(agua), places = 3) # hacer almostEqual para estos 3
        self.assertAlmostEqual(0.6621, medioRaro.proporcionElementoSobreMasa(oxigeno), places = 3)
        self.assertAlmostEqual(0.1108, medioRaro.proporcionElementoSobreMasa(hidrogeno), places = 3) # almostEqual con 4 decimales?

class medioOpcTests(unittest.TestCase):
    def test_MedioOpc(self):
        medioEscalable = crearMedioEscalable()
        medioRaro = crearMedioRaro()
        self.assertEqual(360, medioEscalable.masaDeCompuesto(agua))
        self.assertEqual(17, medioEscalable.masaDeCompuesto(amoniaco))
        self.assertCountEqual([agua, amoniaco], medioEscalable.compuestosPresentes())
        medioEscalable.escalar(5)
        self.assertEqual(1800, medioEscalable.masaDeCompuesto(agua))
        self.assertEqual(85, medioEscalable.masaDeCompuesto(amoniaco))
        medioEscalable.incorporarMedio(medioRaro)
        self.assertCountEqual([agua, amoniaco, metano, dioxidoC], medioEscalable.compuestosPresentes())
        self.assertEqual(3600, medioEscalable.masaDeCompuesto(agua))
        self.assertEqual(442, medioEscalable.masaDeCompuesto(amoniaco))
        medioNuevo = medioEscalable.masMedio(medioRaro)
        self.assertEqual(3600, medioEscalable.masaDeCompuesto(agua))
        self.assertEqual(442, medioEscalable.masaDeCompuesto(amoniaco))
        self.assertEqual(5400, medioNuevo.masaDeCompuesto(agua))
        self.assertEqual(799, medioNuevo.masaDeCompuesto(amoniaco))

class descripcionTests(unittest.TestCase):
    def test_descripcion(self):
        miDescripcion = crearDescripcion()
        medioRaro = crearMedioRaro()
        self.assertEqual(True, miDescripcion.apareceCompuesto(agua))
        self.assertEqual(True, miDescripcion.apareceCompuesto(dioxidoC))
        self.assertEqual(False, miDescripcion.apareceCompuesto(amoniaco))
        self.assertEqual(2, miDescripcion.molesCompuesto(agua))
        self.assertEqual(1, miDescripcion.molesCompuesto(dioxidoC))
        self.assertEqual(0, miDescripcion.molesCompuesto(amoniaco))
        self.assertCountEqual([agua, metano], miDescripcion.quienesAparecen([agua, amoniaco, metano]))
        self.assertEqual([amoniaco], miDescripcion.compuestosDesconocidos([agua,amoniaco,metano]))
        self.assertEqual(1800, medioRaro.masaDeCompuesto(agua))
        self.assertEqual(357, medioRaro.masaDeCompuesto(amoniaco))
        self.assertEqual(320, medioRaro.masaDeCompuesto(metano))
        miDescripcion.agregarAMedio(medioRaro, agua)
        miDescripcion.agregarAMedio(medioRaro, metano)
        miDescripcion.agregarAMedio(medioRaro, amoniaco)
        self.assertEqual(1836, medioRaro.masaDeCompuesto(agua))
        self.assertEqual(357, medioRaro.masaDeCompuesto(amoniaco))
        self.assertEqual(336, medioRaro.masaDeCompuesto(metano))

class descripcionCantTests(unittest.TestCase):
    def test_descripcionCant(self):
        miDescripcionCant = crearDescripcionCant()
        medioRaro = crearMedioRaro()
        self.assertEqual(True, miDescripcionCant.apareceCompuesto(agua))
        self.assertEqual(True, miDescripcionCant.apareceCompuesto(metano))
        self.assertEqual(False, miDescripcionCant.apareceCompuesto(amoniaco))
        self.assertEqual(1000, miDescripcionCant.molesCompuesto(agua))
        self.assertEqual(50, miDescripcionCant.molesCompuesto(dioxidoC))
        self.assertEqual(25, miDescripcionCant.molesCompuesto(metano))
        self.assertCountEqual([agua, metano], miDescripcionCant.quienesAparecen([agua, amoniaco, metano]))
        self.assertEqual([amoniaco], miDescripcionCant.compuestosDesconocidos([agua, amoniaco, metano]))
        self.assertEqual(1800, medioRaro.masaDeCompuesto(agua))
        self.assertEqual(357, medioRaro.masaDeCompuesto(amoniaco))
        self.assertEqual(320, medioRaro.masaDeCompuesto(metano))
        self.assertEqual(616, medioRaro.masaDeCompuesto(dioxidoC))
        miDescripcionCant.agregarTodosAMedio(medioRaro, [agua, metano, amoniaco])
        self.assertEqual(19800, medioRaro.masaDeCompuesto(agua))
        self.assertEqual(357, medioRaro.masaDeCompuesto(amoniaco))
        self.assertEqual(720, medioRaro.masaDeCompuesto(metano))
        self.assertEqual(616, medioRaro.masaDeCompuesto(dioxidoC))
        miDescripcionCant.agregarTodosAMedioConEscala(medioRaro, [agua], 0.1)
        self.assertEqual(21600, medioRaro.masaDeCompuesto(agua))

class reaccionesQuimicasTests(unittest.TestCase):
    def test_reaccionesQuim(self):
        medioParaReaccion = crearMedioReaccion()
        medioEscalable = crearMedioEscalable()
        reaccion = crearReaccion()
        self.assertEqual(True, reaccion.sePuedeAplicar(medioParaReaccion))
        self.assertEqual(20, reaccion.maximoMoles(medioParaReaccion))
        self.assertCountEqual([agua,metano,amoniaco], medioParaReaccion.compuestosPresentes())
        self.assertEqual(1800, medioParaReaccion.masaDeCompuesto(agua))
        self.assertEqual(340, medioParaReaccion.masaDeCompuesto(amoniaco))
        self.assertEqual(800, medioParaReaccion.masaDeCompuesto(metano))
        self.assertEqual(0, medioParaReaccion.masaDeCompuesto(dioxidoC))
        reaccion.aplicar(medioParaReaccion,0.5)
        self.assertCountEqual([agua,metano,amoniaco,dioxidoC], medioParaReaccion.compuestosPresentes())
        self.assertEqual(1800, medioParaReaccion.masaDeCompuesto(agua))
        self.assertEqual(170, medioParaReaccion.masaDeCompuesto(amoniaco))
        self.assertEqual(640, medioParaReaccion.masaDeCompuesto(metano))
        self.assertEqual(440, medioParaReaccion.masaDeCompuesto(dioxidoC))
        self.assertEqual(False, reaccion.sePuedeAplicar(medioEscalable))







