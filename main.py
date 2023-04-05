import stepbrother
import atomic_energy
from datetime import datetime,timedelta



def all_parse():
    final_dict = {**stepbrother.parse(), **atomic_energy.parse()}
    printing_info = []
    for sources in  final_dict:
        printing_info.append(sources)
        for dates in final_dict[sources]:
            if datetime.strptime(dates, '%d.%m.%Y') > datetime.today() - timedelta(days=3):
                printing_info.append(final_dict[sources][dates])
    return printing_info




if __name__ == '__main__':
    print (all_parse())