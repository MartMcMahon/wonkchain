import json
import hashlib

from time import time


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        self.new_block(prev_hash="prev_hash", proof=100)

    def new_block(self, proof, prev_hash=None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.pending_transactions,
            "proof": proof,
            "prev_hash": prev_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        transaction = {"sender": sender, "recipient": recipient, "amount": amount}
        self.pending_transactions.append(transaction)
        return self.last_block["index"] + 1

    def hash(self, block):
        string_ob = json.dumps(block, sort_keys=True)
        block_string = string_ob.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash
