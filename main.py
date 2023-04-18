import stepbrother
import atomic_energy
from datetime import datetime,timedelta
import json
import schedule, time

def all_parse():
    final_dict = stepbrother.parse()
    for key in final_dict:
        if atomic_energy.parse().get(key, "None") != "None":
            for i in range(0,len(atomic_energy.parse()[key])):
                final_dict[key].append(atomic_energy.parse()[key][i])
        else:
            pass
    with open('news', "w", encoding="utf-8") as file:
        json.dump(final_dict, file)

def display():
    with open('news', "r", encoding="utf-8") as file:
        final_dict = json.load(file)
        print(final_dict)
        printing_info = []
        for dates in final_dict:
            if datetime.strptime(dates, '%d.%m.%Y') > datetime.today() - timedelta(days=3):
                printing_info.append(dates)
                if type(final_dict[dates]) == list:
                    for news in final_dict[dates]:
                        for key, value in news.items():
                            printing_info.append(key +" \n " + value)
                else:
                    printing_info.append(final_dict[dates])

    return final_dict




if __name__ == '__main__':
    all_parse()
    print (display())