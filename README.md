<div align="center">

# Miku Friend AI
### *Your Agentic and Autonomous Virtual Assistant*

![Python Version](https://img.shields.io/badge/python-3.10%2B-39c5bb?style=flat-svg&logo=python&logoColor=white)
![UI Framework](https://img.shields.io/badge/UI-PySide6--Qt6-39c5bb?style=flat-svg&logo=qt&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-39c5bb?style=flat-svg)

![Miku Friend Logo](https://i.ibb.co/BVzfJ5cS/MIKU.png)
<br>

[![Official Website](https://img.shields.io/badge/Official_Website-Visit_Us-39c5bb?style=for-the-badge)](https://bejewelled-banoffee-34df8f.netlify.app/)

*Miku Friend is not just a chatbot... she is a living companion on your desktop!*

</div>

---

## Overview

Miku Friend AI is a desktop artificial intelligence assistant with an interactive graphical user interface, inspired by the virtual idol **Hatsune Miku**. Designed with an **Autonomous Agent** approach, Miku takes the initiative to start conversations, listen to your music, read your notifications, reprimand you if you get distracted by games (Focus Mode), and manage memories in a persistent and natural way.

---

## Key Features

- **Comprehensive Autonomous Agent**: Miku takes the initiative. If you are idle, she will reach out to you. She reads your system notifications, knows what music you are listening to, and checks the current weather in your local area.
- **Focus Mode**: A smart timer with a "Files Watcher" that monitors your background processes. If you open a game while you should be studying or working, Miku will close it instantly and scold you.
- **Authentic Personality**: Acts and responds like Miku, using natural and expressive language.
- **Dual Intelligent Model Architecture**: Uses a primary model for fluid conversations and a secondary model for heavy background agentic processes like organizing files, detecting games, and summarizing memory, optimizing resource usage.
- **Long and Short Term Memory**: Automatic context compression structure in Markdown format (`miku_memory.md`, `miku_soul.md`).
- **Web Search**: Uses DuckDuckGo to search the internet in real-time.

---

## Project Architecture and File Structure

Miku Friend AI is organized into several modules, separating the core agent logic, the graphical user interface, and the autonomous tools. Below is a detailed description of the project's file structure:

### Root Directory
- `main.py`: The main entry point of the application. It initializes the environment, loads configurations, and launches the Graphical User Interface (GUI).
- `README.md`: The project documentation file you are currently reading.
- `requirements.txt`: Contains all the Python dependencies required to run the project.
- `.env`: Environment variables file storing your API keys and endpoint URLs.
- `.gitignore`: Specifies intentionally untracked files that Git should ignore.
- `LICENSE`: The MIT License file governing the project's distribution and usage.
- `MikuFriend.spec`: PyInstaller specification file used for building the executable release version of the application.
- `test_hc_direct2.py` / `test_openrouter2.py`: Test scripts used during development to verify API connections and routing.

### `UI/` (User Interface)
Contains all the graphical components built with PySide6.
- `MainWindow.py`: The main chat window where the user interacts with Miku.
- `MikuPopup.py`: Handles small popup notifications or alerts that Miku displays on the screen.
- `chatbot_miku.py`: Contains the UI logic specifically for the chatbot interface and message rendering.
- `configuration.py`: The settings window where users can adjust application parameters and API keys.
- `first_app_screen.py`: The initial setup screen shown when the application is launched for the first time without an API key.
- `miku_cmd.py`: A command-line interface or debug view embedded within the UI.
- `timmer_app.py`: The timer widget used for the Focus Mode feature.

### `core/` (Core Logic)
The central nervous system and main orchestrator of the Miku agent.
- `brain.py`: The core agent logic handling prompting, context assembly, and interaction flow.
- `cmd_brain.py`: Handles the execution of special commands input by the user.
- `config.json`: Configuration file specifying the primary and secondary Language Models to be used.
- `i18n.py`: Internationalization script for handling multi-language support.
- `miku_config_manager.py`: Manages reading and writing application configurations.
- `notifications_listener.py`: Continuously listens to Windows system notifications to provide Miku with real-time context.

### `agent_f/` (Agent Functions)
Contains specialized sub-agents responsible for specific asynchronous or background tasks.
- `Editing_agent.py`: A specialized agent for editing and refining text.
- `YES_or_No_agent.py`: A binary decision-making agent used for quick validations.
- `drafting_agent.py`: Responsible for drafting initial responses or content.
- `essay_agent_brain.py`: Handles long-form text processing using the secondary LLM.
- `research_agent.py`: Conducts background research and gathers information for complex queries.

### `tools/` (Skills and Capabilities)
Scripts that give Miku the ability to interact with the system and the outside world.
- `files_watcher.py`: Scans running background processes to block games during Focus Mode.
- `get_weather.py`: Fetches the local weather data.
- `idle_message.py`: Triggers messages when the user has been inactive for a certain period.
- `music_listener.py`: Detects the music currently playing on the system.
- `open_app.py`: Executes applications and shortcuts on the user's command.
- `open_txt_file.py`: Utility to read the contents of text files.
- `read_memory.py`: Interfaces with the long-term memory files to retrieve past context.
- `web_search.py`: Performs real-time internet searches using DuckDuckGo.

### `miku_agent/` (Persistent Storage)
Markdown and JSON files acting as Miku's memory and knowledge base.
- `miku.md`: General state or instructions.
- `miku_memory.md`: Stores long-term memories and facts about the user.
- `miku_soul.md`: Defines the core personality, traits, and strict behavioral rules for Miku.
- `miku_tools.md`: Documentation or schema of the tools available to the agent.
- `notifications.md`: A temporary log of recent system notifications read by the agent.
- `programs.md`: A cached list of the installed programs on the user's computer.
- `organized_programs.json`: AI-generated classification of the user's applications, critical for identifying games during Focus Mode.

### Other Directories
- `landing_page/`: Contains the source code (`index.html`) and release packages (`MikuFriend_Release.zip`) for the official website.
- `miku_creations/`: Output directory where files generated by the agent (such as essays or documents) are saved.
- `assets/`: Contains visual resources such as images, icons, and fonts used by the UI.
- `build/` & `dist/`: Directories generated by PyInstaller containing the compiled executable files.
- `env/`: The Python virtual environment directory containing installed dependencies.

---

## Installation and Setup

> **Note:** In the future, we will release a streamlined download page with an automatic installer. For now, here are the instructions to install it from the terminal.

1. **Clone this repository**:
   ```bash
   git clone https://github.com/Bimbot-afk/AI-Miku-fiend.git
   cd AI-Miku-fiend
   ```

2. **Create a virtual environment and install dependencies**:
   ```bash
   python -m venv env
   env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure your credentials (`.env`)**:
   Create a file named `.env` in the root of the project. You must add your API Key from OpenRouter or your preferred provider.
   ```env
   api_key=YOUR_API_KEY_HERE
   url_api_key=https://openrouter.ai/api/v1
   ```

4. **Launch Miku**:
   ```bash
   python main.py
   ```

---

## Quick Usage Guide

### Natural Interaction
- **Chat Freely**: Simply type in the text box. If you leave her in the background and play music or receive a Windows notification, Miku will know and might bring it up to start a conversation.
- **Focus Mode**: When you need to work, ask Miku for a timer. The Files Watcher will activate. If you try to open a game during your study time, Miku will intervene and close it to keep you productive.

### Command Console (Admin Mode)
Type these commands directly into the chat to manually operate the system:
- `/save soul <text>` : Appends permanent rules to her personality profile.
- `/save memory <text>` : Forces the writing of a long-term memory about you.
- `/read <soul | session | notifications | music>` : Forces Miku to read a specific data sensor.
- `/web_search <text>` : Manually commands a web search.
- `/start_timer <ms>` : Starts the Focus Mode for a specific time in milliseconds.
- `/happymiku` : Triggers a special reaction.

---

## Contributing

All help is welcome to make Miku even smarter!
1. Fork this repository.
2. Create a feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

---

<div align="center">

**MIT License** | This project is a fan-made creation.
*Hatsune Miku Copyright Crypton Future Media, INC. 2007. Used under piapro guidelines and for non-profit purposes.*

</div>
