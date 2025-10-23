import cv2
import numpy as np
import argparse
import os
import time

# ------------------------------
# Configuração de argumentos CLI
# ------------------------------
parser = argparse.ArgumentParser(description="Segmentação HSV e K-Means em imagem ou vídeo")
parser.add_argument("--input", type=str, required=True,
                    help="Caminho do arquivo de imagem/vídeo ou '0' para webcam")
parser.add_argument("--method", type=str, choices=["hsv", "kmeans"], default="hsv",
                    help="Método de segmentação")
parser.add_argument("--target", type=str, choices=["green", "blue"], default="green",
                    help="Cor alvo")
parser.add_argument("--k", type=int, default=3,
                    help="Número de clusters para K-Means")
parser.add_argument("--hmin", type=int, default=35)
parser.add_argument("--hmax", type=int, default=120)
parser.add_argument("--smin", type=int, default=40)
parser.add_argument("--smax", type=int, default=255)
parser.add_argument("--vmin", type=int, default=0)
parser.add_argument("--vmax", type=int, default=255)
args = parser.parse_args()

os.makedirs("outputs", exist_ok=True)

# ------------------------------
# Função: segmentação por cor HSV
# ------------------------------
def segment_hsv(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([args.hmin, args.smin, args.vmin])
    upper = np.array([args.hmax, args.smax, args.vmax])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    return mask, result

# ------------------------------
# Função: segmentação por K-Means
# ------------------------------
def segment_kmeans(frame):
    Z = frame.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(Z, args.k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented = centers[labels.flatten()].reshape(frame.shape)

    target_color = np.array([0, 255, 0]) if args.target == "green" else np.array([255, 0, 0])
    distances = np.linalg.norm(centers - target_color, axis=1)
    cluster_target = np.argmin(distances)

    mask = (labels.flatten() == cluster_target).astype(np.uint8).reshape(frame.shape[:2]) * 255
    result = cv2.bitwise_and(frame, frame, mask=mask)
    return mask, result

# ------------------------------
# Função auxiliar para salvar resultados
# ------------------------------
def salvar_resultados(frame, mask, result, basename):
    overlay = cv2.addWeighted(frame, 0.7, result, 0.3, 0)
    cv2.imwrite(f"outputs/{basename}_mask.png", mask)
    cv2.imwrite(f"outputs/{basename}_overlay.png", overlay)
    print(f"[+] Resultados salvos em outputs/{basename}_*.png")
    return overlay

# ------------------------------
# Função principal de processamento
# ------------------------------
def processar_frame(frame, basename="frame"):
    start = time.time()
    if args.method == "hsv":
        mask, result = segment_hsv(frame)
    else:
        mask, result = segment_kmeans(frame)

    duration = time.time() - start
    percent = np.sum(mask > 0) / mask.size * 100
    print(f"[{args.method.upper()}] {percent:.2f}% segmentado em {duration:.2f}s")
    overlay = salvar_resultados(frame, mask, result, basename)
    return mask, overlay

# ------------------------------
# Lógica para entrada (imagem, vídeo ou webcam)
# ------------------------------
input_src = args.input

if input_src == "0":
    cap = cv2.VideoCapture(0)
    basename = "webcam"
elif input_src.lower().endswith((".mp4", ".avi", ".mov")):
    cap = cv2.VideoCapture(input_src)
    basename = os.path.splitext(os.path.basename(input_src))[0]
else:
    frame = cv2.imread(input_src)
    if frame is None:
        print(f"Erro: não foi possível abrir {input_src}")
        exit()
    mask, overlay = processar_frame(frame, os.path.splitext(os.path.basename(input_src))[0])
    cv2.imshow("Original", frame)
    cv2.imshow("Resultado", overlay)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit()

# ------------------------------
# Loop para vídeos / webcam
# ------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    mask, overlay = processar_frame(frame, basename)
    cv2.imshow("Original", frame)
    cv2.imshow("Resultado", overlay)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Encerrando...")
        break

cap.release()
cv2.destroyAllWindows()
