import loglevel

loglevel = loglevel.information
base_operation_time = 2.5 #ms
action_cost = 200 # ticks
speed_upgrades = 20 # action cost reduction - TODO: Figure out how to read this dynamically
action_time = (base_operation_time * action_cost / speed_upgrades) / 1000 # s
world_size = get_world_size()
valid_plant_items = [
Items.Hay,
Items.Wood,
Items.Carrot,
Items.Pumpkin,
Items.Cactus,
Items.Bone,
Items.Power
]
