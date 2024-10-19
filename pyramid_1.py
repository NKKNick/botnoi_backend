def createStar():
    getInput = input()
    conI = int(getInput)
    for i in range(conI):
        for j in range(i+1):
            print("*",end="")
        print()
    for i in range(conI):
        for j in range(i+1,conI):
            print("*",end="")
        print()

createStar()