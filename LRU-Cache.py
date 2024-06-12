# CMPE 250 PROJECT4
import math
import random
from collections import deque

# Global Variables
policies = {"dm", "associative"}
validBlockSizes = {1, 2, 4, 8}
indexUnit = ""
userInputAddresses = []
simulationList = []
instructionList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                  20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                  20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                  20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                  40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                  40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                  40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]


class LRUCache:

    def __init__(self, size: int, capacity: int) -> None:
        """
        :param size: Number of indexes in cache
        :param capacity: Capacity at each index (n)
        """
        self.size = size
        self.capacity = capacity
        self.map = {i: deque() for i in range(size)}
        self.hits = 0
        self.misses = 0
        self.hitRate = None
        self.missRate = None

    def searchCache(self, word_Address: int) -> None:
        """
        Searches cache for specified address. Prints miss or hit and uses LRU replacement policy.
        :param word_Address: Address to search for in cache
        """

        blockAddress = int(word_Address) // int(words_per_block)
        #print(blockAddress)
        cacheIndex = blockAddress % self.size
        print("Address: " + str(word_Address) + " is located at index " + str(cacheIndex) + " in cache")
        key = cacheIndex
        queue = self.map[key]

        if blockAddress in queue:
            self.hits += 1
            self.updateHitRate()
            print("Address: " + str(word_Address) + " is a hit")
            self.map[key].remove(blockAddress)
            self.map[key].append(blockAddress)
        else:
            self.misses += 1
            self.updateHitRate()
            print("Address: " + str(word_Address) + " is a miss")
            if len(self.map[key]) == self.capacity:
                self.map[key].popleft()
                self.map[key].append(blockAddress)
            else:
                self.map[key].append(blockAddress)

    def updateHitRate(self) -> None:
        """
        Updates hit rate of cache
        """
        self.hitRate = (self.hits / (self.hits + self.misses)) * 100
        self.missRate = 100 - self.hitRate

    def clear(self) -> None:
        """
        Clears cache dictionary, resets hits, misses, and hit rate.
        """
        for hashValue in self.map.keys():
            self.map[hashValue].clear()
        self.hits = 0
        self.misses = 0
        self.hitRate = None

    def printCache(self) -> None:
        """
        Prints out cache dictionary
        """
        print(self.map)
        print("Hits = " + str(self.hits) + ", Misses = " + str(self.misses) + ", Hit Rate = " + str(self.hitRate) + "%" + ", Miss Rate = " + str(self.missRate) + "%" )


def getNumBlocks(nomSize: int, wordsPerBlock: int) -> int:
    """
    This function divides the nominal size by the number of bytes per blocks
    :param nomSize: Nominal size of the cache
    :param wordsPerBlock: Number of words per block in the cache
    :return: The number of blocks in the cache
    """
    bytesPerBlock = wordsPerBlock * 4
    return nomSize // bytesPerBlock


def getNumSets(blocks: int, nSet: int) -> int:
    """
    This function floor divides the number of blocks by N (N-set Associative Cache)
    :param blocks: Number of blocks in cache
    :param nSet: N from size of N-Set Associative
    :return: The number of sets in the cache
    """
    return blocks // nSet


def getIndex(numOfUnits: int) -> int:
    """
    This function takes the log base 2 of the number of blocks OR sets in the cache.
    :param numOfUnits: Number of Blocks OR Sets per block
    :return: The number of bits in the Index
    """
    return int(math.log2(numOfUnits))


def getOffset(bytesPerBlock: int) -> int:
    """
    This function takes the log base 2 of the bytes per block in a cache
    :param bytesPerBlock: Number of Bytes per block
    :return: The number of bits in the Offset
    """
    return int(math.log2(bytesPerBlock))


def getTag(index: int, offset: int) -> int:
    """
    This function takes the address length (32 bits) and subtracts the number of bits in the index and offset.
    :param index: Number of sets in the address index
    :param offset: Number of bits in the address offset
    :return: The number of bits in the tag
    """
    return 32 - (index + offset)


def getStatus(nSet: int) -> int:
    """
    This function takes 1 valid bit plus the log base 2 of the N size of the set associative cache
    :param nSet: Number of sets in the address index
    :return: The status bits
    """
    return int(1 + math.log2(nSet))


def getRealSize(nomSize: int, numBlocks: int, tag: int, status: int) -> float:
    """
    This function calculates the real size of a cache
    :param nomSize: Nominal size of the cache
    :param numBlocks: Number of blocks in the cache
    :param tag: Number of bits in the tag
    :param status: Status bits
    :return: Real size
    """
    return nomSize + numBlocks * ((tag + status) / 8)


class setAssociative:
    """
    Class for N-Set-Associative Cache. Stores all information about sizing and addressing for cache.
    """

    def __init__(self, nomSize: int, wordsPerBlock: int) -> None:
        """
        :param nomSize: Nominal size of the cache
        :param wordsPerBlock: Number of words per block in the cache
        """
        self.numBlocks = int(getNumBlocks(nomSize, wordsPerBlock))
        self.numSets = getNumSets(self.numBlocks, n)
        self.index = int(getIndex(self.numSets))
        self.offset = int(getOffset(wordsPerBlock * 4))
        self.tag = int(getTag(self.index, self.offset))
        self.status = int(getStatus(n))
        self.realSize = getRealSize(nomSize, self.numBlocks, self.tag, self.status)

    def printInfo(self) -> None:
        print("Number of blocks: \n", self.numBlocks)
        print("Number of sets: \n", self.numSets)
        print("Index(bits): \n", self.index)
        print("Offset(bits): \n", self.offset)
        print("Tag(bits): \n", self.tag)
        print("Real size: \n", self.realSize)


