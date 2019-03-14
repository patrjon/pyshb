__all__ = ['SHBTransactions']

# Standard Library:

# Third party
import pandas as pd
import numpy as np

# Local applications:


class SHBTransactions:
    """
    Class for reading transactions from SHBBase.tables to a pandas.DataFrame
    """
    def __init__(self, shb_base):
        """
        Initiation method.
        :param shb_base: Instance of SHBBase class
        """

        # Init variables
        self.shb_base = shb_base

    def get_transactions(self, transactions_table_id, drop_prel=True):
        """
        Read the transactions section in file.

        :param transactions_table_id: index of transaction table in shb_base.tables
        :type transactions_table_id: int
        :param drop_prel: Skip all PREL transactions.
        :type drop_prel: bool
        :return: pandas.dataframe of transaction with headers as in file
        """
        # Get the table with transaction data:
        transactions = self.shb_base.tables[transactions_table_id]

        # Init Pandas DataFrame:
        # First line is headers. Convert whitespace to underscore
        headers = [header.replace(' ', '_') for header in transactions[0]]

        # Remove the empty '\xa0' from list
        headers_df = [head for head in headers if head != '\xa0']

        # Create pandas DataFrame
        df = pd.DataFrame(columns=headers_df)

        # Get all data:
        # Init row_index in data frame
        row_index = 0

        # Loop from second index (1), i.e. skip headers
        for i in range(1, len(transactions)):

            # Helper variable
            row = transactions[i]

            # Check that the length of row and headers are equal:
            if not len(row) == len(headers):
                raise ValueError(f"row and headers are not equal in length, {len(row)} vs {len(headers)}")

            # Convert to expected types:
            data = self._convert(headers, row, drop_prel=drop_prel)

            if data:
                # Add row to dataframe:
                df.loc[row_index] = data
                row_index += 1

        return df

    @staticmethod
    def _convert(headers, row, drop_prel=True):

        # Helper variables for conversions:
        timestamp_conv = ('reskontradatum', 'transaktionsdatum', 'köpdatum', 'förfallodag')
        float_conv = ('belopp', 'saldo', 'belopp_i_sek')
        int_conv = ('kort',)

        # Init data
        data = []

        # The headers list and row list are of equal length
        for i in range(len(headers)):

            # Skip empty ('\xa0') header columns
            if headers[i] == '\xa0':
                continue

            # TIMESTAMP:
            if headers[i] in timestamp_conv:
                # Reskontradatum, Transaktionsdatum, Köpdatum or Förfallodag

                # Drop all PREL. transactions?
                if all((drop_prel, headers[i] == 'reskontradatum', row[i] == '\xa0')):
                    return []

                # Append to data list
                if row[i] == '\xa0':
                    # Set default value, i.e. 1970-01-01
                    data.append(pd.Timestamp(0))
                else:
                    # Convert to timestamp type (yyyy-mm-dd HH:MM:SS)
                    data.append(pd.Timestamp(row[i]))

            # FLOAT:
            elif headers[i] in float_conv:
                # Belopp, Saldo or "Belopp i SEK"
                # Set default value to nan
                if row[i] == '\xa0':
                    data.append(np.nan)
                else:
                    # Replace whitespace to nothing, comma to dot and convert to float
                    data.append(float(row[i].replace(' ', '').replace(',', '.')))

            # INTEGER
            elif headers[i] in int_conv:
                # Kort
                # Set default value to zero
                if row[i] == '\xa0':
                    data.append(0)
                else:
                    # Convert to integer
                    data.append(int(row[i]))

            # EVERYTHING ELSE
            else:
                # If headers[i] doesnt fall into any of the categories, add headers[i] as is
                # Set default value to empty string
                if row[i] == '\xa0':
                    data.append('')
                else:
                    # Add as is
                    data.append(row[i])

        return data
