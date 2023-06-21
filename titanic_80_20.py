import math
import pandas
import numpy as np


node_list = []
class Node:
    def __init__(self, parent,attributes_list,value,datas):
        self.parent = parent
        self.value = value
        self.remain_attribute_list = attributes_list
        self.examples = datas
        self.chosen_attribute = None
        self.lable= ''                      # for leaf

def Pluarity_Value(examples):
    if examples.empty==True:
        return 0,0
    value = examples.iloc[:,-1].value_counts().nlargest(1).index[0]
    count = examples.iloc[:,-1].value_counts().nlargest(1).tolist()[0]
    return value,count

def Entropy(examples): 
    value,count = Pluarity_Value(examples)
    count_all = examples.shape[0] 
    if count_all==0:
        return 0
    q= count/count_all
    if q ==1 or q ==0:
        return 0
    else:
        return -(q*math.log2(q)+(1-q)*math.log2(1-q))

def Reminder(examples,attribute):
    count_all = examples.shape[0] #number of rows(data)
    unique_values = examples[attribute].unique()
    sum = 0
    for value in unique_values:
        group = examples.loc[examples[attribute] == value]
        count_group = group.shape[0]
        group_Entropy = Entropy(group)
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
        print(i*"\t"+ "Node value: "+str(node.value) +"    Attribute: "+ node.chosen_attribute)# value =    attribute = 
        children = [n for n in node_list if n.parent == node]
        for child in children:
            print_Node(child,i+1)
    else:
        print(i*"\t"+"Node value: "+str(node.value) + "    lable: "+str(node.lable))

def test_row_by_tree(row,node):
    tree_lable=''
    if node.lable=='':
        children = [n for n in node_list if n.parent == node]
        is_find = False
        for child in children:
            v =  row[node.chosen_attribute].tolist()[0]
            if str(child.value) ==str(v):
                is_find=True
                return test_row_by_tree(row,child)
        if is_find==False:
            v,c= Pluarity_Value(df)
            if str(v) == str(row["survived"].tolist()[0]):
                return True
            else:
                return False
    else:
        tree_lable = node.lable
        if str(node.lable) == str(row["survived"].tolist()[0]):
            return True
        else:
            return False
# make tree



n=1100  # number of datas that we select to make tree
df = pandas.read_csv('titanic.csv').head(n)
attributes = list(df.columns)
attributes.remove("survived")                    # result
attributes.remove("name")                        
mainNode = Node(None,attributes_list=attributes,value='',datas=df)
node_list.append(mainNode)
decision_Tree(mainNode)    
# print_Node(mainNode,0)

# test tree
test_df = pandas.read_csv('titanic.csv').tail(1310-n)
correct = 0
for i in range(0,1310-n):
    if test_row_by_tree(test_df.iloc[[i]],mainNode)==True:
        correct+=1

print(correct/(1310-n))


