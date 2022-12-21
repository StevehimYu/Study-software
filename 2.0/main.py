import json
import os
import random
import time
import shutil

'''
关于word_dict的详解：
1.word_map:
word_map由Chi和Eng两部分组成，分别代表英文的释义以及中文的释义的索引，由于
每个单词/中文释义有多种意思，所以会在每个单词的基础上再嵌套一层字典，其中的number
表示当前这个意思有的单词数目。之后从1开始代表每个单词
'''
word_dict_standard = {
    "word_number": {
        "Chi": 0,
        "Eng": 0,
    },
    "word_list": {
        "Eng": {},
        "Chi": {},
    },
}
word_dict = {
    "word_number": {
        "Chi": 0,
        "Eng": 0,
    },
    "word_list": {
        "Eng": {},
        "Chi": {},
    },
}

ifDaoRu = 0

print("Start to check")
try:
    with open("word.json", "r") as w:
        word_dict = json.load(w)
        w.close()
except json.decoder.JSONDecodeError:
    print("Your json in word.txt is broken,please check your data and restart the software")
    os.system("pause")
except FileNotFoundError:
    print("Don't find word.txt in the folder, auto to enter the input method")
    time.sleep(1)
    ifDaoRu = 1


def save(dic):
    with open("word.json", "w") as w:
        json.dump(dic, w)
        w.close()


def _input(method, word_dict):
    if method == 0:
        word_dict = word_dict_standard
    while True:
        os.system("cls")
        eng = input("Please input the words you want to remember:")
        if eng == "ex":  # 退出
            print("start to save your document")
            time.sleep(1.5)
            save(word_dict)
            return
        # 以下是重点
        chi = input("Please input the Chinese meanings:")

        try:
            print(word_dict["word_list"]["Eng"][eng]["number"])
            # 这里是假设字典存在，也就是收录了这个单词,首先查找有没有中文意思
            if word_dict["word_list"]["Eng"][eng]["number"] >= 1:  # 如果大于则说明超过0个意思
                for k, v in word_dict["word_list"]["Eng"][eng].items():
                    if v == chi:
                        print("This Chinese meaning has been included")
                        continue
                # 如果是新的中文释义
                word_dict["word_list"]["Eng"][eng]["number"] += 1  # 个数加一
                number = word_dict["word_list"]["Eng"][eng]["number"]  # 创建数字变量方便添加释义
                word_dict["word_list"]["Eng"][eng][number] = chi  # 注意：这里只管添加中文释义
            # else:  # 如果不超过一，还是0
            #     word_dict["word_list"]["Eng"][eng]["number"] += 1  # 个数加一
            #     number = word_dict["word_list"]["Eng"][eng]["number"]  # 创建数字变量方便添加释义
            #     word_dict["word_list"]["Eng"][eng][number] = chi  # 注意：这里只管添加中文释义
            # 下面的是为了预防这个单词的中文意思已经有了，就把它添加到里面去
            try:
                if word_dict["word_list"]["Chi"][chi]["number"] >= 1:  # 如果大于则说明超过0个意思
                    for k, v in word_dict["word_list"]["Chi"][chi].items():
                        if v == eng:
                            print("This English meaning has been included")
                            continue
                    # 如果是新的中文释义
                    word_dict["word_list"]["Chi"][chi]["number"] += 1  # 个数加一
                    number = word_dict["word_list"]["Chi"][chi]["number"]  # 创建数字变量方便添加释义
                    word_dict["word_list"]["Chi"][chi][number] = eng  # 注意：这里只管添加英文释义
            except KeyError as k:
                print(k)
                print("There is a new")
                time.sleep(0.25)
                word_dict["word_number"]["Chi"] += 1
                word_dict["word_list"]["Chi"][chi] = {}
                number = 1
                word_dict["word_list"]["Chi"][chi]["number"] = number
                word_dict["word_list"]["Chi"][chi][number] = eng
            # else:  # 如果不超过一，还是0
            #     word_dict["word_list"]["Chi"][chi]["number"] += 1  # 个数加一
            #     number = word_dict["word_list"]["Chi"][chi]["number"]  # 创建数字变量方便添加释义
            #     word_dict["word_list"]["Chi"][chi][number] = eng  # 注意：这里只管添加英文释义
        except KeyError as k:
            print(k)
            print("There is a new")
            time.sleep(0.25)
            word_dict["word_number"]["Eng"] += 1

            # 初始化两个子字典
            number = 1
            word_dict["word_list"]["Eng"][eng] = {}
            word_dict["word_list"]["Eng"][eng]["number"] = number
            word_dict["word_list"]["Eng"][eng][number] = chi
            #  同样扫一遍中文释义是否重复
            try:
                if word_dict["word_list"]["Chi"][chi]["number"] >= 1:  # 如果大于则说明超过0个意思
                    for k, v in word_dict["word_list"]["Chi"][chi].items():
                        if v == eng:
                            print("This English meaning has been included")
                            continue
                    # 如果是新的中文释义
                    word_dict["word_list"]["Chi"][chi]["number"] += 1  # 个数加一
                    number = word_dict["word_list"]["Chi"][chi]["number"]  # 创建数字变量方便添加释义
                    word_dict["word_list"]["Chi"][chi][number] = eng  # 注意：这里只管添加英文释义
                # else:  # 如果不超过一，还是0
                #     word_dict["word_list"]["Chi"][chi]["number"] += 1  # 个数加一
                #     number = word_dict["word_list"]["Chi"][chi]["number"]  # 创建数字变量方便添加释义
                #     word_dict["word_list"]["Chi"][chi][number] = eng  # 注意：这里只管添加英文释义
            except KeyError as k:
                print(k)
                print("There is a new")
                time.sleep(0.25)
                number = 1
                word_dict["word_number"]["Chi"] += 1
                word_dict["word_list"]["Chi"][chi] = {}
                word_dict["word_list"]["Chi"][chi]["number"] = number
                word_dict["word_list"]["Chi"][chi][number] = eng


