/**
 * PARTE 4 — Cheatsheet de JavaScript (Node.js & MongoDB)
 * Proyecto: StreamBase
 */

import path from "path";
import fs from "fs/promises"; // Versión asíncrona basada en promesas
import dotenv from "dotenv";

// Configuración de variables de entorno (.env)
dotenv.config(); 
const MONGO_URI = process.env.MONGO_URI;

// Datos para los ejemplos de Arrays
const peliculas = [
  { titulo: "Inception", generos: ["Ciencia Ficción", "Acción"], rating: 4.8 },
  { titulo: "Interstellar", generos: ["Ciencia Ficción", "Drama"], rating: 4.9 }
];


/* 
   1. MÉTODOS DE ARRAYS (Transformación de resultados de consultas)
*/

// .map() -> Extrae o transforma propiedades a un nuevo array
const titulos = peliculas.map(p => p.titulo); // ["Inception", "Interstellar"]

// .filter() -> Filtra documentos que cumplan una condición
const topPelis = peliculas.filter(p => p.rating > 4.8);

// .reduce() -> Acumula valores de los documentos (ej: calcular promedio de rating)
const totalRating = peliculas.reduce((acc, p) => acc + p.rating, 0);
const promedio = totalRating / peliculas.length;

// .flatMap() -> Mapea y aplana arrays anidados en un solo paso (ideal para subdocumentos)
const todosLosGeneros = peliculas.flatMap(p => p.generos); 
// Resultado: ["Ciencia Ficción", "Acción", "Ciencia Ficción", "Drama"]


/* 
   2. DESESTRUCTURACIÓN Y SPREAD OPERATOR (Aplicados a documentos MongoDB)
*/

const docMongo = { _id: "12345", titulo: "Inception", director: "Nolan", __v: 0 };

// Desestructuración + Rest Operator: Limpia propiedades basura (__v, _id) del objeto
const { _id, __v, ...datosLimpios } = docMongo; 
// datosLimpios = { titulo: "Inception", director: "Nolan" }

// Spread Operator: Clona y expande payloads para actualizaciones sin mutar el original
const nuevosCampos = { rating: 4.8, duracion: 148 };
const documentoActualizado = { ...docMongo, ...nuevosCampos, editadoEn: new Date() };


/* 
   3. MANEJO DE ASYNC/AWAIT Y ERRORES (Try/Catch en operaciones asíncronas)
 */

async function obtenerDataPelicula(id) {
  try {
    // Intenta realizar la consulta asíncrona a la base de datos
    const pelicula = await db.collection("peliculas").findOne({ _id: id });
    
    // Control de errores de lógica de negocio manual
    if (!pelicula) {
      throw new Error("Película no encontrada en la base de datos");
    }
    return pelicula;
  } catch (error) {
    // Captura fallos de red, IDs mal formados o excepciones lanzadas arriba
    console.error(`[DB ERROR] Error en la consulta: ${error.message}`);
    throw error; // Propaga el error para el controlador de la API (ej: Express)
  }
}


/* 
   4. CONSULTAS PARALELAS EFICIENTES (Promise.all)
*/

async function getDashboardData() {
  try {
    // Ejecuta múltiples consultas en PARALELO para optimizar el rendimiento del servidor
    // Evita el cuello de botella de usar 'await' línea por línea
    const [peliculasTen, usuariosTop, conteoTotal] = await Promise.all([
      db.collection("peliculas").find().limit(10).toArray(),
      db.collection("usuarios").find().limit(5).toArray(),
      db.collection("peliculas").countDocuments()
    ]);
    
    return { peliculasTen, usuariosTop, conteoTotal };
  } catch (error) {
    console.error("Error en ejecución de consultas paralelas:", error);
  }
}


/* 
   5. MÓDULOS NATIVOS DE NODE.JS RELEVANTES (fs, path)
*/

// Manipulación segura de rutas de archivos (Garantiza compatibilidad Windows/Linux)
const rutaLog = path.join(process.cwd(), "logs", "db-error.log");

// Escritura de archivos asíncrona sin bloquear el hilo principal (Event Loop) de Node
async function registrarError(error) {
  const mensaje = `[${new Date().toISOString()}] - ${error}\n`;
  await fs.appendFile(rutaLog, mensaje, "utf-8");
}


/* 
   6. GUÍA DE REFERENCIA: MÉTODOS DEL DRIVER OFICIAL DE MONGODB
*/

/**
 * findOne(query)
 * -> Devuelve el primer documento que coincida con los criterios o null.
 * -> Ejemplo: db.collection("peliculas").findOne({ titulo: "Inception" });
 * * find(query).toArray()
 * -> Devuelve un cursor con los resultados. .toArray() es OBLIGATORIO para pasarlo a Array de JS.
 * -> Ejemplo: db.collection("peliculas").find({ rating: { $gte: 4.5 } }).toArray();
 * * insertMany(arrayOfObjects)
 * -> Inserta múltiples documentos en la colección en un solo viaje de red de forma masiva.
 * -> Ejemplo: db.collection("peliculas").insertMany([ { titulo: "X" }, { titulo: "Y" } ]);
 * * updateOne(query, update, options)
 * -> Modifica un único documento usando operadores atómicos ($set, $inc, $push, $pull).
 * -> Ejemplo: db.collection("peliculas").updateOne({ _id: 1 }, { $set: { visto: true } });
 * * deleteOne(query)
 * -> Elimina de la colección el primer documento que coincida con el criterio.
 * -> Ejemplo: db.collection("peliculas").deleteOne({ _id: 1 });
 * * aggregate(pipeline)
 * -> Ejecuta una serie de etapas de transformación y filtrado secuenciales (requiere .toArray()).
 * -> Ejemplo: db.collection("peliculas").aggregate([ { $match: { rating: 4.9 } } ]).toArray();
 */