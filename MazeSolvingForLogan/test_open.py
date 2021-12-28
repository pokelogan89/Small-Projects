def main():
    filename = "bigMaze.txt"
    with open(filename) as f:
        lines = f.readlines()

    print(lines[0])

main()