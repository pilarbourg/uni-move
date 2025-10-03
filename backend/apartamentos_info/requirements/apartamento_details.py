class ApartmentDetailNotFound(Exception):
    pass


class ApartmentDetail:
    def __init__(self, id_: int, titulo: str, descripcion: str, direccion: str,
                 barrio: str, precio: float, tamaño_m2: int, amueblado: int, disponible: int):
        self.id = id_
        self.titulo = titulo
        self.descripcion = descripcion
        self.direccion = direccion
        self.barrio = barrio
        self.precio = precio
        self.tamaño_m2 = tamaño_m2
        self.amueblado = amueblado
        self.disponible = disponible

    def __repr__(self):
        return f"{self.titulo} - {self.barrio} ({self.precio}€)"
