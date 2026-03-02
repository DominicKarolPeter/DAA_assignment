"""
Backtracking Strategy
Backtracking in Flood means looking ahead several moves and undoing/reconsidering choices that don't lead to efficient progress. Here's how to apply it:
1. Go Deep, Not Wide
It's wise to go "deep" — select the colour which takes you furthest into the unflooded territory. OSS Blog Don't just pick the colour that absorbs the most adjacent squares; pick the one that opens up the longest path into new regions.
2. Plan Sequences, Not Single Moves
Instead of evaluating one move at a time, mentally (or on paper) plan 3–5 moves ahead. Ask: "If I pick red now, what colours does that unlock next?"
3. Identify "Bottleneck" Colours
Some colours act as bridges to large regions. Delay or avoid wasting moves on colours that are isolated or small — save those for when they connect two large blobs.
4. Backtrack When You Hit a Dead End
If you've used several moves and the flooded region grew slowly, undo (Ctrl+Z) back to the branching point and try the alternative colour sequence. The game supports undo, so use it freely to explore branches.
5. Prioritise the Perimeter
Work toward the farthest corners early. The bottom-right corner is hardest to reach last, so try to connect to distant regions before mopping up nearby ones.
6. Avoid Colour Repetition
Consecutive moves of the same colour are almost always wasted (since you already absorbed all that colour's neighbours). Backtrack if you find yourself cycling through the same colours without gaining ground.
7. Count Remaining Colours
Near the end, count how many distinct colour regions remain and compare to your remaining moves. If the numbers don't match up, backtrack earlier to find a more efficient path.
"""