from peewee import Model
from config.settings import db

class BaseModel(Model):
    class Meta:
        database = db