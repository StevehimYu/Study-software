import json
import os
import random
import time
import shutil
import queue

# preparation = [""]


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

print("Start to check")


def _open():
    ifDaoRu = 0
    word_dict_1 = word_dict_standard  #
    try:
        with open("word.json", "r") as w:
            word_dict_1 = json.load(w)
            w.close()
    except json.decoder.JSONDecodeError:
        print("Your json in word.txt is broken,please check your data and restart the software")
        os.system("pause")
    except FileNotFoundError:
        print("Don't find word.txt in the folder, auto to enter the input method")
        time.sleep(1)
        ifDaoRu = 1
    return word_dict_1, ifDaoRu


def save(dic):
    with open("word.json", "w") as w:
        json.dump(dic, w)
        w.close()


def check(method, word_dict_1, string1,
          string2):  # 注释：string1是指当前输入的英语/语文词，而string2是检索的语文/英语单词，该函数用于检测某单词是否存在于另一个单词的释义中
    op_list = ["Chi", "Eng"]
    option = op_list[method]
    try:
        ifo = 0
        print(word_dict_1["word_list"][option][string1]["number"])
        # 这里是假设字典存在，也就是收录了这个单词,首先查找有没有意思,其中意思字典由输入的模式决定
        if word_dict_1["word_list"][option][string1]["number"] >= 1:  # 如果大于则说明超过0个意思
            for k, v in word_dict_1["word_list"][option][string1].items():
                if v == string2:
                    ifo = 1
            # 如果是新的中文释义
            if ifo == 0:
                return "1"  # 并没有存在
            else:
                return "0"  # 存在了
    except:
        return "error"  # 肯定不存在


def add(opt, method, word_dict_1, string1, string2):
    op_list = ["Chi", "Eng"]
    option = op_list[method]
    if opt == "1":
        word_dict_1["word_list"][option][string1]["number"] += 1  # 个数加一
        number = word_dict_1["word_list"][option][string1]["number"]  # 创建数字变量方便添加释义
        word_dict_1["word_list"][option][string1][number] = string2  # 注意：这里只管添加中文释义
    elif opt == "0":
        print("This meaning has been included")
    else:  # 出错了，说明压根没有
        print("There is a new")
        time.sleep(0.25)
        number = 1
        word_dict_1["word_number"][option] += 1
        word_dict_1["word_list"][option][string1] = {}
        word_dict_1["word_list"][option][string1]["number"] = number
        word_dict_1["word_list"][option][string1][number] = string2


def _input(method, word_dict_1):
    if method == 0:
        word_dict_1 = word_dict_standard
    while True:
        os.system("cls")
        eng = input("Please input the words you want to remember:")
        if eng == "ex":  # 退出
            print("start to save your document")
            time.sleep(1.5)
            save(word_dict_1)
            return
        # 以下是重点
        chi = input("Please input the Chinese meanings:")
        op = check(1, word_dict_1, eng, chi)
        add(op, 1, word_dict_1, eng, chi)
        op = check(0, word_dict_1, chi, eng)
        add(op, 0, word_dict_1, chi, eng)


