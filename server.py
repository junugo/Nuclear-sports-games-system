import os
import uuid
from typing import List

import pandas as pd
import uvicorn
from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse

import data_manager
import excel_maker

app = FastAPI()
data_manager = data_manager.data_manager()
Export = excel_maker.Export()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/guest/{page_name}", response_class=HTMLResponse)
async def guest(page_name: str):
    # 通过路径参数指定页面名称，读取对应的 HTML 文件内容并返回
    if "." not in page_name:
        page_name += ".html"
    file_path = f"website/guest/{page_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        # 如果文件不存在，跳转至欢迎页面
        return RedirectResponse(url="/")


@app.get("/manager/{page_name}", response_class=HTMLResponse)
async def manager(page_name: str):
    # 通过路径参数指定页面名称，读取对应的 HTML 文件内容并返回
    if "." not in page_name:
        page_name += ".html"
    file_path = f"website/manager/{page_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        # 如果文件不存在，返回一个简单的错误页面
        return FileResponse("website/Error.html")


@app.get("/api/manager_page")
async def manager_page():
    return [{"Name": "参赛", "Address": "./join"},
            {"Name": "检录", "Address": "./check"},
            {"Name": "记录", "Address": "./record"},
            {"Name": "修改", "Address": "./edit"},
            {"Name": "查询", "Address": "./query"},
            ]


@app.get("/api/all_class")
async def all_class():
    return data_manager.basics.all_class()


@app.get("/api/all_event")
async def all_event():
    return data_manager.basics.all_event()


@app.get("/api/all_match")
async def all_match():
    return data_manager.basics.all_match()


@app.get("/api/all_class")
async def all_class():
    return data_manager.basics.all_class()


@app.get("/api/all_grade")
async def all_grade():
    grade = []
    all_class = data_manager.basics.all_class()
    data = data_manager.basics.find_class_data()
    for i in all_class:
        if data[i] not in grade:
            grade.append(data[i])
    return grade


@app.get("/api/join/{class_name}/{name}/{event}")
async def join(class_name: str, name: str, event: str):
    return data_manager.join(class_name, name, event)


@app.post("/api/quickly_join")
async def quickly_join(file: bytes = File(...)):
    path = "Temp/up.xlsx"
    with open(path, "wb") as f:
        f.write(file)
    # 读取 Excel 文件
    df = pd.read_excel(path)
    # 将 DataFrame 转换为列表
    data_list = df.values
    print(data_list)
    for student in data_list:
        data_manager.join(str(student[0]), str(student[1]), str(student[2]))
    return "File uploaded successfully."


@app.get("/api/find_event/{event}")
async def find_event(event: str):
    return data_manager.basics.find_event(event)


@app.get("/api/find_class/{class_name}")
async def find_class(class_name: str):
    data = data_manager.basics.find_class(class_name)
    out = []
    for student in data:
        my_data = data_manager.find_student(student["Event1"], class_name, student["Name"])
        out.append({"Class": class_name, "Name": student["Name"], "Event": student["Event1"], "Match": my_data["Match"],
                    "Status": my_data["Status"], "Result": my_data["Result"], "Score": my_data["Score"]})
        if student["Event2"] != "":
            my_data = data_manager.find_student(student["Event2"], class_name, student["Name"])
            out.append(
                {"Class": class_name, "Name": student["Name"], "Event": student["Event2"], "Result": my_data["Result"],
                 "Score": my_data["Score"]})
    return out


@app.get("/api/event_type/{event}")
async def event_type(event: str):
    return data_manager.basics.about_event(event)["type"]


@app.get("/api/check/{class_name}/{name}/{event}")
async def check(class_name: str, name: str, event: str):
    data_manager.check_in(class_name, name, event)


# @app.get("/api/{class_name}/{name}/{event}")
# async def check(class_name:str,name:str,event:str):
#     data_manager.check_in(class_name,name,event)

@app.post("/api/update_event/{event}")
async def create_item(event: str, item: List[dict]):
    for student in item:
        data_manager.record_all(student["Class"], student["Name"], event, student["Status"], student["Result"],
                                student["Score"])


@app.get("/api/query_event/{event}")
async def query_event(event: str):
    uuid_str = uuid.uuid4()
    path = f"Temp/{uuid_str}.xlsx"
    data = await find_event(event)
    top = ["Class", "Name", "Match", "Result", "Score"]
    Export.export_excel(data, path, top)
    return FileResponse(path)


@app.get("/api/query_class/{class_name}")
async def query_class(class_name: str):
    uuid_str = uuid.uuid4()
    path = f"Temp/{uuid_str}.xlsx"
    data = await find_class(class_name)
    top = ["Class", "Name", "Match", "Result", "Score"]
    Export.export_excel(data, path, top)
    return FileResponse(path)


@app.get("/{page_name}", response_class=HTMLResponse)
async def main(page_name: str):
    # 通过路径参数指定页面名称，读取对应的 HTML 文件内容并返回
    if "." not in page_name:
        page_name += ".html"
    file_path = f"website/{page_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        # 如果文件不存在，返回一个简单的错误页面
        return FileResponse("website/Error.html")


@app.get("/", response_class=HTMLResponse)
async def welcome():
    return FileResponse("website/index.html")


if __name__ == "__main__":
    uvicorn.run(app="server:app", host="127.0.0.1", port=80, reload=True)
    # 参数	        作用

    # app	        运行的 py 文件:FastAPI 实例对象
    # host	        访问url，默认 127.0.0.1
    # port	        访问端口，默认 8080
    # reload	        热更新，有内容修改自动重启服务器
    # debug	        同 reload
    # reload_dirs	设置需要 reload 的目录，List[str] 类型
    # log_level	    设置日志级别，默认 info
