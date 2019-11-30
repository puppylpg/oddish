if __name__ == '__main__':

    str_list = '[1, 2, 3]'
    str_list = str_list.lstrip('[')
    str_list = str_list.rstrip(']')
    word_list = str_list.split(',')
    print([float(i) for i in word_list])