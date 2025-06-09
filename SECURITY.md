from abc import ABC, abstractmethod

class Vehiculo(ABC):
    @abstractmethod
    def conducir(self):
        pass

class Auto(Vehiculo):
    def conducir(self):
        print("Conduciendo un auto")

mi_auto = Auto()
mi_auto.conducir()
