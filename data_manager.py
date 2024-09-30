import os.path
import csv
import json
import time
import shutil


class data_manager:
    def __init__(self):
        class basics:
            def __init__(self):
                self.class_path = "data/class"
                self.event_path = "data/event"
                self.match_path = "data/match"
                self.class_data = "data/ClassData.json"
                self.event_data = "data/EventData.json"
                if not os.path.exists(self.class_path):
                    os.makedirs(self.class_path)
                if not os.path.exists(self.event_path):
                    os.makedirs(self.event_path)
                if not os.path.exists(self.match_path):
                    os.makedirs(self.match_path)
                if not os.path.exists(self.class_data):
                    with open(self.class_data, 'w') as file:
                        json.dump({}, file)
                if not os.path.exists(self.event_data):
                    with open(self.event_data, 'w') as file:
                        json.dump({}, file)

            def find_class_data(self):
                with open(self.class_data, 'r') as file:
                    data = json.load(file)
                return data

            def save_class_data(self, data):
                with open(self.class_data, 'w') as file:
                    json.dump(data, file, indent=4)

            def create_class(self, class_name: str, grade: str):
                path = f"{self.class_path}/{class_name}.csv"
                headers = ["Name", "Event1", "Event2"]
                with open(path, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()  # 写入表头
                data = self.find_class_data()
                data[class_name] = grade
                self.save_class_data(data)

            def create_event(self, event_name: str, grade: str, big_event: str, type: str):
                path1 = f"{self.event_path}/{event_name}.csv"
                headers = ["Class", "Name", "Match", "Status", "Result", "Score"]
                with open(path1, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()  # 写入表头
                path2 = f"{self.event_path}/{event_name}.json"
                data = {"grade": grade, "big_event": big_event, "type": type}
                with open(path2, 'w') as file:
                    json.dump(data, file, indent=4)

            def about_event(self,event:str):
                path = f"{self.event_path}/{event}.json"
                with open(path, 'r') as file:
                    data = json.load(file)
                return data

            def find_class(self, class_name: str):
                path = f"{self.class_path}/{class_name}.csv"
                # if not os.path.exists(path):
                #    return []
                ClassData = []
                with open(path, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        ClassData.append(dict(row))
                return ClassData

            def sava_class(self, class_name: str, data: list):
                path = f"{self.class_path}/{class_name}.csv"
                headers = ["Name", "Event1", "Event2"]
                clear_data = sorted(data, key=lambda x: (x['Name'], x['Event1'], x['Event2']))
                with open(path, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()  # 写入表头
                    writer.writerows(clear_data)  # 写入数据行

            def find_event(self, event_name: str):
                path = f"{self.event_path}/{event_name}.csv"
                # if not os.path.exists(path):
                #    return []
                EventData = []
                with open(path, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        EventData.append(dict(row))
                return EventData

            def save_event(self, event_name: str, data: list):
                path = f"{self.event_path}/{event_name}.csv"
                headers = ["Class", "Name", "Match", "Status", "Result", "Score"]
                clear_data = sorted(data, key=lambda x: (
                    x['Class'], x['Name'], int(x['Match']), x['Status'], int(x['Score'])))
                with open(path, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()  # 写入表头
                    writer.writerows(clear_data)  # 写入数据行

            def find_match(self, match_name: str):
                path = f"{self.match_path}/{match_name}.csv"
                # if not os.path.exists(path):
                #    return []
                MatchData = []
                with open(path, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        MatchData.append(dict(row))
                return MatchData

            def save_match(self, match_name: str, data: list):
                up_path = f"{self.match_path}/{match_name}"
                path = f"{up_path}/{match_name}.csv"
                headers = ["Class", "Name", "serial number"]
                clear_data = sorted(data, key=lambda x: x['serial number'])
                if not os.path.exists(up_path):
                    os.makedirs(up_path)
                with open(path, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()  # 写入表头
                    writer.writerows(clear_data)  # 写入数据行

            def all_class(self):
                names = []
                for root, dirs, files in os.walk(self.class_path):
                    for file in files:
                        if file.endswith('.csv'):
                            names.append(os.path.splitext(file)[0])
                return names

            def all_event(self):
                names = []
                for root, dirs, files in os.walk(self.event_path):
                    for file in files:
                        if file.endswith('.csv'):
                            names.append(os.path.splitext(file)[0])
                return names

            def all_match(self):
                folders = [f for f in os.listdir(self.match_path) if os.path.isdir(os.path.join(self.match_path, f))]
                return folders

        self.basics = basics()
        ########## 基础方法完成 ##########
        self.my_data_path = 'data/data.json'
        if os.path.exists(self.my_data_path):
            with open(self.my_data_path, 'r') as json_file:
                my_data = json.load(json_file)
            self.count_match = my_data["count_match"]
        else:
            self.count_match = 0

    def save_system_data(self):
        data = {"count_match": self.count_match}
        with open(self.my_data_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)  # 使用indent参数来格式化输出

    def join(self, class_name: str, student_name: str, event: str):
        class_data = self.basics.find_class(class_name)
        flag = False
        for student in class_data:
            if student["Name"] == student_name:
                if student["Event1"] == event or student["Event2"] == event:
                    return "学生已参赛"
                if student["Event2"] != "":
                    return "学生已满赛"
                if student["Event2"] == "":
                    student["Event2"] = event
                    flag = True
        if not flag:
            class_data.append({"Name": student_name, "Event1": event, "Event2": None})
        self.basics.sava_class(class_name, class_data)

        # 完成班级更新

        event_data = self.basics.find_event(event)
        event_data.append(
            {"Class": class_name, "Name": student_name, "Match": -1, "Status": "未比赛", "Result": 0,
             "Score": 0})
        self.basics.save_event(event, event_data)

        # 完成比赛更新
        return "SUCCESS"

    def divide_match(self, event, max_student):
        def find(List, Class, Name):
            for i in range(len(List)):
                if List[i]["Class"] == Class and List[i]["Name"] == Name:
                    return i

        event_data = self.basics.find_event(event)
        clear_student = [{'Class': data['Class'], 'Name': data['Name']} for data in event_data]
        all_match = [clear_student[i:i + max_student] for i in range(0, len(clear_student), max_student)]
        for match in all_match:
            # 使用列表推导式和enumerate来更新每个字典的"serial number"键
            clear_match = [
                {**d, 'serial number': i} for i, d in enumerate(match)
            ]
            self.count_match += 1
            self.save_system_data()
            self.basics.save_match(self.count_match, clear_match)
            for student in match:
                event_data[find(event_data, student["Class"], student["Name"])]["Match"] = self.count_match
        self.basics.save_event(event, event_data)

    def check_in(self, class_name, student_name, event):
        event_data = self.basics.find_event(event)
        for data in event_data:
            if data["Class"] == class_name and data["Name"] == student_name:
                data["Status"] = "待比赛"
        self.basics.save_event(event, event_data)

    def record_result(self, class_name, student_name, event, result):
        event_data = self.basics.find_event(event)
        for data in event_data:
            if data["Class"] == class_name and data["Name"] == student_name:
                if data["Status"] != "待比赛":
                    return "学生状态错误"
                data["Result"] = result
        self.basics.save_event(event, event_data)

    def record_score(self, class_name, student_name, event, score):
        event_data = self.basics.find_event(event)
        for data in event_data:
            if data["Class"] == class_name and data["Name"] == student_name:
                if data["Status"] != "待比赛":
                    return "学生状态错误"
                data["Score"] = score
        self.basics.save_event(event, event_data)

    def record_all(self, class_name, student_name, event, status, result, score):
        event_data = self.basics.find_event(event)
        for data in event_data:
            if data["Class"] == class_name and data["Name"] == student_name:
                data["Status"] = status
                data["Result"] = result
                data["Score"] = score
        self.basics.save_event(event, event_data)

    def find_student(self,event,class_name,name):
        event_data = self.basics.find_event(event)
        for data in event_data:
            if data["Class"] == class_name and data["Name"] == name:
                return data


def fire():
    shutil.rmtree("data")
    time.sleep(1)
    os.makedirs("data")


if __name__ == "__main__":
    fire()
    # 学生比赛流程：报名-分配场次-检录-比赛-查询成绩
    data_manager = data_manager()
    # print(data_manager.basics.find_class("1"))
    # data_manager.basics.sava_class("912",[{"Name":"JUNU","Event1":"九年级男子实心球","Event2":None}])
    # print(data_manager.basics.find_class("912"))
    # print(data_manager.join(912, "JUNU", "九年级男子实心球"))
    # data_manager.check_in(912, "JUNU", "九年级男子实心球")
    # print(data_manager.basics.find_event("九年级男子实心球"))

    # for i in range(100):
    #    data_manager.join("912", str(i), "九年级男子实心球")
    # a = data_manager.divide_match("九年级男子实心球", 9)

    for i in range(701, 710 + 1):
        data_manager.basics.create_class(str(i), "七年级")
    for i in range(801, 812 + 1):
        data_manager.basics.create_class(str(i), "八年级")
    for i in range(901, 913 + 1):
        data_manager.basics.create_class(str(i), "九年级")

    all1 = ["5KG铅球", "10KG铅球"]
    all2 = ["100米", "400米", "800米", "1000米", "1500米", "4x100米"]
    for i in all1:
        for j in ["七", "八", "九"]:
            data_manager.basics.create_event(f"{j}年级男子{i}", f"{j}年级", i, "田赛")
            data_manager.basics.create_event(f"{j}年级女子{i}", f"{j}年级", i, "田赛")
    for i in all2:
        for j in ["七", "八", "九"]:
            data_manager.basics.create_event(f"{j}年级男子{i}", f"{j}年级", i, "径赛")
            data_manager.basics.create_event(f"{j}年级女子{i}", f"{j}年级", i, "径赛")
