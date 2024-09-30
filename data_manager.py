import csv
import json
import os.path
import shutil
import time
import uuid


def ff(func):
    def wrapper(*args, **kwargs):
        expected_types = func.__annotations__

        # 处理普通参数
        new_args = []
        for i, (arg, expected_type) in enumerate(zip(args[1:], expected_types.values())):  # 跳过 'self' 参数
            if not isinstance(arg, expected_type):
                arg = expected_type(arg)
            new_args.append(arg)

        # 处理关键字参数
        new_kwargs = {}
        for key, value in kwargs.items():
            expected_type = expected_types[key]
            if not isinstance(value, expected_type):
                value = expected_type(value)
            new_kwargs[key] = value

        # 调用原始函数
        return func(args[0], *new_args, **new_kwargs)

    return wrapper


format = True


def writeJson(JsonName: str, data: dict):  # write json
    # 将数据写入JSON文件
    with open(JsonName, "w") as write_file:
        if format:
            json.dump(data, write_file, indent=4)  # 使用indent参数来格式化输出
        else:
            json.dump(data, write_file)


def readJson(JsonName: str):  # read json
    with open(JsonName, "r") as read_file:
        loaded_data = json.load(read_file)
    return loaded_data


def writeCsv(CsvName: str, data: list):
    # 打开一个CSV文件用于写入
    with open(CsvName, "w", newline='') as write_file:
        writer = csv.writer(write_file)

        # 将数据写入CSV文件
        for row in data:
            writer.writerow(row)


def readCsv(CsvName: str):
    # 打开一个CSV文件用于读取
    with open(CsvName, "r", newline='') as read_file:
        reader = csv.reader(read_file)
        # 读取CSV文件的所有行
        data = [row for row in reader]
    return data


class data_manager:
    def __init__(self, Race_Name):
        class basics:
            def __init__(self, Race_Name):
                self.student_path = f"data/{Race_Name}/student"
                self.grade_path = f"data/{Race_Name}/grade"
                self.class_path = f"data/{Race_Name}/class"
                self.event_path = f"data/{Race_Name}/event"
                self.match_path = f"data/{Race_Name}/match"
                if not os.path.exists(self.student_path):
                    os.makedirs(self.student_path)
                if not os.path.exists(self.grade_path):
                    os.makedirs(self.grade_path)
                if not os.path.exists(self.class_path):
                    os.makedirs(self.class_path)
                if not os.path.exists(self.event_path):
                    os.makedirs(self.event_path)
                if not os.path.exists(self.match_path):
                    os.makedirs(self.match_path)

            ### 年级管理 ###
            def all_grade(self):
                folders = [f for f in os.listdir(self.grade_path) if os.path.isdir(os.path.join(self.grade_path, f))]
                return folders

            @ff
            def create_grade(self, Grade: str):
                path = os.path.join(self.grade_path, f"{Grade}.json")
                writeJson(path, {"Class": []})

            @ff
            def get_grade(self, Grade: str):
                path = os.path.join(self.grade_path, f"{Grade}.json")
                return readJson(path)["Class"]

            @ff
            def delete_grade(self, Grade: str):
                path = os.path.join(self.grade_path, Grade)
                shutil.rmtree(path)

            ### 班级管理 ###
            @ff
            def create_class(self, Class: str, Leader: str = "", Student: list = []):
                path = os.path.join(self.class_path, f"{Class}.json")
                writeJson(path, {"Leader": Leader, "Student": Student})

            @ff
            def get_class(self, Class: str):
                path = os.path.join(self.class_path, f"{Class}.json")
                return readJson(path)

            @ff
            def delete_class(self, Class: str):
                path = os.path.join(self.class_path, f"{Class}.json")
                os.remove(path)

            ### 学生管理 ###
            @ff
            def create_student(self, Name:str):
                Id = str(uuid.uuid4())
                path = os.path.join(self.student_path, f"{Id}.json")
                writeJson(path, {"Name": Name})
                return Id

            @ff
            def get_student(self, Id: str):
                path = os.path.join(self.student_path, f"{Id}.json")
                return readJson(path)

            @ff
            def delete_student(self, Id: str):
                path = os.path.join(self.student_path, f"{Id}.json")
                os.remove(path)


            ### 项目管理 ###
            def all_event(self):
                folders = [f for f in os.listdir(self.event_path) if os.path.isdir(os.path.join(self.event_path, f))]
                return folders

            @ff
            def create_event(self, Event: str, config: dict):
                required_keys = {'组别', 'key2'}
                missing_keys = required_keys - set(config.keys())
                if missing_keys:
                    raise KeyError(f"Missing required keys in config: {missing_keys}")

            @ff
            def get_event(self, Event: str):
                path = os.path.join(self.student_path, f"{Id}.json")
                return readJson(path)

            @ff
            def delete_event(self, Event: str):
                path = os.path.join(self.student_path, f"{Id}.json")
                os.remove(path)

            ### 场次管理 ###
            def all_match(self):
                folders = [f for f in os.listdir(self.match_path) if os.path.isdir(os.path.join(self.match_path, f))]
                return folders

        self.basics = basics(Race_Name)
        ########## 基础方法完成 ##########

    def save_system_data(self):
        data = {"count_match": self.count_match}
        writeJson(self.my_data_path, data)

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

    def find_student(self, event, class_name, name):
        event_data = self.basics.find_event(event)
        for data in event_data:
            if data["Class"] == class_name and data["Name"] == name:
                return data


def fire():
    if os.path.exists("data"):
        shutil.rmtree("data")
    time.sleep(1)
    os.makedirs("data")


if __name__ == "__main__":
    fire()
    # 学生比赛流程：报名-分配场次-检录-比赛-查询成绩
    data_manager = data_manager("1-某中学田径运动会（示例）")
    data_manager.basics.create_grade("七年级")
    data_manager.basics.create_grade("八年级")
    data_manager.basics.create_grade("九年级")
    for i in range(701, 710 + 1):
        std=[]
        for j in range(1,11):
            std.append(data_manager.basics.create_student(str(i)+str(j)))
        data_manager.basics.create_class(i,Student=std)
    for i in range(801, 812 + 1):
        std=[]
        for j in range(1,11):
            std.append(data_manager.basics.create_student(str(i)+str(j)))
        data_manager.basics.create_class(i,Student=std)
    for i in range(901, 913 + 1):
        std=[]
        for j in range(1,11):
            std.append(data_manager.basics.create_student(str(i)+str(j)))
        data_manager.basics.create_class(i,Student=std)
    exit()
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
