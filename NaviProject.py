from collections import defaultdict
import math


class Navi:
    def __init__(self):
        self.remainingAmounts = defaultdict(list)

    def loan(self, bankName, borrowerName, principleAmount, loanPeriodYears, rateOfInterest):
        interestToBePaid = principleAmount * loanPeriodYears * rateOfInterest * 0.01
        totalAmountToBePaidByBorrower = principleAmount + interestToBePaid
        emiInstallments = loanPeriodYears * 12
        monthlyPayment = math.ceil(totalAmountToBePaidByBorrower / emiInstallments)
        lumpSumPaidAfterEMI = defaultdict(lambda: 0)
        self.remainingAmounts[borrowerName] = [interestToBePaid, totalAmountToBePaidByBorrower,
                                               bankName, emiInstallments, monthlyPayment, lumpSumPaidAfterEMI]

    def payment(self, borrowerName, lumpSum, emiNumber):
        self.remainingAmounts[borrowerName][5][emiNumber] = lumpSum

    def balance(self, bankName, borrowerName, emiNumber):
        dbDetailsOfBorrowerLoan = self.remainingAmounts[borrowerName]
        totalAmountAlreadyPaid = emiNumber * dbDetailsOfBorrowerLoan[4]
        for emiNum in dbDetailsOfBorrowerLoan[5]:
            if emiNum <= emiNumber:
                totalAmountAlreadyPaid += dbDetailsOfBorrowerLoan[5][emiNum]
        remainingEMIs = math.ceil((dbDetailsOfBorrowerLoan[1] - totalAmountAlreadyPaid)/dbDetailsOfBorrowerLoan[4])
        print(bankName, borrowerName, totalAmountAlreadyPaid, remainingEMIs)

    def beginToReadCommands(self):
        file1 = open("LoanInput", "r+")
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


navi = Navi()
navi.beginToReadCommands()
