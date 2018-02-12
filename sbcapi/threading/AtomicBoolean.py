import threading


class AtomicBoolean:
    """
    AtomicBoolean inspired by java
    """
    def __init__(self, initial_value=False):
        """
        Initialize a new AtomicBoolean with default value false
        :param initial_value: <bool> initial state of the AtomicBoolean
        """
        self.__value = initial_value
        self.__lock = threading.Lock()

    def get(self):
        """
        Returns the current value of the AtomicBoolean
        :return: <bool>
        """
        with self.__lock:
            return self.__value

    def set(self, value):
        """
        Sets new value for the AtomicBoolean
        :param value: <bool>
        """
        with self.__lock:
            self.__value = value

    def getAndSet(self, value):
        """
        Returns the current value and sets a new value to the AtomicBoolean, basically executes swap
        :param value: <bool> new value
        :return: <bool> the current value, before the new value was set
        """
        with self.__lock:
            v = self.__value
            self.__value = value
            return v

    def compareAndSet(self, expected_value, new_value):
        """
        Compares the current value of the AtomicBoolean with an expected value, if the result is true, sets a new value
        and returns True as an output of the operation, if the result is false, does nothing and returns false.
        :param expected_value: <bool>
        :param new_value: <bool>
        :return: <bool>
        """
        with self.__lock:
            if self.__value == expected_value:
                self.__value = new_value
                return True
            else:
                return False
