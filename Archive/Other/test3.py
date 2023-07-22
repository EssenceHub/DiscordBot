def nwa (names=[],ages=[]):
    file = open('Homework 09 Printout.txt','w')
    file.write('Names in the Database\n\n')
    for i in range(len(names)):
        name_parts = names[i].split(",")
        f_name = name_parts[1].strip().capitalize()
        l_name = name_parts[0].strip().capitalize()
        file.write(f"{f_name} {l_name} is {ages[i]} years old.\n")
        
    print("The file Homework 09 Printout.txt has been written.")
    file.close()

names = ["sweigart, Al","Domer, ima","munsch, charlie","Wade, Jess"]

ages = [32, 18, 71, 45]

nwa(names, ages)