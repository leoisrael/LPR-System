import os
import cv2
from ultralytics import YOLO
from flask import Flask, request, render_template, send_from_directory
import uuid

# Inicializar o app Flask
app = Flask(__name__)

# Diretórios para salvar imagens
UPLOAD_FOLDER = "uploads"
DETECTION_FOLDER = "detections"
CROP_FOLDER = "crops"

# Criar as pastas se não existirem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECTION_FOLDER, exist_ok=True)
os.makedirs(CROP_FOLDER, exist_ok=True)

# Carregar o modelo treinado
model = YOLO("runs/detect/train2/weights/best.pt")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Verificar se um arquivo foi enviado
        if "image" not in request.files:
            return "Nenhuma imagem enviada.", 400

        file = request.files["image"]

        if file.filename == "":
            return "Nenhuma imagem selecionada.", 400

        # Salvar o arquivo carregado
        filename = f"{uuid.uuid4().hex}.jpg"  # Gerar um nome único
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Fazer a predição
        results = model(filepath)
        print("Predições brutas:", results)  # Debug para verificar o formato das predições

        # Carregar a imagem original
        image = cv2.imread(filepath)

        # Processar as detecções
        crops = []
        detection_found = False  # Flag para verificar se houve detecção

        if results[0].boxes is not None:  # Garantir que há boxes nas predições
            for idx, box in enumerate(results[0].boxes):  # Usar o objeto boxes diretamente
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas da bounding box
                score = float(box.conf[0])  # Confiança da predição

                print(f"Detecção {idx}: x1={x1}, y1={y1}, x2={x2}, y2={y2}, score={score}")  # Debug

                if score > 0.3:  # Reduzido o limite para 30%
                    detection_found = True  # Marcar que uma detecção foi encontrada
                    # Desenhar a bounding box na imagem original
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(image, f"Score: {score:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Recortar a placa
                    cropped_plate = image[y1:y2, x1:x2]
                    crop_filename = f"{filename}_crop_{idx}.jpg"
                    crop_filepath = os.path.join(CROP_FOLDER, crop_filename)
                    cv2.imwrite(crop_filepath, cropped_plate)
                    crops.append(crop_filename)

        # Se nenhuma detecção foi encontrada, exibir uma mensagem na imagem
        if not detection_found:
            cv2.putText(image, "Nenhuma placa detectada", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Salvar a imagem com detecções
        detection_filepath = os.path.join(DETECTION_FOLDER, filename)
        cv2.imwrite(detection_filepath, image)

        # Renderizar a página com os resultados
        return render_template(
            "result.html",
            original_image=filename,
            detection_image=filename,
            crops=crops,
        )

    return render_template("index.html")

@app.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/detections/<filename>")
def detections(filename):
    return send_from_directory(DETECTION_FOLDER, filename)

@app.route("/crops/<filename>")
def crops(filename):
    return send_from_directory(CROP_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
