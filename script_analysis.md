# Bitcoin Script Analysis

Given Script:
OP_DUP OP_HASH160 <PubKeyHash> OP_EQUALVERIFY OP_CHECKSIG

----------------------------------------------------

1. OP_DUP
Duplicates the public key on the stack.

Stack:
[signature, public_key] → [signature, public_key, public_key]

Purpose:
Allows the public key to be used for both hashing and signature verification.

----------------------------------------------------

2. OP_HASH160
Applies HASH160 to the duplicated public key.

HASH160 = RIPEMD160(SHA256(data))

Stack:
[signature, public_key, public_key] 
→ [signature, public_key, pubKeyHash]

----------------------------------------------------

3. <PubKeyHash>
Pushes the expected public key hash from the locking script.

Stack:
[signature, public_key, pubKeyHash, expectedPubKeyHash]

----------------------------------------------------

4. OP_EQUALVERIFY

Checks if:

pubKeyHash == expectedPubKeyHash

If FALSE → transaction fails immediately.

If TRUE → removes both hashes and continues.

Stack:
[signature, public_key]

----------------------------------------------------

5. OP_CHECKSIG

Uses the public key to verify the signature.

Input:
signature
public_key

If valid:
TRUE is pushed to stack.

If invalid:
FALSE → transaction fails.

----------------------------------------------------

If Signature Verification Fails

OP_CHECKSIG returns FALSE.
The script fails.
The transaction cannot spend the output.

----------------------------------------------------

Security Benefits of Hash Verification

1. Protects public keys until spending
Public keys are hidden until the transaction is spent.

2. Prevents key substitution attacks
Only the correct public key matching the hash can unlock the funds.

3. Reduces blockchain data size
Hashes are smaller than full public keys.

4. Protects against quantum attacks (partially)
Public keys remain hidden until necessary.

----------------------------------------------------

Data Flow Diagram

Unlocking Script (scriptSig):
[signature] [public_key]

Locking Script (scriptPubKey):
OP_DUP
OP_HASH160
<PubKeyHash>
OP_EQUALVERIFY
OP_CHECKSIG


Data Flow:

signature public_key
      │
      ▼
OP_DUP
      │
      ▼
OP_HASH160
      │
      ▼
Compare with PubKeyHash
      │
      ▼
OP_EQUALVERIFY
      │
      ▼
OP_CHECKSIG
      │
      ▼
Transaction Valid
