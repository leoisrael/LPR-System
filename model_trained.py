import os
import cv2
from ultralytics import YOLO

# Carregar o modelo treinado
model = YOLO("runs/detect/train2/weights/best.pt")

# Pasta de entrada e saída
source_folder = "carros_teste/"
output_folder = "placas_recortadas/"
os.makedirs(output_folder, exist_ok=True)

# Processar cada imagem
for image_file in os.listdir(source_folder):
    if image_file.endswith(".jpg"):
        image_path = os.path.join(source_folder, image_file)
        
        # Fazer a predição
        results = model(image_path)

        # Carregar a imagem
        image = cv2.imread(image_path)

        # Iterar sobre as detecções
        for idx, result in enumerate(results[0].boxes.data.tolist()):
            x1, y1, x2, y2, score, class_id = map(int, result[:6])
            if score > 0.5:  # Confiança mínima
                # Recortar a placa
                cropped_plate = image[y1:y2, x1:x2]
                output_path = os.path.join(output_folder, f"{image_file}_crop_{idx}.jpg")
                cv2.imwrite(output_path, cropped_plate)

print("Placas recortadas salvas com sucesso!")
