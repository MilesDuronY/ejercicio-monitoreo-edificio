import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

import monitoreo_edificio_base as modulo


def test_sensor_incrementa_su_conteo() -> None:
    sensor = modulo.Sensor("Sensor Lobby")
    sensor.reportar_incidente("Sensor Lobby")
    assert sensor.total_incidentes() == 1
    assert sensor.incidentes_del_sensor("Sensor Lobby") == 1
    assert sensor.sensores_criticos() == 0


def test_zona_suma_incidentes_de_toda_la_jerarquia() -> None:
    torre = modulo.Zona("Torre Norte")
    lobby = modulo.Zona("Lobby")
    sensor_lobby = modulo.Sensor("Sensor Lobby")
    sensor_pasillo = modulo.Sensor("Sensor Pasillo")

    sensor_lobby.reportar_incidente("Sensor Lobby")
    sensor_lobby.reportar_incidente("Sensor Lobby")
    sensor_pasillo.reportar_incidente("Sensor Pasillo")

    lobby.agregar(sensor_lobby)
    torre.agregar(lobby)
    torre.agregar(sensor_pasillo)

    assert torre.total_incidentes() == 3
    assert torre.sensores_con_incidentes() == 2
    assert torre.sensores_criticos() == 1
    assert torre.incidentes_del_sensor("Sensor Lobby") == 2


def test_reportar_incidente_envia_alerta_al_equipo() -> None:
    torre = modulo.Zona("Torre Norte")
    lobby = modulo.Zona("Lobby")
    equipo = modulo.EquipoMantenimiento("Turno manana")
    lobby.agregar(modulo.Sensor("Sensor Lobby"))
    torre.agregar(lobby)
    torre.agregar_observador(equipo)

    encontrado = torre.reportar_incidente("Sensor Lobby")
    encontrado_segundo = torre.reportar_incidente("Sensor Lobby")

    assert encontrado is True
    assert encontrado_segundo is True
    assert torre.total_incidentes() == 2
    assert torre.sensores_con_incidentes() == 1
    assert torre.sensores_criticos() == 1
    assert len(equipo.alertas) == 2
    assert "Sensor Lobby" in equipo.alertas[0]
    assert "Total acumulado: 1" in equipo.alertas[0]
    assert "Nivel de alerta: MEDIA" in equipo.alertas[0]
    assert "Sensores criticos: 1" in equipo.alertas[1]
    assert "Total acumulado: 2" in equipo.alertas[1]
    assert "Nivel de alerta: ALTA" in equipo.alertas[1]


def test_main_muestra_flujo_completo_para_github_preset() -> None:
    salida = io.StringIO()

    with redirect_stdout(salida):
        modulo.main()

    texto = salida.getvalue()

    assert "Estructura de monitoreo:" in texto
    assert "- Zona: Torre Norte" in texto
    assert "- Sensor: Sensor Lobby" in texto
    assert "Nivel de alerta: MEDIA" in texto
    assert "Nivel de alerta: ALTA" in texto
