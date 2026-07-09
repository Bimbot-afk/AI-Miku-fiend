<div align="center">

# 🧪 [ VERSIÓN BETA ] 🧪
### *Funciones Agénticass*

***
</div>

# Miku Friend AI 

![Miku Friend Logo](https://i.ibb.co/BVzfJ5cS/MIKU.png)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-39c5bb?style=flat-svg&logo=python&logoColor=white)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/UI-PySide6--Qt6-39c5bb?style=flat-svg&logo=qt&logoColor=white)](https://wiki.qt.io/Qt_for_Python)
[![License](https://img.shields.io/badge/license-MIT-39c5bb?style=flat-svg)](LICENSE)

Un asistente de inteligencia artificial de escritorio con interfaz gráfica interactiva, inspirado en **Hatsune Miku**. Diseñado bajo un enfoque de **Agente Autónomo**, Miku es capaz de iniciar conversaciones, escuchar tu música, leer tus notificaciones, consultar el clima en tu ciudad y gestionar recuerdos de forma persistente y natural mediante el uso de APIs.

---

## 📑 Tabla de Contenidos
- [Características principales](#-características-principales)
- [Vista Previa](#-vista-previa)
- [Requisitos de Sistema](#-requisitos-de-sistema)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## ✨ Características principales
* **Agente Autónomo Integral**: Miku toma la iniciativa. Si estás inactivo, ella te escribirá. Puede **leer las notificaciones** de tu sistema, saber **qué música estás escuchando** y consultar el **clima actual de tu ciudad** para tener conversaciones hiper-personalizadas y dinámicas.
* **Personalidad de Hatsune Miku**: Diseñada para actuar como Miku usando respuestas naturales, breves y kaomojis `(◕‿◕✿)`.
* **Doble Modelo Inteligente (Ahorro de Costos)**: Configura un modelo principal (Premium) para el chat y un modelo secundario (Gratuito/Rápido) para procesos en segundo plano como resúmenes de memoria y recolección de datos agénticos.
* **Memoria a Largo y Corto Plazo**: Estructura de compresión automática de contexto en Markdown (`miku_memory.md` para tus gustos, `miku_soul.md` para su personalidad y `miku.md` para la sesión actual).
* **Búsqueda Web Integrada**: Usa el motor DuckDuckGo para buscar en internet en tiempo real y responder preguntas sobre temas actuales.
* **Consola de Comandos (CMD Mode)**: Modo de control interactivo para administrar su alma, forzar lecturas de sensores y revisar logs del sistema en vivo.

---

## 📸 Vista Previa
![Miku Friend Preview](https://i.ibb.co/prdw3QZW/EXAMPLE.png)

---

## ⚙️ Requisitos de Sistema
* **Python 3.10** o superior.
* Conexión a Internet (para consultas a OpenRouter y web search).
* Sistema operativo Windows (para la lectura óptima de notificaciones y música mediante WinSDK).

---

## 🚀 Instalación

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/Bimbot-afk/AI-Miku-fiend.git
   cd AI-Miku-fiend
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   # Si no tienes un requirements.txt, asegúrate de instalar las librerías necesarias:
   pip install PySide6 python-dotenv openrouter ddgs winsdk
   ```

3. **Configura tus credenciales (.env)**:
   Crea un archivo `.env` en la raíz del proyecto (o edita el de la carpeta `env/`) con tu API Key de OpenRouter:
   ```env
   api_key=TU_OPENROUTER_API_KEY
   url_api_key=https://openrouter.ai/api/v1
   ```

4. **Ejecuta la aplicación**:
   ```bash
   python main.py
   ```

---

## 🎮 Uso

### Interfaz de Chat
* **Enviar mensajes**: Escribe en el campo de texto y presiona `Enter`.
* **Miku Activa**: ¡Déjala en segundo plano! Ella notará si te ausentas o si cambias de canción y podría comentarlo (gracias a sus funciones agénticas).
* **Reiniciar chat**: Presiona **Restart** para limpiar el historial temporal.
* **Configuración Avanzada**: Abre el panel de configuración para modificar tu **ciudad** (para que Miku vea tu clima), nombre, idioma, personalidad y modelos de IA.

### Consola de Comandos (CMD Mode)
Utiliza la barra de chat para enviar comandos directos:
* `/save soul <texto>`: Anexa instrucciones de personalidad al prompt base de Miku.
* `/save memory <texto>`: Agrega un recuerdo importante sobre ti en la memoria a largo plazo.
* `/save session <texto>`: Registra notas vitales en la sesión activa.
* `/read <soul / session / notifications / music>`: Obliga a Miku a leer un apartado específico de sus "sensores" o de tu memoria para que responda sobre ello.
* `/web_search <texto>`: Busca información en internet de forma forzada.
* `/happymiku`: Despliega un tierno gatito sorpresa en la pantalla.

---

## 🛠️ Tecnologías Utilizadas
* **Lenguaje**: Python 🐍
* **Interfaz de Usuario**: PySide6 (Qt para Python) 🎨
* **Procesamiento de Lenguaje**: OpenRouter API (Nube) 🧠
* **Agentes & Sensores**: WinSDK (Música y Notificaciones), DuckDuckGo Search API 🌐
* **Almacenamiento**: Markdown (.md) y JSON (.json) 📄

---

## 🤝 Contribución
Las contribuciones son muy bienvenidas. Si deseas colaborar para hacer a Miku aún más lista:
1. Haz un **Fork** de este repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/NuevaMejora`).
3. Realiza tus cambios y haz **Commit** (`git commit -m 'Añade nueva funcionalidad'`).
4. Sube los cambios (`git push origin feature/NuevaMejora`) y abre un **Pull Request**.

---

## 📜 Licencia
Este proyecto es un trabajo de fans basado en Hatsune Miku y se distribuye bajo la licencia **MIT**. 

*Hatsune Miku © Crypton Future Media, INC. 2007. Usado bajo las guías de piapro y uso de personajes sin fines de lucro.*
