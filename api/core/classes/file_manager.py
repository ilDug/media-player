from xmlrpc.client import boolean
from fastapi import HTTPException
from pathlib import Path
import base64
from core.models.file_system_item import FSItem


class FileManager:
    path: Path
    allowed_ext = []
    avoid_parent: bool

    def __init__(self, path: Path, allowed_ext=[], avoid_parent=False) -> None:
        self.path = path
        self.allowed_ext = allowed_ext
        self.avoid_parent = avoid_parent

    def ls(self):
        """elenca il contenuto della cartella"""
        if not self.path.is_dir():
            raise HTTPException(500, "il persorso non è una cartella")

        items = (
            [] if self.avoid_parent else [self.generate_item(self.path.parent, True)]
        )
        # if self.path == "" or self.path.as_posix() == self.base_path.as_posix():
        #     items = [self.generate_item(self.path.parent)]
        #     print("root")
        # else:
        #     items = [self.generate_item(self.path.parent)]
        #     print("no root")

        for item in self.path.iterdir():
            if not self.filter_validate(item):
                print(f"elemento {item.name} non conteggiato")
                continue

            fs = self.generate_item(item)
            items.append(fs)

        # aggiunge il parent
        # parent =
        # items.index(0, parent)

        items = sorted(items, key=lambda i: i.path)
        return items

    def generate_b64(self, path: Path):
        # FROM TEXT TO B64
        path_byte = path.as_posix().encode("utf-8")
        b64_byte = base64.b64encode(path_byte)
        b64_text = b64_byte.decode("utf-8")
        return b64_text

    def generate_item(self, item: Path, parent=False):
        # path = str(item).replace(str(self.base_path) + "/", "")
        b64 = self.generate_b64(item)

        fs = FSItem(
            name=item.name,
            path=item.as_posix(),
            b64=b64,
            isFile=item.is_file(),
            isDir=item.is_dir(),
            parent=parent,
        )
        return fs

    def filter_validate(self, path: Path) -> bool:

        if path.is_file():
            if len(self.allowed_ext) > 0 and path.suffix not in self.allowed_ext:
                return False
            return True

        if path.is_dir():
            return True
