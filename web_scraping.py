from bs4 import BeautifulSoup, NavigableString
from urllib import request, parse
import ssl

WEBSOC_URL = "https://www.reg.uci.edu/perl/WebSoc"

class InvalidCourseCode(Exception):
    pass

class CoursePage:
    def __init__(self, y : str, q : str, cc : str):
        self.year = y
        self.quarter = q
        self.course_code = cc
        self.course_info = None
        self.url = self._build_url()
        self.check_cc_valid()


    def _get_table_info(self, table) -> dict:
        """Gets the table soup and extracts the course information and returns
        it as a dictionary.
        """
        headers = []
        values = []
        for tr in list(table):
            # Find actual headers and values (Should only be two rows)
            if len(list(tr)) > 2:
                for tc in list(tr):
                    if str(tc).strip():
                        if tc.name == "th":
                            headers.append(tc.text.lower())
                        else:
                            values.append(tc.text)
        return {headers[i]: values[i] for i in range(len(headers))}

    def _build_url(self):
        query_parameters = [('YearTerm', self.year + "-" + self.quarter), ('CourseCodes', self.course_code)]
        return WEBSOC_URL + '?' + parse.urlencode(query_parameters)

    def _refresh(self):
        """If this function is called, the url will be built, the data from the page will be saved into dict"""
        context = ssl._create_unverified_context()
        page = request.urlopen(self.url, context=context)
        soup = BeautifulSoup(page, "html.parser")
        table = soup.find(name="div", class_="course-list").find(name="table")
        self.course_info = self._get_table_info(table)

    def check_cc_valid(self):
        context = ssl._create_unverified_context()
        page = request.urlopen(self.url, context=context)
        soup = BeautifulSoup(page, "html.parser")
        if "No courses matched" in soup.text:
            raise InvalidCourseCode()

    def get_status(self):
        self._refresh()
        return self.course_info["status"]

