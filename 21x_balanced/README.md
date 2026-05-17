# 256-bit to 128-of-256 Balanced Rank Coding — 21x Balanced Equal-Pool Version

**Author:** MESUT ERTURHAN  
**License:** MIT License  
**Repository:** https://github.com/piyxu/256bits-to-128k-rank-5bit-x21--metadata/21x_balanced  
**Note:** This README.md was created with assistance from ChatGPT.

---

## 1. Purpose

This project describes a reversible coding method for representing a 256-bit number as:

```text
metadata + one balanced 256-bit block
```

The balanced block always has exactly:

```text
128 ones and 128 zeros
```

In other words, the main 256-bit output block is always a `k = 128` constant-weight binary sequence.

This version uses a **21x balanced equal-pool system**.

The method is not a compression method by itself. It is a reversible representation method that converts a normal 256-bit number into a balanced 256-bit block plus a small metadata value.

---

## 2. Size of the balanced pool

The number of 256-bit binary strings with exactly 128 ones is:

```text
C(256,128)
```

For this system:

```text
C(256,128) = 5768658823449206338089748357862286887740211701975162032608436567264518750790
```

Compared with the full 256-bit number space, this is:

```text
C(256,128) / 2^256 = 4.981910993614%
```

So the full balanced `k=128` combination space covers about:

```text
4.98% of all possible 256-bit numbers
```

This is larger than one equal 21-pool.

---

## 3. New code system: 21 equal metadata pools

The new code uses:

```text
POOL_COUNT = 21
POOL_SIZE  = ceil(2^256 / 21)
```

Numerically:

```text
POOL_SIZE = 5513909011300771210646237381366090850155713555506693525688456381329196649521
```

So each normal pool covers approximately:

```text
POOL_SIZE / 2^256 = 4.761904761905%
```

The code splits the input number like this:

```text
m   = R // POOL_SIZE
idx = R %  POOL_SIZE
```

Then `idx` is converted into a balanced 256-bit block with exactly 128 ones:

```text
balanced_bits = unrank_256_128(idx)
```

This version is designed for cleaner and more uniform metadata-pool distribution.

---

## 4. Pool table for the new equal-pool system

For valid 256-bit inputs:

```text
0 <= R < 2^256
```

the pools are:

| Pool | Metadata value `m` | Share of the 256-bit number space | Note |
|---:|---:|---:|:---|
| 1 | 0 | 4.761904761905% | full equal pool |
| 2 | 1 | 4.761904761905% | full equal pool |
| 3 | 2 | 4.761904761905% | full equal pool |
| 4 | 3 | 4.761904761905% | full equal pool |
| 5 | 4 | 4.761904761905% | full equal pool |
| 6 | 5 | 4.761904761905% | full equal pool |
| 7 | 6 | 4.761904761905% | full equal pool |
| 8 | 7 | 4.761904761905% | full equal pool |
| 9 | 8 | 4.761904761905% | full equal pool |
| 10 | 9 | 4.761904761905% | full equal pool |
| 11 | 10 | 4.761904761905% | full equal pool |
| 12 | 11 | 4.761904761905% | full equal pool |
| 13 | 12 | 4.761904761905% | full equal pool |
| 14 | 13 | 4.761904761905% | full equal pool |
| 15 | 14 | 4.761904761905% | full equal pool |
| 16 | 15 | 4.761904761905% | full equal pool |
| 17 | 16 | 4.761904761905% | full equal pool |
| 18 | 17 | 4.761904761905% | full equal pool |
| 19 | 18 | 4.761904761905% | full equal pool |
| 20 | 19 | 4.761904761905% | full equal pool |
| 21 | 20 | 4.761904761905% | valid remaining pool |

The first 20 pools are full equal pools.

The last valid pool is smaller by only:

```text
5 integer values
```

because:

```text
21 * POOL_SIZE = 2^256 + 5
```

So, for practical percentage calculations, all 21 pools are effectively equal at 12 decimal places.