def _testEngToChi():
    while True:
        os.system("cls")
        print("\nNow let's start to test,you will randomly have a word and you should spell its English CORRECTLY")
        print("You can input ‘ex’ to exit\n")
        ran = random.randint(1, word_dict["word_number"]["Eng"] - 1)
        temp = 1
        right_string = ""
        for k, v in word_dict["word_list"]["Chi"].items():
            if temp == ran:
                right_string = k  # 将字符串找出来
                break
            temp += 1
        number = word_dict["word_list"]["Chi"][right_string]["number"]
        if number >= 2:
            print("There are many words about this Chinese, you can input one of them")
            s = input(right_string + ":")
            if s == "ex":
                return
            ifOk = 0
            for i in range(1, number + 1):  # 默认从0开始，为了达到效果需要将number + 1
                if s == word_dict["word_list"]["Chi"][right_string][str(i)]:
                    print("You are right")
                    ifOk = 1
                    time.sleep(0.5)
                    break  # 直接退出
            if ifOk == 0:
                print("Yor are WRONG! The answer is：", end="")
                for i in range(1, number + 1):  # 默认从0开始，为了达到效果需要将number + 1
                    print(word_dict["word_list"]["Chi"][right_string][str(i)] + '/', end="")
                print("\n")
                time.sleep(number * 1.5)
        else:
            s = input(right_string + ":")
            if s == "ex":
                return
            if s == word_dict["word_list"]["Chi"][right_string]["1"]:  # 肯定只有1个啊
                print("You are right")
                time.sleep(0.5)
            else:
                print("Yor are WRONG! The answer is：" + word_dict["word_list"]["Chi"][right_string]["1"])
                time.sleep(1.5)


def _testChiToEng():
    while True:
        os.system("cls")
        print("\nNow let's start to test,you will randomly have a word and you should spell its Chinese CORRECTLY")
        print("You can input ‘ex’ to exit\n")
        ran = random.randint(1, word_dict["word_number"]["Chi"] - 1)
        temp = 1
        right_string = ""
        for k, v in word_dict["word_list"]["Eng"].items():
            if temp == ran:
                right_string = k  # 将字符串找出来
                break
            temp += 1
        number = word_dict["word_list"]["Eng"][right_string]["number"]
        if number >= 2:
            print("There are many words about this word, you can input one of them")
            s = input(right_string + ":")
            if s == "ex":
                return
            ifOk = 0
            for i in range(1, number + 1):  # 默认从0开始，为了达到效果需要将number + 1
                if s == word_dict["word_list"]["Eng"][right_string][str(i)]:
                    print("You are right")
                    ifOk = 1
                    time.sleep(0.5)
                    break  # 直接退出
            if ifOk == 0:
                print("Yor are WRONG! The answer is：", end="")
                for i in range(1, number + 1):  # 默认从0开始，为了达到效果需要将number + 1
                    print(word_dict["word_list"]["Eng"][right_string][str(i)] + '/', end="")
                print("\n")
                time.sleep(number * 1.5)
        else:
            s = input(right_string + ":")
            if s == "ex":
                return
            if s == word_dict["word_list"]["Eng"][right_string]["1"]:  # 肯定只有1个啊
                print("You are right")
                time.sleep(0.5)
            else:
                print("Yor are WRONG! The answer is：" + word_dict["word_list"]["Eng"][right_string]["1"])
                time.sleep(1.5)


def change(word_dict):
    while True:
        os.system("cls")
        print("Now you can change,input ex to exit\n")
        try:
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
                save(word_dict)
                return
            else:
                print("You print a WRONG word!")
                time.sleep(1.5)
        except:
            print("You print a WRONG word!")


# main函数入口
def main():
    if ifDaoRu == 1:
        _input(0, word_dict)
        print("Ok,please restart the software again")
        os.system("pause")
        exit()
    else:
        time.sleep(5)
        while True:
            os.system("cls")
            try:
                op = int(input("Welcome to the English software, now please choose"
                               "\n1.input word.txt again.\n2.start to test(English to Chinese)\n3.start to test("
                               "Chinese "
                               "to English) "
                               "\n4.attend words to word.txt\n5.change a "
                               "word\n6.exit:"))
            except:
                print("You print a WRONG word!")
                continue
            os.system('cls')
            if op == 1:
                _input(0, word_dict)
                print("Ok,please restart the software again")
                os.system("pause")
                exit()
            elif op == 2:
                _testChiToEng()
            elif op == 3:
                _testEngToChi()
            elif op == 4:
                _input(1, word_dict)
            elif op == 5:
                print("The function is repairing...")
                change(word_dict)
            elif op == 6:
                print("start to save backup your document...")
                try:
                    shutil.copy("word.txt", "/backup")
                except:
                    print("Sorry,please open your software as an administrator")
                os.system("pause")
                exit()
            else:
                print("You input a wrong number!")


main()
