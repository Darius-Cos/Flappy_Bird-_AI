# Flappy Bird with AI 🐦🤖

## Overview
Welcome to the **Flappy Bird with AI** project! This desktop application reimagines the classic Flappy Bird game by integrating an artificial intelligence system powered by the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm. Watch as the AI learns to navigate the bird through a series of pipes, evolving over generations to improve its performance. Test the limits of machine learning in a fun and interactive way!

## Features
- ✨ **AI-Driven Gameplay**: A neural network controls the bird, learning to avoid pipes through evolution.
- 🌐 **Dynamic Obstacles**: Pipes are generated randomly, challenging the AI to adapt.
- 📈 **Score System**: Tracks the number of pipes successfully passed by the AI.
- 🔄 **Generation Tracking**: Displays the current generation and number of birds alive.
- 🎥 **Real-Time Visualization**: See the bird’s movements and the AI’s decision-making process unfold live.
- 🎨 **Smooth Animations**: Enjoy a visually appealing and responsive game experience.

## Getting Started
### 1. Installation
- Clone the repository or download the source code from [GitHub](https://github.com/Darius-Cos/Flappy_Bird-_AI).
- Ensure you have **Python** installed on your system.
- Install the required dependencies by running:
  
  ```bash
  pip install pygame neat-python
  ```

### 2. Running the Game
- Open a **terminal** or **command prompt** in the project directory.
- Run the following command:
  
  ```bash
  python flappy_bird_ai.py
  ```
  
- The game window will open, and the AI will begin training immediately!

### 3. Playing the Game
- The game is **fully autonomous**—sit back and watch the AI control the bird!
- The bird jumps based on decisions made by the neural network, aiming to avoid pipes.
- The game continues across **generations**, with the AI improving its strategy over time.
- Close the window to stop the simulation.

## Rules 📝
- The bird moves forward **automatically**, and the AI decides **when to jump**.
- Each time the bird **passes a pipe**, the score increases, and the AI earns a fitness boost.
- The game **ends for a bird** when it collides with a **pipe, the floor, or flies too high**.
- The simulation runs for up to **50 generations** or until the AI achieves a high score.

## About 📚
This project combines the nostalgic **Flappy Bird** game with **cutting-edge AI technology**. Built using **Python, Pygame, and NEAT-Python**, it demonstrates how neural networks can learn complex tasks through **evolutionary algorithms**. It’s a great showcase of **machine learning applied to game development**, blending entertainment with education.

## Contribution 💪
Contributions are always welcome! If you have ideas for enhancements—like tweaking the NEAT configuration, adding new features, or improving the UI—feel free to **fork** the repository and submit a **pull request**.

## Credits ✨
Inspired by:
- [sourabhv/FlapPyBird](https://github.com/sourabhv/FlapPyBird)
- [sarvagyavaish/FlappyBirdRL](https://github.com/sarvagyavaish/FlappyBirdRL)
- [mihaibivol/Q-learning-tic-tac-toe](https://github.com/mihaibivol/Q-learning-tic-tac-toe)

## License ⚖️
This project is **open-source** under the **MIT license**, allowing you to use and modify it for personal or educational purposes.

---

Enjoy watching your AI learn to fly! 🛩️🐦
