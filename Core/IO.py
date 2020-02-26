import csv
import configparser
import os

class IO:

    def dump(self, data, path):
        cfg = configparser.ConfigParser()
        cfg.read("config.ini")
        if IO.verify(path):
            with open(path, "w+", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for d in data:
                    writer.writerow([d])

    @staticmethod
    def write(path, table):
        if path == "" or path is None:
            return
        cfg = configparser.ConfigParser()
        cfg.read("config.ini")
        path = cfg["IO"]["data_path"] + path + ".csv"
        print("Attempting to write to ", path)
        if IO.verify(path):
            print("Writing to ", path)
            with open(path, 'w+', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(["state", "state", "turn", "score", "value", "visits"])
                for state, node in table.items():
                    writer.writerow([state[0], state[1], state[2], node[0], node[1], node[2]])
            print("Completed writing : ", len(table), " rows to ", path)
        else:
            print("IO error on ", path)
    @staticmethod
    def load(path):

        cfg = configparser.ConfigParser()
        cfg.read("config.ini")
        path = cfg["IO"]["data_path"] + path + ".csv"
        data = {}
        print("Attemping to load ", path)
        if IO.verify(path):
            print("Loading ", path)
            with open(path, 'r+') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                headers = True
                for row in reader:
                    if headers:
                        headers = False
                        continue
                    try:
                        data[tuple([int(row[0]), int(row[1]), int(row[2])])] = (
                    int(row[3]), float(row[4]), int(row[5]))
                    except Exception as e:
                        print(e)
                        print("error loading row: ", row)
        else:
            print("IO error on ", path)

        print("Loaded data, length: ", len(data))
        return data

    @staticmethod
    def verify(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            if os.path.isfile(path):
                f = open(path, "r")
            else:
                f = open(path, "w+")
            f.close()
        except:
            print("Couldn't load ", path)
            return False
        return True