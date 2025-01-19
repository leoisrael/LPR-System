# LPR-System

## Introdução

O LPR-System é um sistema projetado para o reconhecimento de placas de veículos utilizando técnicas modernas de visão computacional e aprendizado profundo. Ele foi desenvolvido com base no modelo YOLOv8 (You Only Look Once, versão 8), um dos frameworks mais avançados para detecção de objetos em tempo real. Este projeto tem como objetivo oferecer um pipeline completo que inclua a detecção de placas em imagens, bem como o recorte das áreas detectadas para processamento posterior.

## Metodologia

### Arquitetura do Modelo

O YOLOv8 é um modelo de detecção de objetos que combina precisão e eficiência. Ele opera dividindo a imagem em uma grade, onde cada célula é responsável por prever caixas delimitadoras (bounding boxes) e suas respectivas probabilidades para cada classe. No caso deste projeto, o modelo foi configurado para detectar apenas uma classe: placas de veículos.

### Treinamento

O modelo foi treinado utilizando um conjunto de dados personalizado de placas de veículos. O dataset foi previamente anotado no formato YOLO, contendo imagens com bounding boxes que delimitam as áreas das placas. O treinamento foi realizado com as seguintes configurações principais:

- **Modelo Base:** YOLOv8 Nano (versão leve para maior eficiência)
- **Tamanho das Imagens:** 640x640 pixels
- **Épocas:** 50
- **Taxa de Aprendizado Inicial:** 0.01
- **Divisão de Dados:** 80% para treino e 20% para validação

### Métricas de Avaliação

Durante o treinamento, as seguintes métricas foram monitoradas:

- **Precision:** Mede a proporção de predições corretas entre todas as predições realizadas.
- **Recall:** Mede a proporção de objetos verdadeiros detectados pelo modelo.
- **mAP@50:** Média da Precisão Média com IoU (Intersection over Union) de 50%.
- **mAP@50-95:** Média da Precisão Média em múltiplos limiares de IoU (50% a 95%).

### Resultados do Treinamento

Os gráficos abaixo, gerados durante o treinamento, ilustram a evolução das métricas:

- **Loss (Perda):** Indica a redução do erro ao longo das épocas de treinamento.
- **Precision e Recall:** Mostram a capacidade do modelo em realizar detecções corretas.
- **mAP:** Demonstra a precisão geral do modelo em múltiplos limiares de IoU.

Os resultados indicaram um desempenho sólido, com valores de **Precision** e **Recall** superiores a 95% e um mAP@50 de aproximadamente 94%.

![Gráfico de Loss](runs/detect/train2/results.png)

![Gráfico de mAP](runs/detect/train2/results.png)

## Estrutura do Pipeline

1. **Pré-processamento:** As imagens são redimensionadas para 640x640 pixels para garantir compatibilidade com o modelo.
2. **Inferência:** O YOLOv8 realiza a detecção de placas nas imagens carregadas.
3. **Pós-processamento:** As caixas delimitadoras são desenhadas nas imagens originais, e as regiões de interesse (ROIs) são recortadas e armazenadas para análise posterior.

## Requisitos de Instalação

Para executar o projeto, siga os passos abaixo:

### 1. Instalar Python
Certifique-se de que o Python 3.8 ou superior está instalado em sua máquina.

### 2. Criar Ambiente Virtual
Crie e ative um ambiente virtual para gerenciar dependências:

- **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- **Linux/Mac**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar Dependências
Com o ambiente virtual ativado, instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Instalar PyTorch
Instale o PyTorch compatível com sua máquina:

- Para CPU:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
  ```

- Para GPU (consulte [PyTorch](https://pytorch.org/get-started/locally/) para configurações específicas):
  ```bash
  pip install torch torchvision torchaudio
  ```

### 5. Executar o Servidor
Inicie o servidor Flask para rodar o sistema:

```bash
python app.py
```

O sistema estará disponível em: [http://127.0.0.1:5000](http://127.0.0.1:5000).

