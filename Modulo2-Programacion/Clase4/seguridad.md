# 🔐 Conceptos de Seguridad en Backend

## 🔑 Autenticación
**¿Qué es?**  
Proceso de verificar la identidad de un usuario o sistema.

**Ejemplos comunes:**
- Usuario y contraseña.
- Tokens JWT.
- OAuth2 (usado por Google, GitHub, etc.).
- Autenticación multifactor (MFA).

**En backend implica:**
- Validar credenciales antes de permitir acceso.
- Proteger rutas con `middlewares` o `guards`.
- Uso de `headers` seguros para transmitir tokens.

---

## 🚦 Rate Limiting (Código 429: Too Many Requests)
**¿Qué es?**  
Control de la frecuencia con la que un cliente puede hacer peticiones al servidor.

**¿Para qué sirve?**
- Evitar abusos del sistema (spam, bots, etc.).
- Proteger contra ataques de fuerza bruta y DDoS.

**Código HTTP asociado:** `429 Too Many Requests`

**Implementación común:**
- Limitar por IP.
- Limitar por usuario autenticado.
- Redis o memoria en backend para contar peticiones.

---

## 💥 Fuerza Bruta
**¿Qué es?**  
Técnica para adivinar contraseñas o claves probando muchas combinaciones posibles.

**Mitigación:**
- Rate limiting.
- Bloqueo temporal tras intentos fallidos.
- Captchas.
- Hashing seguro (bcrypt, Argon2).

---

## 🌐 DDoS (Distributed Denial of Service)
**¿Qué es?**  
Ataque que busca saturar un sistema con millones de peticiones desde múltiples dispositivos.

**Consecuencias:**
- Inaccesibilidad del servicio.
- Caída del servidor.

**Mitigación:**
- CDN y firewalls (Cloudflare, AWS Shield).
- Rate limiting agresivo.
- Detección de tráfico anómalo.

---

## 🕵️‍♂️ Man in the Middle (MitM)
**¿Qué es?**  
Ataque donde un tercero intercepta la comunicación entre cliente y servidor.

**Riesgos:**
- Robo de credenciales.
- Alteración de datos transmitidos.

**Mitigación:**
- Cifrado HTTPS (TLS).
- Certificados válidos y actualizados.
- Evitar transmisión de datos sensibles en texto plano.

---

## 💉 Inyecciones de Código
**¿Qué es?**  
Cuando un atacante inserta código malicioso en una entrada de usuario, aprovechando una validación deficiente.

**Tipos comunes:**
- SQL Injection.
- Command Injection.
- Script Injection (XSS).

**Mitigación:**
- Validación estricta de entradas.
- Uso de consultas preparadas o ORM seguros.
- Escapado de caracteres especiales.

---

## ✅ Buenas Prácticas Generales
- No exponer datos sensibles en respuestas.
- Usar HTTPS siempre.
- Hashing y salting de contraseñas.
- Revisar dependencias y librerías vulnerables.
- Autenticación y autorización bien separadas.

