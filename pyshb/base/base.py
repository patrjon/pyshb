__all__ = ['SHBBase']

# Standard Library:
from pathlib import Path

# Third party
from bs4 import BeautifulSoup

# Local applications:


class SHBBase:
    """
    Base class for PySHB. This class does the following:
        * read the input file
        * extracts all tables in the html file and stores the information in a nested list
    """

    def __init__(self, file_path):
        """
        Initiation method.
        :param file_path: path to file.
        :type file_path: str or pathlib.Path
        """

        # Init variables:
        self.file_path = file_path
        self.html_string = ''
        self.tables = []

        # Read file:
        self._read_file()

        # Parse html to nested list
        self._html_to_list()

    def _read_file(self):
        """
        Private method to read file to string.
        :return:
        """
        # Convert str to pathlib.Path() object.
        if isinstance(self.file_path, str):
            self.file_path = Path(self.file_path)

        # Check if file_path exists:
        if not self.file_path.exists():
            raise FileNotFoundError(f'File not found: {self.file_path}')

        # Open and read the "xls" file
        with open(self.file_path, encoding='windows-1252') as f:
            self.html_string = f.read()

    def _html_to_list(self):
        """
        Private method to extract all tables from html string to a nested list.

        :return: a nested list of all tables in file.
        :rtype list
        """

        #  Parse the HTML as a string
        soup = BeautifulSoup(self.html_string, 'html.parser')

        # Loop through all tables in soup
        for table in soup.find_all('table'):
            # Init table data as an empty list
            table_data = []

            # Loop trough all rows
            for row in table.find_all('tr'):
                # Loop through all columns, get the text and convert to lower case only.
                row_data = [col.get_text().lower() for col in row.find_all('td')]

                # Append to table_data:
                table_data.append(row_data)

            # Append to tables:
            self.tables.append(table_data)
