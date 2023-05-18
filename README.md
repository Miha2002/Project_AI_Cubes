# Project Artificial Inteligence - Cubes

The input data for the program looks something like this:

![input_img](https://github.com/Miha2002/Project_AI_Cubes/assets/81815165/9226e45f-178a-41c7-963a-9419a68def7a)

This represents cubes/blocks with different colors and numbers stacked on each other, creating columns. The endgoal is to have all the top blocks the same color.
This color is specified on the first line of the file.

The blocks can be moved around, but there are some rules:
- The blocks cannot be moved on a block with the same color
- If after moving a block we have a cube of a color between 2 cubes of the same color, then the one in the middle changes colors.
e.g. 9[a]/3[r]/15[a]   =>   9[a]/3[a]/15[a]

- Each move has a cost based on the cube's assigned number. The program tries to get that cost number as low as possible, meaning as few moves as possible.
- At the end of the permutations, all columns must contain at least one cube.
