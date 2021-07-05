#!/usr/bin/python3
from pprint import pprint
from symbols import symbols
import math
from math import cos, sin
from copy import deepcopy
class Cube():
    def __init__(self, s = 17):
        # assert s % 4 == 0
        self.rotation = -15
        self.s = s
        # self.cube = Cube.create_cube(s)
        # Cube.print_rows(self.proyect())
        # new_points = self.rotate(45)
        # self.cube = Cube.create_cube(s)
        # self.write_new_points(new_points)
        # proyect = self.proyect() 
        # Cube.print_rows(proyect)
        # Cube.print_proyection(proyect)
        # self.connect_all()
        # proyect = self.proyect() 
        # Cube.print_proyection(proyect)
        for _ in range(10):
            self.rotate_and_print()

    def rotate_and_print(self):
        self.cube = Cube.create_cube(self.s)
        self.cube = self.write_cube(self.cube)
        new_points = self.rotate(self.rotation + 15)
        self.cube = Cube.create_cube(self.s)
        self.write_new_points(new_points)
        self.connect_all()
        proyection = self.proyect_with_depth()
        Cube.print_proyection_with_depth(proyection)
        print("---------------------------------------------------")

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
        # results = []
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

    def connect(point1: tuple, point2: tuple):
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

    def connect3d(point1: tuple, point2: tuple, new_point: tuple) -> list:
        # Formula new_point = point1 + t * point2
        #                     always (0, 0, 0) so we can remove it
        x, y, z = new_point
        if (x != None and y != None) or (x != None and z != None) or (y != None and z != None) or (x == None and y == None and z == None):
            raise (ValueError, "There must only be one known value")

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


    def connect_all(self):
        points = self.get_points()
        all_new_points = []

        for point in points:
            connection_points = Cube.find_3_smallest(point, points)

            result_points = []
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


    def rotate(self, angle: int):
        self.rotation = angle
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
            new_x = sum([cos(angle) * x, -sin(angle) * y, 0])
            new_y = sum([0, 0, z])
            new_z = sum([sin(angle) * x, cos(angle) * y, 0])

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
    cube = Cube(23)
