from model.model import Model

mymodel = Model()
mymodel.buildGraph('White', 2018)
print(mymodel.printGraphDetails())
mymodel.getEdgeMaxWeight()
