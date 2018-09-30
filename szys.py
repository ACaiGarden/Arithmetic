# -*- coding: UTF-8 -*-
from fractions import Fraction

def ShowFraction(f):
    if f.numerator <= f.denominator:
        return str(f)
    else:
        a = f.numerator // f.denominator
        b = f.numerator % f.denominator
        if(b == 0):
            return str(f)
        else:
            return str(a) + '\'' + str(b) + "/" + str(f.denominator)

class Node():
    def __init__(self, sym, lt = None, rt = None, num = -1):
        self.number = num
        self.symbol = sym
        self.ltree = lt
        self.rtree = rt

class BiTree():
    def __init__(self, node):
        self.root = node

    def show(self, root):
        if root.symbol == "/":
            return ShowFraction(root.number)
        elif root.symbol == "+" or root.symbol == "-":
            if root.rtree.symbol == "+" or root.rtree.symbol == "-":
                return self.show(root.ltree) + " " + root.symbol + " ( " + self.show(root.rtree) + " )"
            return self.show(root.ltree) + " " + root.symbol + " " + self.show(root.rtree)
        else:
            if root.ltree.symbol == "+" or root.ltree.symbol == "-":
                i = "( " + self.show(root.ltree) + " )"
            else:
                i = self.show(root.ltree)
            i += " " + root.symbol + " "
            if root.rtree.symbol != "/":
                i += "( " + self.show(root.rtree) + " )"
            else:
                i += self.show(root.rtree)
            return i

    def Count(self, root):
        if root.symbol == "/":
            return root.number
        elif root.symbol == "+":
            return self.Count(root.ltree) + self.Count(root.rtree)
        elif root.symbol == "-":
            return self.Count(root.ltree) - self.Count(root.rtree)
        elif root.symbol == "*":
            return self.Count(root.ltree) * self.Count(root.rtree)
        elif root.symbol == "÷":
            return self.Count(root.ltree) / self.Count(root.rtree)

def getFraction():
    pass

def getBiTree():
    pass

def fitBiTree(root):
    if root.symbol == "/":
        return root.number
    elif root.symbol == "+":
        return fitBiTree(root.ltree) + fitBiTree(root.rtree)
    elif root.symbol == "*":
        return fitBiTree(root.ltree) * fitBiTree(root.rtree)
    elif root.symbol == "-":
        a = fitBiTree(root.ltree) - fitBiTree(root.rtree)
        if a < 0:
            b = root.ltree
            root.ltree = root.rtree
            root.rtree = b
            a = fitBiTree(root.ltree) - fitBiTree(root.rtree)
        return a
    elif root.symbol == "÷":
        if fitBiTree(root.ltree) >= fitBiTree(root.rtree):
            b = root.ltree
            root.ltree = root.rtree
            root.rtree = b

        a = fitBiTree(root.ltree) / fitBiTree(root.rtree)
        return a

#=====================以下为拓展功能模块=======================================

def StrToFraction(num):#将字符串格式的分数转换为Fraction
    numlist = num.split("'")
    if len(numlist) == 1:
        return Fraction(numlist[0])
    else:
        return Fraction(numlist[1]) + int(numlist[0])


def EleS(element, stack1, stack2):#此处需要递归调用
    if stack1:
        if stack1[-1] == ")" or stack1[-1] == "-" or stack1[-1] == "+":
            stack1.append(element)
        else:
            stack2.append(stack1.pop())
            EleS(element, stack1, stack2)
    else:
        stack1.append(element)

def StrToExpress(express):#将字符串格式的表达式转换成列表类的前缀表达式
    elelist = express.split()
    elelist.reverse()
    s1, s2 = [], []#s1和s2是转换表达式时使用的栈
    for ele in elelist:
        if ele == "-" or ele == "+":
            EleS(ele, s1, s2)
        elif ele == "*" or ele == "÷":
            s1.append(ele)
        elif ele == ")":
            s1.append(ele)
        elif ele == "(":
            while s1[-1] != ")":
                s2.append(s1.pop())
            del s1[-1]
        else:
            s2.append(ele)
    while s1:
        s2.append(s1.pop())
    return s2

def PreToBiTree(prefixlist):#将前缀表达式转换为二叉树
    if prefixlist[-1] == '+' or prefixlist[-1] == '-' or prefixlist[-1] == '*'\
            or prefixlist[-1] == '÷':
        Pnode = Node(prefixlist.pop())
        Pnode.ltree = PreToBiTree(prefixlist)
        Pnode.rtree = PreToBiTree(prefixlist)
        return Pnode
    else:
        return Node('/', num = StrToFraction(prefixlist.pop()))

def Check(expressfile, answerfile):#主程序
    fe = open(expressfile, encoding='UTF-8')
    fa = open(answerfile, encoding='UTF-8')
    express = fe.read().splitlines()#按行读取
    answer = fa.read().splitlines()
    correct, false, i= 0, 0, 0#correct为正确题目数,flase为错误数,i是表达式序号
    correctlist, falselist = [], []#用来保存正确和错误题目的序号
    for line, ans in list(zip(express, answer)):
        i += 1
        line1 = line.split(".")#将前面的序号去掉
        ans1 = ans.split(".")
        tree = BiTree(PreToBiTree(StrToExpress(line1[1])))
        if tree.Count(tree.root) == StrToFraction(ans1[1]):
            correct += 1
            correctlist.append(i)
        else:
            false += 1
            falselist.append(i)
    print("Correct: " + str(correct) + " " + tuple(correctlist).__str__() + \
          "\n" + "Wrong: " + str(false) + " " + tuple(falselist).__str__())


if __name__ == '__main__':
    #test
    '''
    n0 = Node(num = Fraction(1, 2), sym = "/")
    n1 = Node(num = Fraction(7, 3), sym = "/")
    n2 = Node(num = Fraction(1, 1), sym = "/")
    n3 = Node(num = Fraction(4, 5), sym = "/")

    n4 = Node("÷", n0, n1)
    n5 = Node("*",n2,n3)
    root = Node("-", n4, n2)
    tree = BiTree(root)
    print(tree.show(tree.root) + " = " + ShowFraction(tree.Count(tree.root)))
    fitBiTree(root)
    print(tree.show(tree.root) + " = " + ShowFraction(tree.Count(tree.root)))
    '''
    #Check('Exercises.txt', 'Answers.txt')