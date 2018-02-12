import threading


class AtomicCounter:
    """
    Atomic counter inspired by Java AtomicInteger
    """
    def __init__(self, initial_value=0, step=1):
        """
        Initialize a new counter with starting number and incremental step
        :param initial_value: <int>
        :param step: <int>
        """
        self.__initial_value = initial_value
        self.__value = initial_value
        self.__step = step
        self.__lock = threading.Lock()

    def incrementAndGet(self):
        """
        Thread-safe returns of the next number of the counter
        :return:
        """
        with self.__lock:
            self.__value += self.__step
            return self.__value

    def reset(self):
        """
        Resets the counter to the initial value
        """
        with self.__lock:
            self.__value = self.__initial_value
