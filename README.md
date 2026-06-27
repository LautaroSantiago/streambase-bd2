**🎬 StreamBase — MVP con MongoDB**  
   
 **Trabajo Práctico — Parcial 2 | Bases de Datos 2**  
   
    
   
  Universidad Tecnológica Nacional — Facultad Regional Avellaneda  
   
    
   
  Tecnicatura Universitaria en Programación | Div133  
   
 **Grupo 14:**  
- Sebastián Lescano  
- Joaquín Avallone  
- Lautaro Subeldia  
- Thiago Martínez  
- Mateo Corbetto  
 ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANUlEQVR4nO3OQQmAABRAsSfYxKI/kJ0ED6bwYAVvImwJtszMVu0BAPAXx1rd1fn1BACA164HHEAF+D7GUDYAAAAASUVORK5CYII=)  
 **¿Qué hace este programa?**  
   
 StreamBase es un MVP (Mínimo Producto Viable) que simula el backend de una plataforma de streaming tipo Netflix. Demuestra el modelado de datos en MongoDB usando decisiones fundamentadas de **embedding** y   **referencing**, y ejecuta tres   **Aggregation Pipelines** reales sobre la base de datos.  
 ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAM0lEQVR4nO3KsQ0AIRAEsUW6Ruj0GvnivhMSYmKQ7GiCGd09k3wBAOAVf+2o4wYAwE1qAdYyAy2Ap4pWAAAAAElFTkSuQmCC)  
 **⚙️ Requisitos previos**  
