#!/usr/bin/python3
# TODO: make it work with colors
import curses
import argparse
import math
import os
import sys
from copy import deepcopy
from math import cos, sin
from pprint import pprint

from symbols import symbols


class Cube:

    def __init__(self, s=17, color="white"):
        COLORS = {
            "black": curses.COLOR_BLACK,
            "white": curses.COLOR_WHITE,
            "magenta": curses.COLOR_MAGENTA,
            "blue": curses.COLOR_BLUE,
            "green": curses.COLOR_GREEN,
            "red": curses.COLOR_RED
        }
        self.rotation = -15
        self.s = s
        self.screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, COLORS[color], curses.COLOR_BLACK)

        while 1:
            try:
                self.rotate_and_print()
            except KeyboardInterrupt:
                curses.endwin()
                sys.exit()

    def rotate_and_print(self):
        self.cube = Cube.create_cube(self.s)
        self.cube = self.write_cube(self.cube)
        inc = 3
        new_points = self.rotate(
            self.rotation + inc, self.rotation + inc, self.rotation + inc
        )
        self.cube = Cube.create_cube(self.s)
        self.write_new_points(new_points)
        self.connect_all()
        proyection = self.proyect_with_depth()
        proyection = Cube.get_proyection_string(proyection)
        self.window_print(proyection)

    def window_print(self, proyection):
        self.screen.clear()
        self.screen.addstr(proyection, curses.color_pair(1))
        self.screen.refresh()
        curses.napms(1)

    def create_cube(s):
        return [[[0 for _ in range(s)] for _ in range(s)] for _ in range(s)]

    def write_cube(self, cube):
        s = self.s / 2  # Maybe this needs a round
        long = math.ceil(int(s / 2 + s))
        short = math.floor(int(s / 2))
        # long = round(int(s / 2 + s))
        # short = round(int(s / 2))

        cube[short][short][short] = 1

        cube[long][short][short] = 1
        cube[long][long][short] = 1
        cube[long][long][long] = 1

        cube[short][long][short] = 1
        cube[short][long][long] = 1

        cube[short][short][long] = 1
        cube[long][short][long] = 1
        return cube

    def write_new_points(self, points):
        for point in points:
            x, y, z = point
            try:
                self.cube[z][y][x] = 1
            except IndexError:
                continue

    def print_rows(cube):
        pprint(cube)

    def find_3_smallest(point, points):
        i = 0
        points = list(points)
        x, y, z = point
        distances = []
        for p in points:
            x1, y1, z1 = p
            a = [x1 - x, y1 - y, z1 - z]
            distance = list(map(abs, a))
            distance = sum(distance)
            if distance == 0:
                continue
            for i in range(3):
                if len(distances) < 3:
                    # results.append(p)
                    distances.append((distance, p))
                    break

                if distance < distances[i][0]:
                    # results.pop(i)
                    # results.insert(i, p)
                    distances.pop()
                    distances.insert(i, (distance, p))
                    break
                distances.sort(key=lambda x: x[0])

        results = [x[1] for x in distances]
        assert len(results) == 3
        return results

    def connect3d(point1, point2, new_point):
        # Formula new_point = point1 + t * point2
        x, y, z = new_point
        # TODO: rewrite this is ugly
        if (
            (x != None and y != None)
            or (x != None and z != None)
            or (y != None and z != None)
            or (x == None and y == None and z == None)
        ):
            raise ValueError("There must only be one known value")

        for i in range(len(new_point)):
            if new_point[i] != None:
                a = i
        # If a 0 its x, if 1 its y, if its 2 z

        # a = x if x not None else y if y not None else z
        result = [0, 0, 0]
        b = (a + 1) % 3
        c = (a + 2) % 3
        # This may generate a negative number
        t = (new_point[a] - point1[a]) / (point2[a] - point1[a])
        result[b] = point1[b] + t * (point2[b] - point1[b])
        result[c] = point1[c] + t * (point2[c] - point1[c])
        result[a] = new_point[a]
        return tuple(map(round, result))

    def connect(point1, point2):
        x1, y1, z1 = point1
        x2, y2, z2 = point2
        distances = (x1 - x2, y1 - y2, z1 - z2)
        distances = tuple(map(abs, distances))
        bigest = (0, 0)
        for i, distance in enumerate(distances):
            if distance > bigest[1]:
                bigest = (i, distance)
        bigest_index = bigest[0]

        a1, a2 = point1[bigest_index], point2[bigest_index]
        if a1 > a2:
            a1, a2 = a2, a1

        # x1 has to be always smaller
        for a in range(a1, a2):
            arg = [None, None, None]
            arg[bigest_index] = a
            if point1[bigest_index] > point2[bigest_index]:
                point1, point2 = point2, point1
            yield Cube.connect3d(point1, point2, tuple(arg))

    def connect_all(self):
        points = self.get_points()
        all_new_points = []

        for point in points:
            connection_points = Cube.find_3_smallest(point, points)
            for connection_point in connection_points:
                all_new_points.append(Cube.connect(connection_point, point))
        all_points = []
        for i in all_new_points:
            for a in i:
                all_points.append(a)
        self.write_new_points(all_points)

    def get_points(self) -> list:
        result = []
        cube = deepcopy(self.cube)
        for z in range(len(cube)):
            for y in range(len(cube[z])):
                for x in range(len(cube[y])):
                    if self.cube[z][y][x]:
                        # yield (x, y, z)
                        result.append((x, y, z))
        return result

    def print_proyection(proyection):
        for i in proyection:
            s = ""
            for x in i:
                if x == 1:
                    s += " #"
                else:
                    s += " ."
            print(f"{s}")

    def print_proyection_with_depth(proyection):
        for i in proyection:
            s = ""
            for x in i:
                if type(x) == tuple:
                    on, depth = x
                else:
                    on = x
                if on:
                    depth = len(symbols) - round(depth * len(symbols) / len(proyection))
                    s += f" {symbols[depth]}"
                else:
                    s += " ."
            print(f"{s}")

    def get_proyection_string(proyection):
        result = ""
        for i in proyection:
            s = ""
            for x in i:
                if type(x) == tuple:
                    on, depth = x
                else:
                    on = x
                if on:
                    depth = (
                        len(symbols)
                        - 1
                        - math.floor(depth * len(symbols) / len(proyection))
                    )
                    s += f" {symbols[depth]}"
                else:
                    s += "  "
            result += s + "\n"
        return result

    def rotate(self, angle_x: float, angle_y: float, angle_z: float):
        self.rotation = angle_y
        points = self.get_points()
        angle_x, angle_y, angle_z = (
            math.radians(angle_x),
            math.radians(angle_y),
            math.radians(angle_z),
        )

        def transform(point):
            s = math.floor(self.s / 2)
            if point < s:
                return -(s - point)
            elif point == s:
                return 0
            elif point > s:
                return point - s

        def de_transform(point):
            s = math.floor(self.s / 2)
            point = round(point)
            if point == 0:
                return s
            elif point < 0:
                return s + point
            elif point > 0:
                return s + point

        result = []
        for point in points:
            x, y, z = point
            x, y, z = transform(x), transform(y), transform(z)

            x1 = sum([cos(angle_x) * x, -sin(angle_x) * y, 0])
            y1 = sum([0, 0, z])
            z1 = sum([sin(angle_x) * x, cos(angle_x) * y, 0])

            x3 = sum([cos(angle_y) * x1, -sin(angle_y) * y1, 0])
            y3 = sum([0, 0, z1])
            z3 = sum([sin(angle_y) * x1, cos(angle_y) * y1, 0])

            # x3 = sum([cos(angle_z) * x2, -sin(angle_z) * y2, 0])
            # y3 = sum([0, 0, z2])
            # z3 = sum([sin(angle_z) * x2, cos(angle_z) * y2, 0])

            result.append((de_transform(x3), de_transform(y3), de_transform(z3)))
        return result

    def proyect(self):
        # TODO: proyect with closer things bigger and things at the end smaller
        result = [[0 for _ in range(self.s)] for _ in range(self.s)]
        for i in range(len(self.cube)):
            for x in range(len(self.cube[i])):
                for z in range(len(self.cube[i][x])):
                    if self.cube[i][x][z] == 1:
                        result[x][z] = 1
        return result

    def proyect_with_depth(self):
        # TODO: proyect with closer things bigger and things at the end smaller
        result = [[0 for _ in range(self.s)] for _ in range(self.s)]
        for i in range(len(self.cube) - 1, -1, -1):
            for x in range(len(self.cube[i])):
                for z in range(len(self.cube[i][x])):
                    if self.cube[i][x][z] == 1:
                        #             (on/off, depth)
                        result[x][z] = (1, i)
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A spinning Cube')
    parser.add_argument('-c', help='Colors', type=str, default="white")


    args = parser.parse_args()

    terminal_size = os.get_terminal_size()
    size = (
        terminal_size.lines
        if terminal_size.lines < terminal_size.columns
        else terminal_size.columns
    )
    size = size - 1 - (size % 2)
    cube = Cube(size, args.c)

