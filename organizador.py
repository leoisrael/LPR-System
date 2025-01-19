import os
import shutil
from sklearn.model_selection import train_test_split
from PIL import Image

# Caminho para a pasta raiz dos arquivos
base_path = "br"

# Estrutura para organizar os arquivos
output_path = "datasets/placas"
images_train_path = os.path.join(output_path, "images/train")
images_val_path = os.path.join(output_path, "images/val")
labels_train_path = os.path.join(output_path, "labels/train")
labels_val_path = os.path.join(output_path, "labels/val")

# Criar as pastas necessárias
os.makedirs(images_train_path, exist_ok=True)
os.makedirs(images_val_path, exist_ok=True)
os.makedirs(labels_train_path, exist_ok=True)
os.makedirs(labels_val_path, exist_ok=True)

# Listar todos os arquivos na pasta
all_files = os.listdir(base_path)

# Separar imagens e anotações
images = [f for f in all_files if f.endswith(".jpg")]
annotations = [f for f in all_files if f.endswith(".txt")]

# Garantir que cada imagem tem uma anotação correspondente
paired_files = [(img, img.replace(".jpg", ".txt")) for img in images if img.replace(".jpg", ".txt") in annotations]

# Dividir em treino (80%) e validação (20%)
train_files, val_files = train_test_split(paired_files, test_size=0.2, random_state=42)

# Função para converter anotações para YOLO
def convert_to_yolo(txt_path, image_path, output_txt_path):
    with open(txt_path, "r") as f:
        lines = f.readlines()
    
    # Abrir a imagem para obter suas dimensões
    img = Image.open(image_path)
    img_width, img_height = img.size

    yolo_annotations = []
    for line in lines:
        parts = line.strip().split("\t")
        if len(parts) < 5:
            continue  # Ignorar linhas incompletas

        # Coordenadas e dimensões
        _, x, y, width, height, _ = parts
        x, y, width, height = map(int, [x, y, width, height])

        # Calcular as coordenadas YOLO (normalizadas)
        x_center = (x + width / 2) / img_width
        y_center = (y + height / 2) / img_height
        norm_width = width / img_width
        norm_height = height / img_height

        # Formatar para YOLO (classe 0 é "placa")
        yolo_annotations.append(f"0 {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}")
    
    # Salvar as anotações no novo arquivo
    with open(output_txt_path, "w") as out_f:
        out_f.write("\n".join(yolo_annotations))

# Função para mover e converter os arquivos
def move_and_convert(file_pairs, image_dest, label_dest):
    for img, txt in file_pairs:
        # Caminhos de origem
        img_path = os.path.join(base_path, img)
        txt_path = os.path.join(base_path, txt)

        # Caminhos de destino
        new_img_path = os.path.join(image_dest, img)
        new_txt_path = os.path.join(label_dest, txt)

        # Copiar a imagem
        shutil.copy(img_path, new_img_path)

        # Converter o arquivo de anotação
        convert_to_yolo(txt_path, img_path, new_txt_path)

# Mover e converter arquivos para as pastas de treino e validação
move_and_convert(train_files, images_train_path, labels_train_path)
move_and_convert(val_files, images_val_path, labels_val_path)

print("Arquivos organizados e convertidos para o formato YOLO com sucesso!")
