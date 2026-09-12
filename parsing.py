from pydantic import BaseModel, Field
import typing

def parse(configfile: typing.IO[str]) -> None:
    data: str = configfile.read()
    print(data)
