# -------------------------------------------------
# encode.py - 256/128k test
# MIT LICENSE
# MESUT ERTURHAN
# https://github.com/piyxu/256bits-to-128k-rank-5bit-x21--metadata/21x_balanced
# -------------------------------------------------

from math import comb
import random

# -------------------------------------------------
#  Combination Rank / Unrank (fixed n, k)
# -------------------------------------------------

def unrank_nk(n: int, k: int, r: int):
    """
    Lexicographic combinational unrank.
    0 <= r < C(n,k)
    """
    bits = []
    rem = k
    for i in range(n):
        z = comb(n - i - 1, rem) if rem <= (n - i - 1) else 0
        if r < z:
            bits.append(0)
        else:
            bits.append(1)
            r -= z
            rem -= 1
    return bits

def rank_nk(bits, k_fixed: int):
    """
    Lexicographic combinational rank with fixed k.
    """
    n = len(bits)
    rem = k_fixed
    r = 0
    for i, b in enumerate(bits):
        if b == 1:
            z = comb(n - i - 1, rem)
            r += z
            rem -= 1
    return r

# -------------------------------------------------
#  256 / 128k helpers
# -------------------------------------------------


def unrank_256_128(r: int):
    return unrank_nk(256, 128, r)

def rank_256_128(bits):
    return rank_nk(bits, 128)

C256 = comb(256, 128)
FULL_SPACE_256 = 1 << 256
POOL_COUNT = 32
POOL_SIZE = (FULL_SPACE_256 + POOL_COUNT - 1) // POOL_COUNT
MASK_256 = FULL_SPACE_256 - 1  # 256-bit masking

def encode256(R: int):

    if not (0 <= R < POOL_COUNT * POOL_SIZE):
        raise ValueError("R must be in [0, 32*POOL_SIZE)")

    m   = R // POOL_SIZE
    idx = R  % POOL_SIZE
    bits256 = unrank_256_128(idx)
    return bits256, m
    
# -------------------------------------------------
#  MAIN PROGRAM
# -------------------------------------------------

def main():
    num_tests = 50  # increase/decrease if you like

    with open("originals.txt", "w") as f_ori, \
         open("encode.txt", "w") as f_enc:

        for _ in range(num_tests):
            R = random.getrandbits(256)

            # originals.txt: 256-bit view of R (upper bits are discarded by masking)
            ori_bits = format(R & MASK_256, "0256b")
            f_ori.write(ori_bits + "\n")

            # encode: R -> (balanced_256, m)
            bits256, m = encode256(R)

            meta_bin = format(m, "05b")
            enc_bits = "".join(str(b) for b in bits256)

            f_enc.write(meta_bin + enc_bits + "\n")

    print("Encode completed → originals.txt, encode.txt")

if __name__ == "__main__":
    main()
