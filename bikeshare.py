import pandas as pd
import numpy as np
import sys

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities = list(CITY_DATA.keys())
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    The function takes input from the user, verifies whether it is allowed,
    and shows the selected values to the user.
    
    Returns
    -------
    city : string
        which city the user wants to see.
    month : string
        which month the user wants to see.
    day : string
        which day of week the user wants to see.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = str(input("Which city are you interested in? Washington, Chicago, New York City?\n")).lower()
        if city not in cities:
            print("Sorry, you can only get information about Washington, Chicago, New York City. Try again")
        else: 
            break
    while True:
        month = str(input("Which month are you interested in? Type all for all months\n")).lower()
        if month not in months:
            print("Sorry, you can only get information from January to June. Try again")
        else:
            break
    while True:
        day = str(input("Which day of the week are you interested in?? Type all for all days\n")).lower()
        if day not in days:
            print("Sorry, we only accept the full name of the day (for example: Monday). Try again")
        else:
            break
    print("Your filters are city: {}, month: {}, day: {}".format(city.capitalize(), month.capitalize(), day.capitalize()))
    print("")
    return city, month, day


def load_data(city, month, day):
    """
    The function loads the data filtered from the parameter, adding additional columns:
        - Start hour: extracted hour from Start Time
        - Day of week: - extracted day of week from Start Time
        - Month - extraxted number of month from Start Time
    Parameters
    ----------
    city : string
        the parameter is used to filter the selected city
    month : string
        the parameter is used to filter the selected month
    day : string
        the parameter is used to filter the selected day of week

    Returns
    -------
    df : dataframe
    """
    try:
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError as FileNotFound:
        print("We can't find " + FileNotFound.filename + ". Please put the file "
        + FileNotFound.filename + " in the same folder as the .py script")
        sys.exit()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start Hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['month'] = df['Start Time'].dt.month
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """
    The function provides information about the most popular travel times.
    Parameters
    ----------
    df : dataframe

    Returns
    -------
    None.
    """
    print("Information about most popular times of travel:")
    MonthMostCommon = pd.to_datetime(df['month']).dt.month_name().mode()[0]
    print("The most common month is " + MonthMostCommon)
    DayOfWeekMostCommon = df['day_of_week'].mode()[0]
    print("The most common day of week is " + DayOfWeekMostCommon)
    StartHourMostCommon = df['Start Time'].dt.hour.mode()[0]
    print("The most common start hour is " + str(StartHourMostCommon))
    MorningCount = len(df[(df['Start Hour'] >= 5) & (df['Start Hour'] <= 12)])
    print("Number of trip in the morning (5-12) " + str(MorningCount))
    AfternoonCount = len(df[(df['Start Hour'] >= 13) & (df['Start Hour'] <= 20)])
    print("Number of trip in the afternoon (13-20) " + str(AfternoonCount))
    NightCount = len(df[(df['Start Hour'] >= 21)]) + len(df[(df['Start Hour'] <= 4)])
    print("Number of night trips(21-4): " + str(NightCount))
    print("")


def station_stats(df):
    """
    The function provides information about the most popular stations
    Parameters
    ----------
    df : dataframe
    Returns
    -------
    None.
    """

    print("Information about most popular stations:")
    StartStationMostCommon = df['Start Station'].mode()[0]
    print("Most common start station is " + StartStationMostCommon)
    EndStationMostCommon = df['End Station'].mode()[0]
    print("Most common end station is " + EndStationMostCommon)
    df["Start-End Station"] = df["Start Station"] + " -> " + df["End Station"]
    StartEndStationsMostCommon = df["Start-End Station"].mode()[0]
    print("Most frequent combination of start station and end station is " + StartEndStationsMostCommon)
    print("")


def trip_duration_stats(df):
    """
    The function provides information about trip duration
    Parameters
    ----------
    df : dataframe
    Returns
    -------
    None.
    """

    print("Information about trip duration:")
    TotalDuration = df['Trip Duration'].sum()/60
    print("Total duration trip is " + str(round(TotalDuration, 2)) + " minutes")
    MeanDuration = df['Trip Duration'].mean()/60
    print("Mean duration trip is " + str(round(MeanDuration, 2)) + " minutes")
    MeadianDuration = df['Trip Duration'].median()/60
    print("Meadian duration trip is " + str(round(MeadianDuration, 2)) + " minutes")
    ModeDuration = df['Trip Duration'].mode()[0]/60
    print("The most common travel time is " + str(round(ModeDuration, 2)) + " minutes")
    MaxDuration = df['Trip Duration'].max()/60
    print("The maximum duration of the trip is " + str(round(MaxDuration, 2)) + " minutes")
    print("")


def user_stats(df):
    """
    The function provides information about users
    Parameters
    ----------
    df : dataframe

    Returns
    -------
    None.

    """
    print("Information about users:")
    CountUserTypesSub = len(df[df['User Type'] == 'Subscriber'])
    CountUserTypesCus = len(df[df['User Type'] == 'Customer'])
    CountUserTypesDep = len(df[df['User Type'] == 'Dependent'])
    print("User type: Subscriber " + str(CountUserTypesSub))
    print("User type: Customer " + str(CountUserTypesCus))
    print("User type: Dependent " + str(CountUserTypesDep))
    if 'Gender' in df:
        CountGenderMale = len(df[df['Gender'] == 'Male'])
        CountGenderFemale = len(df[df['Gender'] == 'Female'])
        CountGenderNoDef = df['Gender'].isna().sum()
        print("Number of male users " + str(CountGenderMale))
        print("Number of female users " + str(CountGenderFemale))
        print("The number of users without a specified gender " + str(CountGenderNoDef))
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')
    if 'Birth Year' in df:
        YearMostCommon = df['Birth Year'].mode()[0]
        print("Most common Birth Year is " + str(round(YearMostCommon)))
        MaxYear = df['Birth Year'].max()
        print("Recent Birth Year is " + str(round(MaxYear)))
        MinYear = df['Birth Year'].min()
        print("Earliest Birth Year is " + str(round(MinYear)))
        CountBirhtYearNoDef = df['Gender'].isna().sum()
        print("The number of users without a specified birth date " + str(CountBirhtYearNoDef))
    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')


def detalis(df):
    """
    The function allows the user to show detailed data.
    Parameters
    ----------
    df : dataframe

    Returns
    -------
    None.
    """
    DetaliedData = str(input("which you like to see detalis? Enter yes or no.\n")).lower()
    Startiloc = 0
    EndIloc = 4
    while True:
        if DetaliedData != 'yes':
            break
        else:
            df1 = df.iloc[Startiloc:EndIloc]
            print(df1)
            MoreData = str(input("which you like to see another 5 rows? Enter yes or no.\n")).lower()
            if MoreData != 'yes':
                break
            else:
                Startiloc += 4
                EndIloc += 4
                df1 = df.iloc[Startiloc:EndIloc]
                if df1.empty:
                    print("There is no data to show.")
                    break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        detalis(df)
        restart = input('\nWould you explore data again? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()