def _test(word_dict_1):
    op_list = ["Chi", "Eng"]
    try:
        op = int(input("Please input which test you want,1 means Chi to Eng,2 means Eng to Chi：")) - 1
    except ValueError:
        print("Sorry, your input is wrong, I will auto to return to the main function")
        return
    option = op_list[op]
    q = queue.Queue()
    for i in range(3):  # 队列初始化
        num = random.randint(0, word_dict_1["word_number"][option] - 1)  # 先放着看看对不对
        q.put(list(word_dict_1["word_list"][option].keys())[num])  # 取键操作
    while True:
        os.system("cls")
        print("Now let's start to test,you will randomly have a {} word and you should spell its {} CORRECTLY".format(
            op_list[op], op_list[-1 * op + 1]))
        print("You can input ‘ex’ to exit\n")
        right_string = q.get()  # 将目标字符串取出
        number = word_dict_1["word_list"][option][right_string]["number"]
        print("There may be many meanings, you can input one of them")
        s = input(right_string + ":")
        if s == "ex":
            return
        if number >= 2:
            ifOk = 0
            for i in range(1, number + 1):  # 默认从0开始，为了达到效果需要将number + 1
                if s == word_dict_1["word_list"][option][right_string][str(i)]:  # 查找是在对应的字典里面查找，看看有么有这个词
                    print("You are right")
                    ifOk = 1
                    num = random.randint(0, word_dict_1["word_number"][option] - 1)  # 先放着看看对不对
                    q.put(list(word_dict_1["word_list"][option].keys())[num])  # 取键操作
                    time.sleep(0.5)
                    break  # 直接退出
            if ifOk == 0:
                print("Yor are WRONG! The answer is：", end="")
                for i in range(1, number + 1):  # 默认从0开始，为了达到效果需要将number + 1
                    print(word_dict_1["word_list"][option][right_string][str(i)] + '/', end="")  # 一列输出所有意思
                print("")
                input("Press Enter to continue")
                q.put(right_string)  # 将错误的放入队列中
        else:
            if s == word_dict_1["word_list"][option][right_string]["1"]:  # 肯定只有1个啊
                print("You are right")
                num = random.randint(0, word_dict_1["word_number"][option] - 1)  # 先放着看看对不对
                q.put(list(word_dict_1["word_list"][option].keys())[num])  # 取键操作
                time.sleep(0.5)
            else:
                print("Yor are WRONG! The answer is：" + word_dict_1["word_list"][option][right_string]["1"])
                input("Press Enter to continue")
                q.put(right_string)  # 取键操作


def search(word_dict_1):
    op_list = ["Chi", "Eng"]
    while True:
        try:
            option = int(input("查中文还是英文（c:1 / e:2)?[3退出]："))
        except ValueError:
            print("输入信息有误")
            continue
        if option == 3:
            return
        while True:
            os.system("cls")
            option1 = op_list[int(option - 1)]
            try:
                ser_str = input("查什么？（输入4退回中英文选择界面）：")
            except:
                print("输入信息有误")
                continue
            if ser_str == "4":
                break
            try:
                for k, v in word_dict_1["word_list"][option1][ser_str].items():
                    if k == "number":
                        print("共收录{}种意思".format(v))
                    else:
                        print(k + ":" + v)
            except KeyError:
                print("没有这个单词")
            except TypeError as t:
                print(t)
            input("按下回车键继续")


# main函数入口
def main():
    try:
        word_dict_1, ifDaoRu = _open()
        if ifDaoRu == 1:
            _input(0, word_dict_1)
            print("Ok,please restart the software again")
            os.system("pause")
            exit(1)
        else:
            while True:
                word_dict_1, ifDaoRu = _open()
                os.system("cls")
                try:
                    op = int(input("Welcome to the English software, now please choose"
                                   "\n1.input word.txt again.\n2.start to test"
                                   "\n3.attend words to word.txt\n4.change a "
                                   "word\n5.found a word or a Chinese\n6.exit:"))
                except:
                    print("You print a WRONG word!")
                    continue
                os.system('cls')
                if op == 1:
                    _input(0, word_dict_1)
                    print("Ok,please restart the software again")
                    os.system("pause")
                    exit()
                elif op == 2:
                    _test(word_dict_1)
                elif op == 3:
                    _input(1, word_dict_1)
                elif op == 4:
                    print("The function is repairing...")
                elif op == 5:
                    search(word_dict_1)
                elif op == 6:
                    print("start to save backup your document...")
                    try:
                        shutil.copy("word.json", "/backup")
                    except:
                        print("Sorry,please open your software as an administrator")
                    os.system("pause")
                    exit()
                else:
                    print("You input a wrong number!")
    except:
        print("程序出现某些错误，需要退出")


if __name__ == "__main__":
    main()
