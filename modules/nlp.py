
import dataset
import random






async def init(self):
  self.db = dataset.connect('sqlite:///database.db')

