def save_report(data):

    with open("report.txt", "w", encoding="utf-8") as file:

        file.write(data)