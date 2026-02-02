# Gesture Controlled Virtual Keyboard

A real-time gesture-controlled virtual keyboard built using **OpenCV**, **MediaPipe**, and **Pygame**.

The project explores hand-tracking based input systems inspired by XR and spatial computing interfaces.

---

## ✨ Features
- Real-time hand tracking using MediaPipe
- Gesture confidence filtering (Phase 2.1)
- Virtual keyboard UI
- Pinch-based key selection
- Modular and extensible architecture

---

## 🛠 Tech Stack
- Python
- OpenCV
- MediaPipe
- Pygame

---

## Project Note
This project was paused after Phase 2.1 once the core gesture interaction system was stabilized.

Planned improvements:
- UI/UX enhancements (glassy keys, animations)
- Advanced gesture semantics
- XR / Unity port
- Predictive typing and correction

---

## ▶️ How to Run

```bash
git clone <repo-url>
cd GestureKeyboard
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd src
python main.py
