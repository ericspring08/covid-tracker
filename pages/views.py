from django.shortcuts import render
from covid import Covid
import locale
import pandas as pd

# Create your views here.
def covid_view(request, *args, **kwargs):
    covid = Covid()

    state = request.POST.get('state')
    print(state)
    locale.setlocale(locale.LC_ALL, 'en_US')
    covid_data= pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv', usecols = ['date', 'state', 'fips','cases','deaths','confirmed_cases','confirmed_deaths','probable_cases','probable_deaths'])
    covid_data = covid_data.sort_values(by = "cases", ascending=False)
    pd.set_option('display.max_column', None)
    List_of_Countries = covid_data['state'].to_list()
    State_Cases = covid_data['confirmed_cases'].to_list()
    Active_Cases = covid_data['confirmed_cases'].to_list()
    Deaths = covid_data['deaths'].tolist()
    Total_Cases = covid_data['cases'].tolist()
    state_dictionary= {}
    if state in List_of_Countries:
        if state == "Global":
            active = locale.format("%d", covid.get_total_active_cases(), grouping=True)
            deaths = locale.format("%d", covid.get_total_deaths(), grouping=True)
            recovered = locale.format("%d", covid.get_total_recovered(), grouping=True)
            confirmed = locale.format("%d", covid.get_total_confirmed_cases(), grouping=True)
            recovery_rate = str(round(100 - ((covid.get_total_deaths()/covid.get_total_confirmed_cases()) *100), 3)) + "%"
            death_rate = str(round((covid.get_total_deaths()/covid.get_total_confirmed_cases()) * 100,3)) + "%"
        else:
            active = locale.format("%d", Active_Cases[List_of_Countries.index(state)], grouping=True)
            deaths = locale.format("%d", Deaths[List_of_Countries.index(state)], grouping=True)
            recovered = locale.format("%d", Total_Cases[List_of_Countries.index(state)]- Active_Cases[List_of_Countries.index(state)], grouping=True)
            confirmed = locale.format("%d", Total_Cases[List_of_Countries.index(state)], grouping=True)
            recovery_rate = str(round(100 - ((covid.get_total_deaths()/covid.get_total_confirmed_cases()) *100), 3)) + "%"
            death_rate = str(round((covid.get_total_deaths()/covid.get_total_confirmed_cases()) * 100,3)) + "%"
    else:
        state = "Global"
        active = locale.format("%d", covid.get_total_active_cases(), grouping=True)
        deaths = locale.format("%d", covid.get_total_deaths(), grouping=True)
        recovered = locale.format("%d", covid.get_total_recovered(), grouping=True)
        confirmed = locale.format("%d", covid.get_total_confirmed_cases(), grouping=True)
        recovery_rate = str(round(100 - ((covid.get_total_deaths()/covid.get_total_confirmed_cases()) *100), 3)) + "%"
        death_rate = str(round((covid.get_total_deaths()/covid.get_total_confirmed_cases()) * 100,3)) + "%"
    context = {
        "active":active,
        "deaths":deaths,
        "recovered":recovered,
        "confirmed":confirmed,
        "countries":List_of_Countries,
        "confirmed_list":State_Cases,
        "state": state, 
        "active_cases":Active_Cases,
        "recovery_rate":recovery_rate,
        "death_rate":death_rate
    }
    return render(request, "covid.html", context)
def graph_view(request, *args, **kwargs):
    locale.setlocale(locale.LC_ALL, 'en_US')
    covid = Covid()
    active = locale.format("%d", covid.get_total_active_cases(), grouping=True)
    death_rate = str(round((covid.get_total_deaths()/covid.get_total_confirmed_cases())*100, 3)) + "%"
    recovered = locale.format("%d", covid.get_total_recovered(), grouping=True)
    confirmed = str(round((covid.get_total_confirmed_cases()/7000000000)*100, 3)) + "%"

    
    context={
        "confirmed_statistic":confirmed,
        "death_rate":death_rate

    }
    return render(request, "graphs.html", context)