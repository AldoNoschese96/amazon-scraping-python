import json
#To Clear Your JSON Search Report DB
def clear_report():
    cleared = {}
    with open("./history/report.json" , "w") as f:
        try:
            json.dump(cleared, f)
        except:
            raise TypeError("Error While trying to write report")

clear_report()