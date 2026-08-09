<div align="center">

# Miku Friend AI

![Python Version](https://img.shields.io/badge/python-3.10%2B-39c5bb?style=flat-svg&logo=python&logoColor=white)
![UI Framework](https://img.shields.io/badge/UI-PySide6--Qt6-39c5bb?style=flat-svg&logo=qt&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-39c5bb?style=flat-svg)

![Miku Friend Logo](https://i.ibb.co/BVzfJ5cS/MIKU.png)
<br>

[![Official Website](https://img.shields.io/badge/Official_Website-Visit_Us-39c5bb?style=for-the-badge)](https://bejewelled-banoffee-34df8f.netlify.app/)


</div>

---

## What is Miku Friend AI?

Miku Friend AI is a desktop assistant featuring an interactive and cool GUI, inspired by the Vocaloid **Hatsune Miku**. But she's much more than just a simple question-and-answer bot. Built as an **Autonomous Agent**, Miku actually takes the initiative! 

She might start a conversation out of the blue, notice the music you're listening to, read your system notifications, or even scold you if you start playing games instead of focusing on your work. She also manages her own memories about you, making your interactions feel persistent, natural, and uniquely yours. 



---

## Key Features

- **She Has a Mind of Her Own**: Miku doesn't just wait for you to type. If you're idle, she might reach out. She reads your system notifications, knows what's playing on Spotify, and even checks your local weather.
- **Focus Mode (Productivity First!)**: Need to get things done? Miku acts as your personal productivity coach. With her built-in smart timer and "Files Watcher," she keeps an eye on your background apps. Try launching a game while you're supposed to be studying, and she'll close it instantly and give you a piece of her mind!
- **Dual-Brain Architecture**: To keep things fast and smooth, Miku uses two AI models. A fast primary model handles your fluid, real-time conversations, while a heavy-duty secondary model quietly works in the background to organize files, detect games, and summarize her memories.
- **She Remembers You**: Using a smart, automatic context-compression system (`miku_memory.md` & `miku_soul.md`), she maintains both short-term context and long-term memories about your likes, dislikes, and past chats.
- **Always Connected**: Miku can search the web in real-time using DuckDuckGo to answer your questions with up-to-date information.

 <img width="718" height="451" alt="Captura de pantalla 2026-07-17 235255" src="https://github.com/user-attachments/assets/91797305-8cb4-4494-8ee5-09a0f6ad14a8" />


---

## How Her Brain Works (Architecture)

Curious about what's under the hood? Here's a quick tour of how Miku's files and modules are organized:

### `UI/` (The Face)
Everything you see on screen, built with PySide6.
- `MainWindow.py`: Your main chat room with Miku.
- `MikuPopup.py`: Those little desktop notifications she sends you.
- `configuration.py` & `first_app_screen.py`: Where you set up your API keys and customize her settings.
- `timmer_app.py`: The UI for your Focus Mode timer.

### `core/` (The Nervous System)
The main orchestrator that keeps everything running.
- `brain.py`: Where the magic happens. This handles her prompts, context, and how she talks to you.
- `notifications_listener.py`: The module that secretly reads your Windows notifications so Miku knows what's going on.
- `miku_config_manager.py`: Handles all her internal settings.

### `agent_f/` (Her Little Helpers)
Specialized background sub-agents that do a essay for you.
- `research_agent.py`: Digs through the web for complex answers.
- `essay_agent_brain.py`: Helps her write long, structured texts.
- `YES_or_No_agent.py`: A quick decision-making bot for fast validations.

### `tools/` (Her Senses and Skills)
Scripts that allow Miku to interact with your PC.
- `files_watcher.py`: The strict monitor that catches you playing games during Focus Mode.
- `music_listener.py`: Helps her figure out what song you're vibing to.
- `idle_message.py`: Triggers her to say hi when you've been quiet for too long.

### `miku_agent/` (Her Memory)
Markdown and JSON files where she stores everything she knows.
- `miku_soul.md`: The core of who she is—her personality, rules, and traits.
- `miku_memory.md`: The diary of your friendship. Long-term memories go here.
- `organized_programs.json`: The AI-generated list that helps her tell the difference between "Photoshop" (work) and "Minecraft" (game).

---

## Installation and Setup

> **Note:** A super easy one-click installer is coming to the website. For now, here is how you can summon Miku using the terminal.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Bimbot-afk/AI-Miku-fiend.git
   cd AI-Miku-fiend
   ```

2. **Set up the environment**:
   ```bash
   python -m venv env
   env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Give her the keys (`.env`)**:
   Create a file named `.env` in the root folder and paste your API key (from OpenRouter or your favorite provider).
   ```env
   api_key=YOUR_API_KEY_HERE
   url_api_key=https://openrouter.ai/api/v1
   ```

4. **Wake her up**:
   ```bash
   python main.py
   ```

---

## Quick Usage Guide

### Just Hang Out
- **Chat freely**: Just type in the box. If you leave her running in the background, she might randomly comment on a notification you just got or the song you just played!
- **Time to Work (Focus Mode)**: Tell Miku you need to concentrate. She'll set a timer and activate the Files Watcher. Don't even try opening a game—she will catch you and close it!

### Admin Commands
Want to take direct control? Use these slash commands in the chat:
- `/save soul <text>` : Teach her a permanent new personality rule.
- `/save memory <text>` : Force her to remember a specific fact about you.
- `/read <soul | session | notifications | music>` : Manually tell her to check one of her sensors.
- `/start_timer <ms>` : Start the Focus Mode timer (in milliseconds).
- `/happymiku` : Try it and see what happens! ✨

---

## Contributing

We'd love your help to make Miku even smarter! 
1. Fork the repo.
2. Create your feature branch (`git checkout -b feature/CoolNewIdea`).
3. Commit your changes (`git commit -m 'Added something awesome'`).
4. Push to the branch (`git push origin feature/CoolNewIdea`).
5. Open a Pull Request!

---

<div align="center">

**MIT License** | This project is a fan-made creation.
*Hatsune Miku Copyright Crypton Future Media, INC. 2007. Used under piapro guidelines and for non-profit purposes.*

</div>
