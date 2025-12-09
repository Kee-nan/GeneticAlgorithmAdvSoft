# decode_ways.py
def decode_ways_correct(s):
    if not s or s[0] == '0':
        return 0

    dp = [0] * (len(s) + 1)
    dp[0] = 1
    dp[1] = 1

    for i in range(2, len(s) + 1):
        one = int(s[i-1])
        two = int(s[i-2:i])

        if 1 <= one <= 9:
            dp[i] += dp[i-1]

        if 10 <= two <= 26:
            dp[i] += dp[i-2]

    return dp[-1]

#######################################################################

def decode_ways_buggy(s):
    if not s:
        return 0

    dp = [0] * (len(s) + 1)
    dp[0] = 1
    dp[1] = 1  # bug: wrong when s[0] == '0'

    for i in range(2, len(s) + 1):
        one = int(s[i-1])
        two = int(s[i-2:i])

        # Bug: allows zero alone
        if 0 <= one <= 9:
            dp[i] += dp[i-1]

        # Bug: includes numbers like 27–30
        if 1 <= two <= 30:
            dp[i] += dp[i-2]

    return dp[-1]
