from PyQt5 import uic,QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QListWidget, QWidget, QMessageBox,
    QApplication, QVBoxLayout,QTableWidget, QTableWidgetItem)
import requests
import csv
from subprocess import Popen
from datetime import datetime

class UiReviewWallet(QDialog):

    def __init__(self,wallet,date,date_range,date_type,start_date,end_date,run=0,parent=None):
        super().__init__(parent)
        uic.loadUi('ui/review.ui', self)
        print('ui review wallet')

        if(date == True):
            start_date = date_type
            end_date = date_type
            
        out_query = """
            query{
                ethereum(network: ethereum) {
                    transfers(
                        options: {desc: "block.timestamp.time"}
                        date: {since: """+'"'+start_date.toString('yyyy-MM-dd')+'"'+""", till: """+'"'+end_date.toString('yyyy-MM-dd')+'"'+"""}
                        amount: {gt: 0}
                        currency: {is: "ETH"}
                        sender: {is: """+'"'+wallet+'"'+"""}
                        ) {
                        block {
                            timestamp {
                            time(format: "%Y-%m-%d %H:%M:%S")
                            }
                        }
                        address: receiver {
                            address
                            annotation
                            smartContract {
                                contractType
                            }
                        }
                        currency {
                            address
                            symbol
                        }
                        amount
                        transaction {
                            hash
                        }
                    }
                }
            }
        """
        out_result = run_query(out_query)  # Execute the query
        if(out_result == False):
            print('network error')
            return None
        in_query = """
            query{
                ethereum(network: ethereum) {
                    transfers(
                        options: {desc: "block.timestamp.time"}
                        date: {since: """+'"'+start_date.toString('yyyy-MM-dd')+'"'+""", till: """+'"'+end_date.toString('yyyy-MM-dd')+'"'+"""}
                        amount: {gt: 0}
                        currency: {is: "ETH"}
                        receiver: {is: """+'"'+wallet+'"'+"""}
                        ) {
                        block {
                            timestamp {
                            time(format: "%Y-%m-%d %H:%M:%S")
                            }
                        }
                        address: sender {
                            address
                            annotation
                            smartContract {
                                contractType
                            }
                        }
                        currency {
                            address
                            symbol
                        }
                        amount
                        transaction {
                            hash
                        }
                    }
                }
            }
        """
        in_result = run_query(in_query)  # Execute the query
        if(in_result == False):
            print('network error')
            return None
        out_row = 0;
        try:
            out_row = len(out_result['data']['ethereum']['transfers'])
        except:
            print("Something went wrong when count up the length")

        in_row = len(in_result['data']['ethereum']['transfers'])
            
        total_row = out_row + in_row
        self.table.setRowCount(total_row)

        i = 0
        if not out_result['data']['ethereum']['transfers']:
            pass
        else:
            result = out_result['data']['ethereum']['transfers']
            for element in result:
                dateTime = element['block']['timestamp']['time']
                tx = element['transaction']['hash']
                date = dateTime[0:10]
                time = dateTime[11:]
                amount = element['amount']
                symbol = element['currency']['symbol']
                walletFrom = element['address']['address']
                annotation = element['address']['annotation']
                contractType = element['address']['smartContract']['contractType']

                if(annotation == None):
                    annotation = "None"
                if(contractType == None):
                    contractType = "None"
                walletTo = wallet
            
                self.table.setItem(i, 0, QTableWidgetItem(tx))
                self.table.setItem(i, 1, QTableWidgetItem(date))
                self.table.setItem(i, 2, QTableWidgetItem(time))
                self.table.setItem(i, 3, QTableWidgetItem(walletTo))
                self.table.setItem(i, 4, QTableWidgetItem(walletFrom))
                self.table.setItem(i, 5, QTableWidgetItem(symbol))
                self.table.setItem(i, 6, QTableWidgetItem(str(amount)))
                self.table.setItem(i, 7, QTableWidgetItem(annotation))
                self.table.setItem(i, 8, QTableWidgetItem(contractType))

                i = i+1

        if not in_result['data']['ethereum']['transfers']:
            pass
        else:
            result = in_result['data']['ethereum']['transfers']
            for element in result:
                dateTime = element['block']['timestamp']['time']
                tx = element['transaction']['hash']
                date = dateTime[0:10]
                time = dateTime[11:]
                amount = element['amount']
                symbol = element['currency']['symbol']
                walletFrom = wallet
                walletTo = element['address']['address']
                annotation = element['address']['annotation']
                contractType = element['address']['smartContract']['contractType']
                if(annotation == None):
                    annotation = "None"
                if(contractType == None):
                    contractType = "None"

                self.table.setItem(i, 0, QTableWidgetItem(tx))
                self.table.setItem(i, 1, QTableWidgetItem(date))
                self.table.setItem(i, 2, QTableWidgetItem(time))
                self.table.setItem(i, 3, QTableWidgetItem(walletTo))
                self.table.setItem(i, 4, QTableWidgetItem(walletFrom))
                self.table.setItem(i, 5, QTableWidgetItem(symbol))
                self.table.setItem(i, 6, QTableWidgetItem(str(amount)))
                self.table.setItem(i, 7, QTableWidgetItem(annotation))
                self.table.setItem(i, 8, QTableWidgetItem(contractType))

                i = i+1
        print('ok')
        if(run == 0):
            # self.table.setRowCount(i)
            self.discard.clicked.connect(self.closeButton)
            self.save.clicked.connect(self.saveCSV)
            self.show()
        else:
            self.saveCSV()

    def saveCSV(self):
  
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        with open(now+'.csv', 'w') as stream:                  # 'w'
            writer = csv.writer(stream, lineterminator='\n')          # + , lineterminator='\n'

            header = ['Transaction ID', 'Date', 'Time', 'Wallet To','Wallet From','Currency','Amount','annotation','contractType']
            writer.writerow(header)

            for row in range(self.table.rowCount()):
                rowdata = []
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    if item is not None:
    #                        rowdata.append(unicode(item.text()).encode('utf8'))
                        rowdata.append(item.text())                   # +
                    else:
                        rowdata.append('')

                writer.writerow(rowdata)

        p= Popen(now+'.csv', shell=True)

    def closeButton(self):
        self.hide()

def run_query(query):  # A simple function to use requests.post to make the API call.
    headers = {'X-API-KEY': 'BQYyr123PbYDMjzNpQ5knbtZfTIsDtFh'}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,
                        query))

