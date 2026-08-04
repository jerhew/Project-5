# Jeremy Hewitt

#
# This program reads stock information from a CSV file and stores it in a
# dictionary of dictionaries. The user can look up information for a specific
# trading day, calculate the weighted average closing price for a month, or
# print high and low stock information.


MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def read_stock_file(filename):
    """Read stock data and return the main dictionary and summary lists."""

    data_file = open(filename, "r")
    data_file.readline()

    stock_dictionary = {}
    volume_list = []
    high_list = []
    low_list = []

    for line in data_file:
        line = line.strip()

        if line != "":
            fields = line.split(",")

            date_fields = fields[0].split("-")
            year = int(date_fields[0])
            month = int(date_fields[1])
            day = int(date_fields[2])

            open_price = float(fields[1])
            high_price = float(fields[2])
            low_price = float(fields[3])
            close_price = float(fields[4])
            volume = int(fields[5])
            adj_close = float(fields[6])

            month_key = (year, month)
            date_key = (year, month, day)

            trading_info = [open_price, high_price, low_price,
                            close_price, volume, adj_close]

            if month_key not in stock_dictionary:
                stock_dictionary[month_key] = {}

            stock_dictionary[month_key][day] = trading_info

            volume_list.append((volume, date_key))
            high_list.append((high_price, date_key))
            low_list.append((low_price, date_key))

    data_file.close()

    return stock_dictionary, volume_list, high_list, low_list


def print_menu():
    """Print the program menu."""

    print("a) Get information about a particular day of trading")
    print("b) Find average information about a particular month")
    print("c) Print high/low information")
    print("q) Quit")
    print()


def format_date(date_tuple):
    """Return a date tuple as Month Day, Year."""

    year = date_tuple[0]
    month = date_tuple[1]
    day = date_tuple[2]

    return MONTHS[month - 1] + " " + str(day) + ", " + str(year)


def print_day_information(stock_dictionary):
    """Print trading information for one selected day."""

    year_string = input("Please enter the year you are interested in: ")
    print(year_string)

    month_string = input("Please enter the month you are interested in: ")
    print(month_string)

    day_string = input("Please enter the day you are interested in: ")
    print(day_string)
    print()

    year = int(year_string)
    month = int(month_string)
    day = int(day_string)

    try:
        trading_info = stock_dictionary[(year, month)][day]

        print(format_date((year, month, day)))
        print()
        print("Open\tHigh\tLow\tClose\tVolume\t\tAdj. Close")
        print("{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:,}\t{:.2f}".format(
            trading_info[0], trading_info[1], trading_info[2],
            trading_info[3], trading_info[4], trading_info[5]))
        print()

    except KeyError:
        print("No trading occurred on this day.")
        print()


def print_month_average(stock_dictionary):
    """Calculate and print the weighted average for one month."""

    year_string = input("Please enter the year you are interested in: ")
    print(year_string)

    month_string = input("Please enter the month you are interested in: ")
    print(month_string)
    print()

    year = int(year_string)
    month = int(month_string)

    try:
        month_dictionary = stock_dictionary[(year, month)]

        total_volume = 0
        total_value = 0.0

        for day in month_dictionary:
            trading_info = month_dictionary[day]
            close_price = trading_info[3]
            volume = trading_info[4]

            total_value = total_value + close_price * volume
            total_volume = total_volume + volume

        average_price = total_value / total_volume

        print("The average price for", MONTHS[month - 1],
              year, "is {:.2f}.".format(average_price))
        print()

    except KeyError:
        print("Not a legal date.")
        print()


def print_high_low_information(volume_list, high_list, low_list):
    """Print highest and lowest volume and price information."""

    highest_volume = max(volume_list)
    lowest_volume = min(volume_list)
    highest_price = max(high_list)
    lowest_price = min(low_list)

    print("The day with the highest volume was",
          format_date(highest_volume[1]), "with a volume of",
          "{:,} shares.".format(highest_volume[0]))

    print("The day with the lowest volume was",
          format_date(lowest_volume[1]), "with a volume of",
          "{:,} shares.".format(lowest_volume[0]))

    print("The day when the stock reached its highest point was",
          format_date(highest_price[1]), "with a value of",
          "{:.2f}.".format(highest_price[0]))

    print("The day when the stock reached its lowest point was",
          format_date(lowest_price[1]), "with a value of",
          "{:.2f}.".format(lowest_price[0]))

    print()


# Main program

filename = input("Enter the name of the stock file you are interested in: ")
print(filename)
print()

stock_data = read_stock_file(filename)

stock_dictionary = stock_data[0]
volume_list = stock_data[1]
high_list = stock_data[2]
low_list = stock_data[3]

choice = " "

while choice.lower() != "q":
    print_menu()

    choice = input("Enter choice: ")
    print(choice)
    print()

    if choice.lower() == "a":
        print_day_information(stock_dictionary)

    elif choice.lower() == "b":
        print_month_average(stock_dictionary)

    elif choice.lower() == "c":
        print_high_low_information(volume_list, high_list, low_list)

    elif choice.lower() == "q":
        print("Thanks for using my program.")

    else:
        print("You've entered an incorrect choice. Try again.")
        print()
