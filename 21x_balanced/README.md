# 256-bit to 128k Balanced Rank Coding — 21x Balanced Pool System

**MIT License**  
**MESUT ERTURHAN**

Repository:

```text
https://github.com/piyxu/256bits-to-128k-rank-5bit-x21--metadata/21x_balanced
```

---

## 1. What this project does

This project maps a 256-bit integer into:

```text
5-bit metadata + 256-bit balanced binary block
```

The balanced block has exactly:

```text
128 ones
128 zeros
```

So the output block is always a 256-bit binary sequence with `k = 128`.

This is not a general compression algorithm.  
It is a reversible balanced / constant-weight coding experiment.

The main goal is:

```text
any 256-bit value
→ pool metadata
→ balanced 256-bit representation with exactly 128 ones
```

---

## 2. Why C(256,128) matters

The number of 256-bit binary strings with exactly 128 ones is:

```text
C(256,128)
```

In this project:

```text
C(256,128) = 5768658823449206338089748357862286887740211701975162032608436567264518750790
```

This is about:

```text
4.981910993614% of the full 256-bit numeric space
```

So a single balanced `k=128` space cannot represent all possible 256-bit values by itself.

That is why a metadata pool number is needed.

---

## 3. The 21-pool idea

The full 256-bit space is divided into 21 pools.

```text
POOL_COUNT = 21
POOL_SIZE  = ceil(2^256 / 21)
```

In this version:

```text
POOL_SIZE = 5513909011300771210646237381366090850155713555506693525688456381329196649521
```

Each pool covers about:

```text
4.761904761905% of the 256-bit space
```

This gives a near-uniform 21-pool distribution.

The pool number is stored as 5-bit metadata:

```text
0..20  →  needs 5 bits
```

Because:

```text
2^4 = 16  is not enough
2^5 = 32  is enough
```

---

## 4. Why this version uses equal 21 pools

Earlier pool designs can use:

```text
C(256,128)
```

directly as the pool size.

This gives the best use of the full balanced combination space, but the final pool is smaller than the others.

This `21x_balanced` version instead uses:

```text
POOL_SIZE = ceil(2^256 / 21)
```

This means the metadata pools are almost equal in size.

That is useful for scientific and statistical tests where uniform pool distribution is more important than using every possible balanced combination.

In short:

```text
C(256,128)-based pool:
    better theoretical capacity usage

21x balanced pool:
    better pool uniformity and simpler statistical structure
```

---

## 5. Capacity note

The balanced space is slightly larger than one equal 21-pool.

```text
C(256,128) ≈ 4.981910993614% of 2^256
POOL_SIZE  ≈ 4.761904761905% of 2^256
```

So this equal-pool version does not use the complete `C(256,128)` balanced space.

The unused part is the price paid for simpler and more uniform pool division.

---

## 6. Core formulas

For a 256-bit integer `R`:

```text
m   = R // POOL_SIZE
idx = R %  POOL_SIZE
```

Where:

```text
m   = metadata pool number
idx = index inside the selected pool
```

Then `idx` is converted into a 256-bit balanced binary block:

```text
balanced_bits = unrank_256_128(idx)
```

The encoded line is:

```text
5-bit metadata + 256-bit balanced block
```

---

## 7. Encode process

Step-by-step:

```text
1. Read or generate a 256-bit integer R.
2. Compute the metadata pool:

       m = R // POOL_SIZE

3. Compute the index inside the pool:

       idx = R % POOL_SIZE

4. Convert idx into a balanced 256-bit sequence:

       bits256 = unrank_256_128(idx)

5. Write:

       5-bit metadata + 256-bit balanced block
```

Example structure:

```text
metadata bits       balanced 256-bit block
00000               000...111...
```

---

## 8. Decode process

Step-by-step:

```text
1. Read the first 5 bits as metadata.
2. Read the remaining 256 bits as the balanced block.
3. Convert the balanced block back into its rank:

       idx = rank_256_128(bits256)

4. Rebuild the original 256-bit integer:

       R = m * POOL_SIZE + idx

5. Write R as a 256-bit binary string.
```

---

## 9. Rank / unrank explanation

The balanced block is not random text.

It is selected from the ordered list of all 256-bit binary strings that contain exactly 128 ones.

`unrank` means:

```text
take a number idx
find the idx-th balanced sequence
```

`rank` means:

```text
take a balanced sequence
find its numeric position idx
```

This makes the system reversible.

---

## 10. Files

Typical files:

```text
encode.py
decode.py

originals.txt
encode.txt
decode.txt
reports.txt
```

`encode.py` creates:

```text
originals.txt
encode.txt
```

`decode.py` creates:

```text
decode.txt
reports.txt
```

---

## 11. Important limits

The input value must be inside the normal 256-bit unsigned range:

```text
0 <= R < 2^256
```

The metadata value should be:

```text
0 <= m <= 20
```

The balanced block should always have:

```text
K = 128
```

---

## 12. What this project is useful for

This project may be useful for:

```text
balanced coding experiments
constant-weight code experiments
rank / unrank demonstrations
pool-distribution experiments
metadata distribution tests
statistical analysis of balanced binary representations
```

It should not be presented as normal file compression.

A better description is:

```text
reversible pool-based balanced rank coding
```

or:

```text
pool-based constant-weight coding for 256-bit values
```

---

## 13. License

MIT License

Copyright (c) 2026 MESUT ERTURHAN

README.md was created with the assistance of ChatGPT.
