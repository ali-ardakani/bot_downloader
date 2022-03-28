from .base_model import BaseModel
from peewee import *
from config.settings import db


class User(BaseModel):
    """This class defines the user table."""

    username = CharField(unique=True)
