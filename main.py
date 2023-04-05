import stepbrother
import atomic_energy
from datetime import datetime,timedelta
import json
import schedule, time

def all_parse():
    final_dict = {**stepbrother.parse(), **atomic_energy.parse()}
    with open('news', "w", encoding="utf-8") as file:
        json.dump(final_dict, file)

def display():
    with open('news', "r", encoding="utf-8") as file:
        final_dict = json.load(file)
        printing_info = []
        print(final_dict)
        for sources in  final_dict:
            printing_info.append(sources)
            for dates in final_dict[sources]:
                if datetime.strptime(dates, '%d.%m.%Y') > datetime.today() - timedelta(days=3):
                    printing_info.append(dates)
                    if type(final_dict[sources][dates]) == list:
                        for news in final_dict[sources][dates]:
                            for key, value in news.items():
                                printing_info.append(key +" \n " + value)
                    else:
                        printing_info.append(final_dict[sources][dates])

    return printing_info




if __name__ == '__main__':
    print (display())