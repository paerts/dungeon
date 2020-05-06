import typing as t
from game.util import screen
from game.util import player_input
from game.util import talk


class Item:
    def __init__(self, name: t.AnyStr):
        self.name = name


class Armor(Item):
    def __init__(self, name: t.AnyStr):
        super().__init__(name=name)
        self.resistance: int = 10


class Container(Item):
    def __init__(self, name: t.AnyStr, number_of_slots: int = 6):
        super().__init__(name=name)
        self.number_of_slots = number_of_slots
        self.contents: t.List[Item] = []

    def move_item(self, from_container: "Container", item_to_move: Item) -> t.List[t.AnyStr]:
        messages = []

        if len(self.contents) < self.number_of_slots:
            from_container.contents.remove(item_to_move)
            self.contents.append(item_to_move)

        return messages

    def display(self) -> t.List[t.AnyStr]:
        messages = [f'--- {self.name} ---']
        if len(self.contents) == 0:
            messages.append('  nothing here')
        for slot, item in enumerate(self.contents):
            messages.append(f'{slot + 1}: {item.name}')

        return messages


class Entity:
    def __init__(self):
        self.represent: t.AnyStr = ''


class Wall(Entity):
    def __init__(self):
        super().__init__()
        self.represent: t.AnyStr = '#'


class Void(Entity):
    def __init__(self):
        super().__init__()
        self.represent: t.AnyStr = ' '


class Player(Entity):

    def __init__(self):
        super().__init__()
        self.name: t.AnyStr = 'player'
        self.hp: int = 10
        self.represent: t.AnyStr = '*'
        self.backpack: Container = Container(name='backpack')

    def display_stats(self):
        print(f'HP: {self.hp}')


class DungeonMap:
    def __init__(self,
                 map_name: t.AnyStr,
                 layout: t.List[t.AnyStr],
                 legend: t.Dict[t.AnyStr, t.Union[Entity, Player]]):
        self.map_name = map_name
        self.layout = layout
        self.legend = legend
        self.dungeon: t.List[t.List[Entity]] = []
        self.dungeon_builder()

    def dungeon_builder(self):
        for row in self.layout:
            dungeon_row = []
            for char in row:
                dungeon_row.append(self.legend[char])
            self.dungeon.append(dungeon_row)

    def display_dungeon(self):
        for row in self.dungeon:
            for entity in row:
                print(entity.represent, end='')
            print()

    def find_entity(self, entity_to_find: Entity) -> t.Tuple[int, int]:
        for row, cols in enumerate(self.dungeon):
            for col, entity in enumerate(cols):
                if entity == entity_to_find:
                    return row, col

    def get_entity_on_position(self, row: int, col: int) -> Entity:
        return self.dungeon[row][col]

    def set_entity_on_position(self, entity: Entity, row: int, col: int):
        self.dungeon[row][col] = entity

    def move_entity(self, entity: Entity, direction: t.AnyStr) -> t.List[t.AnyStr]:

        messages = []

        old_row, new_row = self.find_entity(entity_to_find=entity)

        if direction == 'UP':
            requested_position = (old_row - 1, new_row)
        elif direction == 'DOWN':
            requested_position = (old_row + 1, new_row)
        elif direction == 'LEFT':
            requested_position = (old_row, new_row - 1)
        elif direction == 'RIGHT':
            requested_position = (old_row, new_row + 1)
        else:
            messages.append(f'can not move {direction}')
            return messages

        entity_on_required_position = self.get_entity_on_position(*requested_position)
        if isinstance(entity_on_required_position, Wall):
            messages.append(f'You step {direction.lower()} and hit a wall')
            messages.append(talk.walk_into_wall())
            return messages
        else:
            self.set_entity_on_position(entity, *requested_position)
            self.set_entity_on_position(Void(), old_row, new_row)

        return messages


class Game:
    def __init__(self, dungeon_maps: t.List[DungeonMap]):
        self.dungeon_maps = dungeon_maps
        self.current_map: DungeonMap = dungeon_maps[0]
        self.player: Player = self.current_map.legend['*']
        self.messages = []

    def process_command(self, command: t.AnyStr) -> t.List[t.AnyStr]:
        self.messages = []
        # self.messages.append(command)
        if command in [
            player_input.PlayerCommands.PLAYER_RIGHT,
            player_input.PlayerCommands.PLAYER_LEFT,
            player_input.PlayerCommands.PLAYER_UP,
            player_input.PlayerCommands.PLAYER_DOWN,

        ]:
            self.messages.extend(self.current_map.move_entity(entity=self.player, direction=command))
        elif command == player_input.PlayerCommands.SHOW_BACKPACK:
            self.messages.extend(self.player.backpack.display())

        return self.messages

    def display_messages(self):
        for message in self.messages:
            print(message)


def game_setup() -> Game:
    # create a new player, and fill backpack
    player = Player()
    player.backpack.contents = [
        Item(name='small red potion'),
        Item(name='snake oil')
    ]

    # create level 1
    level_1 = DungeonMap(map_name='level 1',
                         layout=[
                             '##########################',
                             '#                        #',
                             '#                        #',
                             '#                        #',
                             '#                        ##########',
                             '#                                 #',
                             '#                        #######  #',
                             '#                        #        #',
                             '#    *                   #        #',
                             '#                        #        #',
                             '###################################'
                         ],
                         legend={
                             '#': Wall(),
                             ' ': Void(),
                             '*': player
                         }
                         )

    game = Game(dungeon_maps=[level_1])

    return game


def game_loop(game: Game):
    quit_game = False

    while not quit_game:
        screen.clear()
        game.current_map.display_dungeon()
        game.player.display_stats()
        game.display_messages()

        # get player input
        command = player_input.get_player_command()
        if command == player_input.PlayerCommands.PLAYER_QUIT:
            quit_game = True

        game.process_command(command)


if __name__ == '__main__':
    game_loop(game=game_setup())
