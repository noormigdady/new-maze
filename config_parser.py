import sys
from typing import Any


class DuplicateKey(Exception):

    """
        A class that handles duplicate keys

        Args -> key: The key associated with the duplicate value.

        Return -> None
    """

    def __init__(self, key: str) -> None:

        """
            The DuplicateKey class initializer

            Args -> key: The key associated with the duplicate value.

            Return -> None
        """

        super().__init__(f"Duplicate value for {key}, already exists")


def check_points(Entry: tuple[int, int],
                 Exit: tuple[int, int],
                 width: int,
                 height: int,
                 file: str) -> None:

    """
        Checks that the Entry an Exit cells are following
        the boundries set:
        - Entry and Exit cells are inside the maze borders
        - Entry and Exit cells are not the same [The should be different]

        Args -> Entry and Exit cells [Cell], Width and Height [int],
        file name [str]

        Return -> None
    """

    x, y = Entry
    i, j = Exit
    if not (0 <= x < height and 0 <= y < width):
        raise Exception(f"Invalid ENTRY point, check {file}")
    if not (0 <= i < height and 0 <= j < width):
        raise Exception(f"Invalid EXIT point, check {file}")
    if Entry == Exit:
        raise Exception(
            f"ENTRY and EXIT points must be different, check {file}"
            )


def config_parser(file: str) -> dict[str, Any]:

    """
        Parses and validates the confniguration file values:
        - Checks that all manadtory keys exist and have values
        - Checks that the keys and values are in the right format:
          [KEY=VALUE]
        - Checks the values assigned to the keys are in the right format
        - Ignores comments (lines strats with #)
        - Checks for duplicate values assigned for a single key

        Args -> configuration file name [str]

        Return -> Returns a dictionary of the final parsed vlaues to be used,
                  where the key is a string and the key is [int , str, etc..]
                  [dict[str, Any]]
    """

    required = ["HEIGHT", "WIDTH", "ENTRY", "EXIT", "PERFECT", "OUTPUT_FILE"]
    config: dict[str, Any] = {}
    with open(file, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            lst = line.split("=")
            if len(lst) != 2:
                raise Exception("Invalid format, must be KEY=VALUE")

            lst[0] = lst[0].lower().strip()
            lst[1] = lst[1].strip()

            if lst[0] in ["width", "height"]:
                if lst[0].upper() in config:
                    raise DuplicateKey(lst[0].upper())
                try:
                    value = int(lst[1])
                    config[lst[0].upper()] = value
                except Exception:
                    print(f"Invalid value for {lst[0].upper()}, "
                          f"must be an integer")
                    sys.exit()
                if value < 0:
                    print(f"{lst[0].upper()} can't be nigative value!")
                    sys.exit()

            if lst[0] in ["entry", "exit"]:
                pair = lst[1].split(",")
                if len(pair) != 2:
                    raise Exception(f"Invalid formate {lst[0].upper()}")
                try:
                    i = int(pair[0])
                    j = int(pair[1])
                    config[lst[0].upper()] = (i, j)
                except Exception:
                    print(f"Invalid values for pair {lst[0].upper()}, "
                          f"must be integers (x, y)")
                    sys.exit()
                if i < 0 or j < 0:
                    print("ENTRY/EXIT should be a positive integer pair (x,y)")
                    sys.exit()

            if lst[0] == "perfect":
                if lst[1].lower() == "true":
                    config[lst[0].upper()] = True
                elif lst[1].lower() == "false":
                    config[lst[0].upper()] = False
                else:
                    raise Exception(
                        "Invalid value for PERFECT, "
                        "must be either True or False")

            if lst[0] == "output_file":
                if not lst[1].endswith(".txt"):
                    raise Exception("Invalid extention, must be .txt")
                config["OUTPUT_FILE"] = lst[1]

            if lst[0] == "seed":
                try:
                    seed = int(lst[1])
                    config["SEED"] = seed
                except Exception:
                    print("Invalid value for SEED, must be an integer")
                    sys.exit()

        for item in required:
            if item not in config:
                raise Exception(f"MISSING {item}, Modify your config.txt")

        if "SEED" not in config:
            config["SEED"] = None

        try:
            check_points(config["ENTRY"], config["EXIT"],
                         config["WIDTH"], config["HEIGHT"], file)
        except Exception as e:
            print(e)
            sys.exit()
    return config
