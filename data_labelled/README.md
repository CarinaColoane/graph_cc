# Text processing

Librería con pipelines y procedimientos para manejar texto de forma estándar.

## Instalar

Descargar git:
```
git clone https://github.com/imfd/text-processing.git
cd text_processing
pip install -e .
```

De no tener spacy instalarlo (opcional), y descargar su pipeline de español:
```
(opcional) pip3 install spacy
cd text_processing
python3 -m spacy download es_core_news_sm
```

Correr script deseado, ejemplo con datos de twitter:
```
python3 twitter-data.py
```
