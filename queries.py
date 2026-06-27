"""
queries.py — Aggregation Pipelines de StreamBase
StreamBase | Grupo 14 | BD2 | Div133 | UTN Avellaneda

Contiene 3 pipelines de agregación sobre la base 'streambase':
  - Pipeline 1: Top 5 películas más vistas
  - Pipeline 2: Géneros favoritos de un usuario
  - Pipeline 3: Usuarios premium ordenados por minutos reproducidos
"""

from db import get_db


# ═══════════════════════════════════════════════════════════════════════
# PIPELINE 1 — Top 5 películas más vistas
#
# Colección de origen: reproducciones
#
# Qué hace paso a paso:
#   $group   → agrupa por pelicula_id y cuenta cuántas veces aparece
#   $sort    → ordena de mayor a menor cantidad de reproducciones
#   $limit   → toma solo las 5 primeras (las más vistas)
#   $lookup  → "une" con la colección peliculas para traer el título y la calificación
#   $unwind  → convierte el array resultado del $lookup en un documento plano
#   $project → da forma a la salida final, ocultando el _id
#
# Resultado esperado con los datos de ejemplo:
#   1. Inception         → 3 reproducciones (usuarios 1, 2 y 4)
#   2. The Dark Knight   → 2 reproducciones
#   2. Avengers Endgame  → 2 reproducciones
#   2. Interstellar      → 2 reproducciones
#   2. The Matrix        → 2 reproducciones
# ═══════════════════════════════════════════════════════════════════════
def pipeline_1_top_peliculas():
    client, db = get_db()

    pipeline = [
        {
            "$group": {
                "_id": "$pelicula_id",
                "total_reproducciones": {"$sum": 1}
            }
        },
        {
            "$sort": {"total_reproducciones": -1}
        },
        {
            "$limit": 5
        },
        {
            "$lookup": {
                "from": "peliculas",
                "localField": "_id",
                "foreignField": "_id",
                "as": "info_pelicula"
            }
        },
        {
            "$unwind": "$info_pelicula"
        },
        {
            "$project": {
                "_id": 0,
                "titulo": "$info_pelicula.titulo",
                "calificacion": "$info_pelicula.calificacion",
                "total_reproducciones": 1
            }
        }
    ]

    resultados = list(db.reproducciones.aggregate(pipeline))
    client.close()
    return resultados


# ═══════════════════════════════════════════════════════════════════════
# PIPELINE 2 — Géneros favoritos de un usuario específico
#
# Colección de origen: reproducciones
#
# Qué hace paso a paso:
#   $match   → filtra solo las reproducciones del usuario indicado
#   $lookup  → trae los datos de la película asociada a cada reproducción
#   $unwind  → desanida el array 'pelicula' (resultado del $lookup)
#   $unwind  → desanida el array de géneros dentro de la película,
#              generando un documento por cada género (necesario para agrupar)
#   $group   → agrupa por nombre de género y cuenta cuántas veces aparece
#   $sort    → ordena de mayor a menor frecuencia
#   $project → da forma a la salida final
#
# Resultado esperado para usuario 1 (Sebastián):
#   Vio: Inception (Ciencia Ficción, Acción, Thriller)
#        The Dark Knight (Acción, Drama, Crimen)
#        Interstellar (Ciencia Ficción, Drama, Aventura)
#
#   Géneros: Ciencia Ficción x2, Acción x2, Drama x2,
#            Thriller x1, Crimen x1, Aventura x1
# ═══════════════════════════════════════════════════════════════════════
def pipeline_2_generos_favoritos(usuario_id):
    client, db = get_db()

    pipeline = [
        {
            "$match": {"usuario_id": usuario_id}
        },
        {
            "$lookup": {
                "from": "peliculas",
                "localField": "pelicula_id",
                "foreignField": "_id",
                "as": "pelicula"
            }
        },
        {
            "$unwind": "$pelicula"
        },
        {
            "$unwind": "$pelicula.generos"
        },
        {
            "$group": {
                "_id": "$pelicula.generos",
                "cantidad": {"$sum": 1}
            }
        },
        {
            "$sort": {"cantidad": -1}
        },
        {
            "$project": {
                "_id": 0,
                "genero": "$_id",
                "cantidad": 1
            }
        }
    ]

    resultados = list(db.reproducciones.aggregate(pipeline))
    client.close()
    return resultados


