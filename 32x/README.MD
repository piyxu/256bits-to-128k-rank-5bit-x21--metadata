# 256-bit to 128-of-256 Balanced Rank Coding — 32x Balanced Version

**Author:** MESUT ERTURHAN  
**License:** MIT License  
**Repository:** https://github.com/piyxu/256bits-to-128k-rank-5bit-x21--metadata/blob/main/32x_balanced/  
**Note:** This README.md was created with assistance from ChatGPT.

---

## 1. Purpose

This project describes a reversible coding method for representing a 256-bit number as:

```text
5-bit metadata + one balanced 256-bit block
```

The balanced block always has exactly:

```text
128 ones and 128 zeros
```

So the main 256-bit output block is always a `k = 128` constant-weight binary sequence.

This 32x version is designed as a clean controlled experiment:

```text
32 equal pools
5-bit fixed metadata
no partial final pool
no Huffman or arithmetic metadata advantage needed
```

The method is not a general-purpose compression method by itself.  
It is a reversible balanced / constant-weight representation method.

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

Compared with the full 256-bit number space:

```text
C(256,128) / 2^256 = 4.981910993614%
```

So the full balanced `k=128` combination space covers about:

```text
4.981910993614% of all possible 256-bit numbers
```

This is larger than one 32x pool.

---

## 3. The 32x pool model

The 32x version divides the full 256-bit space into exactly 32 equal pools:

```text
POOL_COUNT = 32
POOL_SIZE  = 2^256 / 32
POOL_SIZE  = 2^251
```

Numerically:

```text
POOL_SIZE = 3618502788666131106986593281521497120414687020801267626233049500247285301248
```

Each pool covers exactly:

```text
1 / 32 = 3.125000000000%
```

of the full 256-bit number space.

Because:

```text
2^5 = 32
```

the metadata fits perfectly into exactly 5 bits.

---

## 4. Pool table

| Pool | Metadata value `m` | 5-bit metadata | Share of the 256-bit number space |
|---:|---:|:---:|---:|
| 1 | 0 | `00000` | 3.125000000000% |
| 2 | 1 | `00001` | 3.125000000000% |
| 3 | 2 | `00010` | 3.125000000000% |
| 4 | 3 | `00011` | 3.125000000000% |
| 5 | 4 | `00100` | 3.125000000000% |
| 6 | 5 | `00101` | 3.125000000000% |
| 7 | 6 | `00110` | 3.125000000000% |
| 8 | 7 | `00111` | 3.125000000000% |
| 9 | 8 | `01000` | 3.125000000000% |
| 10 | 9 | `01001` | 3.125000000000% |
| 11 | 10 | `01010` | 3.125000000000% |
| 12 | 11 | `01011` | 3.125000000000% |
| 13 | 12 | `01100` | 3.125000000000% |
| 14 | 13 | `01101` | 3.125000000000% |
| 15 | 14 | `01110` | 3.125000000000% |
| 16 | 15 | `01111` | 3.125000000000% |
| 17 | 16 | `10000` | 3.125000000000% |
| 18 | 17 | `10001` | 3.125000000000% |
| 19 | 18 | `10010` | 3.125000000000% |
| 20 | 19 | `10011` | 3.125000000000% |
| 21 | 20 | `10100` | 3.125000000000% |
| 22 | 21 | `10101` | 3.125000000000% |
| 23 | 22 | `10110` | 3.125000000000% |
| 24 | 23 | `10111` | 3.125000000000% |
| 25 | 24 | `11000` | 3.125000000000% |
| 26 | 25 | `11001` | 3.125000000000% |
| 27 | 26 | `11010` | 3.125000000000% |
| 28 | 27 | `11011` | 3.125000000000% |
| 29 | 28 | `11100` | 3.125000000000% |
| 30 | 29 | `11101` | 3.125000000000% |
| 31 | 30 | `11110` | 3.125000000000% |
| 32 | 31 | `11111` | 3.125000000000% |

Every pool has exactly the same size.

There is no smaller final pool.

This is the main advantage of the 32x version.

---

## 5. Main formula

Let:

```text
R = the original 256-bit number
P = POOL_SIZE = 2^251
m = pool number / metadata
idx = position inside the selected pool
```

The encoder splits `R` like this:

```text
m   = R // P
idx = R % P
```

Since `P = 2^251`, this can also be interpreted as:

```text
m   = the top 5 bits of R
idx = the lower 251 bits of R
```

Then:

```text
idx
```

is converted into a 256-bit balanced sequence with exactly 128 ones:

```text
balanced_bits = unrank_256_128(idx)
```

The reverse operation is:

```text
idx = rank_256_128(balanced_bits)
R   = m * P + idx
```

---

## 6. Encode process

Encoding works in this order:

1. Read or generate a 256-bit number `R`.
2. Use:

```text
P = 2^251
```

3. Compute the metadata value:

```text
m = R // P
```

4. Compute the pool index:

```text
idx = R % P
```

5. Convert `idx` into a balanced 256-bit block with exactly 128 ones.
6. Write:

```text
5-bit m + 256-bit balanced block
```

The fixed encoded line length is:

```text
5 + 256 = 261 bits
```

---

## 7. Decode process

Decoding works in the reverse order:

1. Read the first 5 bits as metadata `m`.
2. Read the next 256 bits as the balanced block.
3. Convert the balanced block back into its rank value:

```text
idx = rank_256_128(bits256)
```

4. Rebuild the original number:

```text
R = m * 2^251 + idx
```

5. Write `R` as a 256-bit binary number.

If the input was valid, the decoded 256-bit number is exactly the same as the original 256-bit number.

---

## 8. Metadata size

