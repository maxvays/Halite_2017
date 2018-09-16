# Final version for Halite II (mwizard777)
import hlt
from hlt.entity import Position
import logging
import time
import math
import pathfinding
from pathfinding import finder
from pathfinding import core
from pathfinding.core.node import Node
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.

game = hlt.Game("Settler")
# Then we print our start message to the logs
logging.info("Starting my Settler bot!")

initMap = game.initial_map
# scale = 1
# mArray = initMap.makeMap(scale=scale)
# logging.info(mArray)
# grid = Grid(math.floor(initMap.width/scale), math.floor(initMap.height/scale), mArray)
# grid2 = Grid(5,4,[[0,0,0,0,0],[1,1,0,1,1],[0,0,0,1,0],[0,1,0,0,0]])
# starFinder = AStarFinder()
# path = starFinder.find_path(grid2.node(0,0), grid2.node(4,2), grid2)
# logging.info(path)
# shipPaths = [None] * 500

# logging.info("hi")

while True:
	# TURN START
	# Update the map for the new turn and get the latest version
	game_map = game.update_map()

	# Here we define the set of commands to be sent to the Halite engine at the end of the turn
	command_queue = []

	start = time.time()
	end = time.time()
	# For every ship that I control
	# for planet in game_map.all_planets():
	#     if planet.owner == game_map.get_me:
	# for planet in game_map.get_me.all_planets():
	#     entbydist = game_map.nearby_entities_by_distance(ship)
	#     for i in range(0,len(entbydist)):
	#         if entbydist[i].class == Ship:

	if len(game_map._players) == 4:
		for ship in game_map.get_me().all_ships():
			# If the ship is docked
			end = time.time()
			if (end - start > 1.75):
				break
			if ship.docking_status != ship.DockingStatus.UNDOCKED:
				# Skip this ship
				continue

			entities_by_distance = game_map.nearby_entities_by_distance(ship)
			nearest_planet = None
			for distance in sorted(entities_by_distance):
				nearest_planet = next((nearest_entity for nearest_entity in entities_by_distance[distance] if isinstance(nearest_entity, hlt.entity.Planet)), None)
				if nearest_planet and not nearest_planet.is_owned():
					break
				else:
					if nearest_planet and (nearest_planet.owner.id != game_map.get_me().id or (nearest_planet.owner == game_map.get_me() and not nearest_planet.is_full())):
						break

			if nearest_planet:
				if ship.can_dock(nearest_planet):
					# We add the command by appending it to the command_queue
					command_queue.append(ship.dock(nearest_planet))
				else:
					lstShips = nearest_planet.all_docked_ships()
					if nearest_planet.is_owned():
						if  nearest_planet.owner != game_map.get_me():
							if len(lstShips) == 0:
								navigate_command = ship.navigate(
								    ship.closest_point_to(nearest_planet),
								    game_map,
								    speed=int(hlt.constants.MAX_SPEED),
								    ignore_ships=False)
								# if not shipPaths[ship.id]:
								# 	logging.info(math.floor(ship.y/scale))
								# 	logging.info(math.floor(ship.x/scale))
								# 	logging.info(math.floor(nearest_planet.y/scale))
								# 	logging.info(math.floor(nearest_planet.x/scale))
								# 	path, runs = starFinder.find_path(
								# 		grid.node(math.floor(ship.y/scale), math.floor(ship.x/scale)),
								# 		grid.node(math.floor(nearest_planet.y/scale), math.floor(nearest_planet.x/scale)),
								# 		grid)
								# 	logging.info(path)
								# 	logging.info(runs)
								# 	shipPaths[ship.id] = path
								# 	navigate_command = ship.move(shipPaths[ship.id], scale)
								# 	shipPaths[ship.id] = shipPaths[ship.id].pop(0)
								# else:
								# 	navigate_command = ship.move(shipPaths[ship.id], scale)
								# 	shipPaths[ship.id] = shipPaths[ship.id].pop(0)
								logging.info("1")
							else:
								closestShip = None
								minDist = 500
								for ship1 in lstShips:
									newDist = ship.calculate_distance_between(ship1)
									if newDist < minDist:
										closestShip = ship1
										minDist = newDist
								navigate_command = ship.navigate(
									ship.closest_point_to(closestShip),
									game_map,
									speed=int(hlt.constants.MAX_SPEED),
									ignore_ships=False)
								# if ship.calculate_distance_between(nearest_planet) > 12:
								# 	navigate_command = ship.navigate(
								# 		ship.closest_point_to(nearest_planet),
								# 		game_map,
								# 		speed=int(hlt.constants.MAX_SPEED),
								# 		ignore_ships=False)
								# else:
								# 	ship1 = lstShips[0]
								# 	# angle = ship1.calculate_angle_between(nearest_planet)
								# 	# closePoint = Position((ship1.x - 5*math.cos(math.radians(angle))), (ship1.y - 5*math.sin(math.radians(angle))))
								# 	# logging.info(ship1.x)
								# 	# logging.info(ship1.y)
								# 	# logging.info(closePoint)
								# 	# logging.info(nearest_planet)
								# 	navigate_command = ship.navigate(
								# 	    ship.closest_point_to(ship1),
								# 	    game_map,
								# 	    speed=int(hlt.constants.MAX_SPEED),
								# 	    ignore_ships=False)
								# else:
								# 	# angle = nearest_planet.calculate_angle_between(ship) + 30
								# 	# targ = Position(nearest_planet.x + (nearest_planet.radius + 4)*math.cos(math.radians(angle)), nearest_planet.y + (nearest_planet.radius + 4)*math.sin(math.radians(angle)))
								# 	# navigate_command = ship.navigate(
								# 	#     targ,
								# 	#     game_map,
								# 	#     speed=int(hlt.constants.MAX_SPEED),
								# 	#     ignore_ships=False)
								# 	ang = ship.calculate_angle_between(nearest_planet) + 90
								# 	navigate_command = ship.thrust(5, ang)
								# 	logging.info("moving around")
								# if not shipPaths[ship.id]:
								# 	logging.info(math.floor(ship.y/scale))
								# 	logging.info(math.floor(ship.x/scale))
								# 	logging.info(grid.node(math.floor(ship.x/scale), math.floor(ship.y/scale)).walkable)
								# 	logging.info(math.floor(ship1.y/scale))
								# 	logging.info(math.floor(ship1.x/scale))
								# 	logging.info(grid.node(math.floor(ship1.x/scale), math.floor(ship1.y/scale)).walkable)
								# 	logging.info("a")
								# 	path, runs = starFinder.find_path(
								# 		grid.node(math.floor(ship.y/scale), math.floor(ship.x/scale)),
								# 		grid.node(math.floor(ship1.y/scale), math.floor(ship1.x/scale)),
								# 		grid)
								# 	logging.info(path)
								# 	logging.info(runs)
								# 	shipPaths[ship.id] = path
								# 	navigate_command = ship.move(shipPaths[ship.id], scale)
								# 	shipPaths[ship.id].pop(1)
								# else:
								# 	navigate_command = ship.move(shipPaths[ship.id], scale)
								# 	shipPaths[ship.id].pop(1)
								logging.info("2")
						else:
							navigate_command = ship.navigate(
								ship.closest_point_to(nearest_planet),
								game_map,
								speed=int(hlt.constants.MAX_SPEED),
								ignore_ships=False)
							logging.info("3")
					else:
						navigate_command = ship.navigate(
						   ship.closest_point_to(nearest_planet),
						   game_map,
						   speed=int(hlt.constants.MAX_SPEED),
						   ignore_ships=False)
						# if not shipPaths[ship.id]:
						# 	logging.info(math.floor(ship.y/scale))
						# 	logging.info(math.floor(ship.x/scale))
						# 	logging.info(grid.node(math.floor(ship.x/scale), math.floor(ship.y/scale)).walkable)
						# 	logging.info(math.floor(nearest_planet.y/scale))
						# 	logging.info(math.floor(nearest_planet.x/scale))
						# 	logging.info(grid.node(math.floor(nearest_planet.x/scale), math.floor(nearest_planet.y/scale)).walkable)
						# 	logging.info("b")
						# 	path, runs = starFinder.find_path(
						# 		grid.node(math.floor(ship.y/scale), math.floor(ship.x/scale)),
						# 		grid.node(math.floor(nearest_planet.y/scale), math.floor(nearest_planet.x/scale)),
						# 		grid)
						# 	logging.info(path)
						# 	logging.info(runs)
						# 	shipPaths[ship.id] = path
						# 	navigate_command = ship.move(shipPaths[ship.id], scale)
						# 	shipPaths[ship.id].pop(1)
						# else:
						# 	navigate_command = ship.move(shipPaths[ship.id], scale)
						# 	shipPaths[ship.id].pop(1)
						# #if not shipPaths[ship.id]:
						#    path = starFinder.find_path(grid.node(math.floor(ship.x/2),math.floor(ship.y/2)),grid.node(math.floor(nearest_planet.x/2),math.floor(nearest_planet.y/2)))
						#    shipPaths[ship.id] = path
						#    navigate_command = ship.move(shipPaths[ship.id])
						#    shipPaths[ship.id] = pop(shipPaths[ship.id],0)
						#else:
						#    navigate_command = ship.move(shipPaths[ship.id])
						#    shipPaths[ship.id] = pop(shipPaths[ship.id],0)
						logging.info("4")
					# If the move is possible, add it to the command_queue (if there are too many obstacles on the way
					# or we are trapped (or we reached our destination!), navigate_command will return null;
					# don't fret though, we can run the command again the next turn)
					logging.info(navigate_command)
					if navigate_command is None:
						angle = nearest_planet.calculate_angle_between(ship)
						navigate_command = ship.thrust(7, angle)
						logging.info("navigate command set")
					if navigate_command:
						command_queue.append(navigate_command)
						#logging.info("5")

		# Send our set of commands to the Halite engine for this turn
		game.send_command_queue(command_queue)
		# TURN END
	else:
		myShips = game_map.get_me().all_ships()
		for ship in myShips:
			# If the ship is docked
			end = time.time()
			if (end - start > 1.75):
				break
			if ship.docking_status != ship.DockingStatus.UNDOCKED:
				# Skip this ship
				continue
			entities_by_distance = game_map.nearby_entities_by_distance(ship)
			nearest_planet = None
			for distance in sorted(entities_by_distance):
				nearest_planet = next((nearest_entity for nearest_entity in entities_by_distance[distance] if isinstance(nearest_entity, hlt.entity.Planet)), None)
				if nearest_planet and nearest_planet.is_owned():
					if nearest_planet.owner.id != game_map.get_me().id:
						break
			if nearest_planet:
				lstShips = nearest_planet.all_docked_ships()
				if len(lstShips) == 0:
					navigate_command = ship.navigate(
						ship.closest_point_to(nearest_planet),
						game_map,
						speed=int(hlt.constants.MAX_SPEED),
						ignore_ships=False)
					# if not shipPaths[ship.id]:
					# 	logging.info(math.floor(ship.y/scale))
					# 	logging.info(math.floor(ship.x/scale))
					# 	logging.info(math.floor(nearest_planet.y/scale))
					# 	logging.info(math.floor(nearest_planet.x/scale))
					# 	path, runs = starFinder.find_path(
					# 		grid.node(math.floor(ship.y/scale), math.floor(ship.x/scale)),
					# 		grid.node(math.floor(nearest_planet.y/scale), math.floor(nearest_planet.x/scale)),
					# 		grid)
					# 	logging.info(path)
					# 	logging.info(runs)
					# 	shipPaths[ship.id] = path
					# 	navigate_command = ship.move(shipPaths[ship.id], scale)
					# 	shipPaths[ship.id] = shipPaths[ship.id].pop(0)
					# else:
					# 	navigate_command = ship.move(shipPaths[ship.id], scale)
					# 	shipPaths[ship.id] = shipPaths[ship.id].pop(0)
					logging.info("1")
				else:
					closestShip = None
					minDist = 500
					for ship1 in lstShips:
						newDist = ship.calculate_distance_between(ship1)
						if newDist < minDist:
							closestShip = ship1
							minDist = newDist
					navigate_command = ship.navigate(
						ship.closest_point_to(closestShip),
						game_map,
						speed=int(hlt.constants.MAX_SPEED),
						ignore_ships=False)
			else:
				if game_map._players[0] == game_map.get_me():
					enemy = game_map._players[1]
				else:
					enemy = game_map._players[0]
				minDist = 500
				closestShip = None
				for eship in enemy.all_ships():
					if ship.calculate_distance_between(eship) < minDist:
						closestShip = eship
						minDist = ship.calculate_distance_between(eship)
				navigate_command = ship.navigate(
					ship.closest_point_to(closestShip),
					game_map,
					speed=int(hlt.constants.MAX_SPEED),
					ignore_ships=True)
			logging.info(navigate_command)
			lstShips1 = game_map.get_me().all_ships()
			minDist = 400
			for ship1 in lstShips1:
				newDist = ship.calculate_distance_between(ship1)
				if newDist < minDist:
					closestShip1 = ship1
					minDist = newDist
			if ship.calculate_distance_between(closestShip1) < 30 and (ship.x > closestShip1.x or ship.y > closestShip1.y):
				navigate_command = ship.navigate(
					ship.closest_point_to(closestShip1),
					game_map,
					speed=int(0),
					ignore_ships=False)
			if navigate_command:
				navigate_command = navigate_command[:2] + "{}".format(ship.id) + navigate_command[3:]
				logging.info(navigate_command)
				command_queue.append(navigate_command)
		game.send_command_queue(command_queue)
# GAME END
