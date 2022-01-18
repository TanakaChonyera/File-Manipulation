######################################################################################
#
#   CSE 231 Programming Project #6
#
#       Algorithm
#
#           Function definitions
#           Call open_file(fp)
#           Loop while user input incorrect or user quits program
#               Select user preference
#               Call relevant function
#                   Compute data
#                   Return result(s)
#               Output results
#
######################################################################################

import csv
import matplotlib.pyplot as plt

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


def open_file():
    ''' Takes no arguments, prompts for a file name and returns the file pointer to
that file. If no file name is given, the program will open reactors-operating.csv.
The function will keep asking until a file is found. '''

    file_valid = False

    file_name = input('Please input a file to use: ')

    # Check if file name exists
    if file_name == '':
        file_name = 'reactors-operating.csv'
    else:
        while file_valid == False:
            try:

                with open(file_name, 'r', encoding="windows-1252") as file:
                    file_valid = True
            except FileNotFoundError:
                print('Invalid filename, please try again')
                file_valid = False
                file_name = input('Please input a file to use: ')

    return file_name


def read_file(fp):
    ''' Accepts a file pointer and returns a master list of lists of all the data in the
file. Each line of the file will be a list in the master list. The master list will be in the same
order that the data is in the file. The file is a comma-separated-value file (.csv). '''

    master_list = []

    try:
        with fp as file:

            reader = csv.reader(file)

            # Skip both header lines
            next(reader, None)
            next(reader, None)

            # Generate master list
            for line_list in reader:  # note that using csv.reader you get a list!
                master_list.append(line_list)

    except:

        with open(fp, 'r', encoding="windows-1252") as file:

            reader = csv.reader(file)

            # Skip both header lines
            next(reader, None)
            next(reader, None)

            # Generate master list
            for line_list in reader:  # note that using csv.reader you get a list!
                master_list.append(line_list)

    return master_list


def get_reactor_location(location_string):
    ''' Extract and return a string with only the city name and state abbreviation from the long location
string located at the column labeled “Location” in the data file. '''

    # Retrieve city name
    city_name_state_abbreviation = ''
    for char in location_string:
        if char == ',' or char == '(':
            break
        else:
            city_name_state_abbreviation += char

    # Remove spaces from beginning and end of string
    city_name_state_abbreviation = city_name_state_abbreviation.strip()
    location_split = location_string.split(',')

    # Concatenate and format output
    state_abbreviation = location_split[1]
    state_abbreviation = state_abbreviation[1:3]
    city_name_state_abbreviation += ', ' + state_abbreviation

    return city_name_state_abbreviation


def reactors_per_region(master_list):
    ''' Takes as input the master list and returns a list of four integers representing
the number of reactors in each NRC region (1,2,3,4). Returns the data in this order. '''

    NRC_region_1 = 0
    NRC_region_2 = 0
    NRC_region_3 = 0
    NRC_region_4 = 0
    NRC_region_list = []

    # NRC region counters
    for i in range(len(master_list)):
        if master_list[i][5] == '1':
            NRC_region_1 += 1
        elif master_list[i][5] == '2':
            NRC_region_2 += 1
        elif master_list[i][5] == '3':
            NRC_region_3 += 1
        elif master_list[i][5] == '4':
            NRC_region_4 += 1

    NRC_region_list.append(NRC_region_1)
    NRC_region_list.append(NRC_region_2)
    NRC_region_list.append(NRC_region_3)
    NRC_region_list.append(NRC_region_4)

    return NRC_region_list


def top_react_by_mwt(master_list):
    ''' Accepts the master list and returns a sorted list of the top ten tuples where
each tuple has the form: (MWt, plant name, location) '''

    specified_columns_list = []
    extracted_list = []
    top_10_list = []

    # Extracting specified columns and generating list to be sorted
    for i in range(len(master_list)):
        extracted_list.append(int(master_list[i][19]))
        extracted_list.append(master_list[i][0])
        extracted_list.append(get_reactor_location(master_list[i][4]))
        specified_columns_list.append(extracted_list)
        extracted_list = []

    # sorting list (highest to lowest)
    specified_columns_list = sorted(specified_columns_list, reverse=True)

    # Extracting bottom 10
    for i in range(10):
        top_10_list.append(tuple(specified_columns_list[i]))

    return top_10_list


def bot_react_by_mwt(master_list):
    ''' Accepts the master list and returns a sorted list of the top ten tuples from
     lowest to highest MWt.'''

    specified_columns_list = []
    extracted_list = []
    bottom_10_list = []

    # Extracting specified columns and generating list to be sorted
    for i in range(len(master_list)):
        extracted_list.append(int(master_list[i][19]))
        extracted_list.append(master_list[i][0])
        extracted_list.append(get_reactor_location(master_list[i][4]))
        specified_columns_list.append(extracted_list)
        extracted_list = []

    # sorting list (Lowest to highest)
    specified_columns_list = sorted(specified_columns_list)

    # Extracting top 10
    for i in range(10):
        bottom_10_list.append(tuple(specified_columns_list[i]))

    return bottom_10_list


