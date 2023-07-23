import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

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
    return nom_materia[0], f"{nom_alumno[0]} {nom_alumno[1]} {nom_alumno[2]}", porcentaje

@app.route('/api/porcentaje', methods=['GET'])
def obtener_porcentaje():
    materia = int(request.args.get('materia'))
    alumno = int(request.args.get('alumno'))
    
    nom_materia, nom_alumno, porcentaje = CalcularPorcentaje(materia, alumno)
    return jsonify({'Materia' : nom_materia, 'Alumno' : nom_alumno , 'Porcentaje': porcentaje})

if __name__ == '__main__':
    app.run(debug=True)
