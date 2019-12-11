import numpy as np

if __name__ == '__main__':
    # numbers = []
    # print(np.percentile(numbers, 25))

    numbers = [1]
    print(np.percentile(numbers, 25))

    numbers = [1, 2]
    print(np.percentile(numbers, 25))

    numbers = range(3)
    print(np.percentile(numbers, 25))

    numbers = range(10)
    print(np.percentile(numbers, 25))
