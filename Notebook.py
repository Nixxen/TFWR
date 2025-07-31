# This is a sanity check for myself to help keep track of fleeting thoughts
# TODO:
# - [x] Implement basic maze solver
#   - [x] Implement basic DFS with walls for the first solve
#	- [x] Fix the walls debug print
#	- [x] Rewrite astar to support walls between cells
# - [x] Fix watering not using decimals. Round up
# - [x] Add timing benchmarks to all gathering scripts
#	- [x] Hay
#	- [x] Wood
#	- [x] Carrot
#	- [x] Pumpkin
#	- [x] Cactus
#	- [x] Bone
#	- [x] Weird Substance
#	- [x] Gold
#	- [x] Power
# - [ ] Replace field.action with builtins where we do not require field.action benefits
#	- [x] Hay
#	- [x] Wood
#	- [x] Carrot
#	- [-] Pumpkin - Required, unsure if could be replaced
#	- [x] Cactus - Some required, though reduce usage where possible
#	- [x] Bone - Already mostly optimized. Improve the remaining
#	- [x] Weird Substance
#	- [-] Gold - Already using limited and quick moves
#	- [x] Power
# - [ ] Optimize water timer, to trigger on an estimated time when the water should be under 0.75 again
#	- [ ] Hay
#	- [ ] Wood
#	- [x] Carrot
#	- [ ] Pumpkin - Could perhaps be only for regrow?
#	- [-] Cactus - Disabled
#	- [-] Bone - Disabled
#	- [x] Weird Substance
#	- [-] Gold - Disabled
#	- [ ] Power
# - [x] Fix Cactus logic sometimes attempting to move into locked positions
#	- Seems like the source position is some times locked when bubbling
#	- Perhaps check if bubble move accidentally move into the path of any subsequent bubble moves
#   - Temporarily solved by skipping the move if the source is locked, potentially leading to a recalculation
# - [ ] Make upgrade selection strategy prioritize baseline costs
# - [ ] Improve snake with selfpreservation (avoid pathing to apple only to end it all)
#   - Also, see if existing pathfinding can be sped up
#   - Also, experiment with static paths, loops and restricted directions
# - [ ] Look into polyculture
# - [ ] Retake timer gains for all scripts that have not reached full upgrades yet
#	- [ ] Cactus
#	- [ ] Bone
#	- [ ] Gold