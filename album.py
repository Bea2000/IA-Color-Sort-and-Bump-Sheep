class Animales:
    def __init__(self):
        self.lista = []
    
    def dormir(self, animal):
        print("zzz" + animal.nombre)

class Perro:
    def __init__(self, n, e, r):
        self.nombre = n
        self.edad = e
        self.raza = r
        self.frase = ""
    
    def ladrar(self):
        print("woof!", self.frase)
        
    def __str__(self):
        return "Hola me llamo " + self.nombre
    
class Gato:
    def __init__(self, n, e, r):
        self.nombre = n
        self.edad = e
        self.raza = r
        self.frase = ""

perrito = Perro("Baldor", 3, "Quiltro")
gatito = Gato("Baldor", 3, "Quiltro")
animales = Animales()
animales.lista.append(perrito)
animales.lista.append(gatito)

animales.dormir(perrito)
print(animales.lista)