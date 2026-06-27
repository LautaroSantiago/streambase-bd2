"""
seed.py — Script de carga de datos de ejemplo
StreamBase | Grupo 14 | BD2 | Div133 | UTN Avellaneda

Crea e inserta documentos en las 3 colecciones del proyecto:
  - peliculas      (embedding: director y géneros incrustados)
  - usuarios       (embedding: plan de suscripción incrustado)
  - reproducciones (referencing: colección asociativa N:M)
"""

from db import get_db
from datetime import datetime


# ─────────────────────────────────────────────
# COLECCIÓN 1: peliculas
# Decisión de diseño:
#   - 'director' se INCRUSTA porque es una relación 1:1 con la película
#     y siempre se accede junto a ella (lectura frecuente conjunta).
#   - 'generos' se INCRUSTA como array porque es un conjunto LIMITADO Y PEQUEÑO
#     (una película tiene entre 1 y 5 géneros), nunca crece indefinidamente
#     → Aplica la heurística: "Limitado/Pequeño → se puede incrustar".
# ─────────────────────────────────────────────
peliculas = [
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
    },
    {
        "_id": 2,
        "titulo": "The Dark Knight",
        "anio": 2008,
        "duracion_min": 152,
        "director": {
            "nombre": "Christopher Nolan",
            "nacionalidad": "Británico"
        },
        "generos": ["Acción", "Drama", "Crimen"],
        "calificacion": 9.0
    },
    {
        "_id": 3,
        "titulo": "Parasite",
        "anio": 2019,
        "duracion_min": 132,
        "director": {
            "nombre": "Bong Joon-ho",
            "nacionalidad": "Surcoreano"
        },
        "generos": ["Drama", "Thriller"],
        "calificacion": 8.5
    },
    {
        "_id": 4,
        "titulo": "Interstellar",
        "anio": 2014,
        "duracion_min": 169,
        "director": {
            "nombre": "Christopher Nolan",
            "nacionalidad": "Británico"
        },
        "generos": ["Ciencia Ficción", "Drama", "Aventura"],
        "calificacion": 8.6
    },
    {
        "_id": 5,
        "titulo": "The Godfather",
        "anio": 1972,
        "duracion_min": 175,
        "director": {
            "nombre": "Francis Ford Coppola",
            "nacionalidad": "Estadounidense"
        },
        "generos": ["Drama", "Crimen"],
        "calificacion": 9.2
    },
    {
        "_id": 6,
        "titulo": "Avengers: Endgame",
        "anio": 2019,
        "duracion_min": 181,
        "director": {
            "nombre": "Anthony Russo",
            "nacionalidad": "Estadounidense"
        },
        "generos": ["Acción", "Aventura", "Ciencia Ficción"],
        "calificacion": 8.4
    },
    {
        "_id": 7,
        "titulo": "Spirited Away",
        "anio": 2001,
        "duracion_min": 125,
        "director": {
            "nombre": "Hayao Miyazaki",
            "nacionalidad": "Japonés"
        },
        "generos": ["Animación", "Aventura", "Fantasía"],
        "calificacion": 8.6
    },
    {
        "_id": 8,
        "titulo": "The Matrix",
        "anio": 1999,
        "duracion_min": 136,
        "director": {
            "nombre": "Lana Wachowski",
            "nacionalidad": "Estadounidense"
        },
        "generos": ["Ciencia Ficción", "Acción"],
        "calificacion": 8.7
    },
    {
        "_id": 9,
        "titulo": "Pulp Fiction",
        "anio": 1994,
        "duracion_min": 154,
        "director": {
            "nombre": "Quentin Tarantino",
            "nacionalidad": "Estadounidense"
        },
        "generos": ["Crimen", "Drama"],
        "calificacion": 8.9
    },
    {
        "_id": 10,
        "titulo": "La La Land",
        "anio": 2016,
        "duracion_min": 128,
        "director": {
            "nombre": "Damien Chazelle",
            "nacionalidad": "Estadounidense"
        },
        "generos": ["Drama", "Música", "Romance"],
        "calificacion": 8.0
    }
]


# ─────────────────────────────────────────────
# COLECCIÓN 2: usuarios
# Decisión de diseño:
#   - 'plan' se INCRUSTA porque es una relación 1:1 con el usuario,
#     de tamaño fijo y siempre consultada en conjunto con los datos del usuario.
#   - No se crea una colección 'planes' separada porque el plan es
#     un atributo descriptivo del usuario, no una entidad independiente
#     con crecimiento propio → "Limitado/Pequeño → incrustar".
# ─────────────────────────────────────────────
usuarios = [
    {
        "_id": 1,
        "nombre": "Sebastián Lescano",
        "email": "sebastian@streambase.com",
        "plan": {
            "tipo": "premium",
            "precio_mensual": 1499,
            "fecha_inicio": datetime(2024, 1, 15)
        }
    },
    {
        "_id": 2,
        "nombre": "Joaquín Avallone",
        "email": "joaquin@streambase.com",
        "plan": {
            "tipo": "premium",
            "precio_mensual": 1499,
            "fecha_inicio": datetime(2024, 3, 1)
        }
    },
    {
        "_id": 3,
        "nombre": "Lautaro Subeldía",
        "email": "lautaro@streambase.com",
        "plan": {
            "tipo": "basico",
            "precio_mensual": 799,
            "fecha_inicio": datetime(2024, 6, 10)
        }
    },
    {
        "_id": 4,
        "nombre": "Thiago Martínez",
        "email": "thiago@streambase.com",
        "plan": {
            "tipo": "premium",
            "precio_mensual": 1499,
            "fecha_inicio": datetime(2023, 11, 20)
        }
    },
    {
        "_id": 5,
        "nombre": "Mateo Corbetto",
        "email": "mateo@streambase.com",
        "plan": {
            "tipo": "basico",
            "precio_mensual": 799,
            "fecha_inicio": datetime(2025, 1, 5)
        }
    }
]


