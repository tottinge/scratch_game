from itertools import chain
from math import sqrt, floor


def coalesce(paths):
    path_sets = [set(x) for x in paths]
    while path_sets:
        current = path_sets.pop(0)
        matches = [x for x in path_sets if current.intersection(x)]
        if not matches:
            yield current
            continue
        nonmatch = [x for x in path_sets if not current.intersection(x)]
        path_sets = nonmatch + [current.union(*matches)]


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        leg_a = abs(self.x - other.x)
        leg_b = abs(self.y - other.y)
        raw_distance = sqrt((leg_a ** 2) + (leg_b ** 2))
        return floor(raw_distance)

    def __repr__(self):
        return f"Point ({self.x},{self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def as_tuple(self):
        return self.x, self.y




class Room(object):
    id_assigned = 0

    @classmethod
    def next_id(cls):
        cls.id_assigned += 1
        return cls.id_assigned

    @staticmethod
    def rect_centered_on(center_point, width, height):
        x = center_point.x - .5 * width
        y = center_point.y - .5 * height
        return Point(x,y)


    def __init__(self, origin, width, height, connections=None):
        self.origin = origin
        self.width = width
        self.height = height
        self.upperleft = self.rect_centered_on(origin, width, height)
        self.connected = connections or []
        self.id = self.next_id()

    def __repr__(self):
        return f"Room {self.id} ({self.origin.x},{self.origin.y}) w:{self.width}, h:{self.height}"

    def connect_to(self, other):
        self.connected.append(other)
        other.connected.append(self)

    def available(self):
        return len(self.connected) < 3

    def reachable(self, other, exclude=None):
        connected_ids = [c.id for c in self.connected]
        print(f"From {self.id} can we reach {other.id} via {connected_ids}")
        if self.id == other.id:
            return True
        return any(item.reachable(other, self) for item in self.connected if item != exclude)

    def overlaps_with(self, other):
        pass

    def rect_bounds(self):
        return self.upperleft.x, self.upperleft.y, self.width, self.height

    def periphery(self):
        left, top = self.origin.x, self.origin.y
        bottom = top + self.height - 1
        right = left + self.width - 1

        top_row = (Point(x, top) for x in range(left, left + self.width))
        bottom_row = (Point(x, bottom) for x in range(left, left + self.width))
        left_row = (Point(left, y) for y in range(top + 1, top + self.height - 1))
        right_row = (Point(right, y) for y in range(top + 1, top + self.height - 1))

        return chain(top_row, bottom_row, left_row, right_row)

    def nearest_point(self, other):
        return min((mine.distance_to(yours), mine, yours)
                   for mine in self.periphery()
                   for yours in other.periphery()
                   )


class PointGen(object):
    def __init__(self, x_extent, y_extent):

        x_offset = x_extent / 10
        self.x_bounds = (0+x_offset, x_extent-x_offset)

        y_offset = y_extent / 10
        self.y_bounds = (0+y_offset, y_extent-y_offset)

    def selection(self):
        from random import randint
        return Point(randint(*self.x_bounds),randint(*self.y_bounds))


def weird_assed_generation(x_extent, y_extent, initial_rooms):
    from itertools import combinations

    point_gen = PointGen(x_extent, y_extent)

    points = [
        point_gen.selection()
        for _ in range(initial_rooms)
    ]
    distance = (
        (left.distance_to(right), left, right)
        for (left, right) in combinations(points, 2)
    )

    workspace = sorted(distance, key = lambda item: item[0])
    rooms = {}
    for (d, a, b) in workspace:
        possible_diameter = int(d*.8)
        room_a = rooms.setdefault(a, Room(a, possible_diameter, possible_diameter))
        room_b = rooms.setdefault(b, Room(b, possible_diameter, possible_diameter))
        if not room_a.reachable(room_b):
            print(f"Connecting {room_a.id} to {room_b.id}.")
            room_a.connect_to(room_b)
    return rooms.values()


import pygame

black = (0, 0, 0)
green = (0, 128, 0)
blue = (0, 0, 255)


def render_map(roomset, width, height):
    pygame.init()
    display = pygame.display.set_mode((width, height))
    display.fill(black)
    for (room) in roomset:
        bounds = room.rect_bounds()
        print(f"{room.id} {bounds}")
        rect_of_room = pygame.Rect(*bounds)
        pygame.draw.rect(display, green, rect_of_room, 3)
        start = room.origin.as_tuple()
        for connection in room.connected:
            end = connection.origin.as_tuple()
            pygame.draw.line(display, blue, start, end, 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.display.update()


if __name__ == '__main__':
    width = 600
    height = 400
    for i in range(5):
        rooms = weird_assed_generation(width, height, 20)
        render_map(rooms, width, height)
