# Roguelike Game

by Isaac Young

## Description

To create a text-based rogue-like game was the goal of my project.
A game where you could fight monsters, pick up items, encounter traps based on
your respective actions. The monsters are taken from dungeons and dragons and their
respective dice rolls are in accordance with their statistics.


## How to test

There should be no set-up needed. You should only need to run rogueGameWDice.py
and the JSON file should automatically be loaded. If the monsters/items/traps data need to edited or if want to add
additional, the JSON file can be edited.  
If you click the leaderboard button, it should lead list the leaderboard.  
If you click the inventory button, it should display your inventory with all items picked up with the options to either use the item if the item is usable or to drop the item.  
If you click action scenario buttons and then click the submit command button, it should lead to the that specific action/scenario.  
If you encounter a monster, you can either attack or run away from the monster. Damage is calculated with imaginary dice rolls.  
If you encounter a trap, you automatically attempt to evade it. If the evation fails, then the damage is calculated with imaginary dice rolls.  
If you encounter an item, you can either pick up the item if you have inventory space or choose not to pick up the item.

## Personal contribution

All python files (rogueGameWDice.py) and json files (encountersWDice.json) were my personal contribution. 