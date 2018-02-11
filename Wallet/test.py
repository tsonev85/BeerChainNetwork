from sbcapi.model import *



transaction = Transaction(
    date_added_to_block=time.time(),
    to_address="neshto si",
    value=0,
    sender_pub_key="fgjdjjdj",
    sender_signature="hhtht",
    mined_in_block_index=0
)

prev_block = Block(index=1,
              prev_block_hash="aafaf",
              date_created=99,
              transactions=[transaction],
                   mined_by="0")
prev_block.miner_hash = "aaaa"

new_block = Block(index=2,
              prev_block_hash=prev_block.block_hash,
              date_created=99,
              transactions=[transaction],
                  mined_by="0")
new_block.miner_hash='aaaa'
# print(prev_block.calculate_transactions_hash())
print(Block.is_block_valid(new_block,prev_block))
