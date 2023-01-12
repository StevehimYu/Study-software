import json
import os
import queue
import random
import shutil
import time

string_list = ["update", "json", "ifok", "waiting...", "waiting...", "waiting...", "waiting...", "waiting...",
               "waiting...", "waiting...", "waiting..."]

word_dict_standard = {
    "word_number": {
        "Eng": 0,
        "Chi": 0,
    },
    "word_list": {
        "Eng": {},
        "Chi": {},
    },
}

# 链表
node = {
    "number": 0
}

date = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


def update():
    pass


def _sort(word_dict_1, list_name):  # 用于开始新一轮的链表
    print("Start to rebuild, the list name is:{}".format(list_name))
    cover_list = {}
    # word_list = {}
    eng_number = word_dict_1["word_number"]["Eng"]
    cover_list["number"] = eng_number
    num = 0
    string_temp = ""
    for k, v in word_dict_1["word_list"]["Eng"].items():
        if num == 0:
            cover_list[k] = ""
            cover_list["First_string"] = k
            string_temp = k
            num += 1
        else:
            cover_list[string_temp] = k
            string_temp = k
    with open("list/{}.json".format(list_name), "w") as j:
        json.dump(cover_list, j)
        j.close()
    time.sleep(1.5)


def _open(dict_name):
    ifDaoRu = 0
    word_dict_1 = word_dict_standard  #
    try:
        with open("word/{}.json".format(dict_name), "r", encoding="gb2312") as w:
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


def save(dic, dict_name):
    with open("word/{}.json".format(dict_name), "w", encoding="gb2312") as w:
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


def save_log(method, eng, chi, dict_name):
    with open("log.log", "a") as l:
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        l.write("{}  |{}.json|  {}  |  {}  |  {}  |\n".format(date, dict_name, method, eng, chi))


def _input(method, word_dict_1, dict_name):
    if method == 0:
        word_dict_1 = word_dict_standard
    while True:
        os.system("cls")
        eng = input("Please input the words you want to remember,you can input 'ex' to exit:")
        if eng == "ex":  # 退出
            print("start to save your document")
            save(word_dict_1, dict_name)
            return
        # 以下是重点
        chi_all = input("Please input the Chinese meanings\nYou can input more words a time,with the "
                        "spilt '、' \nbut please determine your inputs are right:")
        chi_list = chi_all.split("、")
        for chi in chi_list:
            op = check(1, word_dict_1, eng, chi)
            add(op, 1, word_dict_1, eng, chi)
            op = check(0, word_dict_1, chi, eng)
            add(op, 0, word_dict_1, chi, eng)
            save_log("Input", eng, chi, dict_name)


def _test(word_dict_1, word_name):
    op_list = ["Chi", "Eng"]
    try:
        op = int(input("Please input which test you want,1 means Chi to Eng,2 means Eng to Chi：")) - 1
    except ValueError:
        print("Sorry, your input is wrong, I will auto to return to the main function")
        return
    if word_dict_1["word_number"]["Chi"] == 0 or word_dict_1["word_number"]["Eng"] == 0:
        print("Your word list is empty!")
        time.sleep(1.5)
        return
    option = op_list[op]
    q = queue.Queue()
    for i in range(3):  # 队列初始化
        num = random.randint(0, word_dict_1["word_number"][option] - 1)  # 先放着看看对不对
        q.put(list(word_dict_1["word_list"][option].keys())[num])  # 取键操作
    while True:
        os.system("cls")
        print("Now list:{}".format(word_name))
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


def new_test(cover_list, word_dict_1, list_name):  # 暂时仅限英语
    """
    cover_list 结构：
    cover_list:{
        "number": xx,
        "First_string": xx,
        "xxx":"yyy",
        "yyy":"zzz",
        ....
    }
    """
    if cover_list["number"] == 0:
        print("Your word list is empty!")
        time.sleep(1.5)
        return
    test_string = cover_list["First_string"]  # 取最初字符串
    while cover_list["number"] != 0:
        os.system("cls")
        time.sleep(0.01)
        print("Now list:{}".format(list_name))
        print("If you find the list is wrong,please return to the menu and rebuild the list")
        print("当前剩余：" + str(cover_list["number"]))
        print("Let's test.You can input ‘ex’ to exit\n")
        user_string = input("{}：".format(test_string))
        if user_string == "ex":
            with open("list/{}.json".format(list_name), "w") as j:
                json.dump(cover_list, j)
                j.close()
            return
        ifOk = 0
        for k, v in word_dict_1["word_list"]["Eng"][test_string].items():
            if v == user_string:
                ifOk = 1
        if ifOk == 0:
            print("You are WRONG! The answer is：", end="")
            # print(word_dict_1["word_list"]["Eng"][test_string]["1"])
            for j in range(1, word_dict_1["word_list"]["Eng"][test_string]["number"] + 1):  # range会循环到上界减一停下
                print(word_dict_1["word_list"]["Eng"][test_string][str(j)] + "/", end="")
            # 如果错了就再来一次
            next_string = cover_list[test_string]  # 取出下一个值
            try:
                temp_string = cover_list[next_string]  # 取出下一个值对应的值
                cover_list[next_string] = test_string
                cover_list[test_string] = temp_string
                test_string = next_string  # 开始交换
                cover_list["First_string"] = next_string  # 改变头
            except KeyError:  # 说明是最后一个了
                cover_list[next_string] = test_string
            print("")
            input("请按回车键继续")
        else:
            print("You are right!")
            # 如果对了就删除这个键
            temp_string = test_string
            test_string = cover_list[test_string]
            del cover_list[temp_string]
            cover_list["number"] -= 1
            cover_list["First_string"] = test_string  # 更改头部字符串
            time.sleep(0.25)
    print("You AK IOI !")
    time.sleep(3)
    return


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
        try:
            option1 = op_list[int(option - 1)]
        except IndexError:
            print("输入信息有误")
            continue
        while True:
            os.system("cls")
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


