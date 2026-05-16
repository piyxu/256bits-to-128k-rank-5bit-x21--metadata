# 256-bit to 128-of-256 Balanced Rank Coding

**Author:** MESUT ERTURHAN  
**License:** MIT License  
**Note:** This README.md was created with assistance from ChatGPT.

---

## 1. Purpose

This project describes a reversible coding method for representing any 256-bit number as:

```text
metadata + one balanced 256-bit block
```

The balanced block always has exactly:

```text
128 ones and 128 zeros
```

In other words, the main 256-bit output block is always a `k = 128` constant-weight binary sequence.

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

So one balanced pool covers about:

```text
4.98% of all possible 256-bit numbers
```

This is why one balanced 256-bit block is not enough to represent every possible 256-bit number by itself. It covers only about 4.98% of the full space.

---

## 3. Simple pool explanation

Imagine the full 256-bit number space as a very long line of numbers.

One balanced pool covers about 4.98% of that line.

So the data is divided into repeated pools:

```text
Pool 1:  [about 4.98%]
Pool 2:  [about 4.98%]
Pool 3:  [about 4.98%]
...
Pool 20: [about 4.98%]
Pool 21: [remaining small part]
```

More precisely:

| Pool | Metadata value `m` | Share of the 256-bit number space |
|---:|---:|---:|
| 1 | 0 | 4.981910993614% |
| 2 | 1 | 4.981910993614% |
| 3 | 2 | 4.981910993614% |
| ... | ... | ... |
| 20 | 19 | 4.981910993614% |
| 21 | 20 | 0.361780127720% |

The first 20 pools are full `C(256,128)` pools. The last pool is only the remaining part of the 256-bit number space.

---

## 4. Why 5 bits of metadata are used

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

## 5. Huffman metadata coding

The metadata does not have to be stored as fixed 5-bit values.

A prefix-free Huffman-style table can be used instead:

| m | Code | Approx. pool size |
|---:|:---:|---:|
| 0 | `0000` | 4.981910993614% |
| 1 | `0001` | 4.981910993614% |
| 2 | `0010` | 4.981910993614% |
| 3 | `0011` | 4.981910993614% |
| 4 | `0100` | 4.981910993614% |
| 5 | `0101` | 4.981910993614% |
| 6 | `0110` | 4.981910993614% |
| 7 | `0111` | 4.981910993614% |
| 8 | `1000` | 4.981910993614% |
| 9 | `1001` | 4.981910993614% |
| 10 | `1010` | 4.981910993614% |
| 11 | `10110` | 4.981910993614% |
| 12 | `10111` | 4.981910993614% |
| 13 | `11000` | 4.981910993614% |
| 14 | `11001` | 4.981910993614% |
| 15 | `11010` | 4.981910993614% |
| 16 | `11011` | 4.981910993614% |
| 17 | `11100` | 4.981910993614% |
| 18 | `11101` | 4.981910993614% |
| 19 | `11110` | 4.981910993614% |
| 20 | `11111` | 0.361780127720% |

With this table, the first 11 metadata values use 4 bits, and the remaining metadata values use 5 bits.

Because values `0..19` each cover about 4.9819% of the input space, while value `20` covers only about 0.3618%, the average metadata size becomes approximately:

```text
4.451989790702 bits per block
```

So this is smaller than fixed 5-bit metadata.

A fixed 5-bit system is simpler. A Huffman metadata stream is smaller.

---

## 6. Arithmetic or global metadata coding

If many blocks are encoded together, the metadata values can be collected into one metadata stream.

With arithmetic coding or range coding, the metadata stream can approach the entropy of the metadata distribution:

```text
about 4.340844945453 bits per block
```

A deeper global packing method can approach the theoretical expansion limit:

```text
256 - log2(C(256,128)) = 4.327156943029 bits per block
```

This means:

```text
Fixed metadata:       5.000 bits per block
Huffman metadata:     about 4.451989790702 bits per block
Arithmetic metadata:  about 4.340844945453 bits per block
Global theoretical:   about 4.327156943029 bits per block
```

---

## 7. Main formula

Let:

```text
R = the original 256-bit number
C = C(256,128)
m = pool number / metadata
idx = position inside the balanced pool
```

The encoder splits `R` like this:

```text
m   = R // C
idx = R % C
```

This is simple division.

It is like saying:

```text
R = m full pools + idx steps inside the current pool
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

## 8. Very simple example

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
C = C(256,128)
```

instead of `10`.

---

## 9. Encode process

Encoding works in this order:

1. Read the original 256-bit number `R`.
2. Compute `C = C(256,128)`.
3. Compute the metadata value:

```text
m = R // C
```

4. Compute the pool index:

```text
idx = R % C
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

## 10. Decode process

Decoding works in the reverse order:

1. Read the metadata value `m`.
2. Read the 256-bit balanced block.
3. Convert the balanced block back into its rank value `idx`.
4. Rebuild the original number:

```text
R = m * C(256,128) + idx
```

5. Write `R` as a 256-bit binary number.

If the input was valid, the decoded 256-bit number is exactly the same as the original 256-bit number.

---

## 11. Important notes

This system is reversible when:

```text
0 <= R < 2^256
0 <= m <= 20
0 <= idx < C(256,128)
the balanced block has exactly 128 ones
```

The 256-bit balanced block alone is not enough to represent all 256-bit numbers. The metadata is required.

---
# Repository address changed:

# Old address:
https://github.com/piyxu/256bits-to-128k-rank-4bit-metadata

# New address:
https://github.com/piyxu/256bits-to-128k-rank-5bit-x21--metadata

## MIT License

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

