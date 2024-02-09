
class Vacancy:
    def __init__(self, id: int, employer_id: int, name: str, salary_from: int, salary_to: int, description: str, requirement: str, area: str, alternate_url: str) -> None:
        self.id = id
        self.employer_id = employer_id
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description
        self.requirement = requirement
        self.area = area
        self.alternate_url = alternate_url