---

## 5. Difference from the older C(256,128)-pool formula

The older full-pool formula used:

```text
C = C(256,128)

m   = R // C
idx = R % C
```

That older formula uses the full balanced combination capacity.

The new equal-pool formula uses:

```text
POOL_SIZE = ceil(2^256 / 21)

m   = R // POOL_SIZE
idx = R % POOL_SIZE
```

This gives a cleaner metadata distribution, but it does not use the entire `C(256,128)` balanced combination space.

The unused balanced capacity per equal pool is:

```text
C(256,128) - POOL_SIZE = 254749812148435127443510976496196037584498146468468506919980185935322101269
```

As a share of the full 256-bit number space:

```text
0.220006231709%
```

As a share of one full `C(256,128)` balanced pool:

```text
4.416101210786%
```

In short:

```text
Older C(256,128)-pool formula:
    better balanced-pool fullness
    lower theoretical metadata limit
    less uniform final metadata pool

New 21x equal-pool formula:
    cleaner metadata distribution
    almost equal pool sizes
    slightly less efficient use of the balanced combination space
```

---

## 6. Why 5 bits of metadata are used

The encoder must say which pool the number came from.

There are 21 possible pool numbers:

```text
0, 1, 2, ..., 20
```

To store 21 possible values with a fixed-length binary code, we need:

```text
ceil(log2(21)) = 5 bits
```

Because:

```text
4 bits can store only 16 values
5 bits can store 32 values
```

So 5 fixed bits are enough to store any metadata value from 0 to 20.

The simple fixed-size representation is:

```text
5 metadata bits + 256 balanced bits = 261 bits
```

---

## 7. Huffman metadata coding for the new equal-pool model

The metadata does not have to be stored as fixed 5-bit values.

Because the 21 pools are almost equal, the metadata values are almost uniformly distributed.

A prefix-free Huffman-style table can be used:

| m | Code | Approx. pool size |
|---:|:---:|---:|
| 0 | `0000` | 4.761904761905% |
| 1 | `0001` | 4.761904761905% |
| 2 | `0010` | 4.761904761905% |
| 3 | `0011` | 4.761904761905% |
| 4 | `0100` | 4.761904761905% |
| 5 | `0101` | 4.761904761905% |
| 6 | `0110` | 4.761904761905% |
| 7 | `0111` | 4.761904761905% |
| 8 | `1000` | 4.761904761905% |
| 9 | `1001` | 4.761904761905% |
| 10 | `1010` | 4.761904761905% |
| 11 | `10110` | 4.761904761905% |
| 12 | `10111` | 4.761904761905% |
| 13 | `11000` | 4.761904761905% |
| 14 | `11001` | 4.761904761905% |
| 15 | `11010` | 4.761904761905% |
| 16 | `11011` | 4.761904761905% |
| 17 | `11100` | 4.761904761905% |
| 18 | `11101` | 4.761904761905% |
| 19 | `11110` | 4.761904761905% |
| 20 | `11111` | 4.761904761905% |

With this table, 11 metadata values use 4 bits, and 10 metadata values use 5 bits.

For the new equal-pool model, the average metadata size is approximately:

```text
4.476190476190 bits per block
```

This is smaller than fixed 5-bit metadata.

Because the distribution is almost uniform, this value is very close to the best possible Huffman result for 21 nearly equal symbols:

```text
Optimized Huffman metadata ≈ 4.476190476190 bits per block
```

---

## 8. Arithmetic or global metadata coding

If many blocks are encoded together, the metadata values can be collected into one metadata stream.

With arithmetic coding or range coding, the metadata stream can approach the entropy of the metadata distribution.

For the new equal-pool model:

```text
Arithmetic / entropy limit ≈ 4.392317422779 bits per block
```

This is essentially:

```text
log2(21) = 4.392317422779 bits per block
```

This means:

