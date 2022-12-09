import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
  
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.groupby(['race'])['race'].count().sort_values(ascending = False)

    # What is the average age of men?
    df_male = df[df['sex'] == 'Male']
    average_age_men = round(df_male['age'].mean(), 1)
  
    # What is the percentage of people who have a Bachelor's degree?
    education_series = df.groupby(['education'])['education'].count()
    percentage_bachelors = round(education_series['Bachelors'] / 
                                 education_series.sum() * 100, 
                                 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    # with and without `Bachelors`, `Masters`, or `Doctorate`
  
    high_ed_list = ['Bachelors', 'Doctorate', 'Masters']
    # DF with people who have higher education and >50K salary
    df_high_ed_more_50k = df[df['education'].isin(high_ed_list) & (df['salary'] == '>50K')]
    # Total amount of people who have higher education
    higher_education = education_series.loc[high_ed_list].sum()

    # DF with people who don't have higher education and have >50K salary
    df_low_ed_more_50k = df[(~df['education'].isin(high_ed_list)) & (df['salary'] == '>50K')]
    # Total amount of people who don't have higher education
    lower_education = education_series.drop(index = high_ed_list).sum()
    
    # percentage with salary >50K
    higher_education_rich = round(df_high_ed_more_50k.shape[0] / 
                                  higher_education * 100, 
                                  1)
    lower_education_rich = round(df_low_ed_more_50k.shape[0] /
                                 lower_education * 100,
                                 1)
  
    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    
    # Amount of people who have the minimum number of hours per week
    num_min_workers = df[df['hours-per-week'] == min_work_hours].shape[0]
    # Amount of people who have the minimum number of hours per week and salary >50K
    num_rich_min_workers = df[(df['hours-per-week'] == min_work_hours) & (df['salary'] == '>50K')].shape[0]
    rich_percentage = num_rich_min_workers / num_min_workers * 100
    
    # What country has the highest percentage of people that earn >50K?

    # DF with country, salary and amount of people
    df_country_sal_count =  df[['native-country', 'salary']].groupby(['native-country', 'salary']).agg(country_count = ('native-country', 'count')).reset_index()
    # Series with country and amount of people with all salaries
    series_country_count = df_country_sal_count.groupby(['native-country'])['country_count'].sum()

    # DF with country and amount of people with salaries >50K
    df_country_count = df_country_sal_count[df_country_sal_count['salary'] == '>50K'][['native-country', 'country_count']].set_index('native-country')

    # DF with country, amount of people with all salaries, amount of people with salaries >50K
    df_merge = pd.merge(series_country_count, df_country_count, on='native-country').reset_index()

    # Lists of values from columns in df_merge dataframe
    country_count_total_list = df_merge['country_count_x'].values.tolist()
    country_count_more_than_50K_list = df_merge['country_count_y'].values.tolist()
    native_country_list = df_merge['native-country'].values.tolist()

    # Initial values for searching maximum percentage and highest earning country
    max_percentage = 0
    highest_earning_country = None

    # The loop is searching for the country and maximum
    for i in range(df_merge.shape[0]):
      percentage = country_count_more_than_50K_list[i] / country_count_total_list[i] * 100
      if (percentage > max_percentage):
        highest_earning_country = native_country_list[i]
        max_percentage = percentage
        
    highest_earning_country_percentage = round(max_percentage, 1)
    
    # Identify the most popular occupation for those who earn >50K in India.
  
    IN_more_than_50k_series = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')].groupby(['occupation'])['occupation'].count().sort_values(ascending = False)
    top_IN_occupation = IN_more_than_50k_series.first_valid_index()

    # DO NOT MODIFY BELOW THIS LINE
    
    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)
    
    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