def createList():
    name = input("Please input the name of the list:")
    with open("list/{}.json".format(name), "w") as o:
        o.close()
    _input(0, word_dict_standard, name)


def checkList():
    try:
        json_list = os.listdir("word")
    except FileNotFoundError:
        print("Your word folder is missing!\nauto to return to the menu...")
        time.sleep(1.5)
        return
    if len(json_list) == 0:
        op = input("There is nothing in your word folder \n do you want to create a new list?[y/n]:")
        if op == "n":
            print("Ok, returning to the menu")
            time.sleep(1)
            return
        elif op == "y":
            createList()
        else:
            print("Sorry, you input another answer, returning to the menu")
            return
    try:
        print("Now there are {} word lists in your 'word' folder:".format(len(json_list)))
    except Exception as e:
        print(e)
        os.system("pause")
    num = 1
    for i in json_list:
        print("{}.{}".format(num, i))
        num += 1
    while True:
        try:
            option = int(input("Please input the number of the folder you want to choose:")) - 1
            if json_list[option] in json_list:
                return json_list[option].split('.')[0]
            else:
                print("There is no such a list in your folder")
                continue
        except:
            print("There are some errors! I will return default name 'word'")
            time.sleep(2)
            return "word"


def _print(dic):
    knum = 1
    for k, v in dic.items():
        print(str(knum) + ":" + k)
        knum += 1
        num = 1
        for i in dic[k]:
            print("----" + str(num) + ":{}".format(i))
            num += 1


def lookUpdate():
    try:
        with open("update", 'r') as o:
            dic = json.load(o)
            o.close()
        os.system("cls")
        print("These are updates：")
        _print(dic)
        input("Press the enter key to return...")
        return
    except FileNotFoundError:
        print("There is no update document,please communicate the administrator")
        time.sleep(5)
        return
    except UnicodeDecodeError:
        print("Your update document is broken!Please communicate the administrator")
        time.sleep(5)
        return


# main函数入口
def main():
    word_name = "word"
    list_name = "word"
    try:
        print("Start to check")
        word_dict_1, ifDaoRu = _open(word_name)
        if ifDaoRu == 1:
            _input(0, word_dict_1, word_name)
            print("Ok,please restart the software again")
            os.system("pause")
            exit(1)

        else:
            while True:
                os.system("cls")
                print("Now word list: {}.json, now list: {}.json".format(word_name, list_name))
                # 开机自检
                word_dict_1, ifDaoRu = _open(word_name)
                try:
                    with open("list/{}.json".format(list_name), "r") as j:
                        cover_list = json.load(j)
                        j.close()
                except Exception:
                    print("Your test_list is empty! Auto to rebuild the list...")
                    _sort(word_dict_1, list_name)
                    time.sleep(2)
                    continue
                try:
                    print("Welcome to the English software!")
                    print("------------------------↓         This area is for test         ↓------------------------")
                    print("1.(Recommended)Start to test by link list(Now is ordered)")
                    print("2.(Not recommended)start to test by random")
                    print("------------------------↓ This area is for find or change words ↓------------------------")
                    print("3.Found a word or a Chinese.")
                    print("4.change a word.")
                    print("------------------------↓    This area is for list operations   ↓------------------------")
                    print("5.Input your list again.")
                    print("6.Attend words to your list.")
                    print("7.Rebuild the list.")
                    print("8.Change the word list(Pay attention, your test_list will be changed as well).")
                    print("9.Create a new word list.")
                    print("------------------------↓  This area is for software operation  ↓-----------------------")
                    print("10.exit.")
                    print("11.look update")
                    print("------------------------------------------------------------------------------------------")
                    op = int(input("Now please choose:"))
                except:
                    print("You print a WRONG word!")
                    continue
                os.system('cls')
                if op == 1:
                    new_test(cover_list, word_dict_1, list_name)
                elif op == 2:
                    _test(word_dict_1, word_name)
                elif op == 3:
                    search(word_dict_1)
                elif op == 4:
                    print("The function is repairing...")
                    input("Press enter to return...")
                elif op == 5:
                    _input(0, word_dict_1, word_name)
                    print("OK")
                    time.sleep(1.5)
                    continue
                elif op == 6:
                    _input(1, word_dict_1, word_name)
                elif op == 7:
                    _sort(word_dict_1, list_name)
                elif op == 8:
                    word_name = checkList()
                    list_name = word_name
                elif op == 9:
                    createList()
                elif op == 10:
                    print("start to save backup your document...")
                    shutil.copyfile("word/{}.json".format(word_name), "backup/{}-{}.json".format(date, word_name))
                    os.system("pause")
                    exit(1)
                elif op == 11:
                    lookUpdate()
                else:
                    print("You input a wrong number!")
    except Exception as e:
        print(e)
        print("程序出现某些错误，需要退出")


if __name__ == "__main__":
    main()
