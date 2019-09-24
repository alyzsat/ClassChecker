from bs4 import BeautifulSoup, NavigableString
from urllib import request, parse

def get_table_info(table) -> dict:
    """Gets the table soup and extracts the course information and returns
    it as a dictionary.
    """
    headers = []
    values = []
    table_info = dict()
    for tr in list(table):
        # Find actual headers and values (Should only be two rows)
        if len(list(tr)) > 2:
            for tc in list(tr):
                if str(tc).strip():
                    if tc.name == "th":
                        headers.append(tc.text)
                    else:
                        values.append(tc.text)
    return {headers[i]: values[i] for i in range(len(headers))}



page = request.urlopen("https://www.reg.uci.edu/perl/WebSoc?YearTerm=2019-92&CourseCodes=01020")
soup = BeautifulSoup(page, "html.parser")

# Add error handling for invalid course code
# (because invalid course codes won't have a table to check)

table = soup.find(name="div", class_="course-list").find(name="table")
table_info = get_table_info(table)
print(table_info)

# title = table.find_all(name="th")
#
# value = table.find_all(name="td")

# print(title)
# print(value)