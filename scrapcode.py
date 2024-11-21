# dictofdict = {}
# dictofdict["example"] = {"price": "hello", "date": "yello"}
# dictofdict["example2222"] = {"price": "hello", "date": "yello"}
# # print(dictofdict)
# for dict in dictofdict:
#     print(dict, dictofdict[dict])

from datetime import date, timedelta

# x = date(2020, 1, 1)
# print(x)
# x = str(x)
# print(x)
# parts = x.split("-")
# x = date(int(parts[0]), int(parts[1]), int(parts[2]))
# print(x)

# sdate = date(2020, 1, 1)
# edate = date(2020, 1, 4)
# print(
#     [sdate + timedelta(days=x) for x in range((edate + timedelta(days=1) - sdate).days)]
# )

# with open("report.txt", "w") as f:
#     for dict in dictofdict:
#         print(dict, dictofdict[dict], file=f)

{
    "D:\\Coding\\expensescript\\example1.png": {},
    "D:\\Coding\\expensescript\\example2.png": {
        "date": datetime.date(2024, 11, 21),
        "receiptTotal": 44,
        "mealType": 0,
    },
}
