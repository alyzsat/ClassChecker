from bs4 import BeautifulSoup
from urllib import request, parse
import ssl
import re


WEBSOC_URL = "https://www.reg.uci.edu/perl/WebSoc"


class InvalidCourseCode(Exception):
    """Raise this error if the course code page cannot be found"""
    pass


class CoursePage:
    def __init__(self, year: str, quarter: str, course_code: str):
        """Initializes the CoursePage object with the year, quarter code, and
        course code. If the course code is invalid, then an error will raise.
        """
        self.course_code = course_code
        self.url = self._build_url(year, quarter, course_code)
        self._check_cc_valid()
        self.course_info = dict()

    def get_course_code(self) -> str:
        """Returns the course code of the course"""
        return self.course_code

    def get_status(self) -> str:
        """Returns the availability status of the class"""
        return self.course_info["status"]

    def get_type(self) -> str:
        """Returns the type of the class"""
        return self.course_info["type"]

    def get_enrolled(self) -> int:
        """Returns the number of people that are enrolled in the class"""
        return int(self.course_info["enr"])

    def get_max(self) -> int:
        """Returns the max number of people that can enroll in the class"""
        return int(self.course_info["max"])

    def get_restrictions(self) -> [str]:
        """Returns a list of the restrictions"""
        raw = self.course_info["rstr"]
        return re.findall("[A-ORSX]", raw)

    def refresh(self):
        """If this function is called, the url will be built, the data from the page will be saved into dict"""
        soup = self._open_page()
        table = soup.find(name="div", class_="course-list").find(name="table")
        self.course_info = self._get_table_info(table)

    def _get_table_info(self, table) -> dict:
        """Gets the table soup and extracts the course information and returns
        it as a dictionary.
        """
        headers = []
        values = []
        for tr in list(table):
            # Find actual headers and values (Should only be two rows)
            # (If the row has 1 or 2 cells, then it's not part of the real table)
            if len(list(tr)) > 2:
                for tc in list(tr):
                    if str(tc).strip():
                        if tc.name == "th":
                            headers.append(tc.text.lower())
                        else:
                            values.append(tc.text)
        return {headers[i]: values[i] for i in range(len(headers))}

    def _build_url(self, year: str, quarter: str, course_code: str):
        """Builds the url using the year, quarter code, and course code"""
        query_parameters = [('YearTerm', year + "-" + quarter), ('CourseCodes', course_code)]
        return WEBSOC_URL + '?' + parse.urlencode(query_parameters)

    def _open_page(self) -> BeautifulSoup:
        """Opens the page and returns a soup object"""
        context = ssl._create_unverified_context()
        page = request.urlopen(self.url, context=context)
        return BeautifulSoup(page, "html.parser")

    def _check_cc_valid(self):
        """Checks if the course code is valid by opening the page and seeing
        if the course exists.
        """
        soup = self._open_page()
        if "No courses matched" in soup.text:
            raise InvalidCourseCode()
