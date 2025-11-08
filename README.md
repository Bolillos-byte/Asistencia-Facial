# Asistencia Facial

Sistema en Python que registra la entrada y salida de personas mediante reconocimiento facial en tiempo real. Pensado para escuelas, oficinas o laboratorios que requieren control de asistencia sin tarjetas.

---

## Tecnologías
- Python 3  
- OpenCV  
- face_recognition (dlib)  
- CSV para registros

---

## Funcionalidades
- Detección y reconocimiento facial desde webcam  
- Registro automático de nombre y marca de tiempo en `registro.csv`  
- Carpeta `rostros/` para imágenes de referencia (nombre del archivo = etiqueta)  
- Evita duplicados por sesión

---

## Requisitos e instalación
`bash
pip install opencv-python face_recognition numpy

Nota: face_recognition depende de dlib; en algunos sistemas puede requerir compilación o paquetes adicionales.

Uso
- Coloca imágenes de cada usuario en rostros/ (ej. X.jpg).
- Ejecuta:
python main.py


- Presiona ESC para salir. Revisa registro.csv para ver las marcas de asistencia.
