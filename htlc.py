import hashlib
import time

# ---------- Utility Functions ----------

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Sample secret
secret = "atomic_swap_secret"

# Create hash
hash_value = sha256(secret)

# Timeout (21 minutes)
timeout_seconds = 21 * 60

# ---------- HTLC Script ----------

htlc_script = f"""
OP_IF
    OP_HASH256 {hash_value} OP_EQUALVERIFY
    <Alice_PublicKey> OP_CHECKSIG
OP_ELSE
    {timeout_seconds} OP_CHECKLOCKTIMEVERIFY OP_DROP
    <Bob_PublicKey> OP_CHECKSIG
OP_ENDIF
"""

# ---------- Claim Transaction ----------

claim_script = f"""
<signature_Alice>
{secret}
OP_TRUE
"""

# ---------- Refund Transaction ----------

refund_script = f"""
<signature_Bob>
OP_FALSE
"""

# ---------- Simulation ----------

def simulate_claim(secret_attempt):

    if sha256(secret_attempt) == hash_value:
        return "Alice successfully claims the funds."
    else:
        return "Claim failed: incorrect secret."

def simulate_refund(elapsed_time):

    if elapsed_time >= timeout_seconds:
        return "Bob refunds the funds after timeout."
    else:
        return "Refund not allowed yet."


# ---------- Testing ----------

claim_result = simulate_claim(secret)
refund_result_before = simulate_refund(600)
refund_result_after = simulate_refund(1300)

# ---------- Save Output ----------

with open("output.txt", "w") as f:

    f.write("=== HTLC Script ===\n")
    f.write(htlc_script)

    f.write("\n=== Claim Transaction Script ===\n")
    f.write(claim_script)

    f.write("\n=== Refund Transaction Script ===\n")
    f.write(refund_script)

    f.write("\n=== Test Results ===\n")
    f.write(f"Secret Hash: {hash_value}\n")
    f.write(f"Claim Result: {claim_result}\n")
    f.write(f"Refund Before Timeout: {refund_result_before}\n")
    f.write(f"Refund After Timeout: {refund_result_after}\n")

print("HTLC scripts and test results saved to output.txt")
