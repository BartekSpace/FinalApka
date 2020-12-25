import numpy as np
import matplotlib.pyplot as plt

class Data:


    def __init__(self):
        self.col1 = []
        self.col2 = []
        self.time = 0
    def read_from_arrays(self,a,b):
        self.col1 = a
        self.col2 = b
        self.time = self.col1[-1]
    def read_data(self, file):
        with open(file) as f:
            x=1
            while(x):
             x = f.readline()
             if x:

                if x == '\n':
                    break
                n, g = x.split(",")
                self.col1.append(float(n))
                self.col2.append(float(g))
            self.time = self.col1[-1]


    def plot(self,data=None,plt1=None):
        # if not plt1:
            plt.plot(self.col1,self.col2)
            if data:
                plt.plot(data.col1,data.col2)

            plt.grid()
            plt.xticks(range(0,int(self.col1[-1])+1))
        # else:
        #     plt1.plot(self.col1, self.col2)
        #     if data:
        #         plt1.plot(data.col1, data.col2)

            #plt1.grid()
            #plt1.xticks(range(0, int(self.col1[-1]) + 1))

        #plt.show()
        #plt.savefig("testowe.pdf")


    def filter(self,nums_of_average,eps):
        index = 0
        filter_flag =False
        sum=0
        first_index_flag = True
        for index,value in enumerate(self.col2,index+1):

            sum += abs(value)

            if not index % nums_of_average:
               if filter_flag == False:
                   sum_first = sum
                   sum = 0
                   filter_flag=True
               else:
                   x= abs(sum-sum_first)/nums_of_average
                   if abs(sum-sum_first)/nums_of_average > eps:
                           if first_index_flag == True:
                               first_index = index -nums_of_average
                               first_index_flag = False
                           last_index = index
                   filter_flag = False


        if first_index != 0:
            time_offset = self.col1[first_index]
            index=0
            for index,time in enumerate(self.col1,index):

                self.col1[index] -= time_offset
        self.col1 = self.col1[first_index:last_index]
        self.col2 = self.col2[first_index:last_index]
        self.time = self.col1[-1]
        #return self.col1[first_index:last_index], self.col2[first_index:last_index]

    def integral(self, data = None ):
        i=0
        sum =0
        if data:
            tmp1 = data.col1
            tmp2 = data.col2
        else:
        #print(len(self.col1))
            tmp1 = self.col1
            tmp2 = self.col2


        while i<len(tmp1)-1:
            sum+= 0.5*(tmp1[i+1]-tmp1[i])*(tmp2[i]+tmp2[i+1])
            i+=1
        return sum
    def prepare_log(cls,name, data = ""):
        with open("log.txt","a") as file:
               file.writelines(name+": "+str(data)+"\n")
    def average(self):
        return (self.integral())/self.time


















