import json
import os.path
from typing import List


def print_with_indent(value, indent=0):
    print(("\t" * indent) + str(value))


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        entry.parent = self
        self.entries.append(entry)

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        return {
            "title": self.title,
            "entries": [entry.json() for entry in self.entries]
        }

    @classmethod
    def from_json(cls, value: dict):
        new_entry = cls(value['title'])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as file:
            return cls.from_json(json.load(file))

    def save(self, path):
        with open(os.path.join(path, f"{self.title}.json"), "w") as file:
            json.dump(self.json(), file)


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            with open(os.path.join(self.data_path, f"{entry.title}.json"), 'w') as file:
                json.dump(entry.json(), file)

    def load(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        else:
            for filename in os.listdir(self.data_path):
                if filename.endswith('json'):
                    entry = Entry.load(os.path.join(self.data_path, filename))
                    self.entries.append(entry)
        return self

    def add_entry(self, title):
        self.entries.append(Entry(title))
