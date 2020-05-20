import math
import requests
import re
import statistics
import sys
from typing import List
from errors import ApiError

import matplotlib.pyplot as plt
import squarify
 

ENDPOINT_URL = 'http://dummy.restapiexample.com/api/v1'


class EmployeeApiClient:

    def __init__(self, baseUrl: str):
        self._baseUrl = baseUrl

    def employees(self) -> List[dict]:
        r = requests.get(f"{self._baseUrl}/employees")
        if r.status_code != 200:
            raise ApiError(f"Endpoint responded with an error: {r.status_code}")
        else:
            response = r.json()
            if 'data' not in response:
                raise ApiError("Unexpected response contents for /employees")

            data = response['data']
            return data


class EmployeeStatistics:

    def __init__(self, client: EmployeeApiClient):
        self._client = client
        self._data = []

    def _get_data(self) -> List[dict]:
        if not self._data:
            self._data = self._client.employees()
        return self._data
        
    def first_names(self) -> List[str]:
        return [re.match('^([A-Za-z]+)\\s', i['employee_name']).group(1) for i in self._get_data()]

    def last_names(self) -> List[str]:
        return [re.match('.*\\s([A-Za-z]+)$', i['employee_name']).group(1) for i in self._get_data()]

    def ages(self) -> List[float]:
        return [float(i['employee_age']) for i in self._get_data()]

    def mean_age(self) -> float:
        return statistics.mean(self.ages())

    def median_age(self) -> float:
        return statistics.median(self.ages())

    def age_variance(self) -> float:
        return statistics.pvariance(self.ages())

    def salaries(self) -> List[float]:
        return [float(i['employee_salary']) for i in self._get_data()]

    def mean_salary(self) -> float:
        return statistics.mean(self.salaries())

    def median_salary(self) -> float:
        return statistics.median(self.salaries())

    def salary_variance(self) -> float:
        return statistics.pvariance(self.salaries())

    def salary_age_group(self) -> List[dict]:
        return sorted([
            {'salary': float(d['employee_salary']), 
            'age': float(d['employee_age'])} for d in self._get_data()], key=lambda x: x['salary'])


def print_salary_stats(stats: EmployeeStatistics) -> None:
    """ Prints just the salary statistics """
    print(f"Average salary:       {stats.mean_salary()}")
    print(f"Median salary:        {stats.median_salary()}")
    print(f"Salary variance:      {stats.salary_variance()}")


def print_age_stats(stats: EmployeeStatistics) -> None:
    """ Prints just the age statistics """
    print(f"Average employee age: {stats.mean_age()}")
    print(f"Median employee age:  {stats.median_age()}")
    print(f"Age variance:         {stats.age_variance()}")


def print_modes(stats: EmployeeStatistics) -> None:    
    try:
        print(f"Most popular:     {statistics.mode(stats.first_names())}")
    except statistics.StatisticsError:
        print(f"No unique first name mode, none are more popular than the others")
    
    try:
        print(f"Most popular:      {statistics.mode(stats.last_names())}")
    except statistics.StatisticsError:
        print(f"No unique last name mode, none are more popular than the others")


def print_header():
    print("=================================================================")
    print(" The Path-E-Tech Management EMPLOYEE STATISTICS ")
    print("-----------------------------------------------------------------")
    print("    (`'`'`'`')")
    print("     |      |")
    print("     |      |")
    print("    (|-()()-|)")
    print("     | (__) |")
    print("     |      |")
    print("     |______|")
    print("    /._/\\/\\_.\\                            .------.")
    print("   /  , /\\    \\                          ( ______ )")
    print("  ; / \\\\|| __  ;                         (________)")
    print("  |-|  './ \\/|-|                         (  water )")
    print("  \\ |   |    | /                         (--------)")
    print("   '\\___|____/`           .-\"\"-.         ( ______ )")
    print("     |--LI--|           .'      \\         \\_    _/")
    print("     |  |   |          //  |-()()         __|__|__")
    print("     |  |   |         ; |  |  () |    ___/        \\")
    print("     |  |   |         | `\" `     |    |  |  ____  |")
    print("     |  |   |       ,_|   | |    |    |  | | || | |")
    print("     |  |   |       `-;   (_}    ;    |__| |____| |")
    print("     |  |   |          '.,   __.'      \/|        |")
    print(" jgs |__|___|            / /|  |         |        |")
    print("..----'=||='----.   jgs / / |  |         |        | jrm")
    print(' `""""`"  "`""""`      (__) (__)         |________|')
    print(':*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:._')
    print("=================================================================")


def print_summary(stats: EmployeeStatistics) -> None:
    print_header()
    print_salary_stats(stats)
    print_age_stats(stats)
    print_modes(stats)


def show_treemap(stats: EmployeeStatistics) -> None:
    """ Displays a treemap chart of salaries and ages to help determine if 
    there is any ageism implanted into the corporate policy of selecting
    positions and salaries """
    squarify.plot(sizes=list(map(lambda x: x['salary'], stats.salary_age_group())),
        label=list(map(lambda x: x['age'], stats.salary_age_group())), alpha=.7)
    plt.axis('off')
    plt.show()

def print_help() -> None:
    """ Prints command line options help information """
    print_header()
    print("Options:")
    print('  -salary  print salary statistics')
    print('  -age  print age statistics')
    print('  -summary  print a summary of all statistics')
    print('  -modes  print mode statistics')
    print('  -treemap  show a graphical treemap of salaries vs age')
    print('  -help  print this help information')

def options_map() -> None:
    """ Maps program command line arguments to functions """
    return {
        '-salary': print_salary_stats,
        '-age': print_age_stats,
        '-summary': print_summary,
        '-modes': print_modes,
        '-treemap': show_treemap,
        '-help': print_help
    }

def main(args: List[str]) -> None:
    stats = EmployeeStatistics(EmployeeApiClient(ENDPOINT_URL))
    if not args:
        print_summary(stats)
    else:
        options = options_map()

        for arg in args:
            if arg in options:
                if arg == '-help':
                    options[arg]()
                else:
                    options[arg](stats)
            else:
                print(f"Unknown option: {arg}")


if __name__ == "__main__":
    main(sys.argv[1:])