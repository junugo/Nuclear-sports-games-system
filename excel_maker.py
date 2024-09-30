
import pandas as pd
class Export:
    @classmethod
    def export_excel(cls, data,file,order):
        with pd.ExcelWriter(file) as writer:
            pf_failed = cls.format_excel(data,order)
            pf_failed.to_excel(writer, sheet_name="Sheet1")
            writer._save()  # 保存表格

    @classmethod
    def format_excel(cls, export_data: list,order):
        columns_map = {
            "Grade": "年级",
            "Class": "班级",
            "Name": "名称",
            "Event": "比赛项目",
            "Match": "场次",
            "Status": "状态",
            "Result": "成绩",
            "Score": "得分",
        }  # 将列名替换为中文
        pf = pd.DataFrame(list(export_data))  # 将字典列表转换为DataFrame
        pf = pf[order]
        pf.rename(columns=columns_map, inplace=True)
        pf.fillna(" ", inplace=True)  # 替换空单元格
        return pf