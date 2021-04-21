# Hungry Sharks the Game Notes

## MVC Architecture thoughts

### Model

- The "map"
- Stores all "characters"
  - each character is an instance of a character class
- Handles interaction between characters
- Handle character motion
  - Update characters' positions and velocities

### View

- Draws the map and characters
- ![text](images/model.jpg)
- Draws what the player sees

### Controller

- "keyboard controller"
  - takes mouse/keyboard input from the player and controls the their character
- AI controller
  - Responds to the AI character's distance from the player
  - Has a random choice of behavior pattern
    - Small/dumb
    - Small/smart
    - Large/passive
    - Large/aggressive

## Character Class

### Every character has:

- Attributes
  - Size
  - Position
  - Kinematics
    - Velocity
    - Maybe Acceleration

### AI character inherits from Character and has:

- Attributes
  - Observation radius
  - Behavior pattern

### Player's Character inherits from Character and has:

- Attributes
  - 
  