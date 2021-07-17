
# date: 2021.07.15
# author: Raul Saavedra raul.saavedra.felipe@iais.fraunhofer.de

import openml
import myconstants

class FetchOpenMLData:
    idx = 0
    total_rows = 0
    current_row = 0
    Row_list = []

    def __init__(self):
        idx = myconstants.DATA_ID
        print(f'Getting data with ID: {idx}')
        try:
           dataset = openml.datasets.get_dataset(idx);
        except:
           print(f'Exception: OpenML Dataset {idx} not found')
           return
        data  = dataset.get_data()
        df    = data[0]
        ncols = len(df.dtypes)
        nrows = len(df.values)
        print(f'Dataset ID    : {idx}')
        print(f'Dataset Name  : {dataset.name}')
        print(f'Dataset URL   : {dataset.url}')
        print(f'Num. Columns  : {ncols}')
        print(f'Num. Rows     : {nrows}')
        descr = dataset.description[:400].split("\n")
        print(f'********** Beginning of Dataset description **********')
        for line in descr:
            if line.strip() != "":
                print(f'{line[:80]}')
        print(f'******************************************************')
        print(f'Data Column names:')
        print(f','.join(df.columns))
        #print(f'Data Rows:')
        #for i in range(nrows):
        #    print(f'{i}: {df.values[i]}')
        print(f'Example, First Data Row:')
        print(f'{0}: {df.values[0]}')
        self.Row_list = df.values
        self.total_rows = nrows
        #print("self.Row_list: ", self.Row_list)

    def get_next_row(self, current_row):
        self.current_row = current_row
        #print("current row number: ", self.current_row)
        row = []
        for x in self.Row_list[self.current_row]: row.append(x)
        print(f"Data in row nr. {current_row}: ", row)
        return row

    def get_num_rows(self):
        return self.total_rows
