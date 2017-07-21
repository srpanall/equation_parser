primes = [2, 3]


def prime_gen_test(n):
    for p in primes[2:]:
        if n % p == 0:
            return False
        if p > n ** 0.5 + 1:
            return True
    return True


def find_primes():
    c, delta = 5, 2
    while True:
        if prime_gen_test(c):
            yield c
        c += delta
        delta = delta * 2 % 6


n_p = find_primes()


def prime_test(n):
    for p in primes:
        if p > (n ** 0.5):
            return True
        elif n % p == 0:
            return False
    while primes[-1] < int(n ** 0.5) + 1:
        primes.append(next(n_p))
        if n % primes[-1] == 0:
            return False
    return True


def prod_fact(d_factored):
    val_out = 1
    for item in d_factored.items():
        p, a = item
        val_out = val_out * p ** a
    # print(val_out)
    return val_out


def factor_n(n):
    if prime_test(n):
        return {n: 1}
    out = {}
    new_n = n
    for p in primes:
        a = 0
        if new_n % p == 0:
            while new_n % p == 0:
                a += 1
                new_n = new_n // p
            out[p] = a
        if p > new_n:
            break
    # print(prod_fact(out))
    test = prod_fact(out) != n
    while test:
        primes.append(next(n_p))
        p = primes[-1]
        a = 0
        if new_n % p == 0:
            while new_n % p == 0:
                a += 1
                new_n = new_n // p
            out[p] = a
        test = prod_fact(out) != n
    return out


if __name__ == '__main__':
    print(987)
    print(factor_n(987))
    # print(primes)
    print(123)
    print(factor_n(123))
    # print(primes)
    # print(factor_n(89))
    # print(primes)
    # print(factor_n(9863))
    # print(primes)
    # print(len(primes))
