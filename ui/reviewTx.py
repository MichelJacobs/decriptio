from PyQt5 import uic,QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QListWidget, QWidget, QMessageBox,
    QApplication, QVBoxLayout, QTableWidget, QTableWidgetItem)
import requests
import csv
from subprocess import Popen
from datetime import datetime

class UiReviewTx(QDialog):

    def __init__(self,tx,run=0,parent=None):
        super().__init__(parent)
        uic.loadUi('ui/review.ui', self)
        print('ui review tx')

        self.tx=tx
        self.date=None
        self.time=None
        self.walletTo=None
        self.walletFrom=None
        self.symbol=None
        self.amount=None
        query = """
            query{
                ethereum(network: ethereum) {
                    transactions(txHash: {is: """+'"'+tx+'"'+"""}) {
                        block {
                            timestamp {
                                time(format: "%Y-%m-%d %H:%M:%S")
                            }
                        }
                        amount
                        currency {
                            symbol
                        }
                        sender {
                            address
                            annotation
                        }
                        to {
                            address
                            annotation
                        }
                    }
                }
            }
        """
        result = run_query(query)  # Execute the query
        if(result == False):
            print('network error')
            return None
        if not result['data']['ethereum']['transactions']:
            return None
        else:
            print("list is not empty")
            result = result['data']['ethereum']['transactions'][0]
            dateTime = result['block']['timestamp']['time']
            self.date = dateTime[0:10]
            self.time = dateTime[11:]
            self.amount = result['amount']
            self.symbol = result['currency']['symbol']
            self.walletFrom = result['sender']['address']
            self.walletTo = result['to']['address']
            
        if(run == 0):
            self.table.setItem(0, 0, QTableWidgetItem(self.tx))
            self.table.setItem(0, 1, QTableWidgetItem(self.date))
            self.table.setItem(0, 2, QTableWidgetItem(self.time))
            self.table.setItem(0, 3, QTableWidgetItem(self.walletTo))
            self.table.setItem(0, 4, QTableWidgetItem(self.walletFrom))
            self.table.setItem(0, 5, QTableWidgetItem(self.symbol))
            self.table.setItem(0, 6, QTableWidgetItem(str(self.amount)))

            self.discard.clicked.connect(self.closeButton)
            self.save.clicked.connect(self.saveCSV)
            self.show()
        else:
            self.saveCSV()

    def closeButton(self):
        self.hide()

    
    def saveCSV(self):

        header = ['Transaction ID', 'Date', 'Time', 'Wallet To','Wallet From','Currency','Amount']
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        # open the file in the write mode
        with open(now+'.csv', 'w', encoding='UTF8',newline='') as f:
            # create the csv writer
            writer = csv.writer(f)

            writer.writerow(header)

            row=[self.tx,self.date,self.time,self.walletTo,self.walletFrom,self.symbol,self.amount]
            writer.writerow(row)

            p= Popen(now+'.csv', shell=True)

def run_query(query):  # A simple function to use requests.post to make the API call.
    headers = {'X-API-KEY': 'BQYyr123PbYDMjzNpQ5knbtZfTIsDtFh'}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        return False

