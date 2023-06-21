import math
import pandas
import numpy as np


class Node:
    def __init__(self, parent,attributes_list,value,datas):
        self.parent = parent
        self.value = value
        self.remain_attribute_list = attributes_list
        self.examples = datas
        self.chosen_attribute = None
        self.lable= ''                      # for leaf
        self.gini_index = Gini_Index(self.examples)
        self.info_Gain =None
                         
def Pluarity_Value(examples):
    if examples.empty==True:
        return 0,0
    value = examples.iloc[:,-1].value_counts().nlargest(1).index[0]
    count = examples.iloc[:,-1].value_counts().nlargest(1).tolist()[0]
    return value,count

# def Entropy(examples): 
#     value,count = Pluarity_Value(examples)
#     count_all = examples.shape[0] 
#     q= count/count_all
#     if q ==1 or q ==0:
#         return 0
#     else:
#         return -(q*math.log2(q)+(1-q)*math.log2(1-q))

def Gini_Index(examples): 
    value,count = Pluarity_Value(examples)
    count_all = examples.shape[0] 
    if count_all==0:
        return 0
    q= count/count_all
    return 1-(q*q+(1-q)*(1-q))

def Reminder(examples,attribute):
    count_all = examples.shape[0] #number of rows(data)
    unique_values = examples[attribute].unique()
    sum = 0
    for value in unique_values:
        group = examples.loc[examples[attribute] == value]
        count_group = group.shape[0]
        group_Entropy = Gini_Index(group)
        sum+= group_Entropy*count_group/count_all
    return sum

def choose_Attribute(examples,list_attr):
    chosen = ''
    min_reminder=1000
    for attr in list_attr:
        rem = Reminder(examples,attr)
        if rem<min_reminder:
            min_reminder = rem
            chosen=attr
    return chosen

node_list = []
def decision_Tree(node):

    # if node.examples = null then node.lable =pluarity_value(node.parent) 
    if node.examples.empty==True:
        node.lable,x = Pluarity_Value(node.parent.examples)
    
    # if node.attributes == null then node.lable = pluarity_value(node)
    elif len(node.remain_attribute_list)== 0 or node.remain_attribute_list ==None:
        node.lable,x = Pluarity_Value(node.examples)
    
    # if poluarityvalue(node).count = all => node.lable = poluarityvalue(node)
    elif Pluarity_Value(node.examples)[1] ==node.examples.shape[0]:
        node.lable,x = Pluarity_Value(node.examples)

    else :
        attr = choose_Attribute(node.examples,node.remain_attribute_list)
        node.chosen_attribute = attr
        node.info_Gain = node.gini_index -Reminder(node.examples,attr)
        new_attributes = node.remain_attribute_list
        new_attributes.remove(attr)
        unique_values = node.examples[attr].unique()
        for value in unique_values:
            group = node.examples.loc[node.examples[attr] == value]
            t = Node(node,new_attributes,value=value,datas=group)
            node_list.append(t)
            decision_Tree(t)

def print_Node(node,i):
    if node.lable=='':
        print(i*"\t"+ "Node value: "+str(node.value)+"    Attribute: "+str( node.chosen_attribute)+"    Gini Index : "+str(node.gini_index)+"     info Gain : "+str(node.info_Gain))
        children = [n for n in node_list if n.parent == node]
        for child in children:
            print_Node(child,i+1)
    else:
        print(i*"\t"+"Node value: "+str(node.value)+ "    lable: "+str(node.lable)+"    Gini Index : "+str(node.gini_index))

df = pandas.read_csv('titanic.csv')
attributes = list(df.columns)
attributes.remove("survived")              # result
attributes.remove("name")              # result

mainNode = Node(None,attributes_list=attributes,value='',datas=df)
node_list.append(mainNode)
decision_Tree(mainNode)
print_Node(mainNode,0)
