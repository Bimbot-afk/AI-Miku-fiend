<div align="center">

# Miku Friend AI
### *Tu Asistente Virtual Agéntico y Autónomo*

![Python Version](https://img.shields.io/badge/python-3.10%2B-39c5bb?style=flat-svg&logo=python&logoColor=white)
![UI Framework](https://img.shields.io/badge/UI-PySide6--Qt6-39c5bb?style=flat-svg&logo=qt&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-39c5bb?style=flat-svg)

![Miku Friend Logo](https://i.ibb.co/BVzfJ5cS/MIKU.png)

*Miku Friend no es solo un chatbot... ¡es una compañera viva en tu escritorio!*

</div>

---

## ¿Qué es Miku Friend AI?

Un asistente de inteligencia artificial de escritorio con interfaz gráfica interactiva, inspirado en la idol virtual **Hatsune Miku**. Diseñado bajo un enfoque de **Agente Autónomo**, Miku es capaz de tomar la iniciativa, iniciar conversaciones, escuchar tu música, leer tus notificaciones, regañarte si te distraes jugando (Focus Mode) y gestionar recuerdos de forma persistente y natural.

---

## Características Principales

- **Agente Autónomo Integral**: Miku toma la iniciativa. Si estás inactivo, ella te escribirá. Lee las notificaciones de tu sistema, sabe qué música escuchas y consulta el clima actual de tu ciudad.
- **Modo Concentración (Focus Mode)**: Un cronómetro inteligente con un "Files Watcher" que vigila tus procesos en segundo plano. Si abres un juego mientras deberías estudiar o trabajar... ¡Miku te lo cerrará al instante y te regañará! (>_<)
- **Personalidad Auténtica**: Actúa y responde como Miku, usando lenguaje natural, expresivo y tiernos kaomojis (◕‿◕✿).
- **Doble Modelo Inteligente (Ahorro)**: Utiliza un modelo principal (Premium) para las charlas fluidas y un modelo secundario (Gratuito/Rápido) para procesos agénticos pesados en segundo plano como organizar archivos, detectar juegos y resumir memoria.
- **Memoria a Largo y Corto Plazo**: Estructura de compresión automática de contexto en Markdown (`miku_memory.md`, `miku_soul.md`, `miku_session.md`).
- **Búsqueda Web**: Uso de DuckDuckGo para buscar en internet en tiempo real.

---

## Arquitectura del Proyecto

Mantener un proyecto agéntico ordenado es clave. Así es como funciona el cerebro de Miku por dentro:

```text
miku_friend/
├── main.py                     # Punto de entrada principal y carga de UI
├── README.md                   # ¡Estás aquí!
├── requirements.txt            # Dependencias del proyecto
├── .env                        # Claves de API y configuración de URL
│
├── core/                       # El cerebro principal de Miku
│   ├── brain.py                # Lógica del Agente, promting y memoria
│   └── config.json             # Configuración de modelos (Principal y Secundario)
│
├── UI/                         # Interfaz Gráfica (PySide6)
│   ├── MainWindow.py           # Ventana principal del chat
│   └── timmer_app.py           # Widget de cronómetro para el Focus Mode
│
├── tools/                      # Herramientas y Habilidades (Skills)
│   ├── files_watcher.py        # Escáner de procesos y bloqueador de juegos
│   ├── get_weather.py          # Lector del clima local
│   ├── open_app.py             # Ejecutor de aplicaciones y accesos directos
│   └── discord_search.py       # Interfaz de lectura en Discord
│
├── agent_functions/            # Sub-agentes y procesamiento asíncrono
│   └── essay_agent_brain.py    # Procesamiento con modelo LLM secundario
│
├── miku_agent/                 # Almacenamiento persistente de Miku
│   ├── miku_soul.md            # Reglas base de su personalidad
│   ├── miku_memory.md          # Recuerdos a largo plazo sobre ti
│   ├── programs.md             # Caché de tus programas instalados
│   └── organized_programs.json # Clasificación de tus apps generada por IA
│
└── assets/                     # Recursos visuales
    └── (imágenes, iconos, fuentes)
```

---

## Instalación y Configuración

> **Nota:** En el futuro, lanzaremos una página de descarga basada en Streamlit con un instalador automático mucho más amigable. Por ahora, mantenemos la esencia hacker: aquí tienes las instrucciones para instalarlo desde la consola.

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/Bimbot-afk/AI-Miku-fiend.git
   cd AI-Miku-fiend
   ```

2. **Crea un entorno virtual (Recomendado) e Instala dependencias**:
   ```bash
   python -m venv env
   env\Scripts\activate
   pip install -r requirements.txt
   # Si faltan dependencias manuales: pip install PySide6 python-dotenv openrouter ddgs winsdk psutil
   ```

3. **Configura tus credenciales (`.env`)**:
   Crea un archivo llamado `.env` en la raíz del proyecto. Deberás añadir tu API Key de [OpenRouter](https://openrouter.ai/) o de tu proveedor proxy (ej. HackClub).
   ```env
   api_key=TU_API_KEY_AQUI
   url_api_key=https://openrouter.ai/api/v1
   ```

4. **¡Inicia a Miku!**:
   ```bash
   python main.py
   ```

---

## Guía de Uso Rápida

### Interacción Natural
- **Conversa libremente**: Simplemente escribe en la caja de texto. Si la dejas en segundo plano y pones música en Spotify o te llega una notificación importante de Windows, Miku lo sabrá y podría mencionarlo para sacarte tema de conversación.
- **Modo Concentración (Focus Mode)**: Cuando necesites trabajar, pídele a Miku un temporizador. El *Files Watcher* entrará en acción. Si intentas abrir un juego durante tu tiempo de estudio, Miku te reprenderá y lo cerrará para mantenerte productivo.

### Consola de Comandos (Modo Administrador)
Escribe estos comandos directamente en el chat para operar el sistema manualmente:
- `/save soul <texto>` ➔ Anexa reglas permanentes a su personalidad.
- `/save memory <texto>` ➔ Fuerza la escritura de un recuerdo a largo plazo sobre ti.
- `/read <soul | session | notifications | music>` ➔ Obliga a Miku a leer un sensor específico.
- `/web_search <texto>` ➔ Ordena una búsqueda en la web manualmente.
- `/start_timer <ms>` ➔ Inicia el Focus Mode por un tiempo específico en milisegundos.
- `/happymiku` ➔ ¡Sorpresa adorable!

---

## Contribuyendo

¡Toda ayuda es bienvenida para hacer a Miku aún más inteligente!
1. Haz un **Fork** de este repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/NuevaMejora`).
3. Haz **Commit** de tus cambios (`git commit -m 'Añade nueva funcionalidad'`).
4. Haz **Push** a la rama (`git push origin feature/NuevaMejora`).
5. Abre un **Pull Request**.

---

<div align="center">

**Licencia MIT** | Este proyecto es un trabajo creado por fans.
*Hatsune Miku © Crypton Future Media, INC. 2007. Usado bajo las guías de piapro y sin fines de lucro.*

</div>
