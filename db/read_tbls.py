def tbl_to_csv(filename):
    csv = open("".join(["./data/", filename, ".csv"]), "w+")

    tbl = open("".join(["./tbls/", filename, ".tbl"]), "r")

    lines = tbl.readlines()
    for line in lines:
        length = len(line)
        # Remove last delimeter, but keep newline character
        line = line[: length - 2] + line[length - 1 :]
        csv.write(line)
    tbl.close()
    csv.close()

def main():
    filenames = [
        "customer",
        "lineitem",
        "nation",
        "orders",
        "part",
        "partsupp",
        "region",
        "supplier",
    ]
    for filename in filenames:
        tbl_to_csv(filename)


# If the script is run directly, execute the main function
if __name__ == "__main__":
    main()