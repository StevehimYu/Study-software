import json
import os
import random
import time

word_dict = {
    "word_number": 0,
    "word_list": {

    },
    "word_map": {
        "Eng": {},
        "Chi": {},
    }
}

ifDaoRu = 0

print("Start to check")
try:
    with open("word.txt", "r") as w:
        word_dict = json.load(w)
        w.close()
except json.decoder.JSONDecodeError:
    print("Your json in word.txt is broken,please check your data and restart the software")
    os.system("pause")
except FileNotFoundError:
    print("Don't find word.txt in the folder, auto to enter the input method")
    ifDaoRu = 1


def save():
    with open("word.txt", "w") as w:
        json.dump(word_dict, w)
        w.close()


def _input():
    now_number = 0
    while True:
        os.system("cls")
        eng = input("Please input the words you want to remember:")
        if eng == "ex":
            print("start to save your document")
            word_dict["word_number"] = now_number  # 更新
            time.sleep(1.5)
            return
        chi = input("Please input the Chinese:")
        now_number += 1
        word_dict["word_list"][now_number] = {}
        word_dict["word_list"][now_number]["Eng"] = eng
        word_dict["word_list"][now_number]["Chi"] = chi
        word_dict["word_map"]["Eng"][eng] = now_number
        word_dict["word_map"]["Chi"][chi] = now_number


def _test():
    while True:
        print("\nNow let's start to test,you will randomly have a word and you should spell its Chinese CORRECTLY")
        print("You can input ‘ex’ to exit\n")
        ran = str(random.randint(1, word_dict["word_number"]))
        s = input(word_dict["word_list"][ran]["Eng"] + ":")
        if s == word_dict["word_list"][ran]["Chi"]:
            print("You are right\n")
            time.sleep(0.5)
        elif s == "ex":
            return
        else:
            print("You are WRONG! The answer is:" + word_dict["word_list"][ran]["Chi"] + "\n")
            time.sleep(2)
        os.system("cls")


def add():
    now_number = word_dict["word_number"]
    while True:
        print("Now please add, input ex to exit\n")
        os.system("cls")
        eng = input("Please input the words you want to remember:")
        if eng == "ex":
            print("start to save your document")
            word_dict["word_number"] = now_number  # 更新
            time.sleep(1.5)
            return
        chi = input("Please input the Chinese:")
        now_number += 1
        word_dict["word_list"][now_number] = {}
        word_dict["word_list"][now_number]["Eng"] = eng
        word_dict["word_list"][now_number]["Chi"] = chi
        word_dict["word_map"]["Eng"][eng] = now_number
        word_dict["word_map"]["Chi"][chi] = now_number


def change():
    while True:
        os.system("cls")
        print("Now you can change,input ex to exit\n")
        op = input("Input the type you want to change,eng/chi>")
        if op == "eng":
            s = input("You want to change what?>")
            try:
                number = str(word_dict["word_map"]["Eng"][s])
            except KeyError:
                print("This word is wrong,please try again")
                time.sleep(1.5)
                continue
            ss = input("Input which Chinese you want to change>")
            del word_dict["word_map"]["Chi"][word_dict["word_list"][number]["Chi"]]  # 将wordmap里面的chi删掉改成新的
            word_dict["word_list"][number]["Chi"] = ss
            word_dict["word_map"]["Chi"][ss] = number
        elif op == "chi":
            s = input("You want to change what?>")
            try:
                number = str(word_dict["word_map"]["Chi"][s])
            except KeyError:
                print("This word is wrong,please try again")
                time.sleep(1.5)
                continue
            ss = input("Input which Chinese you want to change>")
            del word_dict["word_map"]["Eng"][word_dict["word_list"][number]["Eng"]]  # 将wordmap里面的chi删掉改成新的
            word_dict["word_list"][number]["Eng"] = ss
            word_dict["word_map"]["Eng"][ss] = number
        elif op == "ex":
            return
        else:
            print("You print a WRONG word!")
            time.sleep(1.5)


# main函数入口
def main():
    if ifDaoRu == 1:
        _input()
        save()
    else:
        time.sleep(5)
        while True:
            os.system("cls")
            op = int(input("Welcome to the English software, now please choose"
                           "\n1.input word.txt again.\n2.start to test\n3.attend words to word.txt\n4.change a "
                           "word\n5.exit:"))
            os.system('cls')
            if op == 1:
                _input()
                save()
            elif op == 2:
                _test()
            elif op == 3:
                add()
                save()
            elif op == 4:
                change()
                save()
            elif op == 5:
                os.system("pause")
                exit()
            else:
                print("You input a wrong number!")


main()
