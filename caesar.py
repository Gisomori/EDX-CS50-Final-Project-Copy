import string
import sys


def main():
    small_abc = list(string.ascii_lowercase)
    big_abc = list(string.ascii_uppercase)
    plain = list(input('plaintext: '))
    cipher = {}
    plain_range = len(plain)
    print('ciphertext: ',end='')
    x = 0
    for x in range(plain_range):
        if str.isalpha(plain[x]):
            if str.isupper(plain[x]):
                y = 0
                while big_abc[y] != plain[x]:
                    y += 1
                cipher[x] = big_abc[(y + key) % 26]
                print(cipher[x],end='')
            else:
                y = 0
                while small_abc[y] != plain[x]:

                    y += 1
                cipher[x] = small_abc[(y + key) % 26]
                print(cipher[x],end='')
        else:
            cipher[x] = plain[x]
            print(cipher[x],end='')
    print('')



if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print('Usage: /home/cs50/pset6/caesar <key>')
        sys.exit(1)
    key = int(sys.argv[1])
    main()