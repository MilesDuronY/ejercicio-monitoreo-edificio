from abc import ABC, abstractmethod


class ObservadorAlerta(ABC):
    @abstractmethod
    def actualizar(self, mensaje: str) -> None:
        pass


class EquipoMantenimiento(ObservadorAlerta):
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.alertas: list[str] = []

    def actualizar(self, mensaje: str) -> None:
        self.alertas.append(mensaje)
        print(f"[MANTENIMIENTO] {mensaje}")


class ElementoMonitoreo(ABC):
    @abstractmethod
    def mostrar(self, nivel: int = 0) -> None:
        pass

    @abstractmethod
    def total_incidentes(self) -> int:
        pass

    @abstractmethod
    def sensores_con_incidentes(self) -> int:
        pass

    @abstractmethod
    def sensores_criticos(self) -> int:
        pass

    @abstractmethod
    def incidentes_del_sensor(self, nombre_sensor: str) -> int | None:
        pass

    @abstractmethod
    def reportar_incidente(self, nombre_sensor: str) -> bool:
        pass


class Sensor(ElementoMonitoreo):
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.incidentes = 0

    def mostrar(self, nivel: int = 0) -> None:
        print(
            f"{'  ' * nivel}- Sensor: {self.nombre} (incidentes: {self.incidentes})"
        )

    def total_incidentes(self) -> int:
        return self.incidentes

    def sensores_con_incidentes(self) -> int:
        return 1 if self.incidentes > 0 else 0

    def sensores_criticos(self) -> int:
        return 1 if self.incidentes >= 2 else 0

    def incidentes_del_sensor(self, nombre_sensor: str) -> int | None:
        # TODO: regresar los incidentes del sensor si el nombre coincide.
        raise NotImplementedError("Paso 1: resuelve la busqueda del sensor hoja.")

    def reportar_incidente(self, nombre_sensor: str) -> bool:
        if self.nombre == nombre_sensor:
            self.incidentes += 1
            return True
        return False


class Zona(ElementoMonitoreo):
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.elementos: list[ElementoMonitoreo] = []
        self.observadores: list[ObservadorAlerta] = []

    def agregar(self, elemento: ElementoMonitoreo) -> None:
        self.elementos.append(elemento)

    def agregar_observador(self, observador: ObservadorAlerta) -> None:
        # TODO: registrar al observador.
        raise NotImplementedError("Checkpoint 2: registra al observador.")

    def notificar_alerta(self, mensaje: str) -> None:
        # TODO: recorrer la lista y avisar a todos.
        raise NotImplementedError("Checkpoint 2: notifica a los observadores.")

    def mostrar(self, nivel: int = 0) -> None:
        # TODO: imprimir la zona y recorrer sus hijos con indentacion.
        raise NotImplementedError("Checkpoint 4: muestra la jerarquia de zonas.")

    def total_incidentes(self) -> int:
        # TODO: sumar recursivamente incidentes de todos los hijos.
        raise NotImplementedError("Checkpoint 1: suma todos los incidentes.")

    def sensores_con_incidentes(self) -> int:
        # TODO: contar cuantos sensores del arbol tienen al menos un incidente.
        raise NotImplementedError("Checkpoint 1: cuenta sensores con incidentes.")

    def sensores_criticos(self) -> int:
        # TODO: contar cuantos sensores del arbol ya son criticos.
        raise NotImplementedError("Paso 2: cuenta sensores criticos.")

    def incidentes_del_sensor(self, nombre_sensor: str) -> int | None:
        # TODO: buscar recursivamente cuantas incidencias lleva un sensor.
        raise NotImplementedError("Paso 4: busca el sensor en el arbol.")

    def reportar_incidente(self, nombre_sensor: str) -> bool:
        # TODO: buscar el sensor, actualizar el arbol y emitir la alerta final.
        raise NotImplementedError("Paso 5: reporta el incidente y alerta.")


def construir_edificio_demo() -> tuple[Zona, EquipoMantenimiento]:
    torre_norte = Zona("Torre Norte")
    lobby = Zona("Lobby")
    piso_2 = Zona("Piso 2")

    lobby.agregar(Sensor("Sensor Lobby"))
    piso_2.agregar(Sensor("Sensor Pasillo"))
    piso_2.agregar(Sensor("Sensor Sala Juntas"))

    torre_norte.agregar(lobby)
    torre_norte.agregar(piso_2)

    mantenimiento = EquipoMantenimiento("Turno manana")
    return torre_norte, mantenimiento


def main() -> None:
    torre_norte, mantenimiento = construir_edificio_demo()

    print("Estructura de monitoreo:")
    torre_norte.mostrar()

    torre_norte.agregar_observador(mantenimiento)
    print()

    if not torre_norte.reportar_incidente("Sensor Lobby"):
        print("No se encontro el sensor indicado.")
        return

    print()

    if not torre_norte.reportar_incidente("Sensor Lobby"):
        print("No se encontro el sensor indicado.")


if __name__ == "__main__":
    main()
