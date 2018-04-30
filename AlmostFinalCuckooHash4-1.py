# Sarah Engel
# April 29th, 2018
# Professor Broder
# Data Structures

import random
import BitHash
import math

# Key Object
# Using to store the key/data pairs that will be used by 
# the hash tables. Better for my implementation and 
# later manipulation needs. 
class Key(object):
    
    # Constructor
    def __init__(self, key, data):
        self.key = key
        self.data = data
    
    def __str__(self):
        return str(self.key) + ", " + str(self.data)
        

class CuckooHash(object):
    
    # Constructor
    def __init__(self, size = 1000):
        self.__hashArr = [None] * size                  # default size is 1000
        self.__numRecords = 0
        self.__numBuckets = 2 * len(self.__hashArr)     # Same lengths
        self.__threshold = 0                            # num of hashes counter
      
    # Adopted from hashTabHW.py
    def __hashFunc(self, s, h = 0): 
        bucketOne = BitHash.BitHash(s, h)
        bucketTwo = BitHash.BitHash(s, bucketOne)
        
        # now using mod
        bucketOne = bucketOne % len(self.__hashArr) 
        bucketTwo = bucketTwo % len(self.__hashArr)
        
        return bucketOne, bucketTwo
    
    # Insertion method
    def insert(self, key, data):

        # Initialize key object 
        k = Key(key, data)
        
        # The conditional statement is sort of odd, for k can never be
        # set to None within our loop. However, it will return upon
        # finishing a cuckoo round, and exit the loop, thus this conditional
        # statement just keeps the hash going while in the cuckoo phase
        while k:
             
            # Hash the two possible nests
            buckets = self.__hashFunc(k.key)
            bOne = buckets[0]
            bTwo = buckets[1]
            
            # Checking for growth needs
            if self.__numRecords >=  0.5 * self.__numBuckets: 
                self.growHash() 
                
            # Checking for reset needs
            if self.__threshold >= 100:
                # Grow the hashArray - which rehashes all of our values 
                # anyways using the new bitHash random factor
                self.growHash()
                # reset threshold
                self.__threshold = 0
                
            # Maybe this key has already been inserted, check
            # if it had already been inserted, then we're done
            # Not allowing double copies
            if self.__hashArr[bOne] == k:
                return True 
            
            # Otherwise, if the hash is empty at our bucket in 
            # insert our key, data at that place in our
            # given hash array
            elif self.__hashArr[bOne] == None:
                self.__hashArr[bOne] = k
                self.__numRecords += 1
                return True 
            
            # Now do the same checks for bucketTwo
            
            # Maybe this key has already been inserted, check
            # if it had already been inserted, then we're done
            elif self.__hashArr[bTwo] == k:
                return True 
            
            # Otherwise, if the hash is empty at our bucket in 
            # insert our key, data at that place in our
            # given hash array
            elif self.__hashArr[bTwo] == None:
                self.__hashArr[bTwo] = k
                self.__numRecords += 1
                return True 
            
            # Cuckoo Phase
            else:
                # evicting what's in bucketOne and storing it in temp
                temp = Key(self.__hashArr[bOne].key, self.__hashArr[bOne].data)
                
                # In its stead, putting a new key object containing k's data
                newK = Key(k.key, k.data)
                self.__hashArr[bOne] = newK
                
                # Reassinging k to temp for the rest of the while loop
                # now it runs through the loop again, with k
                # holding a reference to temp's   
                k = temp
                self.__threshold += 1
            
    
    # Accessor, used in the growHash method
    def getArr(self):         
        return self.__hashArr 
    
    # Grow hash  method              
    def growHash(self):
        
        # Reset the bitHash
        BitHash.ResetBitHash()
        
        # Create new Cuckoo Hash
        tempHash = CuckooHash(2 * len(self.__hashArr))
        
        # update the attribute self.__numBuckets
        self.__numBuckets = len(tempHash.getArr())
        
        # rehash all of the keys from both hash tables,
        # insert into bigger hash tables in the new cuckoo hash
        # using our insert which automatically hashes each key
        for i in range(0, len(self.__hashArr)):
            
            # Skipping the empty buckets
            if self.__hashArr[i]:
                tempHash.insert(self.__hashArr[i].key, self.__hashArr[i].data)               
                
        # reassign back the new cuckoo hash array to our internal
        # hash array 
        self.__hashArr = tempHash.getArr()         
      
            
    # Check either of the nests that belong to the specified key. 
    # The key could only possibly be in one of the two nests.
    # Returns data if found, else None  
    def findKey(self, key):
        
        # Hash the two possible nests
        buckets = self.__hashFunc(key)
        bOne = buckets[0]
        bTwo = buckets[1]
        
        if self.__hashArr[bOne] and self.__hashArr[bOne].key == key:
            return self.__hashArr[bOne].data
        
        # Checking hashTwo
        elif self.__hashArr[bTwo] and self.__hashArr[bTwo].key == key:
            return self.__hashArr[bTwo].data
        
        else: # if not found
            return None 
        
    def deleteKey(self, key):
        # Check either of the nests that belong to the specified key. 
        # The key could only possibly be in one of the two nests.
        # If you found the key, remove the key/data pair from the nest.
        
        # Hash the two possible nests
        buckets = self.__hashFunc(key)
        bOne = buckets[0]
        bTwo = buckets[1]
        
        # Checking in bucket one, deleting by replacing with None
        # if found. 
        if self.__hashArr[bOne] and self.__hashArr[bOne].key == key:
            self.__hashArr[bOne] = None
            return True
        
        # Checking in bucket two, deleting by replacing with None
        # if the desired item is found. 
        elif self.__hashArr[bTwo] and self.__hashArr[bTwo].key == key:
            self.__hashArr[bTwo] = None
            return True
        
        # If it's not there, return False
        else:
            return False
       

    
