from pydantic import BaseModel


class FSItem(BaseModel):
    name: str
    path: str
    b64: str
    isFile: bool
    isDir: bool
    parent: bool
