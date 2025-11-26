import csv
import os
from datetime import datetime
from pathlib import Path
from Clase_Cliente.cliente import Cliente
from Clase_Turnos.turnos import Turnos

DATE_FORMAT = "%H:%M %d/%m/%Y"

class Gestor_de_Turnos:
    def __init__(self, archivo_csv=None):
        if archivo_csv is None:
            base = Path(__file__).resolve().parent.parent
            archivo_csv = base / "turnos.csv"
        else:
            archivo_csv = Path(archivo_csv)

        self.archivo_csv = str(archivo_csv)
        self.turnos = []
        self.dic_turnos = {}
        self.cargar_turnos_desde_csv()

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
        fecha_str = input(f"Ingrese Hora/Fecha ({DATE_FORMAT}): ")

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
        self.guardar_turno_en_csv()
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

        seleccion = input("Turno a modificar: ")
        if not seleccion.isdigit() or int(seleccion) not in range(1, len(encontrado) + 1):
            print("Selección incorrecta.")
            return
        
        t = encontrado[int(seleccion) - 1]
        nuevo_estado = input("Nuevo estado (Pendiente/Confirmado/Cancelado): ").capitalize()
        if nuevo_estado not in ["Pendiente", "Confirmado", "Cancelado"]:
            print("Estado inválido.")
            return
        
        t.estado = nuevo_estado
        self.actualizar_csv()
        self.sobre_escribir_csv()
        print("Turno modificado.")

# FILTRAR LAS FECHAS

    def filtrar_turnos_por_fecha(self):
        fecha_str = input("Ingrese fecha (dd/mm/yyyy): ")
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except ValueError:
            print("Fecha inexistente.")
            return
        
        turnos_filtrados = [t for t in self.turnos if t.hora_fecha.date() == fecha]
        if not turnos_filtrados:
            print("No hay turnos")
            return

        print(f"\n Turnos para {fecha_str}:") 
        for t in turnos_filtrados:
            print(f"Cliente: {t.cliente.nombre} | {t.hora_fecha.strftime(DATE_FORMAT)} | {t.servicio} | {t.estado}")

# ACTUALIZAR CSVDIST

    def actualizar_csv(self):
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

# GUARDADO Y CARGA DE CSV

    def guardar_turno_en_csv(self):
        archivo_vacio = not os.path.exists(self.archivo_csv) or os.path.getsize(self.archivo_csv) == 0

        with open(self.archivo_csv, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
                
            if archivo_vacio:
                writer.writerow(["nombre", "telefono", "dni", "email", "hora_fecha", "servicio", "estado"])
             
            ultimo = self.turnos[-1]
            writer.writerow([
                ultimo.cliente.nombre,
                ultimo.cliente.telefono,
                ultimo.cliente.dni,
                ultimo.cliente.email,
                ultimo.hora_fecha.strftime(DATE_FORMAT),
                ultimo.servicio,
                ultimo.estado
            ])
    
    def sobre_escribir_csv(self):
        with open(self.archivo_csv, "w", newline="", encoding="utf-8") as csvfile:
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

    def cargar_turnos_desde_csv(self):
        if not os.path.exists(self.archivo_csv):
            return
        
        with open(self.archivo_csv, "r", newline="", encoding="utf-8") as csvfile:
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
        self.actualizar_csv()