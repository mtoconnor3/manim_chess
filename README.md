# Manim Chess
A project combining the power of Manim visualizations with the `python-chess` api. This is a work in progress with fuzzy goals. 

# Setup
To set up a local virtualenv, you can use the included makefile. Ensure that you've got `cmake` and `git` installed. 

```
> git clone https://github.com/mtoconnor3/manim_chess.git
> cd manim_chess
> make 
> source .manimchess/bin/activate
```

# Running the example
At the moment, the scene is congigured to animate Morphy's Operat, which is stored in a PGN file in the `assets/` directory. To generate the animation, you can submit it to manim with the following command: 

```
> manim -sq manim_chess.py ChessScene
```

This will produce an .mp4 file in the `media/` subfolder

To change which game is animated, point the scene at a different PGN file in the `assets/` directory.