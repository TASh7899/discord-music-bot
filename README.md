# 🎵 Discord Music Bot

A simple YouTube-powered music bot for Discord built with Python and `discord.py`. It supports playing songs, queuing, pausing, resuming, skipping, and more using the `$` prefix.

---

## ✨ Features

- 🔍 Search and play YouTube songs using keywords
- 📜 Server-specific music queue
- ⏯️ Pause, resume, and skip tracks
- 📂 View and remove songs from the queue
- 📤 Auto-disconnect when queue is empty
- 🧠 Help command with embedded info

---

## ⚙️ Setup Instructions for the Discord Music Bot

### 1. **Clone the Repository**

```bash
git clone https://github.com/your-username/discord-music-bot.git
cd discord-music-bot
```

### 2. **Create a Virtual Environment (Optional but Recommended)**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Create a `.env` File**

Create a file named `.env` in the root directory with the following content:

```
TOKEN=your_discord_bot_token_here
```

### 5. **Enable Privileged Intents**

Go to the [Discord Developer Portal](https://discord.com/developers/applications):

* Click your bot → **Bot** tab → Enable:

  * "MESSAGE CONTENT INTENT"
  * "SERVER MEMBERS INTENT" (optional)

### 6. **Run the Bot**

```bash
python3 main.py
```

---

### ✅ Requirements

Make sure you have:

* Python 3.8 or above
* `ffmpeg` installed and added to your system PATH


---

## 🎵 Discord Music Bot – Usage Instructions

### ✅ Commands List

| Command                   | Description                                      |
| ------------------------- | ------------------------------------------------ |
| `$hello`                  | Greets the user                                  |
| `$ytp <song name or URL>` | Plays or queues a YouTube song                   |
| `$ytpause`                | Pauses the current song                          |
| `$ytresume`               | Resumes a paused song                            |
| `$ytskip`                 | Skips the current song and plays the next one    |
| `$ytqueue`                | Shows the current song queue                     |
| `$ytremove <index>`       | Removes a song from the queue at the given index |
| `$yts`                    | Stops the bot and clears the queue               |
| `$musichelp`              | Shows the command help menu (embed)              |

---

### ▶️ How to Use

1. **Invite the bot** to your Discord server (you must host it yourself).
2. **Join a voice channel**.
3. **Play a song** using:

   ```
   $ytp never gonna give you up
   ```
4. **Pause a song**:

   ```
   $ytpause
   ```
5. **Resume a paused song**:

   ```
   $ytresume
   ```
6. **Skip to next**:

   ```
   $ytskip
   ```
7. **View queue**:

   ```
   $ytqueue
   ```
8. **Remove a song by position** (e.g., 2nd song):

   ```
   $ytremove 2
   ```
9. **Stop bot and disconnect**:

   ```
   $yts
   ```

---


