# This is a sanity check for myself to help keep track of fleeting thoughts
# TODO:
# - [x] Implement basic maze solver
#   - [x] Implement basic DFS with walls for the first solve
#	- [x] Fix the walls debug print
#	- [x] Rewrite astar to support walls between cells
# - [ ] Fix Cactus logic sometimges attempting to move into locked positions
#	- Seems like the source position is some times locked when bubbling
#	- Perhaps check if bubble move accidentally move into the path of any subsequent bubble moves
# - [ ] Replace field.action with builtins where we do not require field.action benefits
# - [ ] Improve snake with selfpreservation (avoid pathing to apple only to end it all)
# - [ ] Add timing benchmarks to all gathering scripts
# - [ ] Look into polyculture