# Conceptos Backend: Internacionalización, Localización, Paginación, Middlewares y Test A/B

---

## 🌐 Internacionalización (i18n)

**¿Qué es?**  
Es el proceso de preparar una aplicación para que pueda ser adaptada fácilmente a diferentes idiomas y regiones **sin cambiar el código fuente**.

**En backend significa:**
- Usar archivos de traducción (`.po`, `.json`, `.yml`, etc.).
- Externalizar cadenas de texto (no meter el idioma fijo en el código).
- Dar soporte a diferentes formatos de fecha, moneda, números, etc.
- Preparar URLs, plantillas y respuestas API para poder ser traducidas.

> **Ejemplo en Django**: usar `gettext()` en lugar de strings fijos.

---

## 🌍 Localización (l10n)

**¿Qué es?**  
Es el proceso de **adaptar una aplicación ya internacionalizada** a un idioma o región específica.

**En backend significa:**
- Usar los archivos de traducción para un idioma concreto.
- Adaptar formatos (fechas, monedas, zonas horarias, unidades de medida).
- Mostrar contenido local o condicionar lógicas de negocio por región.

> **Ejemplo**: mostrar `12/05/2025` en España y `05/12/2025` en EE.UU.

---

## 📄 Paginación

**¿Qué es?**  
Dividir grandes volúmenes de datos en partes pequeñas (páginas) para que las respuestas de la API sean rápidas y manejables.

**En backend significa:**
- Limitar cuántos resultados devuelve una consulta.
- Aceptar parámetros como `page`, `limit`, `offset`, `cursor`, etc.
- Enviar metadatos: total de elementos, página actual, etc.

> **Ejemplo en una API REST**:

```http
GET /productos?page=2&limit=20
```
## 🧩 Middlewares

**¿Qué es?**  
Componentes intermedios que interceptan las peticiones o respuestas para aplicar lógica **antes o después del procesamiento principal**.

**En backend significa:**
- Validar tokens
- Loguear peticiones
- Manejar errores
- Añadir cabeceras

Se usan mucho en frameworks como **Express (Node.js)**, **Django**, **FastAPI**, etc.

**Ejemplo en FastAPI:**

```python
@app.middleware("http")
async def log_request(request, call_next):
    print("Petición entrante:", request.url)
    response = await call_next(request)
    return response
```
## 🧪 Test A/B

**¿Qué es?**  
Técnica para comparar **dos versiones** de algo (por ejemplo, una API, un endpoint o una lógica de negocio) y ver cuál funciona mejor.

**En backend significa:**
- Enviar a los usuarios a diferentes variantes del backend.
- Guardar resultados y analizar cuál tuvo mejor rendimiento, retención, conversión, etc.
- Requiere segmentar usuarios (por ejemplo, 50% A, 50% B, o por criterios específicos).

**Ejemplo:**  
El endpoint `/checkout` tiene dos versiones que calculan descuentos distintos. Se mide cuál convierte más.

---

## 📌 Resumen

| Concepto             | Para qué sirve                                | En backend implica...                                 |
|----------------------|-----------------------------------------------|--------------------------------------------------------|
| Internacionalización | Preparar app para distintos idiomas           | Texto externalizado, soporte multiformato             |
| Localización         | Adaptar app a un idioma/país específico       | Traducciones aplicadas, formatos locales              |
| Paginación           | Limitar datos por respuesta                   | `limit`, `offset`, respuesta parcial con metadatos    |
| Middleware           | Lógica antes/después del manejador principal  | Seguridad, logs, transformación de requests/responses |
| Test A/B             | Comparar versiones para medir rendimiento     | División de usuarios, almacenamiento de métricas      |

