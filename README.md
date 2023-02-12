## Color bottles puzzle

 🌡️ Watter color sort puzzle game 🧪

### Install and play:
```
pip install color-bottles-puzzle

color-bottles
```

### 📈 Objective
Make bottles full with one color or empty -> 📊

### 📌 Rules
You can pour color water from one bottle to another only if destination bottle is not full, is empty or have same color on top.
 
## 🕹️ Controls (Console frontend)
To pour from bottle `3` to bottle `7` just type `3 7` and enter.  
If number of bottles less then 10, you can ommit the space 💥   
Also you can pour multiple times by 1 hit 🔥 - just type in a row 
like `5718` or `5 7 1 8` - will pour `5` to `7` and then `1` to `8`   
🔴 To exit - type `q`   
🔮 Good luck !!  

Examples of a game (monospaced font in console work just fine):

```
🔮 Good luck !!


    |⬛️|    |🟦|    |⬛️|    |🟧|    |🟫|    |🟩|    |🟪|    |  |    |  |  
    |⬛️|    |🟩|    |🟫|    |🟪|    |🟩|    |🟥|    |🟫|    |  |    |  |  
    |🟧|    |🟫|    |🟥|    |🟧|    |🟧|    |🟪|    |🟦|    |  |    |  |  
    |🟩|    |🟥|    |🟦|    |🟥|    |⬛️|    |🟪|    |🟦|    |  |    |  |  
      0       1       2       3       4       5       6       7       8

 🎮 your turn:  0 7   2 7   3 0   4 2   5 4   6 3

    |  |    |🟦|    |🟫|    |🟪|    |🟩|    |  |    |  |    |  |    |  |  
    |🟧|    |🟩|    |🟫|    |🟪|    |🟩|    |🟥|    |🟫|    |⬛️|    |  |  
    |🟧|    |🟫|    |🟥|    |🟧|    |🟧|    |🟪|    |🟦|    |⬛️|    |  |  
    |🟩|    |🟥|    |🟦|    |🟥|    |⬛️|    |🟪|    |🟦|    |⬛️|    |  |  
      0       1       2       3       4       5       6       7       8

 🎮 your turn:  6 8   2 8   5 2   3 5 

    |  |    |🟦|    |  |    |  |    |🟩|    |🟪|    |  |    |  |    |  |  
    |🟧|    |🟩|    |🟥|    |  |    |🟩|    |🟪|    |  |    |⬛️|    |🟫|  
    |🟧|    |🟫|    |🟥|    |🟧|    |🟧|    |🟪|    |🟦|    |⬛️|    |🟫|  
    |🟩|    |🟥|    |🟦|    |🟥|    |⬛️|    |🟪|    |🟦|    |⬛️|    |🟫|  
      0       1       2       3       4       5       6       7       8

 🎮 your turn:  

```

### Frontend

There is a `core` module (water sort rules logic) of color bottles that is frontend agnostic.
Thats why we have 2 frontends for now 
 1. `console` - using `print()` - default
 2. `pygame` - using pygame GUI 

To run game with pygame GUI, install package with pygame extras:
```
python3 -m venv env
source env/bin/activate
pip install "color-bottles-puzzle[pygame]"

color-bottles
```

### Roadmap
 - [ ] Test for game logic
 - [ ] Test console game
 - [ ] Solver
 - [ ] Levels
 - [ ] More frontend
 - [ ] Github actions CI