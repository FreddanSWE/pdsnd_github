import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city do you want to analyse? Please choose from Chicago, New York City or Washington?\n")
    city = city.lower()
    while city not in ('chicago', 'new york city', 'washington'):
        city = input("Please enter valid city name Chicago, New York City or Washington:\n")
        city = city.lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Which month would you like to analyse? Please choose from January, February, March, April, May, June or type 'all' to analyse all the months\n")
    month = month.lower()
    while month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        month = input("Please enter valid month name January, February, March, April, May, June or type 'all' to analyse all the months\n")
        month = month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day would you like to analyse? Please choose from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or type 'all' to analyse all the days\n")
    day = day.lower()
    while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
        day = input("Please enter valid day name Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or type 'all' to analyse all the days\n")
        day = day.lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(r"C:/Users/YI48150/OneDrive - Volvo Group/Fredrik Lindblad/Penta Industrial/Udacity/Python project 1/All project files/" + CITY_DATA[city])
    
    if month != "all" and day != "all":
        df = df[(pd.to_datetime(df['Start Time']).dt.strftime("%B").str.lower() == month) & (pd.to_datetime(df['Start Time']).dt.strftime("%A").str.lower() == day)]

    else:
        if month != "all": 
            df = df[pd.to_datetime(df['Start Time']).dt.strftime("%B").str.lower() == month]
    if day != "all": 
        df = df[pd.to_datetime(df['Start Time']).dt.strftime("%A").str.lower() == day]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df["month"] = pd.to_datetime(df['Start Time']).dt.strftime("%B").str.lower()
    most_common_month = df['month'].mode()[0]
    print('Most Common Month:', most_common_month)
   
   
    
    # display the most common day of week
    df["day_of_week"] = pd.to_datetime(df['Start Time']).dt.strftime("%A").str.lower()
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', most_common_day)

    # display the most common start hour
    df["hour"] = pd.to_datetime(df['Start Time']).dt.strftime("%H").str.lower()
    most_common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most Common Start Station is: "  +df["Start Station"].mode()[0])

    # display most commonly used end station
    print("Most Common End Station is: "  +df["End Station"].mode()[0])

    # display most frequent combination of start station and end station trip
    df["full trip"]="From "+df["Start Station"]+" to "+df["End Station"]
    print("Most frequent combination of start and end station is: "  +df["full trip"].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is: "  + str(df["Trip Duration"].sum()))

    # display mean travel time
    print("The mean travel time is: "  + str(df["Trip Duration"].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df["User Type"]=df["User Type"].fillna("No User Type Found")
    ct=df["User Type"].value_counts().reset_index().rename(columns={"index" : "User Type", "User Type" : "Count of User type"})
    print(ct.to_string(index=False))
    # Display counts of gender
    if city!="washington":
        df["Gender"]=df["Gender"].fillna("Gender N/A")    
        gender_ct=df["Gender"].value_counts().reset_index().rename(columns={"index" : "Gender", "Gender" : "Count of Gender"})
        print(gender_ct.to_string(index=False))
    
        
    # Display earliest, most recent, and most common year of birth
      
    df["Birth Year"] = pd.to_datetime(df['Start Time']).dt.strftime("%Y").str.lower() 
    print("Earliest birth year  " + str(df["Birth Year"].min()))
    print("Most recent birth year  " + str(df["Birth Year"].max()))
    print("Most common birth year  " + str(df["Birth Year"].mode()[0]))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def view_data(df):
    display = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while display == 'yes':
        print(df.iloc[start_loc:start_loc+5].reset_index(drop=True))
        start_loc += 5
        display = input("Do you wish to continue? Yes/No  : ").lower()
    else:
        return


            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        view_data (df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
