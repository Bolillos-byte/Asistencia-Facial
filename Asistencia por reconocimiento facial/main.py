# asistencia_facial/main.py
import os
import csv
import cv2
import face_recognition
from datetime import datetime

ROSTROS_DIR = "rostros"
REGISTRO_CSV = "registro.csv"

# Cargar codificaciones conocidas
rostros_conocidos = []
nombres_conocidos = []

def cargar_rostros():
    for archivo in os.listdir(ROSTROS_DIR):
        ruta = os.path.join(ROSTROS_DIR, archivo)
        if not os.path.isfile(ruta):
            continue
        try:
            imagen = face_recognition.load_image_file(ruta)
            codif = face_recognition.face_encodings(imagen)
            if codif:
                rostros_conocidos.append(codif[0])
                nombres_conocidos.append(os.path.splitext(archivo)[0])
                print(f"Cargado: {archivo}")
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")

def registrar_asistencia(nombre):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Evitar duplicados de la misma sesión
    try:
        with open(REGISTRO_CSV, "r", newline="") as f:
            existentes = [row[0] for row in csv.reader(f)]
    except FileNotFoundError:
        existentes = []
    if nombre not in existentes:
        with open(REGISTRO_CSV, "a", newline="") as f:
            csv.writer(f).writerow([nombre, ahora])
        print(f"Asistencia registrada: {nombre} - {ahora}")

def main():
    if not os.path.isdir(ROSTROS_DIR):
        os.makedirs(ROSTROS_DIR)
        print(f"Crea la carpeta '{ROSTROS_DIR}' y coloca imágenes de referencia.")
        return

    cargar_rostros()
    if not rostros_conocidos:
        print("No hay rostros cargados. Agrega imágenes en la carpeta 'rostros'.")
        return

    camara = cv2.VideoCapture(0)
    if not camara.isOpened():
        print("No se encontró la cámara.")
        return

    print("Presiona ESC para salir.")
    while True:
        ret, frame = camara.read()
        if not ret:
            break

        small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        rgb = small_frame[:, :, ::-1]

        ubicaciones = face_recognition.face_locations(rgb)
        codificaciones = face_recognition.face_encodings(rgb, ubicaciones)

        for codif, ubic in zip(codificaciones, ubicaciones):
            coincidencias = face_recognition.compare_faces(rostros_conocidos, codif, tolerance=0.5)
            nombre = "Desconocido"
            if True in coincidencias:
                idx = coincidencias.index(True)
                nombre = nombres_conocidos[idx]
                registrar_asistencia(nombre)

            top, right, bottom, left = [v*2 for v in ubic]  # reescalar coordenadas
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, nombre, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        cv2.imshow("Asistencia Facial", frame)
        if cv2.waitKey(1) == 27:
            break

    camara.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()