```text
Fixed metadata:       5.000000000000 bits per block
Huffman metadata:     about 4.476190476190 bits per block
Arithmetic metadata:  about 4.392317422779 bits per block
```

---

## 9. Comparison with the older full C(256,128)-pool model

The older full-pool model has these metadata values:

```text
Arithmetic metadata:  about 4.340844945453 bits per block
Global theoretical:   about 4.327156943029 bits per block
```

The new equal-pool model has:

```text
Arithmetic metadata:  about 4.392317422779 bits per block
```

So the new equal-pool model is statistically cleaner, but the older `C(256,128)` full-pool model has a lower theoretical metadata overhead.

A short comparison:

```text
Older C(256,128)-pool model:
    arithmetic metadata ≈ 4.340844945453 bits/block
    global theoretical  ≈ 4.327156943029 bits/block

New 21x equal-pool model:
    arithmetic metadata ≈ 4.392317422779 bits/block
```

---

## 10. Main formula

Let:

```text
R = the original 256-bit number
P = POOL_SIZE = ceil(2^256 / 21)
m = pool number / metadata
idx = position inside the selected pool
```

The encoder splits `R` like this:

```text
m   = R // P
idx = R % P
```

This is simple division.

It is like saying:

```text
R = m equal pools + idx steps inside the current pool
```

Then:

```text
idx
```

is converted into a 256-bit balanced sequence with exactly 128 ones.

This conversion is called:

```text
combination unranking
```

The reverse operation is called:

```text
combination ranking
```

---

## 11. Very simple example

Imagine a smaller world.

Suppose one pool can hold 10 values.

If the original number is:

```text
R = 37
```

Then:

```text
m   = 37 // 10 = 3
idx = 37 % 10  = 7
```

This means:

```text
The number is in pool 3.
Inside that pool, it is item 7.
```

To decode:

```text
R = m * 10 + idx
R = 3 * 10 + 7
R = 37
```

The real system does the same thing, but with:

```text
P = POOL_SIZE = ceil(2^256 / 21)
```

instead of `10`.

---

## 12. Encode process

Encoding works in this order:

1. Read the original 256-bit number `R`.
2. Compute:

```text
POOL_SIZE = ceil(2^256 / 21)
```

3. Compute the metadata value:

```text
m = R // POOL_SIZE
```

4. Compute the pool index:

```text
idx = R % POOL_SIZE
```

5. Convert `idx` into a 256-bit balanced block with exactly 128 ones.
6. Write the metadata and the balanced block.

Simple fixed form:

```text
5-bit m + 256-bit balanced block
```

Optional compact form:

```text
Huffman-coded m + 256-bit balanced block
```

---

## 13. Decode process

Decoding works in the reverse order:

1. Read the metadata value `m`.
2. Read the 256-bit balanced block.
3. Convert the balanced block back into its rank value `idx`.
4. Rebuild the original number:

```text
R = m * POOL_SIZE + idx
```

5. Write `R` as a 256-bit binary number.

If the input was valid, the decoded 256-bit number is exactly the same as the original 256-bit number.

---

## 14. Important notes

This system is reversible when:

```text
0 <= R < 2^256
0 <= m <= 20
0 <= idx < POOL_SIZE
the balanced block has exactly 128 ones
```

The current test code generates valid 256-bit input using random 256-bit values.

Because `POOL_SIZE = ceil(2^256 / 21)`, the mathematical range `21 * POOL_SIZE` is 5 integer values larger than `2^256`.

For normal 256-bit input:

```text
0 <= R < 2^256
```

this does not cause a problem.

---

## 15. Which model should be used?

For equal metadata-pool distribution:

```text
Use the new 21x equal-pool model.
```

For maximum balanced-pool fullness and the lowest theoretical metadata overhead:

```text
Use the older C(256,128)-pool model.
```

This repository version focuses on the new 21x equal-pool system.

---

## 16. MIT License

Copyright (c) 2025-2026 Piyxu / Mesut Erturhan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