def reactors_in_state(master_list, state):
    ''' Returns a list of tuples where each tuple consists of:
(plant name, location) '''

    list_of_tuples = []
    extracted_list = []

    for i in range(len(master_list)):

        # Retrieving location and making list
        current_location = get_reactor_location(master_list[i][4])
        current_location = current_location.split(',')

        # Pulling state and removing spaces before and after string
        current_state = current_location[1]
        current_state = current_state.strip()

        # Generating list of tuples
        if current_state == state:
            extracted_list.append(master_list[i][0])
            extracted_list.append(get_reactor_location(master_list[i][4]))
            list_of_tuples.append(tuple(extracted_list))
            extracted_list = []
        else:
            continue

    return list_of_tuples


def years_active(master_list):
    ''' Takes the master_list and returns a list of ints, where each int is the number
of active years for that plant. '''

    years_of_operation = []

    # Extracting specified data
    for i in range(len(master_list)):
        years_of_operation.append(int(master_list[i][32]))

    # Sorting list (lowest to highest)
    years_of_operation = sorted(years_of_operation)

    return years_of_operation


def plot_years_active(years_active_list):
    '''
    DO NOT CHANGE
    Given list of ints, plot histogram showing age of reactors in US
    '''
    plt.grid(which='both')
    plt.hist(years_active_list, bins=22, edgecolor='black')
    plt.title('Active years per Nuclear Reactor')
    plt.xlabel('Years active')
    plt.ylabel('Number of reactors')
    plt.show()


def display_options():
    '''
    DO NOT CHANGE
    Display menu of options for program
    '''
    OPTIONS = 'Menu\n\
1: # Reactors in each region\n\
2: Top energy producing reactors\n\
3: Bottom energy producing reactors\n\
4: List reactors in specific state\n\
5: Plot histogram for how long reactors have been active'
    print(OPTIONS)


def main():
    ''' This function provides a user interface '''

    option = 'xyz'
    invalid_choice = True
    fp = open_file()
    master_list = read_file(fp)
    valid_choices = ['1', '2', '3', '4', '5', 'q', 'Q']

    # Loop until user quits
    while True:

        display_options()
        option = input('Choose an option, q to quit: ')

        if option not in valid_choices:
            print('\nInvalid choice, please try again\n')

        # Print the number of reactors in each NRC region
        elif option == '1':

            NRC_region_list = reactors_per_region(master_list)
            print('\n{:<8}{:<8}{:<8}{:<8}'.format('NRC 1', 'NRC 2', 'NRC 3', 'NRC 4'))
            print('{:<8}{:<8}{:<8}{:<8}\n'.format(NRC_region_list[0], NRC_region_list[1], NRC_region_list[2] \
                  , NRC_region_list[3]))

        # Print the top 10 power producing plants by MWt
        elif option == '2':

            top_10_list = top_react_by_mwt(master_list)

            print('\nTop 10 Reactors by MWt')
            print('{:<8}{:<30}{:<10}'.format('MWt', 'Reactor Name', 'Location'))
            for i in range(10):
                top_10_name = top_10_list[i][1]
                print('{:<8}{:<30}{:<10}'.format(top_10_list[i][0], top_10_name[:25], top_10_list[i][2]))
            print()

        # Print the bottom 10 power producing plants by MWt
        elif option == '3':

            bottom_10_list = bot_react_by_mwt(master_list)

            print('\nBottom 10 Reactors by MWt')
            print('{:<8}{:<30}{:<10}'.format('MWt', 'Reactor Name', 'Location'))
            for i in range(10):
                bottom_10_name = bottom_10_list[i][1]
                print('{:<8}{:<30}{:<10}'.format(bottom_10_list[i][0], bottom_10_name[:25], bottom_10_list[i][2]))
            print()

        # Call reactors_in_state and print the data appropriately
        elif option == '4':

            print()

            state_valid = False

            while state_valid == False:
                state = input('Please enter a 2 letter state code: ')
                state = state.upper()
                if state not in STATES:
                    state_valid = False
                    print('Please input a valid state')
                else:
                    state_valid = True
                    list_reactors_in_state = reactors_in_state(master_list, state)
                    num_reactors_in_state = len(list_reactors_in_state)

            if num_reactors_in_state == 0:

                print('\nThere are 0 reactors in {}'.format(state))

            else:

                print('\nThere are {} reactors in {}:'.format(num_reactors_in_state, state))
                for i in range(num_reactors_in_state):
                    print('{} in {}'.format(list_reactors_in_state[i][0], list_reactors_in_state[i][1]))
            print()

        # call years_active and use the return value to print a histogram of the data
        elif option == '5':

            years_active_list = years_active(master_list)
            plot_years_active(years_active_list)

        # Quit program upon user request
        elif option == 'q' or 'Q':
            break


if __name__ == '__main__':
    main()