# ─────────────────────────────────────────────
# COLECCIÓN 3: reproducciones
# Decisión de diseño:
#   - Es una COLECCIÓN ASOCIATIVA que resuelve la relación N:M entre
#     usuarios y películas: un usuario puede ver muchas películas,
#     y una película puede ser vista por muchos usuarios.
#   - La relación es SIN LÍMITES (un usuario puede ver miles de películas,
#     una película puede acumular millones de reproducciones con el tiempo).
#   - Según la heurística vista en clase: "Sin Límites → Colección Separada Obligatoria".
#   - Cada documento porta referencias (IDs) a ambos lados: usuario_id y pelicula_id.
#   - Esto evita que cualquiera de los documentos padre crezca sin control,
#     respetando la Regla de Oro: "Si tiene expansión constante, nunca lo incrustes".
# ─────────────────────────────────────────────
reproducciones = [
    # Sebastián (premium) — 3 reproducciones — 412 min totales
    {"usuario_id": 1, "pelicula_id": 1, "duracion_min": 148, "completada": True,  "fecha": datetime(2025, 3, 10)},
    {"usuario_id": 1, "pelicula_id": 2, "duracion_min": 95,  "completada": False, "fecha": datetime(2025, 3, 15)},
    {"usuario_id": 1, "pelicula_id": 4, "duracion_min": 169, "completada": True,  "fecha": datetime(2025, 4, 2)},

    # Joaquín (premium) — 4 reproducciones — 597 min totales
    {"usuario_id": 2, "pelicula_id": 1, "duracion_min": 148, "completada": True,  "fecha": datetime(2025, 2, 20)},
    {"usuario_id": 2, "pelicula_id": 3, "duracion_min": 132, "completada": True,  "fecha": datetime(2025, 3, 5)},
    {"usuario_id": 2, "pelicula_id": 6, "duracion_min": 181, "completada": True,  "fecha": datetime(2025, 3, 22)},
    {"usuario_id": 2, "pelicula_id": 8, "duracion_min": 136, "completada": True,  "fecha": datetime(2025, 4, 10)},

    # Lautaro (basico) — 3 reproducciones
    {"usuario_id": 3, "pelicula_id": 2, "duracion_min": 152, "completada": True,  "fecha": datetime(2025, 1, 8)},
    {"usuario_id": 3, "pelicula_id": 5, "duracion_min": 175, "completada": True,  "fecha": datetime(2025, 2, 14)},
    {"usuario_id": 3, "pelicula_id": 9, "duracion_min": 154, "completada": True,  "fecha": datetime(2025, 3, 30)},

    # Thiago (premium) — 4 reproducciones — 570 min totales
    {"usuario_id": 4, "pelicula_id": 1, "duracion_min": 148, "completada": True,  "fecha": datetime(2025, 1, 19)},
    {"usuario_id": 4, "pelicula_id": 4, "duracion_min": 169, "completada": True,  "fecha": datetime(2025, 2, 28)},
    {"usuario_id": 4, "pelicula_id": 7, "duracion_min": 125, "completada": True,  "fecha": datetime(2025, 3, 17)},
    {"usuario_id": 4, "pelicula_id": 10,"duracion_min": 128, "completada": True,  "fecha": datetime(2025, 4, 5)},

    # Mateo (basico) — 3 reproducciones
    {"usuario_id": 5, "pelicula_id": 3, "duracion_min": 132, "completada": True,  "fecha": datetime(2025, 2, 11)},
    {"usuario_id": 5, "pelicula_id": 6, "duracion_min": 181, "completada": True,  "fecha": datetime(2025, 3, 25)},
    {"usuario_id": 5, "pelicula_id": 8, "duracion_min": 110, "completada": False, "fecha": datetime(2025, 4, 8)},
]


def seed():
    client, db = get_db()

    print("🗑️  Limpiando colecciones anteriores...")
    db.peliculas.drop()
    db.usuarios.drop()
    db.reproducciones.drop()

    print("🎬 Insertando películas...")
    db.peliculas.insert_many(peliculas)
    print(f"   ✅ {len(peliculas)} películas insertadas.")

    print("👤 Insertando usuarios...")
    db.usuarios.insert_many(usuarios)
    print(f"   ✅ {len(usuarios)} usuarios insertados.")

    print("▶️  Insertando reproducciones...")
    db.reproducciones.insert_many(reproducciones)
    print(f"   ✅ {len(reproducciones)} reproducciones insertadas.")

    client.close()
    print("\n✅ Base de datos 'streambase' lista para usar.")
    print("   Ejecutá ahora: python queries.py")


if __name__ == "__main__":
    seed()
