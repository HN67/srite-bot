"""Module for managing SriteBot data"""

# Import python libraries
import json
from pathlib import Path

# Import discord
import discord

# Import config
import config

def data_path(path: object) -> str:
    """Returns a path to the data folder with the given path appended (in str form)"""
    return f"data/{path}"

class User:
    """Represents SriteBot user data for a specific user"""

    def __init__(self, user: discord.User):
        self.user: discord.User = user
        self.id: int = self.user.id # User ID
        self.path: str = data_path(str(self.id)) # User Data Folder Path

    def location(self, path: object) -> str:
        """Appends the given path to this User's data folder"""
        return f"{self.path}/{path}"

    def verify(self) -> None:
        """Verifies the disc folder datastructure integrity for this User"""
        # Verify folder existance
        if not Path(self.path).is_dir():
            Path(self.path).mkdir()

        # Update info file
        with open(self.location("info.json"), "w") as file:
            json.dump({"id": self.id, "name": self.user.name}, file)

    def verify_economy(self) -> None:
        """Verifies the disc economy datastructure integrity for this User"""
        # Verify user structure
        self.verify()

        # Try loading the existing file
        economyData = {}
        try:
            with open(self.location("economy.json"), "r") as file:
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
        with open(self.location("economy.json"), "w") as file:
            json.dump(economyData, file)

class Stocks:
    """Represents SriteBot stock data"""
