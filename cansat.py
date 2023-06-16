import serial
import pyodbc
import time
import re

# Configurar la comunicación serie
ser = serial.Serial("COM6", 9600)  # Ajusta el puerto y la velocidad según corresponda

try:
    # Configuración de la conexión a la base de datos
    server = "tcp:serverejemplo.database.windows.net"
    database = "pruebasensor"
    username = "{jhe0602}"
    password = "{Jhe2390939**}"
    driver = "{ODBC Driver 18 for SQL Server}"

    # Establecer la conexión a la base de datos
    conn = pyodbc.connect(
        "DRIVER="
        + driver
        + ";SERVER="
        + server
        + ";PORT=1433;DATABASE="
        + database
        + ";UID="
        + username
        + ";PWD="
        + password
    )
    cursor = conn.cursor()

    # Imprimir un mensaje si la conexión se estableció correctamente
    print("Conexión exitosa a la base de datos.")

except pyodbc.Error as ex:
    # Imprimir un mensaje si se produce un error al establecer la conexión
    print("Error al establecer la conexión a la base de datos:", ex)

tiempo_inicio = time.time()

while True:
    # Leer una línea de datos del Arduino
    data = ser.readline().decode().strip()  # Decodificar los bytes recibidos a texto

    # Dividir los valores en función del separador utilizado (coma en este caso)
    valores = data.split(",")
    # print(valores)

    numeros = []
    for valor in valores:
        # Buscar números decimales en el elemento
        matches = re.findall(r"\d+\.\d+", valor)
        if matches:
            numero = float(matches[0])  # Convertir a tipo float
            numeros.append(numero)

    consulta = f"INSERT INTO DatosSensor (tempBME, presion, altitud, humBME, tempDHT, humDHT) VALUES (?,?,?,?,?,?)"

    for valor in numeros:
        cursor.execute(consulta, numeros)
        conn.commit()

    # Detener la captura después de un minuto
    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - tiempo_inicio
    if tiempo_transcurrido >= 10800:
        break

# Cerrar conexion BD y la comunicación serie
conn.close()
ser.close()
