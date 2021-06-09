 # Class for plug objects

class Plug:
    """class for plug objects"""

#  attributes set in constructor
#     label     # positive odd integer
#     bits      # array of bits, least significant first
#     bitstring # string of bits, least significant first

    def __init__(self, *args):
        """plug constructor accepts plugnumber or bit string"""
        if isinstance(args[0], int):
            self.label = args[0]
        elif isinstance(args[0], str):
            self.label = int(args[0][::-1],2)
        self.makebits()

    def makebits(self):
        """ called from constructor to set attributes"""
        self.bits = [int(b) for b in bin(self.label)[2:]]
        self.bits.reverse()
        self.bitstring = bin(self.label)[2:][::-1]
        
    def get_plugnumber(self):
        """return the plug number (label)"""
        return self.label

    def get_bitlist(self):
        """return array of bits, left to right"""
        return self.bits

    def get_bitstring(self):
        return self.bitstring
    
#  Execute for testing
if __name__ == "__main__":
    print("testing Plug class")

    plugbits = "1011"
    myplug = Plug(plugbits)

    print(f"myplug({plugbits})")
    print(f"label:     {myplug.get_plugnumber()}")
    print(f"bits:      {myplug.get_bitlist()}")
    print(f"bitstring: {myplug.get_bitstring()}")

