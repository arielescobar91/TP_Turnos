from Gestor.gestor_de_turnos import Gestor_de_Turnos

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