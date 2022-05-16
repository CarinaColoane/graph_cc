# ¿Qué es una ontología?
Es una definición de datos y relaciones entre entidades dentro de un dominio, en nuestro caso, la convención constituyente. Esto nos asegura una comprensión compartida de los datos en este proceso.

# ¿Qué tópicos son relevantes en la Convención Constituyente?
Se realizó un cruce entre la literatura y los temas de la convención chilena.

Desde la literatura la ontología con mayor peso es *Constitute* la cual tiene un total 69 tópicos (y subtópicos) que se consideraron para trabajar y representar en los gráficos.

Por parte de la convención se considerarán las comisiones, y lo que se definió como temas a tratar. Teniendo un total de 14 Tópicos (más otros subtópicos):

**Tópicos**: Derechos fundamentales, Reformas y constitución, Origen, Sistema electoral, Partido político, Estado, FFAA, Derecho internacional, Economía, Comisiones, Medios de comunicación, Igualdad, Cultura, Derechos sociales.

# ¿Datos relevantes?
Se trataron diversos datos dentro de un mismo espacio de tiempo:
- Noticias que tratan de la convención
- Tweets de constituyentes y personas
- Charlas de la convención: lo hablado en plenarias y en comisiones.

# Preparación de texto - Limpieza de datos
A los datos extraídos en CSV se les realiza una primera limpieza de caracteres no deseados como hashtags, @menciones, puntuación, caracteres especiales, emoticones, números y url.

La segunda limpieza consta de la eliminación de palabras de uso común (como "él", "un", "en") que SpaCy ha sido programado para ignorar.

```
frase = "Creemos que el agua, es un derecho universal!"

# limpieza #1
preprocessed_text = [standard_text_pipeline(frase)]
# limpieza #2
stop_words = get_stopwords()
preprocessed_words = [[word for word in get_processed_text(text)
                     if word not in stop_words] for text in preprocessed_text]
```

La limpieza logra:
```
Sin caracteres especiales:  creemos que el agua es un derecho universal
Solo palabras necesarias:  agua derecho universal
```

# Tag de tópicos - Preparación de diccionario
Los 14 tópicos mencionados anteriormente suman un total de 65 conceptos (tópicos más los subtópicos) los cuales serán buscados en los textos. Cada concepto tiene asociado una lista de palabras las cuales apoyarán en la búsqueda. Uno de los 65 conceptos es voto:
- voto = ["elecciones", "votaciones", "proceso electoral", "escrutinios", "voto", "servel", "votos", "referendum", "consulta ciudadana", "voto obligatorio"]

La lista apoya en la búsqueda al actuar como sinónimos de la palabra voto, por lo que SpaCy buscará las palabras presentes en la lista como si fueran la palabra voto. Y para poder captar todas las palabras de forma general, se trabajará con la "lematización" del diccionario.

La "lematización" significa que reduciremos la palabra a su forma primaria o base. Entonces el concepto voto en realidad se buscará con las palabras:
 - voto = ["elección", "obligatorio", "ciudadano", "servel", "voto", "escrutinio", "referendum", "electoral", "consulta"]

*Tener en consideración que SpaCy también buscara la "lematización" de los textos, y así, conseguir un match de forma certera.*

# Tag de tópicos - Match de conceptos
Usamos Spacy para analizar los diferentes textos (datos anteriormente mencionados). Una función importante que realiza este trabajo es "Matcher", el cual permite hacer coincidir eficientemente nuestra gran lista de conceptos, al aceptar patrones de coincidencia en forma de objetos Doc (texto en forma de secuencia de objetos Token).

Matcher definido dentro de la función *detect_concepts*:
```
concept_matcher = Matcher(nlp.vocab)
pattern = [{"LOWER": {"IN": options}}, {"IS_LOWER": True, "OP": "?"}, {"IS_LOWER": True, "OP": "?"}, {"IS_LOWER": True, "OP": "?"}, {"LOWER": {"IN": options}}]
concept_matcher.add(concept, [pattern])
```
Este patrón (pattern) nos permite encontrar el concepto de la lista en un texto y luego buscar en un espacio de 3 palabras si se encuentra otro concepto, esto resulta útil cuando queremos buscar relaciones significativas. Aplicando el patrón en dos frases:

