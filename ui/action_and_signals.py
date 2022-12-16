from PyQt5 import uic
from ui.reviewTx import UiReviewTx
from ui.reviewWallet import UiReviewWallet
import datetime

class UIActionAndSignals():

  def __init__(self,ui_main_window):

    self.ui = ui_main_window
    self.ui.save.clicked.connect(self.SaveAndRun)
    self.ui.review.clicked.connect(self.Review)
    self.ui.clear.clicked.connect(self.Clear)
    Current_Date = datetime.datetime.today()
    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=20)
    self.ui.date_type.setDate(Current_Date)
    self.ui.start_date.setDate(Previous_Date)
    self.ui.end_date.setDate(Current_Date)
    self.result = None

  def SaveAndRun(self):

    transactionId = self.ui.transaction.text()
    wallet = self.ui.wallet.text()
    date = self.ui.date.isChecked()
    date_range = self.ui.date_range.isChecked()
    date_type = self.ui.date_type.date()
    start_date = self.ui.start_date.date()
    end_date = self.ui.end_date.date()
    print(date)
    print(date_range)
    if(transactionId != ""):
        if(len(transactionId) == 66):
          self.ui.tx_error.setText("")
          self.review = UiReviewTx(transactionId,1)
        else:
          self.ui.tx_error.setText("<font color='red'>please input correct Transaction ID</font>")
    elif(wallet != ""):
      if(len(wallet) == 42):
        self.ui.wallet_error.setText("")
        self.review = UiReviewWallet(wallet,date,date_range,date_type,start_date,end_date,1)
      else:
        self.ui.wallet_error.setText("<font color='red'>please input correct wallet number</font>")
    else:
        print('please input transactionID or wallet Number')
        self.ui.tx_error.setText("<font color='red'>please input transactionID or wallet Number</font>")

  def Review(self):

    transactionId = self.ui.transaction.text()
    wallet = self.ui.wallet.text()
    date = self.ui.date.isChecked()
    date_range = self.ui.date_range.isChecked()
    date_type = self.ui.date_type.date()
    start_date = self.ui.start_date.date()
    end_date = self.ui.end_date.date()

    if(transactionId != ""):
        if(len(transactionId) == 66):
          self.ui.tx_error.setText("")
          self.review = UiReviewTx(transactionId)
        else:
          self.ui.tx_error.setText("<font color='red'>please input correct Transaction ID</font>")
    elif(wallet != ""):
      if(len(wallet) == 42):
        self.ui.wallet_error.setText("")
        self.review = UiReviewWallet(wallet,date,date_range,date_type,start_date,end_date)
      else:
        self.ui.wallet_error.setText("<font color='red'>please input correct wallet number</font>")
    else:
        print('please input transactionID or wallet Number')
        self.ui.tx_error.setText("<font color='red'>please input transactionID or wallet Number</font>")
        

  def Clear(self):

    self.ui.transaction.setText('')
    self.ui.wallet.setText('')
    self.ui.tx_error.setText("")
    Current_Date = datetime.datetime.today()
    self.ui.date_type.setDate(Current_Date)
    self.ui.wallet_error.setText("")
    print('clear')
