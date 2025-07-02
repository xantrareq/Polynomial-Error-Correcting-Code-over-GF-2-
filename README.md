# Polynomial Error-Correcting Code over GF(2)

This project implements a basic error-correcting code system using generator polynomials over the Galois Field GF(2). It supports encoding binary messages, generating code matrices, and decoding received messages with single-bit error correction via syndrome decoding.

---

## Features

- Polynomial operations over GF(2)
- Generator matrix `G` and parity-check matrix `H` construction
- Message encoding using a generator polynomial
- Syndrome-based error detection and correction
- Support for linear block codes (e.g., BCH-like)

---

## Dependencies

Install with pip:

```bash
pip install sympy numpy
