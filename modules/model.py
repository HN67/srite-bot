"""Module for managing and modeling SriteBot data."""

# Import python libraries
import random
import json
from pathlib import Path
from contextlib import contextmanager
from typing import Generator

# Import discord
import discord

# Import config
import config


def data_path(path: object) -> str:
    """Compose the data folder path with the given path."""
    return f"data/{path}"


def archive(name: str, data: object) -> None:
    """Save the given object as JSON in the archive under the given name."""
    folder = data_path("archive")
    path = f"{folder}/{name}"
    # Ensure directory exists
    if not Path(folder).is_dir():
        Path(folder).mkdir()
    # Dump data into file
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)


class User:
    """Model to represent SriteBot data for a specific user."""

    def __init__(self, user: discord.User) -> None:
        """Create a User based on a discord.User object."""
        self.user: discord.User = user
        self.id: int = self.user.id
        # Each user data is stored in a folder based on their id
        self.path: str = data_path(str(self.id))
        self.infoPath: str = self.location("Info.json")
        self.economyPath: str = self.location("Economy.json")

    def location(self, path: object) -> str:
        """Compose this User's data folder with the given path."""
        return f"{self.path}/{path}"

    def verify(self) -> None:
        """Verify the stored user data integrity for this User."""
        # Verify folder existance
        if not Path(self.path).is_dir():
            Path(self.path).mkdir()

        # Update info file
        with open(self.infoPath, "w", encoding="utf-8") as file:
            json.dump({"id": self.id, "name": self.user.name}, file)

    def verify_economy(self) -> None:
        """Verify the stored economy data integrity for this User."""
        # Verify user structure
        self.verify()

        # Try loading the existing file
        economyData = {}
        try:
            with open(self.economyPath, "r", encoding="utf-8") as file:
                economyData = json.load(file)
        except FileNotFoundError:
            pass

        # Verify file integrity, will also fully create it if empty (or didnt exist)
        # Verify default attributes with config
        for key in config.economy.attributes:
            if key not in economyData:
                economyData[key] = 0

        # Try loading the existing stock data
        stockData = {}
        try:
            stockData = economyData["stocks"]
        except KeyError:
            pass

        # Verify stock key integrity with config
        for key in config.stocks.items:
            if key not in stockData:
                stockData[key] = 0

        # Repack stock data
        economyData["stocks"] = stockData
        # Save economy data
        with open(self.economyPath, "w", encoding="utf-8") as file:
            json.dump(economyData, file)

    @contextmanager
    def open_economy(self) -> Generator[dict, None, None]:
        """Manipulate economy data within a context.

        Changes to the data are automatically saved on context exit.
        """
        # Verify data
        self.verify_economy()
        # Load data
        data = {}
        with open(self.economyPath, "r", encoding="utf-8") as file:
            data = json.load(file)
        try:
            # Yield data
            yield data
        finally:
            # Resave data
            with open(self.economyPath, "w", encoding="utf-8") as file:
                json.dump(data, file)


class Guild:
    """Model to represent SriteBot data for a specific server."""

    def __init__(self, guild: discord.Guild) -> None:
        """Create a Guild based on a discord.Guild object."""
        self.guild: discord.Guild = guild
        self.id: int = guild.id
        # Guild data is stored in a folder based on its id
        self.path: str = data_path(f"guild/{str(self.id)}")
        self.info_path: str = self.location("info.json")
        self.roles_path: str = self.location("roles.json")

    def location(self, path: object) -> str:
        """Compose this Guild's data folder with the given path."""
        return f"{self.path}/{path}"

    def verify(self) -> None:
        """Verify the stored data integrity for this Guild."""
        # Verify folder existance
        if not Path(self.path).is_dir():
            Path(self.path).mkdir(parents=True, exist_ok=True)

        # Update info file
        with open(self.info_path, "w", encoding="utf-8") as file:
            json.dump({"id": self.id, "name": self.guild.name}, file)

    def verify_roles(self) -> None:
        """Verify the stored role data integrity for this Guild."""
        # Verify guild structure
        self.verify()

        # Try loading existing roles file
        try:
            with open(self.roles_path, "r", encoding="utf-8") as file:
                roles_data = json.load(file)
        except FileNotFoundError:
            roles_data = {}

        # Verify file integrity
        self_roles_id = "self_roles"
        if self_roles_id not in roles_data:
            roles_data[self_roles_id] = []

        with open(self.roles_path, "w", encoding="utf-8") as file:
            json.dump(roles_data, file)

    @contextmanager
    def open_roles(self) -> Generator[dict, None, None]:
        """Manipulate roles data within a context.

        Changes to the data are automatically saved on context exit.
        """
        # Verify data
        self.verify_roles()
        # Load data
        with open(self.roles_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        try:
            yield data
        finally:
            # Resave data on context exit
            with open(self.roles_path, "w", encoding="utf-8") as file:
                json.dump(data, file)


class Stocks:
    """Model to represent SriteBot stock data.

    Every instance references the same data.
    """

    def __init__(self) -> None:
        """Construct a view of the stock data."""
        self.path: str = data_path("stocks.json")

    def verify(self) -> None:
        """Verify the stored stock data."""
        # Try loading the existing file
        stockData = {}
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                stockData = json.load(file)
        except FileNotFoundError:
            pass

        # Verify stock keys from config
        for stock in config.stocks.items:
            if stock not in stockData:
                stockData[stock] = config.stocks.standard

        # Resave stock data
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(stockData, file)

    @contextmanager
    def open(self) -> Generator[dict, None, None]:
        """Manipulate stock data within a context.

        Changes to the data are automatically saved on context exit.
        """
        # Verify data
        self.verify()
        # Load data
        data = {}
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)
        try:
            # Yield data
            yield data
        finally:
            # Resave data
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(data, file)

    def update(self) -> None:
        """Perform a stock update using config data."""
        # Verify stock data
        self.verify()

        # Update data
        with self.open() as data:
            for stock in data:
                data[stock] += random.randint(
                    -config.stocks.change, config.stocks.change
                )
