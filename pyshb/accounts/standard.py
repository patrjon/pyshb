# __all__ = ['SHBStandard']

# Standard Library:

# Third party

# Local applications:
from pyshb.accounts.base_account import SHBBaseAccount
from pyshb.base.transactions import SHBTransactions


class SHBAccount(SHBBaseAccount):
    """
    Class for parsing Allkonto and Sparkonto files.
    """

    def __init__(self, shb_base):

        # Init parent object
        super().__init__()

        # Init variables:
        self.shb_base = shb_base

        # Init info dict with info_keys to None
        info_keys = ('kontoform', 'clearingnummer',
                     'saldo',
                     'konto', 'period', 'transtyp', 'belopp', 'antal_transaktioner',
                     )
        self.info = dict.fromkeys(info_keys)

        # Read tabels
        self._read_tables(shb_base.tables)

        # Get transactions
        shb_trans = SHBTransactions(shb_base)
        self.transactions = shb_trans.get_transactions(3)

    def _read_tables(self, tables):
        """
        Read and set information in self.info

        :return:
        """
        # Table: 0
        try:
            self.info['kontoform'] = tables[0][0][1]
            self.info['clearingnummer'] = tables[0][0][4]
        except:
            pass

        # Table: 1
        try:
            self.info['saldo'] = tables[1][0][1].replace(' ', '').replace(',', '.')
        except:
            pass

        # Table: 2
        try:
            # Split tables
            t1 = tables[2][0][0].split('\xa0\xa0')

            self.info['konto'] = t1[0].split(':')[1].replace(' ', '')
            self.info['period'] = t1[1].split(':')[1].replace(' ', '').replace('till', '_')
            self.info['transtyp'] = t1[2].split(':')[1].replace('\xa0', '')

            # Split last element in t1
            t2 = t1[3].split('\xa0')

            self.info['belopp'] = t2[0].split(':')[1].replace(' ', '')
            self.info['antal_transaktioner'] = t2[3]
        except:
            pass


class SHBStandard(SHBAccount):
    """
    Class to represent the standard account (allkonto)
    """
    def __init__(self, shb_base):

        # Init parent object
        super().__init__(shb_base)

        # Init variables:
        self.account_type = 'allkonto'

    @staticmethod
    def identify(shb_base):
        """
        Account type identification method

        :param shb_base: Instance of SHBBase class
        :return: True or False
        """
        try:
            if 'allkonto' in shb_base.tables[0][0]:
                return True
            else:
                return False
        except Exception as e:
            return False


class SHBSavings(SHBAccount):
    """
    Class to represent the savings account (sparkonto)
    """
    def __init__(self, shb_base):

        # Init parent object
        super().__init__(shb_base)

        # Init variables:
        self.account_type = 'sparkonto'

    @staticmethod
    def identify(shb_base):
        """
        Account type identification method

        :param shb_base: Instance of SHBBase class
        :return: True or False
        """
        try:
            if 'sparkonto' in shb_base.tables[0][0]:
                return True
            else:
                return False
        except Exception as e:
            return False
