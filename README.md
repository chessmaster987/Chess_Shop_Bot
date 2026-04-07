# Chess Shop Bot 🏰♟️
**A telegram bot for a chess shop. You can find it in Telegram via this link: https://t.me/chess_shop_bot**

[![Python](https://img.shields.io/badge/Python-3.10+-blue)]()
[![Telegram Bot](https://img.shields.io/badge/Platform-Telegram-blue)]()
[![Status](https://img.shields.io/badge/status-active-success)]()

A Telegram bot for browsing chess products (boards, pieces, clocks) with a simple interactive menu and simulated order system.

---

## 📖 Table of Contents

- [Features](#features)
- [Menu Structure](#menu-structure)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Common Issues](#common-issues)
- [Tips](#tips)
- [Author](#author)

---

## 🚀 Features

- Interactive Telegram menu
- Product categories and subcategories
- Display of photos + descriptions
- Generation of unique order numbers
- Automatic deletion of old messages
- Easy extensibility (just add a photo + .txt)

---

## 📊 Menu Structure
- /start
  - Shop items
    - Chess boards
      - Classic
      - 3 players
      - 4 players
    - Customise
      - Chess pieces
        - Classic
        - Royal period
        - Harry Potter
      - Chess clocks
        - Mechanical
        - Electronic
        - Custom
    - Share this bot

---

## 📂 Project Structure
- Chess_Shop_Bot/
  - chess_shop_bot.py
  - requirements.txt
  - .env
  - README.md
  - imgs/
    - logo.jpg
    - boards/
    - pieces/
    - clocks/

⚠️ Each image must have a matching `.txt` file: &nbsp;
```board1.jpg```
and
```board1.txt```

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/chessmaster987/Chess_Shop_Bot.git
cd Chess_Shop_Bot 
```

### 2. Create virtual environment

```python -m venv venv```

**Activate:**

Windows
```venv\Scripts\activate```

Linux / Mac
```source venv/bin/activate```

### 3. Install dependencies

```pip install -r requirements.txt```

### 4. Create .env file
```BOT_TOKEN=your_telegram_bot_token_here```

**Get token via Telegram `@BotFather`**

---

## ▶️ Usage

### Run the bot

``` python chess_shop_bot.py ```

Make sure your code includes:
```bot.remove_webhook()```
```bot.infinity_polling()```

---

## ⚠️ Common Issues

### Error 409: webhook active

``` bot.remove_webhook() ```

### Images not showing

- check imgs/ folder
- check filenames

### SSL / HTTPS errors

Use polling instead of webhook

---

## 💡 Tips

1. Add new products → just add:
    - image
    - .txt description
2. Easy to modify categories via callback_data
3. Bot auto-cleans old messages

---

## 👨‍💻 Author

**Vladyslav Lavrov**
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/chessmaster987)&nbsp;[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vlad-lavrov/)