# ═══════════════════════════════════════════════════════════════════════
# PIPELINE 3 — Usuarios premium con más minutos reproducidos
#
# Colección de origen: reproducciones
#
# Qué hace paso a paso:
#   $lookup  → une reproducciones con usuarios para obtener el plan
#   $unwind  → desanida el array 'usuario' resultado del $lookup
#   $match   → filtra solo usuarios con plan.tipo == "premium"
#              (usa notación de punto para acceder al campo embebido,
#               tal como se vio en clase con 'direccion.calle')
#   $group   → agrupa por usuario y suma sus minutos reproducidos
#   $sort    → ordena de mayor a menor tiempo
#   $project → da forma final, añade campo calculado 'total_horas'
#
# Resultado esperado:
#   1. Joaquín Avallone  → 597 min (9.95 hs)
#   2. Thiago Martínez   → 570 min (9.5 hs)
#   3. Sebastián Lescano → 412 min (6.87 hs)
# ═══════════════════════════════════════════════════════════════════════
def pipeline_3_premium_mas_tiempo():
    client, db = get_db()

    pipeline = [
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "usuario_id",
                "foreignField": "_id",
                "as": "usuario"
            }
        },
        {
            "$unwind": "$usuario"
        },
        {
            "$match": {"usuario.plan.tipo": "premium"}
        },
        {
            "$group": {
                "_id": "$usuario_id",
                "nombre": {"$first": "$usuario.nombre"},
                "total_minutos": {"$sum": "$duracion_min"}
            }
        },
        {
            "$sort": {"total_minutos": -1}
        },
        {
            "$project": {
                "_id": 0,
                "nombre": 1,
                "total_minutos": 1,
                "total_horas": {
                    "$round": [{"$divide": ["$total_minutos", 60]}, 2]
                }
            }
        }
    ]

    resultados = list(db.reproducciones.aggregate(pipeline))
    client.close()
    return resultados


# ───────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA — ejecutar desde consola con: python queries.py
# ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 55)
    print("  STREAMBASE — Consultas con Aggregation Pipeline")
    print("  Grupo 14 | BD2 | Div133 | UTN Avellaneda")
    print("=" * 55)

    # ── Pipeline 1 ──────────────────────────────────────────
    print("\n🎬 PIPELINE 1: Top 5 películas más vistas")
    print("-" * 55)
    for i, r in enumerate(pipeline_1_top_peliculas(), 1):
        print(f"  {i}. {r['titulo']:<25} "
              f"{r['total_reproducciones']} reproducciones  "
              f"⭐ {r['calificacion']}")

    # ── Pipeline 2 ──────────────────────────────────────────
    print("\n🎭 PIPELINE 2: Géneros favoritos de Sebastián Lescano")
    print("-" * 55)
    for r in pipeline_2_generos_favoritos(1):
        barra = "█" * r["cantidad"]
        print(f"  {r['genero']:<20} {barra} ({r['cantidad']})")

    # ── Pipeline 3 ──────────────────────────────────────────
    print("\n👑 PIPELINE 3: Usuarios premium — ranking por tiempo")
    print("-" * 55)
    for i, r in enumerate(pipeline_3_premium_mas_tiempo(), 1):
        print(f"  {i}. {r['nombre']:<25} "
              f"{r['total_minutos']} min  "
              f"({r['total_horas']} hs)")

    print("\n" + "=" * 55)
    print("  Consultas ejecutadas correctamente. ✅")
    print("=" * 55)
