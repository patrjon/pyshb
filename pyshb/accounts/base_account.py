__all__ = ['SHBBaseAccount']

# Standard Library:

# Third party

# Local applications:


class SHBBaseAccount:
    """
    This is a common accounts class. This class initiate variables and defines str dunder method.
    """

    def __init__(self):
        """
        Initiation method.
        """

        # Init variables:
        self.account_type = None
        self.shb_base = None
        self.info = None
        self.transactions = None

    def __str__(self):

        msg = ""

        # Account type:
        msg += "Account type:\n"
        if self.account_type is not None:
            msg += f"  Type: {self.account_type}\n"

        # SHBBase object:
        msg += "\nSHBBase Object Information:\n"
        if self.shb_base is not None:
            msg += f"  File Path: {self.shb_base.file_path}\n"
            msg += f"  Number of Tables: {len(self.shb_base.tables)}\n"

        # Information:
        msg += f"\nInformation:\n"
        if self.info is not None:
            for k, v in self.info.items():
                msg += f"  {k}: {v}\n"

        # Transaction:
        msg += f"\nTransactions:\n"
        if self.transactions is not None:
            msg += f"  Number of Transactions: {self.transactions.shape[0]}"

        return msg
