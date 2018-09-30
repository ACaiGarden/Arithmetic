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
        elif root.symbol == "&":
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
    elif root.symbol == "&":
        if fitBiTree(root.ltree) >= fitBiTree(root.rtree):
            b = root.ltree
            root.ltree = root.rtree
            root.rtree = b

        a = fitBiTree(root.ltree) / fitBiTree(root.rtree)
        return a




if __name__ == '__main__':
    #test
    n0 = Node(num = Fraction(1, 2), sym = "/")
    n1 = Node(num = Fraction(7, 3), sym = "/")
    n2 = Node(num = Fraction(1, 1), sym = "/")
    n3 = Node(num = Fraction(4, 5), sym = "/")

    n4 = Node("&", n0, n1)
    n5 = Node("*",n2,n3)
    root = Node("-", n4, n2)
    tree = BiTree(root)
    print(tree.show(tree.root) + " = " + ShowFraction(tree.Count(tree.root)))
    fitBiTree(root)
    print(tree.show(tree.root) + " = " + ShowFraction(tree.Count(tree.root)))