This version uses exactly 32 metadata values:

```text
0..31
```

So fixed metadata is already optimal:

```text
log2(32) = 5 bits
```

Metadata summary:

```text
Fixed metadata:       5.000000000000 bits per block
Huffman metadata:     5.000000000000 bits per block
Arithmetic metadata:  5.000000000000 bits per block
Theoretical metadata: 5.000000000000 bits per block
```

Because all 32 metadata values are exactly equally likely, Huffman or arithmetic coding cannot reduce metadata below 5 bits per block.

---

## 9. Theoretical advantages

The 32x version has several clean theoretical advantages.

### 9.1 Exact 5-bit metadata

The number of pools is exactly:

```text
32 = 2^5
```

So metadata fits perfectly into 5 bits.

There are no unused metadata states.

---

### 9.2 Perfectly equal pool distribution

Every pool has exactly:

```text
2^251
```

values.

So the metadata distribution is perfectly uniform:

```text
P(m=0) = P(m=1) = ... = P(m=31)
```

This is useful for controlled experiments, statistical tests, and simple uniform metadata analysis.

---

### 9.3 No partial final pool

The older 21-pool systems have a final pool issue:

```text
C(256,128)-based 21-pool:
    final pool is smaller

ceil(2^256 / 21)-based 21-pool:
    mathematical range has 5 extra values
```

The 32x version avoids both problems:

```text
32 * 2^251 = 2^256
```

So the pool division is exact.

---

### 9.4 Simple implementation

Because:

```text
POOL_SIZE = 2^251
```

the split can be implemented very efficiently:

```text
m   = top 5 bits
idx = lower 251 bits
```

This is simpler than division by `C(256,128)` or by `ceil(2^256 / 21)`.

---

## 10. Theoretical disadvantages

The 32x version also has important disadvantages.

### 10.1 It does not use the full C(256,128) balanced space

A full balanced pool contains:

```text
C(256,128)
```

possible balanced blocks.

But the 32x version uses only:

```text
2^251
```

rank values per pool.

The used part of the full balanced pool is:

```text
2^251 / C(256,128) = 62.726933580422%
```

The unused balanced capacity is:

```text
37.273066419578%
```

So about 37.27% of the possible balanced `k=128` blocks are not used by this version.

---

### 10.2 Metadata cannot be improved below 5 bits

Because the 32 metadata values are exactly uniform, there is no entropy advantage to exploit.

So:

```text
fixed 5-bit metadata
```

is already optimal, but it is also the lower limit.

In contrast, the older `C(256,128)`-based pool system has a lower global theoretical metadata limit:

```text
about 4.327156943029 bits per block
```

So the 32x version loses:

```text
5.000000000000 - 4.327156943029 = 0.672843056971 bits per block
```

compared with the older full `C(256,128)` pool model.

---

### 10.3 It is less efficient than the 21x equal-pool model

The 21x equal-pool model has an entropy limit of:

```text
log2(21) = 4.392317422779 bits per block
```

The 32x model has:

```text
log2(32) = 5.000000000000 bits per block
```

So the 32x model uses:

```text
0.607682577221 bits per block
```

more metadata than the 21x equal-pool model.

---

## 11. Comparison with the previous two models

### 11.1 Older C(256,128)-based 21-pool model

Formula:

```text
C = C(256,128)

m   = R // C
idx = R % C
```

Advantages:

```text
best balanced-pool fullness
lowest theoretical metadata overhead
uses the full C(256,128) capacity for the first 20 pools
```

Disadvantages:

```text
last pool is much smaller
metadata distribution is not uniform
division by C(256,128) is less simple than bit-splitting
```

Metadata:

```text
Global theoretical metadata ≈ 4.327156943029 bits per block
```

---

### 11.2 21x equal-pool model

Formula:

```text
P = ceil(2^256 / 21)

m   = R // P
idx = R % P
```

Advantages:

```text
almost equal metadata distribution
21 metadata values instead of 32
lower entropy than 32x
```

Disadvantages:

```text
not an exact power-of-two pool split
mathematical range has 5 extra values
does not use the full C(256,128) capacity
```

Metadata:

```text
Arithmetic / entropy limit ≈ 4.392317422779 bits per block
```

---

### 11.3 New 32x balanced model

Formula:

```text
P = 2^251

m   = R // P
idx = R % P
```

Advantages:

```text
exact 32 equal pools
exact 5-bit metadata
no partial pool
no extra tail values
simple top-5-bits / lower-251-bits split
excellent for controlled experiments
```

Disadvantages:

```text
uses only 62.726933580422% of each full C(256,128) balanced pool
cannot reduce metadata below 5 bits
less metadata-efficient than both previous models
```

---

## 12. Which model should be used?

Use the older `C(256,128)`-based model if the goal is:

```text
maximum balanced-pool fullness
lowest theoretical metadata overhead
best coding efficiency
```

Use the 21x equal-pool model if the goal is:

```text
near-uniform metadata distribution
fewer metadata states than 32x
better entropy than 32x
```

Use the 32x balanced model if the goal is:

```text
controlled experiments
exact 5-bit metadata
perfectly equal metadata distribution
simple power-of-two pool splitting
```

The 32x version is best understood as a clean experimental baseline, not as the most capacity-efficient version.

---

## 13. Important notes

This system is reversible when:

```text
0 <= R < 2^256
0 <= m <= 31
0 <= idx < 2^251
the balanced block has exactly 128 ones
```

The balanced block alone is not enough to represent all 256-bit numbers. The metadata is required.

The 32x version uses only a subset of all possible `C(256,128)` balanced blocks.

---

## 14. MIT License

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
