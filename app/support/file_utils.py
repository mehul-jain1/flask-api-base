import time
import os

def get_unique_file_name(file_name, user_name):
  file_split_up_name = os.path.splitext(file_name)
  file_name, file_extension = file_split_up_name

  current_time = int(time.time())
  username = user_name.lower()
  
  return f"{file_name}_{username}_{current_time}{file_extension}"

def lowercase(dataframe, columns):
  # convert to lowercase and also trim whitespaces on both sides of string
  for column in columns:
    dataframe[column] = dataframe[column].str.strip().str.lower()