```
frase = "la votación se mueve para el día martes"
...
Lematización frase: votación mueve
Lista de tópicos en frase:  []
```

```
frase = "en chile el voto de todas las persona debe ser obligatorio"
...
Lematización frase:  voto obligatorio
Lista de tópicos en frase:  ['voto']
```

# Uniendo todo
Ejemplo texto breve:
```
data = "Creemos, que el agua es un derecho universal!"
...
Limpieza de texto:  creemos que el agua es un derecho universal
Eliminación de palabras:  agua derecho universal
Lematización de texto:  agua derecho universal
Lista de tópicos:  ['agua']
```
Ejemplo texto mediano-largo:
```
data = "...y anunciando un nuevo proyecto ahora hace tan sólo seis días acaba de ingresar una propuesta de cierre que es un insulto a las comunidades y a la propia institucionalidad ambiental quiere irse sin tratar las aguas que sigue contaminando por los impactos que ya provocó quiero aprovechar esta tribuna para decirle a la compañía barrick gold nombre de la comunidad organizada seguiremos defendiendo las nacientes de las aguas en la alta cordillera porque son lo que garantizan la vida de todo lo que viene aguas abajo y por eso también estamos aquí creo en el colectivo y traigo un mandato de la asamblea constituyente de atacama acá para redactar una constitución que responda a un nuevo pacto ecosocial que permita la construcción de una sociedad plurinacional que garantice todos los derechos sociales no sexista digna basada en el buen vivir y que protejan los bienes comunes y los elementos vitales conservando la naturaleza como sujeto de derecho ..."
...
Limpieza de texto:  y anunciando un nuevo proyecto ahora hace tan sólo seis días acaba de ingresar una propuesta de cierre que es un insulto a las comunidades y a la propia institucionalidad ambiental quiere irse sin tratar las aguas que sigue contaminando por los impactos que ya provocó quiero aprovechar esta tribuna para decirle a la compañía barrick gold nombre de la comunidad organizada seguiremos defendiendo las nacientes de las aguas en la alta cordillera porque son lo que garantizan la vida de todo lo que viene aguas abajo y por eso también estamos aquí creo en el colectivo y traigo un mandato de la asamblea constituyente de atacama acá para redactar una constitución que responda a un nuevo pacto ecosocial que permita la construcción de una sociedad plurinacional que garantice todos los derechos sociales no sexista digna basada en el buen vivir y que protejan los bienes comunes y los elementos vitales conservando la naturaleza como sujeto de derecho 
Eliminación de palabras:  anunciando ingresar propuesta cierre insulto comunidades institucionalidad ambiental irse tratar aguas contaminando provocó aprovechar tribuna decirle barrick gold comunidad organizada defendiendo nacientes aguas alta cordillera garantizan aguas mandato pacto ecosocial construcción plurinacional garantice derechos sociales sexista digna basada protejan bienes comunes elementos vitales conservando derecho
Lematización de texto:  anunciar ingresar propuesta cierre insulto comunidad institucionalidad ambiental ir él tratar agua contaminar provocar aprovechar tribuna decir él barrick gold comunidad organizado defender nacient agua alto cordillerar garantizar agua mandato pacto ecosocial construcción plurinacional garantizar derechos social sexista digno basado protejar bien común elemento vital conservar derecho
Lista de tópicos:  ['agua', 'derecho_social']
```

# Final - ¿Cómo consultamos estos datos?
Fuera del alcance de este repositorio, generamos un grafo, este grafo final nos permite relacionar estos datos con información profesional de los convencionales, por ejemplo, podemos preguntar si el constituyente “X” hablo del tema “Y”, ya que tenemos una correspondencia tipo **entidad** -> relación -> **entidad**:

**Constituyente** -> participaEnDiscurso -> **Discurso** -> tieneTópico -> **Tópico**
