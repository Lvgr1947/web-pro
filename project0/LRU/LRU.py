class LRUcache :
    def _init_(self):
        self.input=[]

    def put(self,number):
        self.input.append(number)

    def get(self):
        return self.input.pop()

    def get_cache(self):
        return self.input


class LRUTest:

    def _init_(self):
        self.LRUcacheobject = LRUcache()
        self.count =0

    def put_test(self):
        self.LRUcacheobject.put(7)
        self.LRUcacheobject.put(10)
        try:
            assert self.LRUcacheobject.input == [7,10]
            self.count += 1
        except Exception as e:
            print("put function doesn't work.")
        
        

    def get_test(self):
        value = self.LRUcacheobject.get()
        try:
            assert self.LRUcacheobject.input == [7]
            self.count += 1
        except Exception as e:
            print("get function doesn't work.")
        
        

    def get_cache_test(self):
        value1 = self.LRUcacheobject.get_cache()
        try:
            assert value1 == self.LRUcacheobject.input
            self.count += 1
        except Exception as e:
            print("get_cache function doesn't work.")
        



def main():
    LRUTestobject = LRUTest()
    LRUTestobject.put_test()
    LRUTestobject.get_test()
    LRUTestobject.get_cache_test()
    if LRUTestobject.count == 3:
        print ("All Test cases passed")

if _name_ == "_
main_":
    main()