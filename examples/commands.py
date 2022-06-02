from vrage_api.vrage_api import VRageAPI
from dotenv import dotenv_values
from argparse import ArgumentParser
import json

env = dotenv_values(".env")
api = VRageAPI(url=env["API_URL"], token=env["API_TOKEN"])

commands = {
    "get_players": api.get_players,
    "get_asteroids": api.get_asteroids,
    "get_floating_objects": api.get_floating_objects,
    "get_grids": api.get_grids,
    "get_planets": api.get_planets,
    "get_chat": api.get_chat,
    "get_server_info": api.get_server_info,
    "get_server_ping": api.get_server_ping,
    "get_banned_players": api.get_banned_players,
    "get_kicked_players": api.get_kicked_players,
    "delete_asteroid": api.delete_asteroid,
    "delete_floating_object": api.delete_floating_object,
    "delete_grid": api.delete_grid,
    "delete_planet": api.delete_planet,
    "stop_floating_object": api.stop_floating_object,
    "stop_grid": api.stop_grid,
    "power_down_powered_grid": api.power_down_powered_grid,
    "power_up_powered_grid": api.power_up_powered_grid,
    "player_ban": api.player_ban,
    "player_unban": api.player_unban,
    "player_kick": api.player_kick,
    "player_unkick": api.player_unkick,
    "player_promote": api.player_promote,
    "player_demote": api.player_demote,
}

parser = ArgumentParser(description="Test the vrage_api module...")
parser.add_argument(
    "--command", choices=commands.keys(), required=True, help="Function to call"
)
parser.add_argument("--data", help="Required if --command doesn't start with 'get'")

args = parser.parse_args()
if not args.command.startswith("get") and not args.data:
    exit("Non 'get' commands must also run with the --data argument")

if args.command.startswith("get"):
    data = commands[args.command]()
else:
    data = commands[args.command](args.data)

print(json.dumps(data, indent=4))