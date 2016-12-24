import datetime
import inspect
import sys

class Log(object):
    """
    This class is used for logging, debugging and error handling.
    """

    def __init__(self, maxRows=100, fileName="Log.txt"):

        self.maxRows = maxRows - 1  # Max number of rows to be saved
        self.fileName = fileName  # Name of the log file

    def bug(self, TAG, bugText, e = None):
        """
        Prints and logs the bug according to given standard.
        TAG  - String tag for categorize bug.
        bugText - String for expressing bug.
        """

        line = inspect.currentframe().f_back.f_lineno  # Find line number

        if e is None:  # Check is error message is Null

            outText = ": " + str(line) + " : " + str(datetime.datetime.now()) + " : " + TAG + " : " + str(bugText)

        else:

            outText = ": " + str(line) + " : " + str(datetime.datetime.now()) + " : " + TAG + " : " + str(
                bugText) + " : " + str(e)

        print(outText)

        try:

            with open(self.fileName, 'r', ) as f:  # Count number of rows in file

                countedRows = sum(1 for lines in f)

        except:

            open(self.fileName, 'w')
            countedRows = 0

        with open(self.fileName, 'r+', ) as f:  # Write to file

            if countedRows < self.maxRows:  # Make sure that the max number of rows are not exceeded

                content = f.read()

            else:

                content = [next(f) for lines in range(self.maxRows)]

            f.seek(0, 0)
            f.write(outText.rstrip('\r\n') + '\n' + ''.join(content))

        return

    def err(self, TAG, errorText, e=None):
        """
        Prints and logs the error according to given standard, shuts down the program.
        TAG  - String tag for categorize error.
        errorText - String for expressing error.
        """

        line = inspect.currentframe().f_back.f_lineno  # Find line number

        if e is None:  # Check is error message is Null

            outText = ": " + str(line) + " : " + str(datetime.datetime.now()) + " : " + TAG + " : " + str(errorText)

        else:

            outText = ": " + str(line) + " : " + str(datetime.datetime.now()) + " : " + TAG + " : " + str(
                errorText) + " : " + str(e)

        print(outText)

        try:

            with open(self.fileName, 'r', ) as f:  # Count number of rows in file

                countedRows = sum(1 for lines in f)

        except:

            open(self.fileName, 'w')
            countedRows = 0

        with open(self.fileName, 'r+', ) as f:  # Write to file

            if countedRows < self.maxRows:  # Make sure that the max number of rows are not exceeded

                content = f.read()

            else:

                content = [next(f) for lines in range(self.maxRows)]

            f.seek(0, 0)
            f.write(outText.rstrip('\r\n') + '\n' + ''.join(content))

        print("Error encountered, shutting down.")

        sys.exit(1)

    def inf(self, TAG, infoText, e=None):
        """
        Prints the info according to given standard.

        TAG  - String tag for categorize info.
        infoText - String for expressing info.
        """

        line = inspect.currentframe().f_back.f_lineno  # Find line number

        if e is None:  # Check is error message is Null

            outText = ": " + str(line) + " : " + str(datetime.datetime.now()) + " : " + TAG + " : " + str(infoText)

        else:

            outText = ": " + str(line) + " : " + str(datetime.datetime.now()) + " : " + TAG + " : " + str(
                infoText) + " : " + str(e)

        print(outText)

        return
