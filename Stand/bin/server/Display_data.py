import matplotlib.pyplot as plt

def dis(name="name"):
    # Function to place labels at the center of each bar
    def add_labels(x, y):
        for i in range(len(x)):
            plt.text(i, y[i] // 2, y[i], ha='center')  # Placing text at half the bar height

    x = ["Engineering", "BSc", "MBA", "Bcom", "BBA", "MSc"]
    y = [9330, 4050, 3030, 5500, 8040, 4560]

    # Setting figure size
    plt.figure(figsize=(10, 5))

    # Creating bar chart
    plt.bar(x, y)

    # Adding value labels
    add_labels(x, y)

    # Adding title and labels
    plt.title("College Admission")
    plt.xlabel("Courses")
    plt.ylabel("values")

    plt.show()