def __main():
    
    # spacing
    print("")
    
    print("TESTING: Insert with overflow")
    trial1 = CuckooHash(3)
    numIn = 0
    size = 100
    print("Inserted " + str(size) + " elements to overflow")
    for i in range(0, size):
        
        # generating string key
        key = chr(i + 65)
        
        # generating random letter for data
        data = str(i)
        
        n = Key(key, data)
        
        # inserting
        trial1.insert(n.key, n.data)
        numIn += 1   

    # Checking that counter matches size intention
    if numIn == size:
        print("SUCCESS: this cuckoo was able to rehash and grow.")
    else:
        print("Insertions failed.")  
    
   
    # TESTING FIND KEY
        
    # spacing
    print()
    print("TESTING: findKey()")
    
    keepTrack = [None] * 1000      # array keeping track of attempted inputs
    trial2 = CuckooHash(11)        # Tiny hash to help with print statements
    counter = 0                    # Number of successful inserts         
    
    # Inserting, not overflowing 
    for i in range(0, 5):
        
        # generating random string key
        key = str(random.randint(1, 100000))
        
        # generating random letter for data
        data = chr(random.randint(65, 123))
        
        n = Key(key, data)
        
        # updating list of values that should have been found 
        keepTrack[i] = n
        
        # inserting into our cuckoo hash
        trial2.insert(n.key, n.data)
        print("Inserted: " + str(n))
        counter += 1
    
    
    # Checking if each insertion into the hash matches our artificial
    # insertions into the parallel list
    numFilled = 0
    for i in range(0, len(keepTrack)):
        if keepTrack[i]:
            numFilled += 1
    
    # Automated message if actual insertions to hash matched insertions
    # to the side-by-side table. 
    if counter == numFilled:
        print("SUCCESS: All desired elements inserted successfully") 
    else:
        print("FAILED: Unsuccessful insertion by a margin of " + \
              str(math.abs(counter - numFilled)) + " discrepancies")

    # Testing findKey specifically on this hash. Should return 0 mistakes
    # especially since the above test code, if successful, should have
    # established that all of the insertions were successful. 
    numMistakes = 0  
    
    print()
    for i in range(0, len(keepTrack)): 
        # If there was a key inserted into the hash here, and its returned
        # data after being passed through findKey() does not match its actual
        # data, increment the number of mistakes
        if keepTrack[i]: 
            if (trial2.findKey(keepTrack[i].key) is not keepTrack[i].data):
                result = False
            else:
                result = True
            print("In arr: " + str(keepTrack[i]) + " and it's " + str(result) + \
                  " that findKey worked finding data " + \
                  str(trial2.findKey(keepTrack[i].key)))
        if keepTrack[i] and (trial2.findKey(keepTrack[i].key) is not keepTrack[i].data): 
                numMistakes += 1

    print("While testing findKey() without overflow, there were " + \
          str(numMistakes)  + " mistakes.")
    
    # output spacing
    print()
    
    # TESTING DELETEKEY
    print("TESTING: deleteKey()")
    
    trial3 = CuckooHash(5)
    trial3.insert("a", "data")
    trial3.insert("b", "data")
    
    # trying to delete something not there
    result = trial3.deleteKey("Sarah")
    print("Feeding the method a fake key, expected result: False")
    print("Result: " + str(result))
    
    # Testing delete works with a true case
    result = trial3.deleteKey("a")
    print("Feeding the method a valid key, expected result: True")
    print("Result: " + str(result))    
    
    
if __name__ == '__main__':
    __main()