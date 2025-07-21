def primitive_dyck_rank(s):
    """
    Given a primitive Dyck word s (a well‐formed parenthesis string
    that only returns to balance 0 at the very end), return its 0-based
    rank in the sequence:
      semilength=1: "()"
      semilength=2: "(())"
      semilength=3: "((()))", "(()())"
      semilength=4: "(((())))", "((()()))", "((())())", "(()(()))", "(()()())"
      ...
    within each semilength, listed in lex order with '(' < ')'.
    """
    L = len(s)
    if L % 2 != 0 or L < 2:
        raise ValueError("input must be a primitive Dyck word of even length ≥2")
    k = L // 2
    # check basic primitive‐Dyck structure
    bal = 0
    for i, ch in enumerate(s):
        if ch == '(':
            bal += 1
        elif ch == ')':
            bal -= 1
        else:
            raise ValueError("invalid character")
        if bal < 0 or (bal == 0 and i != L - 1):
            raise ValueError("not primitive Dyck")
    if bal != 0:
        raise ValueError("not a Dyck word")

    # 1) Compute Catalan numbers C0..C_{k-1}
    catalan = [1]  # C0 = 1
    for i in range(1, k):
        # C_i = C_{i-1} * 2*(2i-1)/(i+1)
        c = catalan[-1] * 2 * (2 * i - 1) // (i + 1)
        catalan.append(c)

    # Number of primitives of semilength j is C_{j-1}, so
    # all primitives of smaller semilengths occupy
    # sum_{j=1..k-1} C_{j-1} = sum_{i=0..k-2} C_i
    prev_count = sum(catalan[0:k - 1])  # = 0 when k=1

    # 2) Extract the inner Dyck word of semilength m = k-1
    m = k - 1
    inner = s[1:-1]  # length = 2m

    # 3) Build DP_rem[r][b] = # of ways to complete a Dyck path
    #    of remaining length r starting from balance b.
    N = 2 * m
    DP_rem = [[0] * (m + 2) for _ in range(N + 1)]
    DP_rem[0][0] = 1
    for length in range(1, N + 1):
        for b in range(m + 1):
            cnt = 0
            # place '(' => balance b+1
            if b + 1 <= m:
                cnt += DP_rem[length - 1][b + 1]
            # place ')' => balance b-1
            if b > 0:
                cnt += DP_rem[length - 1][b - 1]
            DP_rem[length][b] = cnt

    # 4) Rank the inner Dyck word in lex order
    r = 0
    bal = 0
    for pos, ch in enumerate(inner):
        rem = N - pos - 1
        # how many completions if we put '(' here?
        cnt_open = DP_rem[rem][bal + 1] if bal + 1 <= m else 0
        if ch == '(':
            bal += 1
        else:  # ch == ')'
            # skip over all the words that start with '(' here
            r += cnt_open
            bal -= 1

    return prev_count + r


# --- Example / sanity check ---
if __name__ == '__main__':
    test = ["()", "(())", "((()))", "(()())", "(((())))", "((()()))"]
    for w in test:
        print(f"{w:10s}  -> rank = {primitive_dyck_rank(w)}")


    # round‐trip check against the unranker from before:
    def primitive_dyck_by_rank(n):
        # (same unranker as given previously)
        if n < 0: raise ValueError()
        # build Catalan & locate semilength
        cat = [1];
        total = 1;
        k = 0
        while total <= n:
            j = k + 1
            cat.append(cat[k] * 2 * (2 * j - 1) // (j + 1))
            total += cat[k + 1]
            k += 1
        semilen = k + 1
        prev = total - cat[k]
        r = n - prev
        m = semilen - 1
        # build DP_rem
        N = 2 * m
        DP = [[0] * (m + 2) for _ in range(N + 1)]
        DP[0][0] = 1
        for L in range(1, N + 1):
            for b in range(m + 1):
                v = 0
                if b + 1 <= m: v += DP[L - 1][b + 1]
                if b > 0:     v += DP[L - 1][b - 1]
                DP[L][b] = v
        # unrank inner
        bal = 0;
        inner = []
        for i in range(N):
            rem = N - i - 1
            cnt = DP[rem][bal + 1] if bal + 1 <= m else 0
            if r < cnt:
                inner.append('(')
                bal += 1
            else:
                r -= cnt;
                inner.append(')')
                bal -= 1
        return "(" + "".join(inner) + ")"


    for i in range(10):
        w = primitive_dyck_by_rank(i)
        assert primitive_dyck_rank(w) == i
    print("round‐trip OK")
