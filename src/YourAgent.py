# Custom imports to assist in interfacing with the simulator
from src.DriveInterface import DriveInterface
from src.DriveState import DriveState
from src.Constants import DriveMove, SensorData


class YourAgent(DriveInterface):

    def __init__(self, game_id: int, is_advanced_mode: bool):
        """
        Constructor for YourAgent

        Arguments:
        game_id -- a unique value passed to the player drive, you do not have to do anything with it, but will have access.
        is_advanced_mode -- boolean to indicate if 
        """
        self.game_id  = game_id
        self.need_to_find_target_pod = is_advanced_mode
        self.path = []
        self.field_limits = []
        self.path_move_index = 0
        
    def will_next_state_collide(self, state: DriveState, sensor_data: dict) -> bool:
        # Not implemented yet
        return False

    def get_move_for_next_state_in_path(self) -> DriveMove:
        # Function to find the move which will get the player to the next state in self.path
        current_state = self.path[self.path_move_index]
        self.path_move_index += 1
        next_state = self.path[self.path_move_index]

        for move in DriveMove:
            if current_state.get_next_state_from_move(move) == next_state.to_tuple():
                return move, next_state

        print('WARN next move could not be found')
        return DriveMove.NONE, next_state


    def list_all_next_possible_states(self, state: DriveState) -> list[int]:
        # Returns a list of all reachable states from the argument state by iterating over all possible drive moves
        next_states = []
        for move in DriveMove:
            x, y = state.get_next_state_from_move(move)
            next_states.insert(0, DriveState(x=x, y=y))

        return next_states

    def is_state_in_bounds(self, state: DriveState, sensor_data: dict) -> bool:
        # Checks if state argument is not a field wall
        return [state.x, state.y] not in sensor_data[SensorData.FIELD_BOUNDARIES]

    def is_player_drive_carrying_a_pod(self, sensor_data: dict) -> bool:
        # Checks if player game id is the first value in any of the entries in SensorData.DRIVE_LIFTED_POD_PAIRS
        return self.game_id in [drive_pod_pair[0] for drive_pod_pair in sensor_data[SensorData.DRIVE_LIFTED_POD_PAIRS]]
            


    def dfs_solve_path_to_goal(self, sensor_data: dict, goal: list[int]):
        # Depth First Search solver to find a path between SensorData.PLAYER_LOCATION and the goal argument
        # Stores solved path as a list of DriveState(s) in the self.path variable
        start_state = sensor_data[SensorData.PLAYER_LOCATION]

        new_states = [DriveState(x=start_state[0], y=start_state[1])]
        visited_states = set([])
        paths = [[new_states[0]]]

        while len(paths) > 0:
            current_path = paths.pop(len(paths)-1)
            curr_state = current_path[-1]
            if curr_state.x == goal[0] and curr_state.y == goal[1]:
                self.path = current_path
                return

            visited_states.add(curr_state)
            
            for state in self.list_all_next_possible_states(curr_state):
                if state not in visited_states and self.is_state_in_bounds(state, sensor_data):
                    paths.append(current_path + [state])

        print('WARN Could not find solution from DFS solver')

    # This is the main function the simulator will call each turn 
    def get_next_move(self, sensor_data: dict) -> DriveMove:
        """
        Main function for YourAgent. The simulator will call this function each loop of the simulation to see what your agent's
        next move would be. You will have access to data about the field, your robot's location, other robots' locations and more
        in the sensor_data dict arguemnt.

        Arguments:
        sensor_data -- a dict with state information about other objects in the game. The structure of sensor_data is shown below:
            sensor_data = {
                SensorData.FIELD_BOUNDARIES: [[-1, -1], [-1, 0], ...],  
                SensorData.DRIVE_LOCATIONS: [[x1, y1], [x2, y2], ...], 
                SensorData.POD_LOCATIONS: [[x1, y1], [x2, y2], ...],
                SensorData.PLAYER_LOCATION: [x, y],
                SensorData.GOAL_LOCATION: [x, y], (Advanced Mode)
                SensorData.TARGET_POD_LOCATION: [x, y], # Only used for Advanced mode
                SensorData.DRIVE_LIFTED_POD_PAIRS: [[drive_id_1, pod_id_1], [drive_id_2, pod_id_2], ...] (Only used in Advanced mode for seeing which pods are currently lifted by drives)

            }

        Returns:
        DriveMove - return value must be one of the enum values in the DriveMove class:
            DriveMove.NONE – Do nothing
            DriveMove.UP – Move 1 tile up (positive y direction)
            DriveMove.DOWN – Move 1 tile down (negative y direction)
            DriveMove.RIGHT – Move 1 tile right (positive x direction)
            DriveMove.LEFT – Move 1 tile left (negative x direction)
            
            (Advanced mode only)
            DriveMove.LIFT_POD – If a pod is in the same tile, pick it up. The pod will now move with the drive until it is dropped
            DriveMove.DROP_POD – If a pod is in the same tile, drop it. The pod will now stay in this position until it is picked up

        """
        raise Exception('get_next_move in YourAgent not implemented')

