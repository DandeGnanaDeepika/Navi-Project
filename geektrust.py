from collections import defaultdict
import math
import sys


class Navi:
    def __init__(self):
        self.remainingAmounts = defaultdict(list)

    # Storing all the loan details of individual borrowers into remainingAmounts dictionary
    def loan(self, bankName, borrowerName, principleAmount, loanPeriodYears, rateOfInterest):
        interestToBePaid = principleAmount * loanPeriodYears * rateOfInterest * 0.01
        totalAmountToBePaidByBorrower = principleAmount + interestToBePaid
        emiInstallments = loanPeriodYears * 12
        monthlyPayment = math.ceil(totalAmountToBePaidByBorrower / emiInstallments)
        lumpSumPaidAfterEMI = defaultdict(lambda: 0)
        self.remainingAmounts[borrowerName] = [interestToBePaid, totalAmountToBePaidByBorrower,
                                               bankName, emiInstallments, monthlyPayment, lumpSumPaidAfterEMI]

    # storing emiNumber and its corresponding lumpSum in remainingAmount dictionary at index 5
    def payment(self, borrowerName, lumpSum, emiNumber):
        self.remainingAmounts[borrowerName][5][emiNumber] = lumpSum

    # Calculating the balance amount and remainingEMIs after a particular emiNumber
    def balance(self, bankName, borrowerName, emiNumber):
        dbDetailsOfBorrowerLoan = self.remainingAmounts[borrowerName]
        totalAmountAlreadyPaid = emiNumber * dbDetailsOfBorrowerLoan[4]

        # Adding all the lumpSum amounts paid before or during the given emiNumber
        for emiNum in dbDetailsOfBorrowerLoan[5]:
            if emiNum <= emiNumber:
                totalAmountAlreadyPaid += dbDetailsOfBorrowerLoan[5][emiNum]
        remainingEMIs = math.ceil((dbDetailsOfBorrowerLoan[1] - totalAmountAlreadyPaid)/dbDetailsOfBorrowerLoan[4])
        print(bankName, borrowerName, totalAmountAlreadyPaid, remainingEMIs)

    # Reading the input from LoanInput file
    def beginToReadCommands(self, fileName):
        file1 = open(fileName, "r+")
        commandLines = file1.readlines()
        for commandLine in commandLines:
            command = commandLine.split(" ")[0]
            if command == "LOAN":
                command, bankName, borrowerName, principleAmount, loanPeriodYears, rateOfInterest = \
                    commandLine.split(" ")
                self.loan(bankName, borrowerName, int(principleAmount), int(loanPeriodYears), int(rateOfInterest))
            elif command == "PAYMENT":
                command, bankName, borrowerName, lumpSum, emiNumber = commandLine.split(" ")
                self.payment(borrowerName, int(lumpSum), int(emiNumber))
            elif command == "BALANCE":
                command, bankName, borrowerName, emiNumber = commandLine.split(" ")
                self.balance(bankName, borrowerName, int(emiNumber))


def main():
    input_file = sys.argv[1]
    navi = Navi()
    navi.beginToReadCommands(input_file)


if __name__ == "__main__":
    main()
