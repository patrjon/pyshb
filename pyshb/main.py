__all__ = ['shb']

# Standard Library:

# Third party

# Local applications:
from pyshb.base.base import SHBBase
from pyshb.accounts.standard import SHBStandard, SHBSavings
from pyshb.accounts.credit import SHBCreditAccount, SHBCreditTransactions


def shb(file_path):
    """
    Main function for reading transaction files.

    :param file_path: path to file.
    :type file_path: str or pathlib.Path:
    :return:
    """

    # Init SHBTransaction object
    shb_base = SHBBase(file_path)

    # Identify which account type and return appropriate object
    if SHBStandard.identify(shb_base):
        return SHBStandard(shb_base)

    elif SHBSavings.identify(shb_base):
        return SHBSavings(shb_base)

    elif SHBCreditAccount.identify(shb_base):
        return SHBCreditAccount(shb_base)

    elif SHBCreditTransactions.identify(shb_base):
        return SHBCreditTransactions(shb_base)

    else:
        return None

