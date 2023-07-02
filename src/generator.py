import random
import csv

def generate_substances_file(size):
    # Generate substance data
    substances = []
    for i in range(size):
        substance = {
            "name": f"s{i+1}",
            "cost": round(random.uniform(0.1, 1.0), 2),
            "efficacy": round(random.uniform(10, 1.0), 2)
        }
        substances.append(substance)

    # Generate efficacy matrix
    matrix = [[0] * (size) for _ in range(size )]
    for i in range(size):
        for j in range(size):
            if i != j:
                difference = substances[j]["cost"] - substances[i]["cost"]
                efficacy = substances[j]["efficacy"] - substances[i]["efficacy"]
                score = round(difference * efficacy, 2)
                matrix[i][j] = score
            else:
                matrix[i][j] = 0  # Set diagonal elements to zero

    # Write substances and efficacy matrix to a file
    filename = f"data/substances_{size}.csv"
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["name", "cost", "efficacy"])
        for substance in substances:
            writer.writerow([substance["name"], substance["cost"], substance["efficacy"]])

        writer.writerow([])  # Empty line between sections

        writer.writerow(["name"] + [substance["name"] for substance in substances])
        for i in range(size):
            writer.writerow([substances[i]["name"]] + matrix[i])

    print(f"File '{filename}' generated.")

# Specify the different substance sizes
sizes = [5, 10, 20, 30, 40, 45, 50, 100, 1000]

# Generate a file for each substance size
for size in sizes:
    generate_substances_file(size)
