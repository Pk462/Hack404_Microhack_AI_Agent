# Hack404_Microhack_AI_Agent
Here is our team's project for the AI Agents Microhack.

## 🤖 AI Reminder Buddy

AI Reminder Buddy is a customizable, persona-driven reminder tool, which comes with several different personalities.

---

### 🚀 Features

- 📅 Add custom reminders at set intervals  
- 🎭 Choose from a range of AI personas  
- 🤖 Generates motivational messages using the Alith AI Agent  
- 🎮 Earn experience points as you complete tasks  
- 💬 Live terminal input: snooze, update intervals, or complete reminders on the fly.

---

### 📦 Setup Instructions

> ⚠️ This project is designed to run in a Python environment (Google Colab-friendly).

**1. Clone the repository**

```bash
git clone https://github.com/Pk462/Hack404_Microhack_AI_Agent.git
cd ai-reminder-buddy
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Set up environment variables**

Create a `.env` file and add your Alith API key:

```env
ALITH_API_KEY=your_alith_api_key_here
```

**4. Run the script**

```bash
python reminder_buddy.py
```

### 🛠 Commands

While the reminder loop is running, you can:

- `snooze` — Snooze the last reminder for 60 seconds  
- `change [seconds]` — Change interval of the last triggered reminder  
- `complete [number]` — Mark a reminder as done  
- `exit` / `stop` — Stop the reminder buddy

---

### 🧠 Built With

- [Alith](https://alith.run/) — for custom AI agent prompts  
- `dotenv` — to securely handle API keys  
- `threading` & `time` — for concurrent input and reminder logic  
- Google Colab — for real time coordination and coding with our team

---

### 📜 License

MIT License

---

### 🙏 Acknowledgements

- The Alith team
- Google Colab
