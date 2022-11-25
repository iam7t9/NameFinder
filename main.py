import os
import time
import json

def getNames(numbers,init=True, device="07586311CO072403"):
    '''Manupulating Android Using ADB'''
    if init:
        os.system(f"adb -s {device} shell am force-stop com.truecaller")
        os.system(f"adb -s {device} shell monkey -p com.truecaller -v 1")
        time.sleep(5)
        os.system(f"adb -s {device} shell input tap 400 210")
        time.sleep(1)
    Data = {}
    for number in numbers:
        os.system(f"adb -s {device} shell input text {number}")
        time.sleep(3)
        os.system(f"adb -s {device} shell uiautomator dump")
        os.system(f"adb -s {device} pull /sdcard/window_dump.xml")
        f = open("window_dump.xml", "r", encoding='utf8')
        textList = f.read().replace("><", ">\n<").split("\n")
        f.close()
        for line in textList:
            if 'resource-id="com.truecaller:id/title"' in line:
                items = line.split("\"")
                Data[number] = items[3]
        os.system(f"adb -s {device} shell input tap 800 225")
    return Data

def getNumbers(device="07586311CO072403"):
        '''Getting Numbers From Whatsapp Groups'''
        os.system(f"adb -s {device} shell am force-stop com.whatsapp.w4b")
        os.system(f"adb -s {device} shell monkey -p com.whatsapp.w4b -v 1")
        print("\n\n\t Open Group and Tap View all \n\n ")
        time.sleep(10)

        ns = []
        flag = 1
        while flag:
            #Taking UI Screenshot
            os.system(f"adb -s {device} shell uiautomator dump")
            os.system(f"adb -s {device} pull /sdcard/window_dump.xml")

            f = open("window_dump.xml", "r", encoding='utf8')
            lines = f.read().replace("><", ">\n<").split("\n")
            f.close()

            for line in lines:
                if "View past participants" in line:
                    flag = 0
                elif "com.whatsapp.w4b:id/name" in line :
                    numValue = line.split("\"")[3]
                    number01 = numValue.replace(" ", "")[2:]
                    if number01.isnumeric():
                        #append if number is not saved Use else for saved names
                        ns.append(numValue.replace(" ", "")[3:])
            os.system(f"adb -s {device} shell input swipe 550 1300 550 300 1000 ")
        return ns


if __name__ == "__main__":
    Contacts = getNames(getNumbers())
    print(Contacts)
    dataFile = open("Contacts.json", "w", encoding='utf8')
    result = json.dumps(Contacts)
    dataFile.write(result)
