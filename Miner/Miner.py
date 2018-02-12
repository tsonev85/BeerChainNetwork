import threading, concurrent.futures, multiprocessing, time, json
import requests as req
from sbcapi.utils.crypto import CryptoUtils
from sbcapi.threading import AtomicCounter, AtomicBoolean


class Miner(object):

    def __init__(self):
        self.miner_name = None
        self.node_address = None
        self.payment_address = None
        self.parallel_jobs = None

        if not self.init():
            return

        self.nonce = AtomicCounter()
        self.job_finished = AtomicBoolean()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.parallel_jobs)
        self.workers = []
        self.difficulty = ""
        self.hash_to_mine = ""

        print("Miner successfully initialized! Proceeding with mining...")
        self.start()

    def init(self):
        """
        Reads the config file and initialize the miner. Returns True or False, depending if the initializing is done.
        :return: <bool>
        """
        cfg_file = open("miner_config.json", "r")
        cfg = json.load(cfg_file)
        try:
            self.miner_name = cfg['miner_name']
            self.node_address = cfg['node_address']
            self.payment_address = cfg['payment_address']
        except KeyError as err:
            print("Key not found in cfg file: ", err)
            return False
        try:
            self.parallel_jobs = int(cfg['num_parallel_job'])
        except KeyError:
            self.parallel_jobs = multiprocessing.cpu_count()
        return True

    def mine(self):
        """
        Main mining function, loops until a nonce is found to satisfy the network difficulty
        :return:
        """
        if not self.check_difficulty():
            raise Exception("Difficulty is not properly set, mining will not start!")

        if not self.check_hash_to_mine():
            raise Exception("Hash to mine is not properly set")

        while not self.job_finished.get():
            current_nonce = self.nonce.incrementAndGet()
            hash = CryptoUtils.calc_miner_hash(self.hash_to_mine, current_nonce)
            # print(threading.current_thread().getName(), " CHECKING =>> ", hash, " ", current_nonce) #left for debug purposes
            if hash[:len(self.difficulty)] == self.difficulty:
                self.job_finished.compareAndSet(False, True)
                self.submit_result({
                    'miner_name': self.miner_name,
                    'miner_address': self.payment_address,
                    'original_hash': self.hash_to_mine,
                    'mined_hash': hash,
                    'nonce': current_nonce,
                    'difficulty': len(self.difficulty)
                })

    def submit_result(self, result):
        """
        Submits the completed job to the node
        :param <dict> result:
        :return:
        """
        print(str(time.time()), " ", result)
        headers = {'content-type': 'application/json'}
        resp = req.post("http://localhost:5555/heres_beer", data=json.dumps(result), headers=headers)

    def acquire_job(self):
        """
        Requests the node for a hash to mine, if the hash received is the same as previous
        returns False indicating no new work is found. If the hash is different returns True,
        indicating that new hash should be scheduled for mining
        :return: <bool>
        """
        headers = {'content-type': 'application/json'}
        data = {
            "miner_name": self.miner_name,
            "minerAddress": self.payment_address
        }
        resp = req.post("http://localhost:5555/give_me_beer", data=json.dumps(data), headers=headers)
        json_resp = json.loads(resp.content.decode())

        try:
            new_hash = json_resp['hash']
            difficulty = int(json_resp['dificulty'])
        except KeyError as err:
            print(err, " missing from node response! Rescheduling...")
            return False

        if new_hash != self.hash_to_mine:
            self.set_difficulty(difficulty)
            self.set_hash_to_mine(new_hash)
            return True
        else:
            return False

    def run_job(self):
        """
        Creates new threads to mine the hash, based on the parallel configuration
        :return:
        """
        self.job_finished.set(True)
        if len(self.workers) == 0:
            self.job_finished.set(False)
            self.nonce.reset()
        else:
            while len(self.workers) != 0:
                print("Waiting for: ", self.workers)
                for future in self.workers:
                    print("Future: ", future.done())
                    if future.done():
                        self.workers.remove(future)

            self.job_finished.set(False)
            self.nonce.reset()

        for i in range(0, self.parallel_jobs):
            self.workers.append(self.executor.submit(self.mine))

        print("Job Submitted: " + str(self.parallel_jobs) + " threads will mine hash: " + self.hash_to_mine)

    def start(self):
        """
        Main starting point of the miner after initialization.
        Starts the scheduling.
        :return:
        """
        thread = threading.Thread(target=self.schedule)
        thread.start()

    def schedule(self):
        """
        Scheduling a thread to check for new job every xx seconds.
        :return:
        """
        while True:
            new_job_aquired = self.acquire_job()
            if new_job_aquired:
                print(str(time.time()) + " New job aquired! Hash: " + self.hash_to_mine)
                self.run_job()
            else:
                print("No new job aquired... Rescheduling... ")
            time.sleep(60)

    def set_hash_to_mine(self, hash_to_mine):
        """
        Sets new hash to miner
        :param <str> hash_to_mine:
        :return:
        """
        self.hash_to_mine = hash_to_mine

    def check_hash_to_mine(self):
        """
        Validation of hash_to_mine
        :return:
        """
        if len(self.hash_to_mine) <= 0:
            return False

        return True

    def set_difficulty(self, difficulty):
        """
        Sets new difficulty
        :param difficulty:
        :return:
        """
        if isinstance(difficulty, int):
            self.difficulty = "0" * difficulty
        else:
            raise Exception("Provided difficulty is not int")

    def check_difficulty(self):
        """
        Validates difficulty
        :return: <bool>
        """
        if len(self.difficulty) <= 0:
            return False
        if not self.difficulty.isdigit():
            return False
        check = "0" * len(self.difficulty)
        if self.difficulty != check:
            return False

        return True


Miner()
