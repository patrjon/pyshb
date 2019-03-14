__all__ = ['SHBCreditAccount', 'SHBCreditTransactions']

# Standard Library:

# Third party

# Local applications:
from pyshb.accounts.base_account import SHBBaseAccount
from pyshb.base.transactions import SHBTransactions


class SHBCreditAccount(SHBBaseAccount):
    """
    Class to represent the credit account (allkortskonto - konto)
    """
    def __init__(self, shb_base):

        # Init parent object
        super().__init__()

        # Init variables:
        self.shb_base = shb_base
        self.account_type = 'allkortskonto'

        # Init info dict with info_keys to None
        info_keys = ('beviljad_kredit', 'kontoform',
                     'saldo_på_kontot', 'clearingnummer', 'kortköp_ej_fakturerat', 'kortköp_fakturerat',
                     'disponibelt_belopp'
                     'konto', 'period', 'transtyp', 'belopp', 'antal_transaktioner')

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
            self.info['beviljad_kredit'] = tables[0][0][1].replace(' ', '').replace(',', '.')
            self.info['kontoform'] = tables[0][0][4]
        except:
            pass

        # Table: 1
        try:
            self.info['saldo_på_kontot'] = tables[1][0][1].replace(' ', '').replace(',', '.')
            self.info['clearingnummer'] = tables[1][0][4]
            self.info['kortköp_ej_fakturerat'] = tables[1][1][1].replace(' ', '').replace(',', '.')
            self.info['kortköp_fakturerat'] = tables[1][2][1].replace(' ', '').replace(',', '.')
            self.info['disponibelt_belopp'] = tables[1][3][1].replace('\xa0', '').replace(',', '.')
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

    @staticmethod
    def identify(shb_base):
        """
        Account type identification method

        :param shb_base: Instance of SHBBase class
        :return: True or False
        """
        try:
            if 'allkortskonto' in shb_base.tables[0][0]:
                return True
            else:
                return False
        except Exception as e:
            return False


class SHBCreditTransactions(SHBBaseAccount):
    """
    Class to represent the credit transactions (Allkortskonto - transaktion)
    """
    def __init__(self, shb_base):

        # Init parent object
        super().__init__()

        # Init variables:
        self.shb_base = shb_base
        self.account_type = 'allkortstransaktioner'

        # Init info dict with info_keys to None
        info_keys = ('kontonummer', 'kontonamn', 'urval', 'period',
                     'kort')
        self.info = dict.fromkeys(info_keys)

        # Read tabels
        self._read_tables(shb_base.tables)

        # Get transactions
        shb_trans = SHBTransactions(shb_base)
        self.transactions = shb_trans.get_transactions(2)

    def _read_tables(self, tables):
        """
        Read and set information in self.info

        :return:
        """
        # Table: 0
        try:
            self.info['kontonummer'] = tables[0][0][1].replace(' ', '')
            self.info['kontonamn'] = tables[0][2][1]
            self.info['urval'] = tables[0][4][1]
            self.info['period'] = tables[0][5][1]\
                .replace('\n', '')\
                .replace('\t', '')\
                .replace('\xa0', '')\
                .replace('--', '_')
        except:
            pass

        # Table: 1
        self.info['kort'] = {}

        try:
            for i in range(len(tables[1])):
                self.info['kort'][i+1] = tables[1][i][1].replace('\n', '').replace('\t', '')
        except:
            pass

    @staticmethod
    def identify(shb_base):
        """
        Account type identification method

        :param shb_base: Instance of SHBBase class
        :return: True or False
        """
        try:
            if 'allkort' in shb_base.tables[0][1][1]:
                return True
            else:
                return False
        except Exception as e:
            return False
