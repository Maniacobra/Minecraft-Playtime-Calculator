import gzip
import re
import os
import datetime

work_hours_per_month = 160 # Depends of your country

def to_seconds(time_str):
    return int(time_str[1:3]) * 3600 + int(time_str[4:6]) * 60 + int(time_str[7:9])

def add_s(nb):
    return "s" if nb > 1 else ""

if __name__ == "__main__":

    path = os.getenv("APPDATA") + "\\.minecraft\\logs\\"

    while True:
        if len(path) > 0 and path[-1] != "\\":
            path += "\\"
        if not path.endswith("\\logs\\"):
            path += "logs\\"
        try:
            files_list = os.listdir(path)
            break
        except:
            print("\nCouldn't find the logs folder at : " + path)
            path = input("\nEnter the absolute path of your .minecraft folder (include the .minecraft in the path) : ")

    input("\nMinecraft logs folder found. Press enter to start.\n")

    reg_time = r"^\[[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\]"
    reg_file = r"^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9]+\.log\.gz"

    valid_files = []
    for file_name in files_list:
        if re.match(reg_file, file_name):
            valid_files.append(file_name)
    
    files_list.clear()
    nb_files = len(valid_files)
    nb_digits = len(str(nb_files))
    count = 0
    total_time = 0
    day_str = None
    x_axis = []
    y_axis = []

    for file_name in valid_files:

        if day_str != file_name[:10]:
            if day_str is not None:
                x_axis.append(datetime.datetime.strptime(day_str,'%Y-%m-%d').date())
                y_axis.append(total_time // 3600)
            day_str = file_name[:10]

        count += 1
        file = gzip.open(path + file_name, "rt", encoding="utf-8", errors="ignore")
        content = file.readlines()
        
        first = None
        last = None
        for line in content:
            if re.match(reg_time, line):
                segment = line[:10]
                if first is None:
                    first = segment
                last = segment
        if first is not None:
            diff = to_seconds(last) - to_seconds(first)
            total_time += diff

        # Display
        current_year = file_name[:4]
        hours = total_time // 3600
        str_count = str(count)
        print("[{} / {}] ({}) {} hour{} at this point".format("0" * (nb_digits - len(str_count)) + str_count, nb_files, current_year, hours, add_s(hours)))

        file.close()
    if day_str is not None:
        x_axis.append(datetime.datetime.strptime(day_str,'%Y-%m-%d').date())
        y_axis.append(total_time // 3600)

    print("\n- FINAL TIME -\n")

    weeks = total_time / 604800
    days = total_time // 86400
    hours = total_time // 3600 % 24
    minutes = total_time // 60 % 60
    seconds = total_time % 60
    job = total_time / (3600 * work_hours_per_month)
    print("{} day{}".format(days, add_s(days)))
    print("{} hour{} ({} total)".format(hours, add_s(hours), total_time // 3600))
    print("{} minute{} ({} total)".format(minutes, add_s(minutes), total_time // 60))
    print("{} second{} ({} total)".format(seconds, add_s(seconds), total_time))

    print("\nThis is the equivalent of spending {:.2f} week{} of non-stop playing.".format(weeks, add_s(weeks)))
    if job >= 1:
        print("You could have used this time to work in a full-time job for {:.2f} month{} !".format(job, add_s(job)))
    
    print("\nProgram made by Maniacobra\nVisit website : https://maniacobra.com\n")

    input("Press enter to draw the graph.\n")

    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates

        fig = plt.figure("Time spent on Minecraft")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        plt.gca().xaxis.grid(visible=True)
        plt.plot(x_axis, y_axis)
        plt.gcf().autofmt_xdate()
        plt.ylabel("Amount of hours spent")
        plt.show()

    except ModuleNotFoundError:
        print("Libraries are missing, unable to draw the graph.")
        print("Enter these commands, then start the program again :")
        print("python -m pip install -U pip")
        print("python -m pip install -U matplotlib")
        print("\nIf that doesn't work, try with the prefix 'py' or 'python3' instead of 'python'.\n")
        os.system("pause")
