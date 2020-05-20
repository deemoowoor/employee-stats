import math
import requests
import re
import statistics
import sys
from typing import List
from errors import ApiError

ENDPOINT_URL = 'http://dummy.restapiexample.com/api/v1'


class EmployeeApiClient:

    def __init__(self, baseUrl: str):
        self._baseUrl = baseUrl

    def employees(self):
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

    def __init__(self, data: List[str]):
        self._data = data

    def first_names(self) -> List[str]:
        return [re.match('^([A-Za-z]+)\\s', i['employee_name']).group(1) for i in self._data]

    def last_names(self) -> List[str]:
        return [re.match('.*\\s([A-Za-z]+)$', i['employee_name']).group(1) for i in self._data]

    def ages(self) -> List[float]:
        return [float(i['employee_age']) for i in self._data]

    def mean_age(self) -> float:
        return statistics.mean(self.ages())

    def median_age(self) -> float:
        return statistics.median(self.ages())

    def age_variance(self) -> float:
        return statistics.pvariance(self.ages())

    def salaries(self) -> List[float]:
        return [float(i['employee_salary']) for i in self._data]

    def mean_salary(self) -> float:
        return statistics.mean(self.salaries())

    def median_salary(self) -> float:
        return statistics.median(self.salaries())

    def salary_variance(self) -> float:
        return statistics.pvariance(self.salaries())


def options_map() -> None:
    return {
        '-salary': print_salary_stats,
        '-age': print_age_stats,
        '-summary': print_summary,
        '-modes': print_modes
    }

def print_salary_stats(stats: EmployeeStatistics) -> None:
    print(f"Average salary:       {stats.mean_salary()}")
    print(f"Median salary:        {stats.median_salary()}")
    print(f"Salary variance:      {stats.salary_variance()}")

def print_age_stats(stats: EmployeeStatistics) -> None:
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

def main(args: List[str]) -> None:
    client = EmployeeApiClient(ENDPOINT_URL)
    data = client.employees()
    stats = EmployeeStatistics(data)

    if not args:
        print_summary(stats)
    else:
        options = options_map()
        for arg in args:
            if arg in options:
                options[arg](stats)

if __name__ == "__main__":
    main(sys.argv[1:])