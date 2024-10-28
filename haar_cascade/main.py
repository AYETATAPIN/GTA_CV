from cascade import learn, makeWrongInfo


def main():
    makeWrongInfo("falseCars", 200, 200, "wrongInfo200")
    makeWrongInfo("falseCars", 300, 200, "wrongInfo300")
    learn("cars_footage/left", "modelLeft.txt", 300, 200)
    learn("cars_footage/front", "modelFront.txt", 200, 200)
    learn("cars_footage/back", "modelBack.txt", 200, 200)
    learn("cars_footage/right", "modelRight.txt", 300, 200)
    print("learn compl")

if __name__ == "__main__":
    main()