class directMapped:
    """
    Class for Direct Mapped Cache. Stores all information about sizing and addressing for cache.
    """

    def __init__(self, nomSize: int, wordsPerBlock: int) -> None:
        """
        :param nomSize: Nominal size of the cache
        :param wordsPerBlock: Number of words per block in the cache
        """
        self.numBlocks = int(getNumBlocks(nomSize, wordsPerBlock))
        self.index = int(getIndex(self.numBlocks))
        self.offset = int(getOffset(wordsPerBlock * 4))
        self.tag = int(getTag(self.index, self.offset))
        self.status = 1
        self.realSize = getRealSize(nomSize, self.numBlocks, self.tag, self.status)

    def printInfo(self) -> None:
        print("Number of blocks: \n", self.numBlocks)
        print("Index(bits): \n", self.index)
        print("Offset(bits): \n", self.offset)
        print("Tag(bits): \n", self.tag)
        print("Real size: \n", self.realSize)


nominalSize = int(input("Please enter the nominal size of cache in bytes (Must be power of 2): \n"))
while math.ceil(math.log2(nominalSize)) != math.floor(math.log2(nominalSize)):
    nominalSize = int(input("Invalid input, nominal size must be a power of 2. \n"))

words_per_block = int(input("Please enter the number of words per block: \n"))
while words_per_block not in validBlockSizes:
    words_per_block = int(input("Please enter the number of words per block: \n"))

map_policy = input("Please enter mapping policy ('dm' or 'associative'): \n").lower()
while map_policy not in policies:
    map_policy = input("Invalid policy, enter 'dm' or 'associative': \n").lower()

if map_policy == "dm":
    directCache = directMapped(nominalSize, words_per_block)
    directCache.printInfo()
    cache = LRUCache(directCache.numBlocks, 1)
    indexUnit = directCache.numBlocks

elif map_policy == "associative":
    n = int(input("Please enter number of ways: \n"))
    associativeCache = setAssociative(nominalSize, words_per_block)
    associativeCache.printInfo()
    cache = LRUCache(associativeCache.numSets, n)
    indexUnit = associativeCache.numBlocks

else:
    print("Invalid Map Policy")
    exit(99)

# Ask user for simulation or manual mode
# if sim ask for number of inputs
# 
    
# the exponent of the nominal size is the starting block that is populated in simulation, and then continues
# from that block onward

wordAddressInputMethod = input("Please select which method to input word addresses ('s' for simulation or 'm' for "
                               "manual): \n")
if wordAddressInputMethod == 's':
    startingBlock = int(math.log2(nominalSize)*2)
    # Calculate starting block based on nominal size, if nominal size is
    # 256, then starting block is 8, for example
    randOrLocality = input("Please input whether you want random addresses, or locality using instructions (R - "
                           "Random, ""L - Locality):\n").lower()
    if randOrLocality == "r":
        wordAddressQuantity = int(input("Please input the quantity of word addresses you'd like to simulate: \n"))
        for i in range(wordAddressQuantity):
            simulationList.append(random.randrange(getNumBlocks(nominalSize, words_per_block) * 4))

        random.shuffle(simulationList)

        for i in simulationList:
            cache.searchCache(i)

    elif randOrLocality == "l":
        numInstructions = int(input("Enter the number of instruction sets you would like to parse\n"))
        for i in range(1, numInstructions+1):
            for j in instructionList:
                cache.searchCache(j*i)

    totalAccesses = cache.hits + cache.misses
    missRate = (cache.misses / totalAccesses) * 100
    hitRate = 100 - missRate
    print("Miss rate of simulation:", missRate, "%")
    print("Hit rate of simulation:", hitRate, "%")
    cache.printCache()
    print("Simulation values: " + str(simulationList))

    
elif wordAddressInputMethod == 'm':
    wordAddress = input("Please enter address of word (q=quit, c=clear p=print): \n")
    while wordAddress != 'q':
        userInputAddresses.append(wordAddress)
        if wordAddress == 'c':
            cache.clear()
            userInputAddresses.clear()
            wordAddress = input("Please enter address of word (q=quit, c=clear, p=print): \n")
        elif wordAddress == 'p':
            print("User Accesses")
            print(userInputAddresses)
            print("\n")
            print("Cache")
            cache.printCache()
            wordAddress = input("Please enter address of word (q=quit, c=clear, p=print): \n")
        else:
            cache.searchCache(int(wordAddress))
            wordAddress = input("Please enter address of word (q=quit, c=clear, p=print): \n")
else:
    print("Invalid Input Method")
    exit(99)
print("Cache emulator created by Jade Kimmel, Jonathan Jacobs, Joe Rosenberg, and Daniel Tsouri (April 2024).")