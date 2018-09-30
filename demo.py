# -*- coding: UTF-8 -*-
from fractions import Fraction
import re
import random
from szys import *
import sys,getopt
import NBL

class Generate():
    def __init__(self):
        self.topic_num = 10
        self.max_num = 0

        self.exercisefile = ''
        self.answerfile = ''

        self.topic_list = set([])
        self.get_info()
        if self.max_num != 0:
            self.NewExpressions()
        elif (self.exercisefile != '') and (self.answerfile != ''):
            Check(self.exercisefile, self.answerfile)

    def get_info(self):
        #获取传入参数 -r -n
        try:
            option, arg = getopt.getopt(sys.argv[1:], "n:r:e:a:")
            print(option)
            for opt, args in option:
                if (opt in '-n') or (opt in '-r'):
                    if opt in '-n':
                        self.topic_num = int(args)
                    elif opt in '-r':
                        self.max_num = int(args)
                    else:
                        print('Please input the -r max_num')
                        exit()

                elif (opt in '-e') or (opt in '-a'):
                    if opt in '-e':
                        self.exercisefile = args
                    elif opt in '-a':
                        self.answerfile = args


        except getopt.error as e:
            pass

    def NewExpressions(self):
        # 写入文件
        fe = open("Exercises.txt", "a", encoding='UTF-8')
        fa = open("Answers.txt", "a", encoding='UTF-8')
        for i in range(0, self.topic_num):
            bitree = BiTree(self.generate())
            fa.write(str(i + 1) + ". " + str(ShowFraction(bitree.Count(bitree.root))) + "\n")
            fe.write(str(i + 1) + ". " + str(bitree.show(bitree.root)) + "\n")
        fe.close()
        fa.close()

    def generate(self):
        type_list = ['F', 'I']  # Fraction or Int
        sym_num = random.randint(1, 3)  # 符号数
        type = random.sample(type_list, 1)[0]   # 数类型
        root = self.built_Tree(sym_num, type)
        tree = BiTree(root)
        fitBiTree(root)
        tree_string = str(tree.show(tree.root))
        is_repeat = self.check_repeat(tree_string)
        if  is_repeat == True:
            print(tree.show(tree.root) + " = " + ShowFraction(tree.Count(tree.root)))
            return root
        else:
            while is_repeat == False:
                #print('error')
                root = self.built_Tree(sym_num, type)
                tree = BiTree(root)
                fitBiTree(root)
                tree_string = str(tree.show(tree.root))
                is_repeat = self.check_repeat(tree_string)
            print(tree.show(tree.root) + " = " + ShowFraction(tree.Count(tree.root)))
            #print('mark')
            return root

    def check_repeat(self, tree_str):
        tree_NBL = NBL.middle_to_after(tree_str)
        topic_num = len(self.topic_list)
        self.topic_list.add(tree_NBL)
        if len(self.topic_list) == topic_num:
            # 重复公式
            return False
        else:
            return True

    def built_Tree(self, sym_num, type):
        #按照sym_num（字符数）构造二叉树
        if sym_num == 1:
            return self.built_1(type)
        elif sym_num == 2:
            return self.built_2(type)
        elif sym_num == 3:
            return self.built_3(type)

    def built_1(self, type):
        sym_list = ['+', '-', '*', '÷']
        symbol = random.sample(sym_list, 1)[0]
        num1 = random.randint(1, self.max_num - 1)
        num2 = random.randint(1, self.max_num - 1)
        if type == 'I':
            num3 = num4 = 1
        else:
            num3 = random.randint(1, self.max_num)
            num4 = random.randint(1, self.max_num)
        root = Node(sym=symbol, lt=Node('/', num=Fraction(num1, num3)),
                    rt=Node('/', num=Fraction(num2, num4)))
        return root

    def built_2(self, type):
        sym_list = ['+', '-', '*', '÷']
        symbol1 = random.sample(sym_list, 1)[0]

        lc = self.built_1(type)

        num1 = random.randint(1, self.max_num - 1)
        if type == 'I':
            num2 = 1
        else:
            num2 = random.randint(1, self.max_num)

        rc = Node('/', num = Fraction(num1, num2))

        root = Node(symbol1, lc, rc)
        return root

    def built_3(self, type):
        sym_list = ['+', '-', '*', '÷']
        symbol1 = random.sample(sym_list, 1)[0]

        lc = self.built_1(type)
        rc = self.built_1(type)

        root = Node(symbol1, lc, rc)
        return root

g = Generate()
print("题目数量：", len(g.topic_list))