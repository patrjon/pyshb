# PySHB

PySHB is a Python package to parse transaction files downloaded from www.handelsbanken.se (Svenska Handelsbanken AB). 
This is an unofficial project not supported by Svenska Handelsbanken AB.

## Users Guide:

1. Download transactions file from SHB homepage. The following account
types are currently supported:
    * allkonto
    * sparkonto
    * allkortskonto - konto
    * allkortskonto - transaktioner
2. Download or clone PySHB from github, https://github.com/patrjon/pyshb.git
3. Install PySHB in an virtual environment or add path to python path
4. To parse a file run the following code:

```python
import pyshb

# Set path to file (str or pathlib.Path object)
file_path = "/path/to/file.xls"

# Parse the file 
account_info = pyshb.shb(file_path)

```

## Developers Guide:

Some notes on PySHB code structure.

#### Base Classes:

* **SHBBase** is the base class for PySHB and do the following:
    * read file to string
    * parse html string to nested list
* **SHBTransaction** class do the following:
    * reads and converts transactions to a pandas.DataFrame

#### Account Classes:

* **SHBBaseAccount** is the common account class for all account classes below. 
    * **SHBAccount** inherit *SHBBaseAccount* 
        * **SHBStandard** inherit *SHBAccount*
        * **SHBSavings** inherit *SHBAccount*
    * **SHBCreditAccount** inherit *SHBBaseAccount*
    * **SHBCreditTransactions** *SHBBaseAccount*

The SHBStandard, SHBSavings, SHBCreditAccount, SHBCreditTransactions classes have the following variables:
* account_type - type of account
* shb_base - SHBBase instance
* info - account information
* transactions - pandas.DataFrame with transaction data

and the following methods:
* _read_tables - private method for parsing tables and setting keys in *info* dictionary
* identify - static method for identifying if current file is of object account type

#### Main function

The main pyshb.shb function is a factory returning either an instance of SHBStandard, SHBSavings, SHBCreditAccount, 
SHBCreditTransactions or None if the identification process fail.
