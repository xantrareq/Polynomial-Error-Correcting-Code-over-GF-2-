from sympy import symbols, div
from sympy.polys import GF, Poly
import numpy as np

def poly_div_to_k(k, g, n):
    """
    Divide the polynomial x^k by the generator polynomial g(x) in GF(2)
    and return the remainder as a padded coefficient array of length n.
    """
    x = symbols('x')
    g_poly = Poly(g, x, domain=GF(2))
    xk = x**k
    _, remainder = div(xk, g_poly, domain=GF(2))
    remainder_coeffs = remainder.all_coeffs()

    while len(remainder_coeffs) < n:
        remainder_coeffs.insert(0, 0)

    return np.flip(remainder_coeffs)

def poly_div(a, b):
    """
    Divide polynomial a by polynomial b in GF(2) and return the quotient coefficients.
    """
    x = symbols('x')
    poly_a = Poly(a, x, domain=GF(2))
    poly_b = Poly(b, x, domain=GF(2))
    quotient, _ = div(poly_a, poly_b, domain=GF(2))
    return quotient.all_coeffs()

def poly_mul(a, b):
    """
    Multiply polynomials a and b in GF(2) and return the resulting coefficients.
    """
    a = list(a)
    b = list(b)
    x = symbols('x')
    poly_a = Poly(a, x, domain=GF(2))
    poly_b = Poly(b, x, domain=GF(2))
    product = poly_a * poly_b
    return product.all_coeffs()

def generate_matrices(n, k, g):
    """
    Generate generator matrix G and parity-check matrix H for a (n, k) code.
    """
    G = np.zeros((k, n), dtype=int)
    for i in range(k):
        G[i, i:i+len(g)] = g

    H = np.zeros((n-k, n), dtype=int)
    for j in range(n):
        div_result = poly_div_to_k(j, g, n)
        for i in range(n - k):
            H[i][j] = div_result[i]

    return G, H

def generate_error_syndromes(H, n):
    """
    Create a mapping from error syndrome to the corresponding error position.
    """
    error_syndromes = {}
    for i in range(n):
        error_vector = np.zeros(n, dtype=int)
        error_vector[i] = 1
        syndrome = np.dot(H, error_vector) % 2
        error_syndromes[tuple(syndrome)] = i
    return error_syndromes

def encode(data, g):
    """
    Encode a message of k bits into an n-bit codeword using generator polynomial g.
    """
    return poly_mul(data, g)

def decode(received, H, g):
    """
    Decode an n-bit received codeword, correcting at most one error.
    """
    H = np.flip(H)
    received = np.array(received, dtype=int)

    syndrome = np.dot(H, received) % 2

    if np.any(syndrome):
        error_syndromes = generate_error_syndromes(H, len(received))
        error_index = error_syndromes.get(tuple(syndrome), None)

        if error_index is not None:
            received[error_index] ^= 1
            print("Corrected codeword:", f"\033[93m[{', '.join(map(str, received))}]\033[0m")
            print("Error corrected at index", f"\033[95m{error_index}\033[0m")
        else:
            print("Failed to correct error.")
    else:
        print("No errors detected.")

    return poly_div(received, g)

def main():
    n, k = 15, 7
    g = [1, 1, 1, 0, 1, 0, 0, 0, 1]

    G, H = generate_matrices(n, k, g)

    message = [1, 0, 1, 0, 1, 0, 1]
    if len(message) != k:
        print("!!!!!!!!\nInvalid message length\n!!!!!!!!")
        return
    print("Message:                 ", f"\033[92m{message}\033[0m")

    encoded = encode(message, g)
    print("Encoded message:         ", f"\033[93m{encoded}\033[0m")

    # Only one error supports
    encoded_with_error = encoded.copy()
    encoded_with_error[9] ^= 1
    print("Message with error:      ", f"\033[93m{encoded_with_error}\033[0m")

    decoded = decode(encoded_with_error, H, g)
    print("Decoded message:         ", f"\033[93m{decoded}\033[0m")

if __name__ == "__main__":
    main()
