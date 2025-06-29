import pandas as pd

class Reader(object):
  def parse(self, file_data, sheets=0):
    self.workbook = pd.read_excel(file_data, sheets)
    return self.workbook