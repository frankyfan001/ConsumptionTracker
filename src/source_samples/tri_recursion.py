def tri_recursion(k):
    if k > 0:
        result = k + tri_recursion(k - 1)
        print(result)
    else:
        result = 0
    return result


def main():
    print("\n\nRecursion Example Results")
    tri_recursion(6)


main()
