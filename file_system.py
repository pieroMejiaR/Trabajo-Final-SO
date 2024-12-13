import os

class FileSystem:
    def __init__(self, base_path="."):  # Cambia el directorio base al actual (raíz del proyecto)
        self.base_path = base_path

    def mkdir(self, name):
        """Crea un directorio físicamente."""
        dir_path = os.path.join(self.base_path, name)
        if os.path.exists(dir_path):
            print(f"Directory {name} already exists.")
        else:
            os.makedirs(dir_path)
            print(f"Directory {name} created.")

    def touch(self, name):
        """Crea un archivo físicamente."""
        file_path = os.path.join(self.base_path, name)
        if os.path.exists(file_path):
            print(f"File {name} already exists.")
        else:
            with open(file_path, "w") as f:
                pass
            print(f"File {name} created.")

    def write(self, name, content):
        """Escribe contenido en un archivo físicamente."""
        file_path = os.path.join(self.base_path, name)
        if os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(content)
            print(f"Content written to file {name}.")
        else:
            print(f"File {name} does not exist.")

    def read(self, name):
        """Lee el contenido de un archivo físicamente."""
        file_path = os.path.join(self.base_path, name)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()
            print(f"Content of {name}: {content}")
        else:
            print(f"File {name} does not exist.")

    def rm(self, name):
        """Elimina un archivo o directorio físicamente."""
        path = os.path.join(self.base_path, name)
        if os.path.exists(path):
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.remove(path)
            print(f"{name} deleted.")
        else:
            print(f"{name} does not exist.")

    def ls(self):
        """Lista los contenidos del directorio base."""
        contents = os.listdir(self.base_path)
        print("\nContents:")
        for item in contents:
            print(item)
