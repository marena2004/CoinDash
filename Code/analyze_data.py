import csv
import os
import matplotlib.pyplot as plt


def load_sessions(folder="stats"):
    data = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            session_data = {}
            with open(os.path.join(folder, file)) as f:
                reader = csv.reader(f)
                for row in reader:
                    session_data[row[0]] = float(row[1])
            data.append(session_data)
    return data


def plot_statistics(data):
    distances = [d["Distance Traveled"] for d in data]
    coins = [d["Coins Collected"] for d in data]
    jumps = [d["Jump Count"] for d in data]
    times = [d["Completion Time"] for d in data]

    deaths_falling = [d.get("Deaths - falling", 0) for d in data]
    deaths_obstacle = [d.get("Deaths - obstacle", 0) for d in data]

    sessions = list(range(1, len(data) + 1))

    # Graph 1: Line Graph - Distance Traveled
    plt.figure(figsize=(10, 5))
    plt.plot(sessions, distances, marker='o')
    plt.title("Distance Traveled Over Sessions")
    plt.xlabel("Session")
    plt.ylabel("Distance")
    plt.grid(True)
    plt.show()

    # Graph 2: Scatter Plot - Jumps
    plt.scatter(sessions, jumps)
    plt.title("Jump Frequency")
    plt.xlabel("Session")
    plt.ylabel("Jumps")
    plt.grid(True)
    plt.show()

    # Graph 3: Bar Chart - Coins
    plt.bar(sessions, coins)
    plt.title("Coins Collected Per Session")
    plt.xlabel("Session")
    plt.ylabel("Coins")
    plt.show()

    # Graph 4: Pie Chart - Deaths
    total_deaths = sum(deaths_falling) + sum(deaths_obstacle)
    plt.pie([sum(deaths_falling), sum(deaths_obstacle)],
            labels=["Falling", "Obstacle"],
            autopct='%1.1f%%')
    plt.title("Death Causes Proportion")
    plt.show()

    # Graph 5: Histogram - Completion Time
    plt.hist(times, bins=5)
    plt.title("Completion Time Distribution")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frequency")
    plt.show()


data = load_sessions()
plot_statistics(data)
