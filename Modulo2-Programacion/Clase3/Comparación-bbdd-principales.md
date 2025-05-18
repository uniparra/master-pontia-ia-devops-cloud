🧱 **¿Qué es SQLite?**  
SQLite es una base de datos relacional ligera que:

- No necesita un servidor (es embebida).  
- Guarda todo en un único archivo `.db`.  
- Usa SQL, como PostgreSQL o MySQL.  
- Viene incluida en Python por defecto (`sqlite3`).

✅ **¿Por qué es ideal para desarrollo local?**  
- Simplicidad absoluta: no tienes que instalar ni configurar nada.  
- Sin servidor: no tienes que levantar PostgreSQL o MySQL localmente.  
- Portabilidad: puedes enviarle a alguien el archivo `.db` y ya tiene la base de datos.  
- Compatible con SQLAlchemy: se comporta como cualquier otra base SQL (aunque con algunas limitaciones).

Ejemplo de conexión:

```python
DATABASE_URL = "sqlite:///./usuarios.db"
```
Esto guarda el archivo `usuarios.db` en el mismo directorio.

🧠 **¿Pero es "la mejor opción"?**  
Para prototipos, tests, scripts locales o cursos:  
✅ Sí, es perfecta.

Para producción o apps multiusuario reales:  
❌ No, tiene limitaciones:

| Limitación            | Detalle                                             |
|-----------------------|----------------------------------------------------|
| Concurrencia baja     | No maneja bien muchos usuarios accediendo al mismo tiempo. |
| Transacciones avanzadas| Carece de algunas capacidades de bases más robustas.      |
| Integraciones         | No es compatible con muchos entornos empresariales.         |
| Escalabilidad         | No está diseñada para crecer más allá de cierto punto.      |

🔁 **Otras opciones comunes**

### PostgreSQL 🐘

- Robusta, open source, ideal para producción.  
- Muy usada con FastAPI + SQLAlchemy.  
- Potente en relaciones, transacciones, JSON, etc.

Ejemplo conexión:

```python
DATABASE_URL = "postgresql://user:password@localhost:5432/mydb"
```
### MySQL / MariaDB

- Popular, estable, especialmente en entornos heredados o PHP.  
- Menos funciones avanzadas que PostgreSQL, pero más ligera.

### SQL Server / Oracle

- Entornos empresariales, generalmente no usados en entornos Python de código abierto.

### Bases no relacionales (MongoDB, Redis...)

- Se usan en otros casos (documentales, clave-valor), pero no sustituyen a SQL si necesitas relaciones complejas.

🧪 **Recomendación práctica**

| Fase       | Recomendado           |
|------------|----------------------|
| Curso      | SQLite               |
| Desarrollo | SQLite o PostgreSQL  |
| Producción | PostgreSQL           |
