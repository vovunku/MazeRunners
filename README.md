# MazeRunners
Console version of the game Labyrinth (paper-and-pencil game).

## Table of contents

- [Rules](#rules)
- [How to use?](#how-to-use)
- [How it's organized?](#how-organized)

## Rules
The essence of the game is this: there is a certain field with walls, traps and an exit that only the host knows. The other players secretly give him the coordinates of the starting location. Next, they take turns walking in a maze, and the host tells them whether they have stuck to the wall or managed to pass. In this way, the players explore the map, carefully looking around, thinking about where the traps are located and trying to get to the exit before their opponents. This continues until some player stumbles across the exit, in which case he wins!
### Какие есть клетки
- Stun. A player who comes to this cell skips the next few steps. He is notified of where he has gone and how many moves he will miss.
- Rubber room. The player can leave this cell in only one given direction, known only to the host. If he tries to go in the other direction, he will simply stay where he is, and the host will lie to him boldly that he has made good progress. When the player does go in the right direction, he is told that he has left the rubber room. How long he stayed there is not specified.
- Teleport. The player who comes to this cell is transferred to the cell with the coordinates that are known only to the host. The player is informed that he has been teleported, but not told where. The effect of the cell where he has been teleported does not work.
- Armory. If a player who has come to this cage has less than three bullets (no one has them at the start of the game), the number of bullets in his inventory becomes three. He can now shoot in a given direction. If he hits another player, this player dies, his inventory becomes empty, he goes to his starting point and misses his next move. If the players are standing in the same cell, the shot in either direction is a hit.
- Exit. If a player moves out of that cell in a given direction, he wins. And he is even informed about it.
## How to use?
### Before you start:
You need to clone your project. Next, run **main.py** (when you run it, it will pick up the path to **maps** where the maps will lie). Next we get to the menu. For now, all commands need to be written as suggested (in most cases, the numbers + additional information). Later we will add the possibility to write commands in various formats. To navigate the menu - you only need numbers - 1, 2, 3.
### Game Mode
Here you will be asked to select a card from among the available ones (for this purpose, write its number in the list). After that, you will need to enter the information about the players in succession. Firstly, the number of players is a number, and then the name and three coordinates for each player. Example:  
3  
vovunku 1 1 1  
onaga1958 1 2 2  
demist 1 3 3  
###### The coordinates are set as in the matrix: < map number > < down y-axis coordinates > < axis x-axis coordinates to the right >.
###### e.g. coordinates at the bottom left corner - in 1x3x3 map - 1 3 1
After that, the game will start and a list of possible teams will be displayed. Here, commands are written in lowercase and referrals in uppercase.
###### Important! The move ends automatically as soon as the action points end!
Example:
help  
move DOWN  
shoot RIGHT  
backpack

When the game ends, everything is discarded in the menu.
### Map change mode
there will be two options - to check the map for correctness and add the map to the storage (in both cases the path to the map is required)
An example of checking and adding:  
1 /home/vovun/PycharmProjects/MazeRunners/maps/2.txt  
2 /home/vovun/PycharmProjects/MazeRunners/maps/2.txt  

### Description of maps
Example:  
1  
3 3  
.|S E  
. . _  
S T L  
. . .  
A R .  
E Exit(UP)  
S Stun(2)  
A Armory()  
R RubberRoom(RIGHT)  
L RubberRoom(LEFT)  
T Teleport(0, 0, 2)  

We pass on the necessary parameters to the cell description:
Exit(<DESTINATION>)  
RubberRoom(<DESTINATION>)  
Teleport(<lay>, <x>, <y>) // считая с нуля и через запятую!
Stun(<num>)  

## How it's organized?
Inside, a **MenuFacade** object is created, as well as objects of the **Display** and **Receiver** classes (customization will be available later). The user is then given the option of switching to **GameFacade** and **EditorFacade**. When user chooses **GameFacade**, an object of the corresponding type is created and initialized according to user data.  Inside **GameFacade**, a game cycle is started in which users enter commands. Commands are received by the corresponding **Player** class object. Then, using the **GameVisitor**, commands for the corresponding player are processed (note that commands come not only from the player, but also from the game environment, those of **Cell** and **Board** class objects). In this way, the game process becomes a step-by-step execution and entry of commands. When user switches to **EditorFacade**, the object of this type is also created and the user is given the opportunity to use MapManager and MapEditor (methods for checking/reading/adding cards are implemented in them).
### 1. Input, output - receiver display 
Implementation of **Bridge** pattern, in order to be able to further extend its functionality. Now they can exchange either lines or commands from the corresponding block.
### 2. menu_facade
This is the facade of the facades. It will provide access to other facades (and correctly initialise them accordingly) as the user wishes.
### 3. Game client - game_facade
Implementation of **Facade** pattern, to provide limited functionality and to implement interaction between users and their virtual players and the game in general.
### 4. Playing field - Board
Implementation of cell storage and the interaction of the environment with the totality of cells. Also implements some features (for example, shooting).
### 5. Player
Represents some storage of information for each player. They log the commands and also implement the internal logic of the players. You can inherit from players to add individual behaviours depending on the type.
### 6. Cell
Implementation of the main facilities in the game. Implementation of the **Factory method** pattern, since the basic functionality of all cells is the same (look, interact, move). We use **Command** pattern to transfer information from the cells to the objects (this way we can log the player's actions and separate the implementations of cells and players)
### 7. Commands - Command
The whole game process is based on it. With the help of it, the player changes, depending on his actions. They are placed in the player's command queue, which is later processed by **Visitor**. The commands make the process more flexible and make the course of the game consistent. There are commands to interact with the board, commands from the player, etc.
### 8. Facade of adding maps - editor_facade, который за собой тянет map_manager и map_editor
Knows how to get cards from storage, and add them there. When added, it makes a small check for correctness by the bfs, and in case of error displays from which cell it was not possible to reach the exit. It is also possible to simply check the map.
### 9. Storage of maps (map_manager)
Отдельные файл(ы) и класс, который работает с этим хранилищем - проверяет, добавляет и удаляет карты.
### 10. map_editor
Implements map validation and reading.
### 11. Handler - game_visitor
Implementation of the **Visitor** pattern. Allows you to separate the execution of commands and notifying the user about game events. Runs in game_facade and works with the player's command queue.
### 12. Strategy - move_strategy
Since the game can move in 4 directions, the **Strategy** pattern is implemented. Allows to unify movement / shooting / logic of cells.
