from stat1 import all_calls
from pprint import pprint


def reverse(a):
    a2 = []
    for i in range(len(a) - 1, -1, -1):
        a2.append(a[i])
    return a2



all_calls = reverse(all_calls)
calls = []

for i in range(len(all_calls)):

    if all_calls[i]['Тип'] == 'Звонок ВАТС' and all_calls[i]['Статус'] == 'Потерянный':

        j = i
        b = []
        b.append(all_calls[i])

        while True:
            if len(b) >= 6 or (len(b) > 0 and b[-1]['Статус'] == 'Принятый') or j == len(all_calls):
                break
            if all_calls[j]['Тип'] == 'Автоперезвон по пропущенным' and all_calls[i]['Номер абонента'] == all_calls[j]['Номер абонента']:
                b.append(all_calls[j])
            j += 1

        calls.append(b)

'''
print(len(calls))
pprint(calls[0])
print()
pprint(calls[100])
'''


worktime = []
offhours = []
weekends = []

for call in calls:
    if call[0]['time'] == 'рабочее':
        worktime.append(call)
    elif call[0]['time'] == 'нерабочее':
        offhours.append(call)
    elif call[0]['time'] == 'выходной':
        weekends.append(call)


def statistic(a):

    stat = [0, 0, 0, 0, 0, 0]
    lost = 0

    for i in a:
        f = 0
        for j in range(len(i)):
            if i[j]['Статус'] == 'Принятый':
                stat[j] += 1
                f = 1
                break
        if f == 0:
            lost += 1

    return [stat, lost]


worktime_stat, worktime_lost = statistic(worktime)
offhours_stat, offhours_lost = statistic(offhours)
weekends_stat, weekends_lost = statistic(weekends)

print(f'В рабочее время: {len(worktime)}')
print(f'1-ая попытка - {worktime_stat[1]}')
print(f'2-ая попытка - {worktime_stat[2]}')
print(f'3-я попытка - {worktime_stat[3]}')
print(f'4-ая попытка - {worktime_stat[4]}')
print(f'5-ая попытка - {worktime_stat[5]}')
print(f'Потеряно - {worktime_lost}')


print()

print(f'В нерабочее время: {len(offhours)}')
print(f'1-ая попытка - {offhours_stat[1]}')
print(f'2-ая попытка - {offhours_stat[2]}')
print(f'3-я попытка - {offhours_stat[3]}')
print(f'4-ая попытка - {offhours_stat[4]}')
print(f'5-ая попытка - {offhours_stat[5]}')
print(f'Потеряно - {offhours_lost}')

print()

print(f'В выходные: {len(weekends)}')
print(f'1-ая попытка - {weekends_stat[1]}')
print(f'2-ая попытка - {weekends_stat[2]}')
print(f'3-я попытка - {weekends_stat[3]}')
print(f'4-ая попытка - {weekends_stat[4]}')
print(f'5-ая попытка - {weekends_stat[5]}')
print(f'Потеряно - {weekends_lost}')

print()

print(f'Всего: {len(worktime+offhours+weekends)}')
print(f'1-ая попытка - {worktime_stat[1] + offhours_stat[1] + weekends_stat[1]}')
print(f'2-ая попытка - {worktime_stat[2] + offhours_stat[2] + weekends_stat[2]}')
print(f'3-я попытка - {worktime_stat[3] + offhours_stat[3] + weekends_stat[3]}')
print(f'4-ая попытка - {worktime_stat[4] + offhours_stat[4] + weekends_stat[4]}')
print(f'5-ая попытка - {worktime_stat[5] + offhours_stat[5] + weekends_stat[5]}')
print(f'Потеряно - {worktime_lost + offhours_lost + weekends_lost}')

'''
[[0, 137, 21, 8, 0, 1], 119]
[[0, 6, 5, 3, 6, 4], 153]
[[0, 24, 16, 6, 8, 3], 142]
'''