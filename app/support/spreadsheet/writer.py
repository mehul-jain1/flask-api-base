import pandas as pd
import io

class Writer(object):
  def __init__(self):
    pass

  def perform(self, data_frame):
    with io.BytesIO() as output:
      with pd.ExcelWriter(output) as writer:
        data_frame.to_excel(writer)
      file_data = output.getvalue()

    return file_data