class Turnos:
    def __init__(self, cliente, hora_fecha, servicio, estado="Pendiente"):
        self.cliente = cliente
        self.hora_fecha = hora_fecha
        self.servicio = servicio
        self.estado = estado