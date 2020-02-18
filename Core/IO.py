import configparser
import os

class IO:

    @staticmethod
    def write(path, table, headers, ):
        cfg = configparser.ConfigParser()
        cfg.read("config.ini")

        if not os.path.isdir(cfg["IO"]["data"]):
            os.makedirs(cfg["IO"]["data"])

        pass

    @staticmethod
    def load():
        pass


    '''
def save_data(self, path):
      print("Saving data now.")

      if not os.path.isdir(self.get_name()):
          os.makedirs(self.get_name())

      if not os.path.isfile(self.get_name() + "/" + path):
          f = open(self.get_name() + "/" + path, "w+")
          f.close()
      with open(self.get_name() + "/" + path, 'w', newline='') as csvfile:
          writer = csv.writer(csvfile, delimiter=',')
          writer.writerow(["state", "state", "turn", "visit count", "score", "value"])
          for state, node in self.tree_data.items():
              writer.writerow([state[0], state[1], state[2], node[0], node[1], node[2]])
      print("Completed writing : ", len(self.tree_data), " rows to ", path)

  def load_data(self, path):
      print("Loading Tree data, ", path)
      self.tree_data = {}

      if not os.path.isdir(self.get_name()):
          os.makedirs(self.get_name())

      if not os.path.isfile(self.get_name() + "/" + path):
          f = open(self.get_name() + "/" + path, "w+")
          f.close()

      with open(self.get_name() + "/" + path, 'r') as csvfile:
          reader = csv.reader(csvfile, delimiter=',')
          headers = True
          for row in reader:
              if headers:
                  headers = False
                  continue

              try:
                  self.tree_data[tuple([int(row[0]), int(row[1]), int(row[2])])] = (int(row[3]), float(row[4]), float(row[5]))
              except Exception as e:
                  print(e)
                  print("error loading row: ", row)
      print("Succesfully loaded data, length: ", len(self.tree_data))
      '''