import csv
import os
from datetime import datetime

DATE_FORMAT = "%H:%M %d/%m/%Y"
# CLASES

class Cliente:
    def __init__(self, nombre, telefono, dni, email):
        self.nombre = nombre
        self.telefono = telefono
        self.dni = dni
        self.email = email


class Turnos:
    def __init__(self, cliente, hora_fecha, servicio, estado="Pendiente"):
        self.cliente = cliente
        self.hora_fecha = hora_fecha
        self.servicio = servicio
        self.estado = estado


class Gestor_de_Turnos:
    def __init__(self, archivo_csvdist="turnos.csv"):
        self.archivo_csvdist = archivo_csvdist
        self.turnos = []
        self.dic_turnos = {}
        self.cargar_turnos_desde_csvdist()


# REGISTRO DE CLIENTES

    def registrar_cliente(self):
        nombre = input("Ingrese el nombre: ")
        telefono = input("Ingrese el teléfono: ")
        dni = input("Ingrese el DNI: ")
        email = input("Ingrese el email: ")
        nuevo_cliente = Cliente(nombre, telefono, dni, email)
        return nuevo_cliente
    
# GESTIÓN DE TURNOS

    def solicitar_turno(self):
        cliente = self.registrar_cliente()
        fecha_str = input("Ingrese Hora/Fecha ({DATE_FORMAT}): ")

        try:
            fecha = datetime.strptime(fecha_str, DATE_FORMAT)
        except ValueError:
            print("Hora/Fecha incorrectas")
            return
        
        servicio = input("Servicio: ")

        if self.turno_duplicado(fecha):
            print("Ya existe un turno para esa Hora/Fecha.")
            return
        
        turno = Turnos(cliente, fecha, servicio)
        self.turnos.append(turno)
        self.actualizar_csvdist()
        self.guardar_turno_en_csvdist()
        print("Turno Guardado.")

# VERIFICACIÓN TURNOS DUPLICADOS

    def turno_duplicado(self, fecha):
        for turno in self.turnos:
            if turno.hora_fecha == fecha:
                print("Turno Existente.")
                return True
        return False
    
# LISTA 

    def listar_turnos(self):
        if not self.turnos:
            print("No hay registro.")
            return
        
        print("Lista de Turnos:")
        for t in sorted(self.turnos, key=lambda x: x.hora_fecha):
            print(f"Cliente: {t.cliente.nombre} | {t.hora_fecha.strftime(DATE_FORMAT)} | {t.servicio} | {t.estado}")

# MODIFICACION DE TURNOS

    def modificar_turno(self):
        telefono = input("Telefono del cliente: ")
        encontrado = [t for t in self.turnos if t.cliente.telefono == telefono]

        if not encontrado:
            print("No existe turno previo.")
            return
        
        for i, t in enumerate(encontrado, 1):
            print(f"{i}. {t.hora_fecha.strftime(DATE_FORMAT)} | {t.servicio} | {t.estado}")

        seleccion = int(input("Turno a modificar: "))
        if not seleccion.isdigit() or int(seleccion) not in range(1, len(encontrado) + 1):
            print("Selección incorrecta.")
            return
        
        t = encontrado[int(seleccion) - 1]
        nuevo_estado = input("Nuevo estado (Pendiente/Confirmado/Cancelado): ")
        t.estado = nuevo_estado
        self.actualizar_csvdist()
        self.guardar_turno_en_csvdist()
        print("Turno modificado.")

# FILTRAR LAS FECHAS

    def filtrar_turnos_por_fecha(self):
        fecha_str = input("Ingrese fecha (dd/mm/yyyy): ")
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except ValueError:
            print("Fecha inesixtente.")
            return
        
        turnos_filtrados = [t for t in self.turnos if t.hora_fecha.date() == fecha]
        if not turnos_filtrados:
            print("No hay turnos")
            return

        print(f"\n Turnos para {fecha_str}:") 
        for t in turnos_filtrados:
            print(f"Cliente: {t.cliente.nombre} | {t.hora_fecha.strftime(DATE_FORMAT)} | {t.servicio} | {t.estado}")

# ACTUALIZAR CSVDIST

    def actualizar_csvdist(self):
        self.dic_turnos = {}
        for i, t in enumerate(self.turnos):
            self.dic_turnos[i] = {
                "nombre": t.cliente.nombre,
                "telefono": t.cliente.telefono,
                "dni": t.cliente.dni,
                "email": t.cliente.email,
                "hora_fecha": t.hora_fecha.strftime(DATE_FORMAT),
                "servicio": t.servicio,
                "estado": t.estado
            }

# GUARDADO Y CARGA DE CSVDIST

    def guardar_turno_en_csvdist(self):
        with open(self.archivo_csvdist, "w", newline="", encoding="utf-8") as csvfile:
             writer = csv.writer(csvfile)
             writer.writerow(["nombre", "telefono", "dni", "email", "hora_fecha", "servicio", "estado"])
             for t in self.turnos:
                 writer.writerow([
                     t.cliente.nombre,
                     t.cliente.telefono,
                     t.cliente.dni,
                     t.cliente.email,
                     t.hora_fecha.strftime(DATE_FORMAT),
                     t.servicio,
                     t.estado
                 ])

    def cargar_turnos_desde_csvdist(self):
        if not os.path.exists(self.archivo_csvdist):
            return
        
        with open(self.archivo_csvdist, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cliente = Cliente(
                    row["nombre"],
                    row["telefono"],
                    row["dni"],
                    row["email"]
                )
                hora_fecha = datetime.strptime(row["hora_fecha"], DATE_FORMAT)
                servicio = row["servicio"]
                estado = row["estado"]
                turno = Turnos(cliente, hora_fecha, servicio, estado)
                self.turnos.append(turno)
        self.actualizar_csvdist()

# MENU

def main():
    gestor = Gestor_de_Turnos()

    while True:
        print("\n--- Menú de Peluquería ---")
        print("1. Solicitar Turno")
        print("2. Listar Turnos")
        print("3. Modificar Turno")
        print("4. Filtrar Turnos por Fecha")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestor.solicitar_turno()
        elif opcion == "2":
            gestor.listar_turnos()
        elif opcion == "3":
            gestor.modificar_turno()
        elif opcion == "4":
            gestor.filtrar_turnos_por_fecha()
        elif opcion == "5":
            print("Saliendo.")
            break
        else:
            print("Opción incorrecta.")

if __name__ == "__main__":
    main()