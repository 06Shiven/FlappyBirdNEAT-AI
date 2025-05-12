# FlappyBirdNEAT-AI

This project is an AI-powered Flappy Bird built using Python, Pygame, and NEAT (NeuroEvolution of Augmenting Topologies). The AI learns how to play Flappy Bird through trial and error by evolving its strategy over generations.

---

## 🧠 Features

- ✅ AI learns from scratch with no pre-defined rules
- ✅ Persistent learning across runs (`checkpoint.pkl`)
- ✅ Best-performing bird saved after each generation (`best_bird.pkl`)
- ✅ Live graph of fitness over generations
- ✅ Pause/resume anytime with `SPACEBAR`
- ✅ Press `R` to reset to a fresh population

---

## 🚀 How It Works

- The bird makes decisions based on:
  - Its vertical position
  - Distance to the next pipe’s top and bottom
- Each generation consists of multiple birds (neural networks) evaluated by how far they go.
- NEAT evolves the population over time, favoring higher fitness scores.

---

## 🎮 Controls

| Key        | Action                       |
|------------|------------------------------|
| `SPACEBAR` | Pause/resume training        |
| `R`        | Reset all progress (fresh AI)|

---

## 📊 Output Files

- `checkpoint.pkl` – AI population memory (used to resume learning)
- `best_bird.pkl` – The best-performing bird genome
- **Matplotlib Plot** – Shows best fitness score per generation (auto-refreshes)
