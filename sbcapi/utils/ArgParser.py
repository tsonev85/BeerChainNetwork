import argparse, json


class ArgParser:

    __instance = None

    def __init__(self):
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument('-u', '--url', type=str, help='host url of the node')
        self.__parser.add_argument('-p', '--port', type=int, help='port to listen on')
        self.__parser.add_argument('-d', '--debug', type=str2bool,
                                   help='enable or disable debug mode <bool>')
        self.__parser.add_argument('-f', '--faucet', type=str, help='faucet url')
        self.__args = self.__parser.parse_args()

        cfg_file = open("node_config.json", "r")
        cfg = json.load(cfg_file)

        if self.__args.url is None:
            self.__args.url = cfg['node_host']

        if self.__args.port is None:
            self.__args.port = int(cfg['node_port'])

        if self.__args.debug is None:
            self.__args.debug = bool(cfg['node_debug'])

        if self.__args.faucet is None:
            self.__args.faucet = cfg['faucet_url']

        print(self.__args)

    @staticmethod
    def get_args():
        if ArgParser.__instance is None:
            ArgParser.__instance = ArgParser()
        return ArgParser.__instance.__args


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')