- Python 3.9 o superior  
- MongoDB instalado y corriendo en localhost:27017  
- pip  
 ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANElEQVR4nO3OQQmAUBBAwSfIj+HZmJvAlAaxgjcRZhLMNjNHdQUAwF/ce7Wq8+sJAACvrQctfwNKYUQ0YAAAAABJRU5ErkJggg==)  
  🚀 **Cómo ejecutarlo**  
 **1. Clonar el repositorio**  
   
 git clone [https://github.com/LautaroSantiago/streambase-bd2  
   
 cd streambase-bd2  
   
    
 **2. Crear entorno virtual e instalar dependencias**  
   
 python -m venv venv  
   
    
   
  # En Windows:  
   
  venv\Scripts\activate  
   
    
   
  # En Linux/Mac:  
   
  source venv/bin/activate  
   
    
   
  pip install -r requirements.txt  
   
    
 **3. Configurar variables de entorno**  
   
 Crear un archivo .env en la raíz del proyecto con el siguiente contenido:  
   
 MONGO_URI=mongodb://localhost:27017  
   
  DB_NAME=streambase  
   
    
 **4. Cargar los datos de ejemplo**  
   
 python seed.py  
   
    
 **5. Ejecutar las consultas (Aggregation Pipelines)**  
   
 python queries.py  
   
    
 ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANElEQVR4nO3OQQmAABRAsad4EkMY9ecwnkms4E2ELcGWmTmrKwAA/uLeqrU6vp4AAPDa/gDzXAM6/j8dDQAAAABJRU5ErkJggg==)  
 **📁 Estructura del proyecto**  
   
 streambase/  
   
  ├── db.py              # Módulo de conexión a MongoDB  
   
  ├── seed.py            # Script de carga de datos de ejemplo  
   
  ├── queries.py         # Aggregation Pipelines (consultas principales)  
   
  ├── requirements.txt   # Dependencias del proyecto  
   
  ├── .env               # Variables de entorno (NO subir a GitHub)  
   
  ├── .gitignore  
   
  └── README.md  
   
    
 ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANUlEQVR4nO3OQQmAABRAsSd4tIF9zPWxpgGsYQVvImwJtszMXp0BAPAX91pt1fH1BACA164HhagENzj41xIAAAAASUVORK5CYII=)  
 **🗂️ Colecciones y modelo de datos**  
   
 peliculas  
   
 Almacena el catálogo de contenido disponible en la plataforma.  
   
 {  
   
    "_id": 1,  
   
    "titulo": "Inception",  
   
    "anio": 2010,  
   
    "duracion_min": 148,  
   
    "director": {  
   
      "nombre": "Christopher Nolan",  
   
      "nacionalidad": "Británico"  
   
    },  
   
    "generos": ["Ciencia Ficción", "Acción", "Thriller"],  
   
    "calificacion": 8.8  
   
  }  
   
    
   
 usuarios  
   
 Almacena los suscriptores de la plataforma con su plan vigente.  
   
 {  
   
    "_id": 1,  
   
    "nombre": "Sebastián Lescano",  
   
    "email": "sebastian@streambase.com",  
   
    "plan": {  
   
      "tipo": "premium",  
   
      "precio_mensual": 1499,  
   
      "fecha_inicio": "2024-01-15"  
   
    }  
   
  }  
   
    
   
 reproducciones  
   
 Colección asociativa que registra cada vez que un usuario reproduce una película.  
   
 {  
   
    "usuario_id": 1,  
   
    "pelicula_id": 1,  
   
    "duracion_min": 148,  
   
    "completada": true,  
   
    "fecha": "2025-03-10"  
   
  }  
   
    
 ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANUlEQVR4nO3OQQmAABRAsSd4NoCpTCQ/pwmMYQVvImwJtszMXp0BAPAX91pt1fH1BACA164HosMEPiBLnfkAAAAASUVORK5CYII=)  
 **🏗️ Justificación de las decisiones de diseño**  
   
 **¿Por qué **director ** y **generos ** están embebidos en **peliculas **?**  
   
 Según la **heurística principal** vista en clase — el espectro "Limitado vs. Ilimitado":](https://github.com/LautaroSantiago/streambase-bd2 "https://github.com/LautaroSantiago/streambase-bd2")  
- **director** es una relación   **1:1** con la película. Un director no se consulta nunca de forma independiente al film; siempre se accede junto a él. Al ser de tamaño fijo y acceso conjunto, corresponde   **embeber**.  
- **generos** es un array de tamaño   **Limitado y Pequeño** (una película tiene entre 1 y 5 géneros, nunca crece). Aplicando la Regla de Oro: *"Si el dato es Limitado/Pequeño, puede incrustarse en el documento padre"*.  
   
 **¿Por qué **plan ** está embebido en **usuarios **?**  
   
 El plan de suscripción es un atributo directo del usuario: relación **1:1**, tamaño fijo, siempre consultado junto al perfil del usuario. No es una entidad independiente con vida propia. →   **Embeber**.  
   
 **¿Por qué **reproducciones ** es una colección separada?**  
   
 La relación entre usuarios y películas es **N:M Sin Límites**:  
- Un usuario puede ver miles de películas a lo largo del tiempo.  
- Una película puede acumular millones de reproducciones.  
   
 Intentar almacenar las reproducciones dentro del documento de un usuario o de una película violaría la **Regla de Expansión Constante**: *"Si un dato crece indefinidamente, nunca lo incrustes en el documento padre"*. El documento superaría el límite de 16 MB de MongoDB.  
   
 La solución correcta es la **Colección Asociativa**: cada reproducción es un documento independiente que porta referencias (usuario_id y pelicula_id) a ambos lados de la relación.  
 ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANUlEQVR4nO3OMQ2AUBBAsUfyNbBi9VRgEA3sWGAjJK2CbjNzVGcAAPzFtapV7V9PAAB47X4AEXIELdGZ+p4AAAAASUVORK5CYII=)  
 **🔍 Aggregation Pipelines**  
 **Pipeline 1 — Top 5 películas más vistas**  
   
 Etapas: $group → $sort → $limit → $lookup → $unwind → $project  
 **Pipeline 2 — Géneros favoritos de un usuario**  
   
 Etapas: $match → $lookup → $unwind (×2) → $group → $sort → $project  
 **Pipeline 3 — Usuarios premium con más tiempo reproducido**  
   
 Etapas: $lookup → $unwind → $match → $group → $sort → $project  
 ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANklEQVR4nO3OMQ2AABAAsSNBACvucMH6NpGACyywEZJWQZeZ2aszAAD+4l6rrTo+jgAA8N71AL/GBEhnueqbAAAAAElFTkSuQmCC)  
 **📚 Fuentes consultadas**  
- Apuntes de clase — Bases de Datos 2 — UTN Avellaneda (2026)  
- [Documentación oficial de MongoDB](https://www.mongodb.com/docs/ "https://www.mongodb.com/docs/")  
- [PyMongo Documentation](https://pymongo.readthedocs.io/ "https://pymongo.readthedocs.io/")  
- [Python Dotenv](https://pypi.org/project/python-dotenv/ "https://pypi.org/project/python-dotenv/")  
