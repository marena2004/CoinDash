# CoinDash
## Project Overview
This project aims to develop a basic 2D platformer game using Python and Pygame. The game will involve a player-controlled character navigating through a single-level environment, avoiding obstacles, and reaching a goal. The mechanics will include jumping, running, and collecting simple items.

## Game Concept
The game will be a side-scrolling platformer where the player navigates through a single-level environment, avoiding obstacles and collecting coins to achieve the highest possible score. The player must jump over gaps, evade spikes, and avoid enemy objects while progressing. If they collide with an obstacle, fall into a gap, or are hit by an enemy, the game will be over. The game will track deaths based on their cause, such as falling or hitting an obstacle, to analyze difficulty. Since there is only one level, players must carefully time their movements and master the mechanics to successfully reach the goal.

## Main Features
1. character movement(jumping, running)
2. Collision detection
3. Collectibles(coins)
4. A single-level environment
5. Score tracking

## How To Run
1. Clone the repository:
```
https://github.com/marena2004/CoinDash.git
```
2. Navigate to the project directory:
```
cd CoinDash/Code
```
3. Create virtual environment using this command:
```
python -m venv env
```
4. Activate the virtual environment:
On Linux or MacOS
```
source venv/bin/activate
```
On Windows, use:
```
venv\Scripts\activate
```
5. Install the required dependencies:
```
pip install -r requirements.txt
```
6. Run the application:
```
python main.py
```
## Data Source
