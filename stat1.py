import pandas as pd

hr = pd.read_excel('comagic.xlsx')
#hr = pd.read_excel('report-call-01062019-14062019.xlsx')

all = 0
lost = 0
fully_lost = 0
good = 0
all_cc = 0
lost_cc = 0
all_not_wt = 0

cc_lost_clients = set()
wt_cc_lost_clients = set()
not_wt_cc_lost_clients = set()

answered_clients = set()
all_clients = set()


wt_all_cc = 0
wt_lost_cc = 0

not_wt_all_cc = 0
not_wt_lost_cc = 0



all_calls = []
times = []


hr['Дата и время']= pd.to_datetime(hr['Дата и время'])


for ind, call in hr.iterrows():

    is_fully_lost = call['Статус'] == 'Потерянный'
    all_clients.add(call['Номер абонента'])

    if not is_fully_lost:
        answered_clients.add(call['Номер абонента'])

#   if call['Тип'] != 'Звонок ВАТС': # пока не считаем автоперезвоны
#       continue

    all += 1
    if is_fully_lost:
        lost += 1



    op_str = call['Операции']

    if type(op_str) is str:
        operations = [s.strip() for s in op_str.split(',')]
    else:
        all -= 1
        continue

    cc_was = 'Колл-центр' in operations
    if cc_was:
        all_cc += 1

    cc_not_answer = False

    if operations[-1] == 'Колл-центр': #последняя операции колл-центр
        if (call['Причина завершения'] != 'Абонент разорвал соединение'
                and call['Статус'] == 'Потерянный'):
            cc_not_answer = True
    elif cc_was: # не в конце, значит точно не ответил
        cc_not_answer = True

    if cc_not_answer:
        lost_cc += 1
        cc_lost_clients.add(call['Номер абонента'])

    working_time = True

    calldt = call['Дата и время']

    time = 'рабочее'

    dm = calldt.strftime('%d.%m')
    if calldt.dayofweek in (5,6):
        working_time = False
        time = 'выходной'
    elif calldt.hour < 9 or calldt.hour >= 18:
        working_time = False
        time = 'нерабочее'

    times.append(time)

    if working_time:
        if cc_was:
            wt_all_cc += 1
        if cc_not_answer:
            wt_lost_cc += 1
            wt_cc_lost_clients.add(call['Номер абонента'])

    else:
        all_not_wt += 1
        if cc_was:
            not_wt_all_cc += 1
        if cc_not_answer:
            not_wt_lost_cc += 1
            not_wt_cc_lost_clients.add(call['Номер абонента'])

    call2 = dict(call)
    call2['time'] = time
    all_calls.append(call2)


fully_lost = len(all_clients - answered_clients)

cc_fully_lost = len(cc_lost_clients - answered_clients)
wt_cc_fully_lost = len(wt_cc_lost_clients - answered_clients)
not_wt_cc_fully_lost = len(not_wt_cc_lost_clients - answered_clients)

'''
print(f'Всего = {all}, Пропущено {lost} ({100*lost/all:.1f}%), так и не дозвонились: {fully_lost} ({100*fully_lost/all:.1f}%)')
print(f'Колл-центр всего шло звонков = {all_cc}, не отвечено {lost_cc} ({100*lost_cc/all_cc:.1f}%), так и не дозвонились: {cc_fully_lost} ({100*cc_fully_lost/all_cc:.1f}%)')
print(f'Колл-центр в рабочее время = {wt_all_cc}, не отвечено {wt_lost_cc} ({100*wt_lost_cc/wt_all_cc:.1f}%), так и не дозвонились: {wt_cc_fully_lost} ({100*wt_cc_fully_lost/wt_all_cc:.1f}%)')
print(f'Колл-центр в НЕ рабочее время = {not_wt_all_cc}, не отвечено {not_wt_lost_cc} ({100*not_wt_lost_cc/not_wt_all_cc:.1f}%), так и не дозвонились: {not_wt_cc_fully_lost} ({100*not_wt_cc_fully_lost/not_wt_all_cc:.1f}%)')
print(f'Всего в нерабочее время {all_not_wt} ({100*all_not_wt/all:.1f}%)')
'''