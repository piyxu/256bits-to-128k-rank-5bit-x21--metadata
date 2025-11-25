# 256bits-to-128k-rank-4bit-metadata
Save the date. First in the world.
Deterministic Balanced Encoding & Fully Reversible Rank-Based Mapping for 256-bit Data

This project provides a reversible encoding system that transforms arbitrary 256-bit binary data 
into a balanced 256-bit block containing exactly 128 ones, combined with a 4-bit metadata value.
The method is fully deterministic and guarantees 100% reversible decoding through rank/unrank 
operations on the combinational space C(256,128).

---

## Features
- Converts any 256-bit value into a 128-weight balanced 256-bit block
- Only 4 bits of metadata required for perfect reversibility
- Rank/Unrank combinational mapping
- Fully deterministic encode/decode pipeline
- No external dependencies beyond Python standard library

---
## Reports.txt
- 000: K_ori=126  K_enc=128  K_dec=126  SAME=TRUE
- 001: K_ori=124  K_enc=128  K_dec=124  SAME=TRUE
- 002: K_ori=122  K_enc=128  K_dec=122  SAME=TRUE

## System Architecture

A 256-bit integer R is mapped into two components using:

    R = (m × C(256,128)) + idx

Where:
- C(256,128) is the number of 256-bit sequences containing exactly 128 ones
- m is the quotient (0–15) which becomes 4-bit metadata
- idx is the remainder, defining the rank of the balanced 256-bit sequence

The idx value determines which balanced sequence (128 ones) represents the data.

---

## Encode Pipeline (encode.py)

1. Generate random R in the range [0, 16×C(256,128)).
2. Split R into:
       m   = R // C(256,128)
       idx = R %  C(256,128)
3. Unrank idx into a 256-bit balanced sequence (128 ones).
4. Write:
       [4-bit metadata] + [256-bit balanced block]
   into encode.txt.
5. Write the 256-bit representation of R into originals.txt.

---

## Decode Pipeline (decode.py)

1. Read metadata and the balanced block from encode.txt.
2. Convert the balanced 256-bit block back to its rank idx.
3. Reconstruct:
       R = m × C(256,128) + idx
4. Write reconstructed 256-bit binary values to decode.txt.
5. Write correctness checks to reports.txt, including:
   - original weight
   - encoded weight (always 128)
   - decoded weight
   - SAME=TRUE/FALSE

---

## Output Files

originals.txt  → original random 256-bit values  
encode.txt     → encoded metadata + balanced block  
decode.txt     → decoded 256-bit values  
reports.txt    → verification report  

---

## Why Balanced 128-Weight Blocks?

All 256-bit sequences with exactly 128 ones:
- have the same Hamming weight
- belong to a stable combinational space
- each has a unique rank (index)
- allow reversible mapping without ambiguity

The rank of a balanced block always fits into C(256,128), making it suitable to hold the remainder of R.

---

## Usage

Encode:
    python encode.py

Decode:
    python decode.py

This produces originals.txt, encode.txt, decode.txt, reports.txt.

---

## Project Structure

256bits-to-128k-rank-4bit-metadata/
 ├── encode.py
 ├── decode.py
 ├── originals.txt
 ├── encode.txt
 ├── decode.txt
 └── reports.txt

---

## License
MIT License  
Copyright © Mesut Erturhan

https://github.com/piyxu/256bits-to-128k-rank-4bit-metadata/
 