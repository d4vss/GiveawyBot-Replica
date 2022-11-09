import os

class Loader:
    def load(self, path, client, files: list):
        for file in os.listdir(path):
            if file.endswith(".py"):
                if file in files: return

                client.load_extension(f"{path}.{file[:-3]}")
                print(f"File {file[:-3]} is loaded.")