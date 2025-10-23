import cv2
import numpy as np
from matplotlib import pyplot as plt

# Caminho do vídeo
video_path = "samples/video1.mp4"

# Abre o vídeo
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

plt.ion()  # Modo interativo do matplotlib

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Converte o frame para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Calcula histogramas para H, S e V
    h_hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])  # Matiz (Hue)
    s_hist = cv2.calcHist([hsv], [1], None, [256], [0, 256])  # Saturação
    v_hist = cv2.calcHist([hsv], [2], None, [256], [0, 256])  # Valor

    # Mostra o vídeo
    cv2.imshow("Frame", frame)

    # Atualiza o histograma
    plt.clf()
    plt.subplot(3, 1, 1)
    plt.plot(h_hist, color='r')
    plt.title("Histograma - Matiz (H)")
    plt.xlim([0, 180])

    plt.subplot(3, 1, 2)
    plt.plot(s_hist, color='g')
    plt.title("Histograma - Saturação (S)")
    plt.xlim([0, 256])

    plt.subplot(3, 1, 3)
    plt.plot(v_hist, color='b')
    plt.title("Histograma - Valor (V)")
    plt.xlim([0, 256])

    plt.tight_layout()
    plt.pause(0.001)

    # Sai ao pressionar 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
plt.close()
