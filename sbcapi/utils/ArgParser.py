import argparse


class ArgParser:

    __instance = None

    def __init__(self):
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument('-p', '--port', default=5555, type=int, help='port to listen on')
        self.__parser.add_argument('-d', '--debug', default='True', type=str2bool,
                                   help='enable or disable debug mode <bool>')
        self.__args = self.__parser.parse_args()
        print(self.__args);

    @staticmethod
    def get_args():
        if ArgParser.__instance is None:
            ArgParser.__instance = ArgParser()
        return ArgParser.__instance.__args


def str2bool(v):
    if v.lower() in ('yes', 'true', 'True', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'False', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')