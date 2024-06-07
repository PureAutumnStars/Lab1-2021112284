from DataProcessing import *
from BackendUtils import *


if __name__ == "__main__":
    nx_graph, word_list, G = text_to_graph(TEST_FILE_PATH)

    word_1, word_2 = input_query()

    queryBridgeWords(G, word_1, word_2)
