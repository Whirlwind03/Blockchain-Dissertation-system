import hashlib
import time
import json


class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.ctime(timestamp)
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.data, sort_keys=True)}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        print(f"⛏️ Mining block {self.index}...")
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"✅ Block {self.index} mined: {self.hash}")


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 3 

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        prev_block = self.get_latest_block()
        new_block = Block(len(self.chain), prev_block.hash, time.time(), data)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            if curr.hash != curr.calculate_hash():
                print(f"🚨 Invalid hash at block {i}")
                return False
            if curr.previous_hash != prev.hash:
                print(f"🚨 Invalid chain link at block {i}")
                return False
        return True

    def print_chain(self):
        for block in self.chain:
            print(json.dumps(block.__dict__, indent=4, default=str))


def main():
    blockchain = Blockchain()

    while True:
        print("\n--- Blockchain Menu ---")
        print("1. Add a new block")
        print("2. View the blockchain")
        print("3. Validate the chain")
        print("4. Exit")
        print("5. Simulate tampering (Invalidate the Blockchain)")

        choice = input("Choose an option: ")

        if choice == "1":
            event = input("Enter event name: ")
            info = input("Enter event details: ")
            data = {"event": event, "info": info}
            blockchain.add_block(data)

        elif choice == "2":
            blockchain.print_chain()

        elif choice == "3":
            if blockchain.is_chain_valid():
                print("✅ The blockchain is valid.")
            else:
                print("❌ The blockchain is invalid!")

        elif choice == "4":
            print("👋 Exiting.")
            break

        elif choice == "5":
            if len(blockchain.chain) > 1:
                blockchain.chain[1].data = {"event" : "Hacked Match", "info": "Tampered score"}
                print("Block has been tampered with!")
            else:
                print("not enough blocks to tamper.")

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":

    main()

