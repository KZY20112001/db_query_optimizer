import os

def tbl_to_csv(filename):
    tbl_path = "".join(["./tbls/", filename, ".tbl"])

    if not os.path.exists(tbl_path):
        print(f"The file '{filename}.tbl' does not exist.")
        return
    else: 
        tbl = open(tbl_path, "r")

    csv_path = os.path.join("./data/", f"{filename}.csv")

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, "w+") as csv:
        lines = tbl.readlines()
        for line in lines:
            length = len(line)
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