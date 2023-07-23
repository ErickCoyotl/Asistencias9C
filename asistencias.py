import mysql.connector

def CalcularPorcentaje(materia, alumno):
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
        
print(CalcularPorcentaje(1, 20))