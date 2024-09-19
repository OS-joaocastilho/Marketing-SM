"""
This script defines two classes, `Description` and `Business`, for managing business-related data and their
associated descriptions, suggestions, Instagram profiles, and colors. Additionally, it includes a `State` class
to manage the state of multiple businesses and functionality to load and store this state from/to a JSON file.

### Components

1. **Imports**:
   - `json`: Used for serializing and deserializing data to/from JSON format.
   - `os`: Provides functionality to interact with the operating system, used for file path management.
   - `time`: Used for generating timestamps.
   - `dataclasses`: Provides the `dataclass` decorator to simplify class definitions.
   - `typing`: Includes type hints for improved code readability and type checking.

2. **Classes**:
   - **`Description`**:
     - **Purpose**: Represents a simple data container for descriptions with a title.
     - **Attributes**:
       - `title`: The title of the description.
       - `description`: The content of the description.
     - **Methods**:
       - `from_dict(data: Dict) -> 'Description'`: Creates a `Description` instance from a dictionary.

   - **`Business`**:
     - **Purpose**: Manages various aspects of a business, including descriptions, suggestions, Instagram profiles, and colors.
     - **Attributes**:
       - `name`: The name of the business.
       - `descriptions`: A dictionary of descriptions related to the business.
       - `suggestions`: A dictionary of suggestions for the business.
       - `instagram_urls`: A dictionary of Instagram URLs and their scraped profiles.
       - `colors`: A list of colors associated with the business.
     - **Methods**:
       - `add_description(title: str, description: str)`: Adds a description to the business.
       - `add_suggestion(title: str, suggestion: str)`: Adds a suggestion to the business.
       - `add_instagram(instagram_url: str, scraped_profile: str)`: Adds an Instagram URL and its scraped profile.
       - `save_colors(colors: List[str])`: Saves a list of colors associated with the business.
       - `to_dict() -> Dict`: Converts the business instance to a dictionary.
       - `from_dict(data: Dict) -> 'Business'`: Creates a `Business` instance from a dictionary.

   - **`State`**:
     - **Purpose**: Manages the state of multiple businesses and provides functionality to store and load the state from a file.
     - **Attributes**:
       - `businesses`: A dictionary of `Business` instances indexed by business names.
     - **Methods**:
       - `from_dict(data: Dict) -> 'State'`: Creates a `State` instance from a dictionary.
       - `store_state()`: Stores the current state to a JSON file.

3. **Functions**:
   - **`load_state() -> State`**:
     - **Purpose**: Loads the state of businesses from a JSON file, or initializes an empty state if the file is not found or is corrupted.
     - **Returns**: An instance of `State` with loaded or initialized businesses.

### Example Usage

To use this module:
1. Create instances of `Business` and populate them with data using the provided methods.
2. Manage and store the state of multiple businesses using the `State` class.
3. Use `load_state()` to load previously saved state or initialize a new one.

This script provides a structured way to handle business-related data and maintain state persistence across program executions.
"""

import json
import os
import time
from dataclasses import dataclass
from typing import Dict, List

from marketing_sm.data.constants import DATA_DIR, STATE_FILENAME


@dataclass
class Description:
    title: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict) -> "Description":
        return cls(data["title"], data["description"])


class Business:
    def __init__(self, name: str):
        self.name: str = name
        self.descriptions: Dict[str, Description] = {}
        self.suggestions: Dict[str, Description] = {}
        self.instagram_urls: Dict[str, Description] = {}
        self.colors: List[str] = []

    def add_description(self, title: str, description: str):
        self.descriptions[title] = Description(title, description)

    def add_suggestion(self, title: str, suggestion: str):
        self.suggestions[title] = Description(title, suggestion)

    def add_instagram(self, instagram_url: str, scraped_profile: str):
        self.instagram_urls[instagram_url] = Description(instagram_url, scraped_profile)

    def save_colors(self, colors: List[str]):
        self.colors = colors

    def to_dict(self) -> Dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict) -> "Business":
        business = cls(data["name"])
        business.descriptions = {
            k: Description.from_dict(v) for k, v in data.get("descriptions", {}).items()
        }
        business.suggestions = {
            k: Description.from_dict(v) for k, v in data.get("suggestions", {}).items()
        }
        business.instagram_urls = {
            k: Description.from_dict(v)
            for k, v in data.get("instagram_urls", {}).items()
        }
        business.colors = data.get("colors", [])
        return business


@dataclass
class State:
    businesses: Dict[str, Business]

    @staticmethod
    def from_dict(data: Dict) -> "State":
        businesses = {
            name: Business.from_dict(business_data)
            for name, business_data in data.get("businesses", {}).items()
        }
        return State(businesses=businesses)

    def store_state(self):
        filepath = os.path.join(DATA_DIR, STATE_FILENAME)
        print(f"Storing state: {self} in file {filepath}")
        with open(filepath, "w") as f:
            json.dump(self.__dict__, f, default=vars)


def load_state() -> State:
    filepath = os.path.join(DATA_DIR, STATE_FILENAME)
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        state = State.from_dict(data)
        print(f"Loading state {state} from file {STATE_FILENAME}")
    except FileNotFoundError:
        state = State(businesses={})
        print(f"File {STATE_FILENAME} does not exists. State will be initialized...")
    except json.JSONDecodeError:
        if data:
            with open(filepath + str(time.time()), "w") as f:
                json.dump(data, f)
        state = State(businesses={})
    return state
