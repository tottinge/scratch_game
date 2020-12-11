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
        return self.x,self.y


class Room(object):
    id_assigned = 0
    @classmethod
    def next_id(cls):
        cls.id_assigned += 1
        return cls.id_assigned
    def __init__(self, origin, width, height, connections=None):
        self.origin = origin
        self.width = width
        self.height = height
        self.connected = connections or []
        self.id = self.next_id()

    def __repr__(self):
        return f"Room {self.id} ({self.origin.x},{self.origin.y}) w:{self.width}, h:{self.height}"

    def connect_to(self, other):
        self.connected.append(other)

    def overlaps_with(self, other):
        pass

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


def weird_assed_generation(x_extent, y_extent, initial_rooms):
    from random import randint
    from itertools import combinations
    points = [
        (randint(0,x_extent),randint(0,y_extent))
        for i in range(initial_rooms)
    ]
    workspace = sorted(
        (Point(*left).distance_to(Point(*right)), left, right)
        for (left,right) in combinations(points, 2)
    )
    for(d, a, b) in workspace:
        print(f"{d} between {a} and {b}")
        possible_diameter = d//3
        if possible_diameter < 2:
            print(f"Too close! {a}<-{possible_diameter}->{b}")
            continue
        room = Room(Point(*a), possible_diameter, possible_diameter)
        print(f"Room is {room}")
        room.connect_to(b)
        yield room

def rect_centered_on( center, width, height):
    from pygame import Rect
    centerx, centery = center
    left = max(0, centerx - width/2)
    top = max(0, centery - height/2)
    return Rect(left,top, width,height)

def render_map(roomset):
    import pygame
    black = (0,0,0)
    green = (0,128,0)
    blue = (0, 0, 255)
    pygame.init()
    display = pygame.display.set_mode((200,400))
    display.fill(black)
    for (origin,room) in roomset.items():
        rect_of_room = rect_centered_on(origin.as_tuple(), room.width, room.height)
        pygame.draw.rect(display, green, rect_of_room, 3)
        for connection in room.connected:
            pygame.draw.line(display, blue, room.origin.as_tuple(), connection, 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.display.update()

if __name__ == '__main__':
    indexed = { room.origin:room for room in weird_assed_generation(200,400, 4) }
    for (origin,room) in indexed.items():
        print(room)
        print(f"    {room.connected}")
        print()
    render_map(indexed)