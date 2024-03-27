# Create an income tax calculator:
#  - Generate at least 500 documents , with fields: name, surname, date of birth , age (determined from date of birth), anual salary before tax (EUR, round to 2 numbers after comma)
#  - Create a CLI application that would let us get first 10 people from database within the age bracket [min_age, max_age]
#  - Those people name surname and age should be shown as an option to choose.
#  - When one of ten options is chosen, there should be calculated tax return (it should be created a document as a tax card, values taken from database). Lets say GPM tax is 20% and HealtTax is 15% from 90% of the income left after GPM deduction.
#  - The final values should be show and wrriten to database (like a generated data and taxes paid, take home pay etc.) and portrayed in a web page (use flask and docker, show the url were to click )


# import random
# from datetime import datetime, timedelta
# from typing import Dict, List
# from pymongo import MongoClient
# from faker import Faker


# class DocumentGenerator:
#     def __init__(self) -> None:
#         self.fake = Faker()
#         self.start_date = datetime(1950, 1, 1)
#         self.end_date = datetime(2005, 1, 1)

#     def generate_document(self) -> Dict:
#         first_name = self.fake.first_name()
#         last_name = self.fake.last_name()
#         date_of_birth = self.generate_date_of_birth()
#         age = self.calculate_age(date_of_birth)
#         salary = self.generate_salary()
#         return {
#             "name": first_name,
#             "surname": last_name,
#             "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
#             "age": age,
#             "annual_salary_before_tax": salary,
#         }

#     def generate_date_of_birth(self):
#         return self.start_date + timedelta(
#             days=random.randint(0, (self.end_date - self.start_date).days)
#         )

#     def calculate_age(self, date_of_birth) -> int:
#         today = datetime.today()
#         return (
#             today.year
#             - date_of_birth.year
#             - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
#         )

#     def generate_salary(self) -> float:
#         return round(random.uniform(20000, 120000), 2)

#     def people_in_age_range(self, min_age, max_age) -> List:
#         query = {"age": {"$gte": min_age, "$lte": max_age}}
#         people = self.collection.find(query).limit(10)
#         return list(people)


# class TaxCalculator:
#     def __init__(self) -> None:
#         self.gpm_tax_rate = 0.20
#         self.health_tax_rate = 0.15

#     def calculate_tax_return(self, salary) -> float:
#         remaining_income = salary * (1 - self.gpm_tax_rate)
#         health_tax_base = remaining_income * 0.90
#         health_tax = health_tax_base * self.health_tax_rate
#         return round(health_tax, 2)


# if __name__ == "__main__":
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client["taxcalculator"]
#     collection = db["taxcalculator_collection"]

#     document_generator = DocumentGenerator()
#     documents = []
#     for _ in range(500):
#         document = document_generator.generate_document()
#         documents.append(document)

#     min_age = 20
#     max_age = 40
#     people = list(
#         collection.find({"age": {"$gte": min_age, "$lte": max_age}}).limit(10)
#     )

#     print("Select one of the following people:")
#     for idx, person in enumerate(people):
#         print(f"{idx+1}. {person['name']} {person['surname']} (Age: {person['age']})")

#     option = int(input("Enter the option number: ")) - 1

#     print("Number of people:", len(people))
#     print("Chosen option:", option)

#     if 0 <= option < len(people):
#         selected_person = people[option]

#         tax_calculator = TaxCalculator()
#         tax_return = tax_calculator.calculate_tax_return(
#             selected_person["annual_salary_before_tax"]
#         )

#         print(
#             f"Tax return for {selected_person['name']} {selected_person['surname']}: {tax_return} EUR"
#         )
#     else:
#         print("Invalid option number. Please choose a valid option.")


import random
from datetime import datetime, timedelta
from typing import Dict
from pymongo import MongoClient
from faker import Faker


class DocumentGenerator:
    def __init__(self) -> None:
        self.fake = Faker()
        self.start_date = datetime(1950, 1, 1)
        self.end_date = datetime(2005, 1, 1)

    def generate_document(self) -> Dict:
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        date_of_birth = self.generate_date_of_birth()
        age = self.calculate_age(date_of_birth)
        salary = self.generate_salary()
        return {
            "name": first_name,
            "surname": last_name,
            "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
            "age": age,
            "annual_salary_before_tax": salary,
        }

    def generate_date_of_birth(self):
        return self.start_date + timedelta(
            days=random.randint(0, (self.end_date - self.start_date).days)
        )

    def calculate_age(self, date_of_birth) -> int:
        today = datetime.today()
        return (
            today.year
            - date_of_birth.year
            - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        )

    def generate_salary(self) -> float:
        return round(random.uniform(20000, 1000000), 2)


class TaxCalculator:
    def __init__(self) -> None:
        self.gpm_tax_rate = 0.20
        self.health_tax_rate = 0.15

    def calculate_tax_return(self, salary) -> float:
        remaining_income = salary * (1 - self.gpm_tax_rate)
        health_tax_base = remaining_income * 0.90
        health_tax = health_tax_base * self.health_tax_rate
        return round(health_tax, 2)


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["taxcalculator"]
    collection = db["taxcalculator_collection"]

    document_generator = DocumentGenerator()
    documents = []
    for _ in range(500):
        document = document_generator.generate_document()
        documents.append(document)

    collection.insert_many(documents)

    min_age = 20
    max_age = 40
    people = list(
        collection.find({"age": {"$gte": min_age, "$lte": max_age}}).limit(10)
    )

    print("Select one of person:")
    for idx, person in enumerate(people):
        print(f"{idx+1}. {person['name']} {person['surname']} (Age: {person['age']})")

    option = int(input("Enter the option number: ")) - 1

    print("Number of people:", len(people))
    print("Chosen option:", option)

    if 0 <= option < len(people):
        selected_person = people[option]

        tax_calculator = TaxCalculator()
        tax_return = tax_calculator.calculate_tax_return(
            selected_person["annual_salary_before_tax"]
        )

        print(
            f"Tax for {selected_person['name']} {selected_person['surname']} is {tax_return} EUR"
        )
    else:
        print("Invalid option number. Please choose a valid option.")
