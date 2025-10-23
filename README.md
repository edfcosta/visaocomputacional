# Segmentação de Cor — HSV e K-Means

Este projeto realiza segmentação de cor em imagens, vídeos ou webcam, utilizando dois métodos: **HSV Thresholding** e **K-Means Clustering**.  
Ele permite isolar regiões de cor específicas (verde ou azul), exibindo e salvando os resultados automaticamente.

---

## 1. Bibliotecas Utilizadas

### **OpenCV (`cv2`)**
Usada para leitura, exibição e processamento de imagens/vídeos.  
Funções principais:
- `cv2.imread()` / `cv2.VideoCapture()` — leitura de arquivos e captura de vídeo.
- `cv2.cvtColor()` — conversão entre espaços de cor (ex: BGR → HSV).
- `cv2.inRange()` — criação de máscaras baseadas em limites de cor.
- `cv2.kmeans()` — aplicação do algoritmo de clusterização K-Means.
- `cv2.imshow()` e `cv2.imwrite()` — exibição e salvamento de resultados.

### **NumPy (`numpy`)**
Usado para operações matriciais, manipulação de pixels e cálculos vetoriais.  
Funções principais:
- Criação de arrays (`np.array`, `np.uint8`).
- Cálculo de distâncias (`np.linalg.norm`).
- Operações de máscara e porcentagem de pixels segmentados.

### **Argparse**
Responsável pelo gerenciamento de argumentos de linha de comando (CLI).  
Permite definir opções como método de segmentação, cor-alvo, número de clusters e limites HSV.

### **OS / TIME**
- `os.makedirs()` — cria automaticamente a pasta de saída `outputs`.
- `time.time()` — mede o tempo de execução da segmentação.

---

## 2. Como Usar

### **Execução Geral**
```bash
python main.py --input <arquivo> --method <metodo> --target <cor> [opções]
```

### **Exemplos:**
#### Processar uma imagem:
```bash
python main.py --input img1.jpg --method hsv --target blue
```

#### Processar um vídeo:
```bash
python main.py --input video1.mp4 --method kmeans --target green
```

#### Usar a webcam:
```bash
python main.py --input 0 --method hsv --target green
```

Os resultados (máscara e overlay) serão salvos automaticamente em:
```
outputs/
    nome_arquivo_mask.png
    nome_arquivo_overlay.png
```

---

## 3. Flags de Linha de Comando

| Flag | Tipo | Padrão | Descrição |
|------|------|---------|------------|
| `--input` | `str` | **Obrigatório** | Caminho do arquivo de imagem/vídeo ou `0` para webcam |
| `--method` | `str` | `hsv` | Método de segmentação (`hsv` ou `kmeans`) |
| `--target` | `str` | `green` | Cor-alvo da segmentação (`green` ou `blue`) |
| `--k` | `int` | `3` | Número de clusters para o método K-Means |
| `--hmin` | `int` | `35` | Limite inferior do matiz (Hue) |
| `--hmax` | `int` | `120` | Limite superior do matiz (Hue) |
| `--smin` | `int` | `40` | Saturação mínima |
| `--smax` | `int` | `255` | Saturação máxima |
| `--vmin` | `int` | `0` | Valor (brilho) mínimo |
| `--vmax` | `int` | `255` | Valor (brilho) máximo |

Para pausar o vídeo ou webcam, pressione **p**.
Para retomar o vídeo ou webcam, pressione **r**.
Para encerrar o vídeo ou webcam, pressione **q**.

---

## 4. Exemplos Práticos

### **HSV para Azul**
```bash
python3 main.py --input samples/video1.mp4 --method hsv --hmin 90 --hmax 130 --smin 30 --smax 121 --vmin 140 --vmax 220
```

### **HSV para Verde**
```bash
python3 main.py --input samples/video1.mp4 --method hsv --hmin 35 --hmax 85 --smin 40 --smax 255 --vmin 0 --vmax 255
```

### **K-Means para Azul**
```bash
python3 main.py --input samples/video1.mp4 --method kmeans --target blue --k 4
```

### **K-Means para Verde**
```bash
python3 main.py --input samples/video1.mp4 --method kmeans --target green --k 4
```

---

## 5. Referências e Leituras Recomendadas

- **HSV Color Space (OpenCV Docs):**  
  [https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)

- **K-Means Clustering (OpenCV Docs):**  
  [https://docs.opencv.org/4.x/d1/d5c/tutorial_py_kmeans_opencv.html](https://docs.opencv.org/4.x/d1/d5c/tutorial_py_kmeans_opencv.html)

- **Tabela de Cores HSV (Wikipedia):**  
  [https://en.wikipedia.org/wiki/HSL_and_HSV](https://en.wikipedia.org/wiki/HSL_and_HSV)

- **Documentação oficial OpenCV-Python:**  
  [https://docs.opencv.org/4.x/](https://docs.opencv.org/4.x/)
