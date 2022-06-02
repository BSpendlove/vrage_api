.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/vrage_api.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/vrage_api
    .. image:: https://readthedocs.org/projects/vrage_api/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://vrage_api.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/vrage_api/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/vrage_api
    .. image:: https://img.shields.io/pypi/v/vrage_api.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/vrage_api/
    .. image:: https://img.shields.io/conda/vn/conda-forge/vrage_api.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/vrage_api
    .. image:: https://pepy.tech/badge/vrage_api/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/vrage_api
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/vrage_api

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=========
vrage_api
=========


    Space Engineers Dedicated Server Remote API in Python


This module is essentially a python wrapper around the `requests` module to interact with the Space Engineers Dedicated Server Remote API. This module is (will) also be used in a server management tool which provides insight to your server(s). Currently if you run the GUI tool, you can't get any insight into players that have logged on and played on the server, performance over a period of time, chat logs, existing planets/asteroids and floating objects for example.

Once you have installed the package, you can view some of the example commands in the [examples](./examples/) folder. The example [commands.py](./examples/commands.py) will load a .env file in the root folder, so you can copy the `.env-example` as `.env` and fill out the information as required. All non 'get' commands will require the `--data` argument to pass a variable such as EntityId or SteamID. Ensure that you install argparse if you want to test out the commands using this script `pip install argparse`.

Function endpoint data
======================

GET
-------------------

[get_players](./examples/get/players.json) - Gathers data about all the players such as: SteamID, Display Name, Faction, Faction Level and Ping
[get_asteroids](./examples/get/asteroids.json) - Gathers data about all the asteroids in the current session such as: EntityId, position and display name
[get_floating_objects](./examples/get/floating_objects.json) - Gathers data about all the floating objects that exist in the current session such as: EntityId, Kind, Position, Mass and Speed
[get_grids](./exmaples/get/grids.json) - Gathers data about all the grids that exist in the current session such as: EntityId, Display Name, Position, Mass, Owner SteamID, total amount of PCU, powered status, etc...
[get_planets](./examples/get/planets.json) - Gathers data about all the planets that exist in the current session such as: EntityId, Display Name and Position
[get_chat](./examples/get/chat.json) - Gathers data about all the chat messages in the current session such as: SteamID, Display Name, Content (Message) and Timestamp
[get_server_info](./examples/get/server_info.json) - Gathers data about the server such as: ServerId, Server Name, Total uptime, CPU load, World Name, Version, total amount of Players, total used PCU etc...
[get_server_ping](./examples/get/server_ping.json) - Simple healthcheck for the server that responds "Pong" if successful.
[get_banned_players](./examples/get/banned_players.json) - Gathers data about all banned players such as:
[get_kicked_players](./examples/get/kicked_players.json)

DELETE / BAN / KICK
-------------------

All delete endpoints will typically just return a HTTP status code of 200 even if the EntityID doesn't exist...::

    {
        "meta": {
            "apiVersion": "1.0",
            "queryTime": 0.1115
        }
    }

So some care is required if you really want to identify for example, if a player has actually been kicked/banned properly based on gathering the data after performing a specific action.

A centralized API for multiple servers (and ensuring things like log history, player history) will be linked here directly once developed.

.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.2.2. For details and usage
information on PyScaffold see https://pyscaffold.org/.