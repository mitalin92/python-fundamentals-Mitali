# data_analyzer.py

import argparse
from utils import get_sample   # import from utils.py

# tuple example
CATEGORIES = ("High", "Medium", "Low")

def main():
    # variables
    script_name = "data_analyzer"
    version = 1
    print(script_name, "v", version)

    # get data
    data = get_sample()          
    sales = []

    # loop 
    for row in data:
        s = int(row["sales"])    # string -> int
        sales.append(s)

    # built-in functions
    print("Enumerate demo:")
    for i, row in enumerate(data, start=1):
        print(i, row["name"], row["sales"])

    print("Range demo:", list(range(1,4)))
    print("id(data):", id(data))

    # conditions
    total = sum(sales)
    avg = total / len(sales)
    print("Total:", total, "Average:", avg)
    if avg > 100:
        print("Good performance")
    else:
        print("Needs improvement")

    # min and max
    print("Min:", min(sales), "Max:", max(sales))

    count = 3
    while count > 0:
        print("Countdown:", count)
        count -= 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=2, help="show top N")
    args = parser.parse_args()

    main()

