<div align="center">

# 🧪 [ VERSIÓN BETA ] 🧪
### *Desarrollo e implementacion de API y lectura de notificaciones*

***
</div>

# Miku Friend AI 

![Miku Friend Logo](https://i.ibb.co/BVzfJ5cS/MIKU.png)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-39c5bb?style=flat-svg&logo=python&logoColor=white)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/UI-PySide6--Qt6-39c5bb?style=flat-svg&logo=qt&logoColor=white)](https://wiki.qt.io/Qt_for_Python)
[![License](https://img.shields.io/badge/license-MIT-39c5bb?style=flat-svg)](LICENSE)

Un asistente de inteligencia artificial de escritorio con interfaz gráfica interactiva, inspirado en **Hatsune Miku**. Utiliza las APIs de OpenRouter para responder y gestionar recuerdos sobre ti de forma persistente y natural.

---

## Tabla de Contenidos
- [Características principales](#-características-principales)
- [Vista Previa](#-vista-previa)
- [Requisitos de Sistema](#%EF%B8%8F-requisitos-de-sistema)
- [Instalación](#-instalación)
- [Uso](#%EF%B8%8F-uso)
- [Tecnologías Utilizadas](#%EF%B8%8F-tecnologías-utilizadas)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## Características principales
* **Personalidad de Hatsune Miku**: Diseñada para actuar como Miku usando respuestas naturales, breves y kaomojis `(◕‿◕✿)`.
* **Doble Modelo Inteligente (Ahorro de Costos)**: Permite configurar un modelo principal (Premium) para las conversaciones y un modelo secundario (Gratuito/Rápido) para procesos en segundo plano como resúmenes de memoria.
* **Agente Autónomo (Tools Loop)**: Miku "piensa" y utiliza herramientas dinámicamente antes de responderte. Puede leer archivos, buscar en internet o inyectar imágenes mediante comandos como `output[WebSearch...]`.
* **Memoria a Largo y Corto Plazo**: Estructura de compresión automática de contexto. Reduce historiales largos a resúmenes sólidos y persistentes basados en Markdown (`miku_memory.md` para gustos y `miku_soul.md` para personalidad).
* **Búsqueda Web Integrada**: Usa `ddgs` (DuckDuckGo) para buscar en la web en tiempo real, procesar la información de internet y usarla para responder preguntas sobre temas de actualidad o datos desconocidos.
* **Consola de Comando**: Modo CMD interactivo para administrar su alma, guardar sesiones y revisar logs del sistema en tiempo real.

---

## Vista Previa
![Miku Friend Preview](https://i.ibb.co/prdw3QZW/EXAMPLE.png)

---

## Requisitos de Sistema
* **Python 3.10** o superior.
* Conexión a Internet (para consultas OpenRouter).

---

## Instalación

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/Bimbot-afk/AI-Miku-fiend.git
   cd AI-Miku-fiend
   ```

2. **Instala las dependencias**:
   ```bash
   pip install PySide6 python-dotenv openrouter ddgs
   ```

3. **Configura tus credenciales (.env)**:
   Crea un archivo `.env` en la raíz del proyecto (o edita el de la carpeta `env/`) con tu API Key de OpenRouter:
   ```env
   api_key=TU_OPENROUTER_API_KEY
   url_api_key=https://openrouter.ai/api/v1
   ```

5. **Ejecuta la aplicación**:
   ```bash
   python main.py
   ```

---

## Uso

### Interfaz de Chat
* **Enviar mensajes**: Escribe en el campo de texto y haz clic en **Send** o presiona `Enter`.
* **Reiniciar chat**: Presiona **Restart** para limpiar el historial temporal de la sesión activa.
* **Configuración**: Abre el panel de configuración para modificar tu nombre, idioma de Miku, personalidad, modelo de OpenRouter e incluso el prompt base de su Alma.

### Consola de Comandos (CMD Mode)
Puedes usar comandos en la consola integrada para gestionar la memoria de Miku de forma directa:
* `/save soul <texto>`: Anexa instrucciones de personalidad directamente al prompt base en `miku_soul.md`.
* `/save memory <texto>`: Agrega un recuerdo general sobre ti (gustos, eventos pasados) en `miku_memory.md`.
* `/save session <texto>`: Registra notas y registros de la sesión de chat activa en `miku.md`.
* `/web_search <texto>`: (O mediante el uso autónomo de Miku). Permite al agente buscar información en línea, condensarla y responder basado en esos datos.
* `/read <palabras clave>`: Busca dentro de la memoria general del usuario.
* `/happymiku`: Inyecta automáticamente imágenes de gatitos para alegrarte si nota que estás triste.

---

## Tecnologías Utilizadas
* **Lenguaje**: Python 🐍
* **Interfaz de Usuario**: PySide6 (Qt para Python) 🎨
* **Procesamiento de Lenguaje**: OpenRouter API (Nube) 🧠
* **Almacenamiento**: Markdown (.md) y JSON (.json) 📄

---

## Contribución
Las contribuciones son bienvenidas. Si deseas colaborar:
1. Haz un **Fork** de este repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/NuevaMejora`).
3. Realiza tus cambios y haz **Commit** (`git commit -m 'Añade nueva funcionalidad'`).
4. Sube los cambios (`git push origin feature/NuevaMejora`) y abre un **Pull Request**.

---

## Licencia
Este proyecto es un trabajo de fans basado en Hatsune Miku y se distribuye bajo la licencia **MIT**. 

*Hatsune Miku © Crypton Future Media, INC. 2007. Usado bajo las guías de piapro y uso de personajes sin fines de lucro.*
