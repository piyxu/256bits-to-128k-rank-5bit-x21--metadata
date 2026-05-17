# -------------------------------------------------
# encode.py - 256/128k Balanced Rank Coding
# MIT LICENSE
# MESUT ERTURHAN
# https://github.com/piyxu/256bits-to-128k-rank-5bit-x21--metadata/21x_balanced
# -------------------------------------------------

from math import comb

# -------------------------------------------------
#  Combination Rank / Unrank
# -------------------------------------------------


def unrank_nk(n: int, k: int, r: int):
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
    n = len(bits)
    rem = k_fixed
    r = 0
    for i, b in enumerate(bits):
        if b == 1:
            z = comb(n - i - 1, rem)
            r += z
            rem -= 1
    return r

def unrank_256_128(r: int):
    return unrank_nk(256, 128, r)

def rank_256_128(bits):
    return rank_nk(bits, 128)

C256 = comb(256, 128)
FULL_SPACE_256 = 1 << 256
POOL_RATIO_DENOMINATOR = 100
POOL_TOTAL_NUMERATOR = 272
TOTAL_CAPACITY = (C256 * POOL_TOTAL_NUMERATOR) // POOL_RATIO_DENOMINATOR
METADATA_CODES = ("0", "10", "11")
POOL_SIZES = (
    C256,
    C256,
    TOTAL_CAPACITY - (2 * C256),
)
POOL_STARTS = (
    0,
    POOL_SIZES[0],
    POOL_SIZES[0] + POOL_SIZES[1],
)
MASK_256 = FULL_SPACE_256 - 1

def parse_metadata(enc: str):
    if enc.startswith(METADATA_CODES[0]):
        return 0, len(METADATA_CODES[0])
    if enc.startswith(METADATA_CODES[1]):
        return 1, len(METADATA_CODES[1])
    if enc.startswith(METADATA_CODES[2]):
        return 2, len(METADATA_CODES[2])

    raise ValueError("unknown metadata prefix")

def decode256(bits256, m: int):
    """
    encode256'in tersi:
        bits256 (128 tane 1) + m → R
    """
    idx = rank_256_128(bits256)
    if not (0 <= m < len(POOL_SIZES)):
        raise ValueError("metadata is outside configured pools")
    if not (0 <= idx < POOL_SIZES[m]):
        raise ValueError("idx is outside configured pool size")

    R = POOL_STARTS[m] + idx
    return R

# -------------------------------------------------
#  MAIN PROGRAM
# -------------------------------------------------

def main():
    with open("originals.txt") as f_ori, \
         open("encode.txt") as f_enc, \
         open("decode.txt", "w") as f_dec, \
         open("reports.txt", "w") as f_rep:

        ori_lines = [line.strip() for line in f_ori]
        enc_lines = [line.strip() for line in f_enc]

        for idx, (ori, enc) in enumerate(zip(ori_lines, enc_lines)):

            # encode.txt: prefix meta + 256 bit balanced
            m, meta_len = parse_metadata(enc)
            bits_str = enc[meta_len:]

            bits256 = [int(b) for b in bits_str]

            # ---- decode: only from encode.txt ----
            R2 = decode256(bits256, m)

            # rebuild 256-bit form (same rule as MASK_256)
            dec_bits = format(R2 & MASK_256, "0256b")
            f_dec.write(dec_bits + "\n")

            # ---- K values ----
            k_ori = ori.count("1")
            k_enc = bits_str.count("1")       # expected to be 128
            k_dec = dec_bits.count("1")

            same = "TRUE" if ori == dec_bits else "FALSE"

            f_rep.write(
                f"{idx:03d}: "
                f"K_ori={k_ori:3d}  "
                f"K_enc={k_enc:3d}  "
                f"K_dec={k_dec:3d}  "
                f"SAME={same}\n"
            )

    print("Decode completed → decode.txt, reports.txt")

if __name__ == "__main__":
    main()
