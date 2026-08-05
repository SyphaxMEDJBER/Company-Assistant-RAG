FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
# torch CPU uniquement : sans cette ligne, pip installe par defaut la version
# CUDA/GPU de torch (plusieurs Go de librairies NVIDIA inutiles, notre
# machine n'a pas de GPU et le conteneur n'y aurait de toute facon pas acces).
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY data/ data/
COPY app.py .

RUN python -m src.indexing

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
