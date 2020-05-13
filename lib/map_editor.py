import lib.cell as cell
import lib.game as game
from queue import Queue


# это ужас, подскажите, пожалуйста, как это чудо переделать

class MapEditor:
    """Module between map manager and other modules"""

    def read_map(self, raw_map):
        maps_count = int(raw_map[0])
        types_gen = self.get_types(raw_map)
        file_it = 1
        shift_for_teleports = []
        game_map = []
        for t in range(maps_count):
            game_map.append([])

            # set game_map with cells
            rows, cols = map(int, raw_map[file_it].split(' '))
            for i in range(rows):
                game_map[t].append([])
                for j in range(cols):
                    cell_id = raw_map[file_it + 1 + 2 * i][2 * j]
                    new_cell = self.create_cell(types_gen[cell_id][0], types_gen[cell_id][1])
                    game_map[t][i].append(new_cell)
                    new_cell.set_coords(t, i, j)
                    if types_gen[cell_id][0] == "Teleport":
                        shift_for_teleports.append([[t, i, j], types_gen[cell_id][2]])  # [from, to]

            # set row siblings
            for i in range(rows):
                for j in range(cols - 1):
                    self.set_row_siblings(game_map[t][i][j],
                                          game_map[t][i][j + 1],
                                          raw_map[file_it + 1 + 2 * i][2 * j + 1])

            # set col siblings
            for i in range(rows - 1):
                for j in range(cols):
                    self.set_col_siblings(game_map[t][i][j],
                                          game_map[t][i + 1][j],
                                          raw_map[file_it + 1 + 2 * i + 1][2 * j])

            file_it += 2 * rows - 1

        for shift in shift_for_teleports:
            (game_map[shift[0][0]]
                     [shift[0][1]]
                     [shift[0][2]]).set_shift_destination(game_map[shift[1][0]]
                                                                  [shift[1][1]]
                                                                  [shift[1][2]])

        return game_map

    def create_cell(self, cell_type, *args):  # [0] - type specific; ?[1] - items
        if cell_type == "Empty":
            return cell.Empty()
        elif cell_type == "Stun":
            return cell.Stun(args[0])  # duration
        elif cell_type == "RubberRoom":
            return cell.RubberRoom(args[0])  # exit_destination
        elif cell_type == "Teleport":
            return cell.Teleport(args[0])  # shift_destination
        elif cell_type == "Armory":
            return cell.Armory()
        elif cell_type == "Exit":
            return cell.Exit(args[0])  # exit_destination

    def get_types(self, raw_map):  # needed to be rewritten and probably transferred in another module
        maps_count = int(raw_map[0])
        map_it = 1
        while maps_count > 0:
            skip = int(raw_map[map_it][0])
            map_it += skip * 2
            maps_count -= 1
        types_gen = {}
        while map_it < len(raw_map):
            type_inp = raw_map[map_it]
            op = type_inp.find('(')
            cl = type_inp.find(')')
            if "Teleport" in type_inp:
                coords = list(map(int, type_inp[op + 1: cl].split(" ")))
                for i in range(3):
                    coords[i] -= 1
                types_gen[type_inp[0]] = [type_inp[2: op], None, coords]
            elif "RubberRoom" in type_inp or "Exit" in type_inp:
                types_gen[type_inp[0]] = [type_inp[2: op], type_inp[op + 1: cl]]
            elif "Stun" in type_inp:
                types_gen[type_inp[0]] = [type_inp[2: op], int(type_inp[op + 1: cl])]
            else:
                types_gen[type_inp[0]] = [type_inp[2: op], None]
            map_it += 1
        types_gen['.'] = ["Empty", None]
        return types_gen

    def set_row_siblings(self, left, right, divider):
        if divider == " ":
            left.right = right
            right.left = left

    def set_col_siblings(self, up, down, divider):
        if divider == ".":
            up.down = down
            down.up = up

    def bfs_check_cell(self, lay, x, y, dest_lay, dest_x, dest_y, game_map):
        visited = []
        for l, layer in enumerate(game_map):
            visited.append([])
            for row in layer:
                visited[l].append([False for _ in range(len(row))])
        pool = Queue()
        pool.put(game_map[lay][x][y])
        while not pool.empty():
            cur_cell = pool.get()
            visited[cur_cell.lay][cur_cell.x][cur_cell.y] = True
            neighbours = cur_cell.get_accessible()
            for next_cell in neighbours:
                if not visited[next_cell.lay][next_cell.x][next_cell.y]:
                    pool.put(next_cell)

        if not visited[dest_lay][dest_x][dest_y]:
            return [lay, x, y]
        return None

    def bfs_check_map(self, exit_cell, game_map):
        ans = []
        for l, layer in enumerate(game_map):
            for x, row in enumerate(layer):
                for y, checked in enumerate(row):
                    problematic_cell = self.bfs_check_cell(l, x, y, exit_cell.lay, exit_cell.x, exit_cell.y, game_map)
                    if problematic_cell is not None:
                        return problematic_cell
        return None

    def check_map(self, game_map):
        exit_cell = None
        for lay in game_map:
            for row in lay:
                for unit in row:
                    if type(unit).__name__ == "Exit":
                        exit_cell = unit
        if exit_cell is None:
            raise ImportError("No Exit")
        return self.bfs_check_map(exit_cell, game_map)
