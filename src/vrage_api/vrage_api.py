import requests
import base64
import hmac
import hashlib
import uuid
from datetime import datetime
from loguru import logger

class VRageAPI:
    """A simple wrapper that uses the request module to build
    the correct payload and headers to query the Space Engineers
    Server API

    Arguments:
        url:        Base URL (eg. http://<your-ip>:8080)
        token:      API Token found in the configuration GUI/XML
    """

    def __init__(
        self, url: str, token: str, api_endpoint: str = "/vrageremote/v1"
    ) -> None:
        self.url = url
        self.token = token
        self.api_endpoint = api_endpoint
        self.headers = {"Content-Type": "application/json"}

    def build_headers(self, endpoint: str) -> dict:
        """Returns the relevant headers required to query
        the Space Engineers VRage API. Terrible API implementation from Keen Software house...

        Arguments:
            endpoint:   URL endpoint (eg. /vrageremote/v1/server)
        """
        now = datetime.utcnow()
        nonce = uuid.uuid4().hex + uuid.uuid1().hex
        date = now.strftime("%a, %d %b %Y %H:%M:%S")
        pre_hash_str = f"""{endpoint}\r\n{nonce}\r\n{date}\r\n"""

        hmac_obj = hmac.new(
            base64.b64decode(self.token), pre_hash_str.encode("utf-8"), hashlib.sha1
        )
        hmac_encoded = base64.b64encode(hmac_obj.digest()).decode()
        self.headers.update({"Date": date, "Authorization": f"{nonce}:{hmac_encoded}"})
        return self.headers

    def query(self, endpoint: str, operation: str = "get") -> dict:
        """Builds a GET HTTP message

        Arguments:
            endpoint:   URL endpoint (eg. /server/ping)
        """
        valid_operations = {
            "get": requests.get,
            "patch": requests.patch,
            "post": requests.post,
            "delete": requests.delete,
        }

        if not operation.lower() in valid_operations.keys():
            raise ValueError(
                f"Operation {operation} is not valid. Supported operations are: {valid_operations}"
            )

        logger.info(endpoint)
        operation_method = valid_operations[operation.lower()]

        if json is None:
            request = operation_method(
                self.url + endpoint,
                headers=self.build_headers(endpoint=endpoint),
            )
        else:
            request = requests.post(self.url + endpoint,json=json,headers=self.build_headers(endpoint=endpoint))

        if not request.status_code == 200:
            raise ValueError(
                f"Endpoint is most likely invalid due to request.status_code = {request.status_code}"
            )

        try:
            return request.json()
        except:
            logger.error(f"Unable to decode JSON response {request.text}")
            raise ValueError("Unable to decode JSON response")

    def get_players(self) -> dict:
        """Gets all players in the current session"""
        return self.query(f"{self.api_endpoint}/session/players")

    def get_asteroids(self) -> dict:
        """Gets all the asteroids in the current session"""
        return self.query(f"{self.api_endpoint}/session/asteroids")

    def get_floating_objects(self) -> dict:
        """Gets all floating objects in the current session"""
        return self.query(f"{self.api_endpoint}/session/floatingObjects")

    def get_grids(self) -> dict:
        """Gets all the grids in the current session"""
        return self.query(f"{self.api_endpoint}/session/grids")

    def get_planets(self) -> dict:
        """Gets all the planets in the current session"""
        return self.query(f"{self.api_endpoint}/session/planets")

    def get_chat(self) -> dict:
        """Gets the chat history for the current session"""
        return self.query(f"{self.api_endpoint}/session/chat")

    def get_server_info(self) -> dict:
        """Gets Server Info like used PCU stats, Server Name, CPU Load, etc.."""
        return self.query(f"{self.api_endpoint}/server")

    def get_server_ping(self) -> dict:
        """Gets Server Ping (eg. if server is up and responding)"""
        return self.query(f"{self.api_endpoint}/server/ping")

    def get_banned_players(self) -> dict:
        """Gets all banned players for the server"""
        return self.query(f"{self.api_endpoint}/admin/bannedPlayers")

    def get_kicked_players(self) -> dict:
        """Gets all kicked players for the current session"""
        return self.query(f"{self.api_endpoint}/admin/kickedPlayers")

    def delete_asteroid(self, entity_id: int) -> dict:
        """Deletes an asteroid in the current session

        Arguments:
            entity_id:  ID of the entity
        """
        return self.query(
            f"{self.api_endpoint}/session/asteroids/{entity_id}", operation="delete"
        )

    def delete_floating_object(self, entity_id: int) -> dict:
        """Deletes a floating object in the current session

        Arguments:
            entity_id:  ID of the entity
        """
        return self.query(
            f"{self.api_endpoint}/session/floatingObjects/{entity_id}",
            operation="delete",
        )

    def delete_grid(self, entity_id: int) -> dict:
        """Deletes a grid in the current session

        Arguments:
            entity_id:  ID of the entity
        """
        return self.query(
            f"{self.api_endpoint}/session/grids/{entity_id}", operation="delete"
        )

    def delete_planet(self, entity_id: int) -> dict:
        """Deletes a planet in the current session

        Arguments:
            entity_id:  ID of the entity
        """
        return self.query(
            f"{self.api_endpoint}/session/planets/{entity_id}", operation="delete"
        )

    def stop_grid(self, entity_id: int) -> dict:
        """Stops a moving grid in the current session

        Arguments:
            entity_id:  ID of the entity
        """
        return self.query(
            f"{self.api_endpoint}/session/grids/{entity_id}", operation="patch"
        )

    def stop_floating_object(self, entity_id: int) -> dict:
        """Stops a floating object in the current session

        Arguments:
            entity_id:  ID of the entity
        """
        return self.query(
            f"{self.api_endpoint}/session/floatingObjects/{entity_id}",
            operation="patch",
        )

    def power_down_powered_grid(self, entity_id: int) -> dict:
        """Powers down a grid in the current session

        Arguments:
            entity_id:  ID of the entity
        """
        return self.query(
            f"{self.api_endpoint}/session/poweredGrids/{entity_id}", operation="delete"
        )

    def power_up_powered_grid(self, entity_id: int) -> dict:
        """Powers up a grid in the current session

        Arguments:
            entity_id:  ID of the entity
        """
        return self.query(
            f"{self.api_endpoint}/session/poweredGrids/{entity_id}", operation="post"
        )

    def send_chat_message(self, message: str) -> dict:
        return self.query(f"{self.api_endpoint}/session/chat",operation='post',json=message)

    def stop_server(self) -> dict:
        """Stops the current server session"""
        return self.query(f"{self.api_endpoint}/server", operation="delete")

    def player_promote(self, steam_id: str) -> dict:
        """Promotes a player up 1 level based on the SteamID

        Arguments:
            steam_id:   SteamID of the player
        """
        return self.query(
            f"{self.api_endpoint}/admin/promotedPlayers/{steam_id}", operation="post"
        )

    def player_demote(self, steam_id: str) -> dict:
        """Demotes a player down 1 level based on the SteamID

        Arguments:
            steam_id:   SteamID of the player
        """
        return self.query(
            f"{self.api_endpoint}/admin/promotedPlayers/{steam_id}", operation="delete"
        )

    def player_ban(self, steam_id: str) -> dict:
        """Ban a player based on the SteamID

        Arguments:
            steam_id:   SteamID of the player
        """
        return self.query(
            f"{self.api_endpoint}/admin/bannedPlayers/{steam_id}", operation="post"
        )

    def player_unban(self, steam_id: str) -> dict:
        """Unban a player based on the SteamID

        Arguments:
            steam_id:   SteamID of the player
        """
        return self.query(
            f"{self.api_endpoint}/admin/bannedPlayers/{steam_id}", operation="delete"
        )

    def player_kick(self, steam_id: str) -> dict:
        """Kick a player based on the SteamID

        Arguments:
            steam_id:   SteamID of the player
        """
        return self.query(
            f"{self.api_endpoint}/admin/kickedPlayers/{steam_id}", operation="post"
        )

    def player_unkick(self, steam_id: str) -> dict:
        """Unkick a player based on the SteamID

        Arguments:
            steam_id:   SteamID of the player
        """
        return self.query(
            f"{self.api_endpoint}/admin/kickedPlayers/{steam_id}", operation="delete"
        )
