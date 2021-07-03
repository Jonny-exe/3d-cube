#!/usr/bin/python3
from pprint import pprint
import math
from math import cos, sin
from copy import deepcopy
class Cube():
    def __init__(self, s = 17):
        # assert s % 4 == 0
        self.s = s
        self.cube = Cube.create_cube(s)
        self.cube = self.write_cube(self.cube)
        Cube.print_rows(self.proyect())
        new_points = self.rotate(45)
        self.cube = Cube.create_cube(s)
        self.write_new_points(new_points)
        proyect = self.proyect() 
        Cube.print_rows(proyect)
        Cube.print_proyection(proyect)

    def create_cube(s):
        return [[[0 for _ in range(s)] for _ in range(s)] for _ in range(s)]
    def write_cube(self, cube):
        s = self.s / 2 # Maybe this needs a round
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
            self.cube[z][y][x] = 1

    def print_rows(cube):
        pprint(cube)

    def get_points(self):
        cube = deepcopy(self.cube)
        for z in range(len(cube)):
            for y in range(len(cube[z])):
                for x in range(len(cube[y])):
                    if self.cube[z][y][x]:
                        yield (x, y, z)

    def print_proyection(proyection):
        for i in proyection:
            s = ""
            for x in i:
                if x == 1:
                    s += "✅"
                else:
                    s += "❌"
            print(f"{s}")


    def rotate(self, angle: int):
        points = self.get_points()
        angle = math.radians(angle)

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
            print(x, y, z)
            new_x = sum([cos(angle) * x, -sin(angle) * y, 0])
            new_y = sum([0, 0, z])
            new_z = sum([sin(angle) * x, cos(angle) * y, 0])
            print(round(new_x), round(new_y), round(new_z))

            result.append((de_transform(new_x), de_transform(new_y), de_transform(new_z)))
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

if __name__ == "__main__":
    cube = Cube(23)
