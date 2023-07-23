import mysql.connector
from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class AsistenciasService(ServiceBase):
    @rpc(Integer, Integer, _returns=Unicode)
    def CalcularPorcentaje(self, materia, alumno):
        db = mysql.connector.connect(
            host="localhost",
            user="Max",
            password="yatagarasu1224",
            database="DBasistencias"
        )

        try:
            cursor = db.cursor()
            cursor.execute("SELECT asistencia FROM Asistencias WHERE id_materias = %s AND id_alumnos = %s", (materia, alumno))
            asistencias = cursor.fetchall()
            cursor.execute("SELECT horas_tot FROM Materias WHERE id = %s", (materia,))
            horas = cursor.fetchone()
            cursor.execute("SELECT nombre, apellido_p, apellido_m FROM Alumnos WHERE id = %s", (alumno,))
            nom_alumno = cursor.fetchone()
            cursor.execute("SELECT nombre FROM Materias WHERE id = %s", (materia,))
            nom_materia = cursor.fetchone()
        except mysql.connector.Error as error:
            return f"Error al ejecutar la consulta: {error}"
        finally:
            if 'cursor' in locals():
                cursor.close()
            db.close()

        porcentaje = sum(i[0] for i in asistencias) / horas[0] * 100
        return f"El porcentaje de asistencias para la materia {nom_materia[0]} del alumno {nom_alumno[0]} {nom_alumno[1]} {nom_alumno[2]} es {porcentaje}%"

application = Application([AsistenciasService],
                          tns='soap.server',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(application)

    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
