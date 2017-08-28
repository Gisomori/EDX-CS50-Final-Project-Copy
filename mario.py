import cs50


def get_positive_int():
    while True:
        n = cs50.get_int()
        if n > 0:
            break
    return n

def main():
    while True:
        print("Height:",end = " ")
        input_pyramid_height = get_positive_int()
        if input_pyramid_height >= 0 and input_pyramid_height < 24:
            break
    print_pyramid(input_pyramid_height)

def print_pyramid(input_pyramid_height):
    for i in range(input_pyramid_height):
        space_retain = input_pyramid_height - i - 1
        for x in range(space_retain,0,-1):
            print(' ',end="")
        for y in range(input_pyramid_height, space_retain-1,-1):
            print('#',end="")
        print("")


if __name__ == "__main__":
    main()
