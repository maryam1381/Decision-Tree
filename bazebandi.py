import math
import pandas
import numpy as np


def SplitDataToGroups(attribute,min_value,max_value,numberofBaze,examples):
    new_Values = []
    new_attr = str(attribute)+" group"
    len_baze = (max_value-min_value)//numberofBaze
    for i in range(0,examples.shape[0]):
        row = examples.iloc[[i]]
        if row[attribute].tolist()[0] < min_value:
            new_Values.append("group -1")
        elif row[attribute].tolist()[0] >= max_value:
            new_Values.append("group "+str(numberofBaze))
        else :
            i = (row[attribute].tolist()[0] - min_value)//len_baze
            new_Values.append("group "+str(i))
    examples.insert(2,new_attr,new_Values,True)
    attributes.remove(attribute)
    print(examples)


df = pandas.read_csv('titanic.csv')
attributes = list(df.columns)
attributes.remove("survived")              # result
attributes.remove("name") 

SplitDataToGroups('parch',0,5,5,df)


# then give it to decision tree

# mainNode = Node(None,attributes_list=attributes,value='',datas=df)
# node_list.append(mainNode)
# decision_Tree(mainNode)    
# print_Node(mainNode,0)