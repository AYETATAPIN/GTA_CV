import os

os.chdir("D:\Downloads\cars_front")
print(os.getcwd())

for count, f in enumerate(os.listdir()):
    f_name, f_ext = os.path.splitext(f)
    print(f_name)
    f_name = "car_front_view" + str(count)
    new_name = f"{f_name}{f_ext}"
    print(new_name)
    os.rename(f, new_name)