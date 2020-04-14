import csv
import configparser
import os
from Core.Logger import LOGGER
from Core.Conf import cfg
logger = LOGGER.attach(__name__)

class IO:


    map = {}

    def dump(self, data, path):
        if IO.verify(path):
            with open(path, "w+", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for d in data:
                    writer.writerow([d])

    @staticmethod
    def write(path, table):
        if path == "" or path is None:
            return
        path = cfg["IO"]["data_path"] + path + ".csv"
        print("Attempting to write to ", path, end="\r")
        logger.info("Attempting to write to " + str(path))
        if IO.verify(path):
            print("Writing to ", path, end="\r")
            logger.info("Writing to " + str(path))
            with open(path, 'w+', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(["state", "state", "turn", "score", "value", "visits"])
                for state, node in table.items():
                    writer.writerow([state[0], state[1], state[2], node[0], node[1], node[2]])
            print("Completed writing : ", len(table), " rows to ", path)
            logger.info("Completed writing : " +str(len(table)) + " rows to " + str(path))
        else:
            logger.error("IO ERROR ON " + str(path))
            print("IO error on ", path)


    @staticmethod
    def list(path):
        path = cfg["IO"]["data_path"] + path
        return os.listdir(path)

    @staticmethod
    def load(path):

        if path == "" or path is None:
            return {}

        path = cfg["IO"]["data_path"] + path + ".csv"
        data = {}

        if path in IO.map:
            print("Already loaded ", path, " returning : ", len(IO.map[path]), " rows")
            logger.info("Already loaded " + str(path) + " returning : " + str(len(IO.map[path])) + " rows")
            return IO.map[path]

        print("Attemping to load ", path, end="\r")
        logger.info("Attemping to load " + str(path))
        if IO.verify(path):
            print("Loading ", path, end="\t\t\r")
            logger.info("Loading " + str(path))
            with open(path, 'r+') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                headers = True
                for row in reader:
                    if headers:
                        headers = False
                        continue
                    try:
                        data[tuple([int(row[0]), int(row[1]), int(row[2])])] = (
                    float(row[3]), float(row[4]), int(row[5]))
                    except Exception as e:
                        print(e)
                        print("error loading row: ", row)
                        logger.exception(e)
                        logger.error("Error loading row: " + str(row))
        else:
            logger.error("IO error on " + str(path))
            print("IO error on ", path)

        print("Loaded data, length: ", len(data), " from: ", path)
        logger.info("Loaded data, length: " + str(len(data)) + " from: " + str(path))
        IO.map[path] = data
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
            logger.error("Couldn't load " + str(path))
            return False
        return True