""" file_intento = "Dibujos/intento-{}.txt".format("3")
f = open(file_intento, "r")
print(f.read())
 """
def get_content_file(file_name):
    f = open(file_name, "r")
    content = f.read()
    return content


print(get_content_file("Dibujos/intento-{}.txt".format("3")))