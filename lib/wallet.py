from lib.util import Util
utils = Util()


class Wallet:
    def __init__(self, seed):
        self.seed = seed
        self.addresses = {}
        self.generate_address()

    def generate_address(self):
        address = utils.hash(str(self.seed) + str(len(self.addresses)))
        self.addresses[address] = 0
        return address

    def getWalletAddresses(self):
        return self.addresses

    def getbalance(self, address):
        if address in self.addresses.keys():
            return self.addresses[address]
        else:
            print "[-] This wallet does not have such an address!! (%s)" % address
            return None

    def deposit(self, address, amount):
        if address in self.addresses.keys():
            self.addresses[address] += amount
            print "[+] Deposit Successful. Current Balance: (%s)" % str(self.addresses[address])
            return self.addresses[address]
        else:
            print "[-] This wallet does not have such an address!! (%s)" % address
            return None

    def withdraw(self, address, amount):
        if address in self.addresses.keys():
            if amount >= self.addresses[address]:
                self.addresses[address] -= amount
                print "[+] Withdraw Successful. Current Balance: (%s)" % str(self.addresses[address])
                return self.addresses[address]
        else:
            print "[-] This wallet does not have such an address!! (%s)" % address
            return None