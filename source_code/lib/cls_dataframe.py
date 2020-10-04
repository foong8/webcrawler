import pandas as pd
from multiprocessing import Queue
from multiprocessing import Process

class SubclassedSeries(pd.Series):

    @property
    def _constructor(self):
        return SubclassedSeries

    @property
    def _constructor_expanddim(self):
        return SubclassedDataFrame

class SubclassedDataFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return SubclassedDataFrame

    @property
    def _constructor_sliced(self):
        return SubclassedSeries

    @classmethod
    def initial_df_based_json(cls, fp_json):
        df_temp = pd.read_json(fp_json)
        df_temp = df_temp.index.tolist()
        return cls(pd.DataFrame(columns = df_temp))

    def rephrase_columns_based_json(self, fp_json):
        df_temp = pd.read_json(fp_json)
        df_temp = df_temp.iloc[:, 0].tolist()
        return self.rename(columns = dict(zip(self.columns, df_temp)))

    def run_multiprocessing(self, 
                            int_parts    = None,
                            str_funcname = None,
                            configInfo   =  None):

        output = Queue()
        list_temp = self.values.tolist()
        
        #break down the dataframe into parts
        # div = [list_values[i::int_parts] for i in range(int_parts)]
        div = [list_temp[i::int_parts] for i in range(int_parts)]
        
        #create the multiprocessing
        processes = [Process(target=str_funcname,args=(div[i],configInfo, output)) for i in range(int_parts)]

        #Run processes
        for p in processes:p.start()

        #get process results from the output queue
        results = [(output.get()) for p in processes]
        results = pd.concat(results)
        
        #exit the completed process
        for p in processes:p.join()

        return SubclassedDataFrame(results)

