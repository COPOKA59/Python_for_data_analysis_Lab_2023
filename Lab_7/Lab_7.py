import numpy as np
import pandas as pd

if __name__ == '__main__':
    # 0
    """
    Данная таблица содержит описание mcc-кодов транзакций.
    mcc_code – mcc-код транзакции;
    mcc_description — описание mcc-кода транзакции;
    """
    tr_mcc_codes = pd.read_csv('data/tr_mcc_codes.csv', encoding = 'utf-8', sep = ';')
    """
    Данная таблица содержит описание типов транзакций.
    tr_type – тип транзакции;
    tr_description — описание типа транзакции;
    """
    tr_types = pd.read_csv('data/tr_types.csv', encoding = 'utf-8', sep = ';')

    """
    Данная таблица содержит информацию по полу для части клиентов, для которых он известен. 
            Для остальных клиентов пол неизвестен.
    customer_id — идентификатор клиента;
    gender — пол клиента;
    """
    gender_train = pd.read_csv('data/gender_train.csv', encoding = 'utf-8', sep = ',')

    """
    Таблица содержит историю транзакций клиентов банка за один год и три месяца.
    customer_id — идентификатор клиента;
    tr_datetime — день и время совершения транзакции (дни нумеруются с начала данных);
    mcc_code — mcc-код транзакции;
    tr_type — тип транзакции;
    amount — сумма транзакции в условных единицах со знаком; 
            + — начисление средств клиенту (приходная транзакция), 
            - — списание средств (расходная транзакция);
    term_id — идентификатор терминала.
    """
    transactions = pd.read_csv('data/transactions.csv', encoding = 'utf-8', sep = ',', nrows=1000000)

    #print(transactions)

    # Task 5
    # В tr_types выберите произвольные 100 строк с помощью метода sample
    #       (указав при этом random_seed равный 242)
    print('Task 5')

    np.random.seed(242)
    # Выбор произвольных 100 строк
    tr_100 = tr_types.sample(100)
    print('Выбор произвольных 100 строк ->\n', tr_100)
    # В полученной на предыдущем этапе подвыборке найдите долю наблюдений
    #       (стобец tr_description), в которой содержится подстрока 'плата'
    #       (в любом регистре). (*)
    # .str.match() — используется для определения, соответствует ли каждая строка в базах данных данного объекта series регулярному выражению
    # 'плата' — выражение, по которому будет производится поиск
    # case=False — игнорирует изменения регистра
    tr_1 = tr_100['tr_description'][tr_100['tr_description'].str.match('плата', case=False)].count()/len(tr_100)
    print(f"\nДоля наблюдений, в которой содержится подстрока 'плата' ->\n{tr_1:.2f}")

    # Task 6
    # Для поля tr_type датафрейма transactions посчитайте частоту встречаемости
    #       всех типов транзакций tr_type в transactions.
    # .value_counts() — Возвращает ряд, содержащий частоту каждой отдельной строки в Dataframe
    print('\n\nTask 6')

    transaction_counts = transactions["tr_type"].value_counts()
    print('\nДля поля tr_type датафрейма transactions посчитайте частоту встречаемости'
          '\nвсех типов транзакций tr_type в transactions ->\n', transaction_counts)

    # Из перечисленных вариантов выберите те, которые попали в топ-5 транзакций
    #       по частоте встречаемости.
    # .head(5) — возвращает первые 5 значений
    transaction_counts = transaction_counts.head(5)
    mask = transaction_counts.index.to_list()
    transaction_5 = tr_types.loc[tr_types['tr_type'].isin(mask)]
    print('\nТранзакцие попавшие в топ 5 по встречаемости ->\n', transaction_5)

    # Выберите все верные пункты:
    # - 1) Выдача наличных в АТМ Сбербанк России
    # - 2) Комиссия за обслуживание ссудного счета
    # - 3) Списание по требованию
    # - 4) Оплата услуги. Банкоматы СБ РФ
    # - 5) Погашение кредита (в пределах одного филиала)
    # - 6) Покупка. POS ТУ СБ РФ
    # 1 4 6

    # Task 7
    # В датафрейме transactions задайте столбец customer_id в качестве индекса.
    print('\n\nTask 7')

    transactions.set_index('customer_id', inplace=True)

    # Выделите клиента с максимальной суммой транзакции (то есть с максимальным приходом на карту). (*)
    #max_amount = transactions['amount'].max()
    #print(f'Максимальная сумма транзакции ->\n{max_amount}')
    transactions_id_max = transactions['amount'].idxmax()
    print(f"Клиент с максимальной суммой транзакции ->\n{transactions_id_max}\n")

    transactions_id = transactions.loc[transactions_id_max]
    transactions_id['amount'] = transactions_id['amount'].abs()

    # Найдите у него наиболее часто встречающийся модуль суммы приходов/расходов. (**)
    print(f"Наиболее встречающийся модуль суммы транзакций ->\n"
                f"{transactions_id.pivot_table(index=['amount'], aggfunc='size').idxmax()}")

    # Выберите все верные пункты:
    # - 1) 1122957.89
    # - 2) 15721.41
    # - 3) 22459.16
    # - 4) 13475494.63
    # - 5) 107407.78
    # - 6) 65019.26
    # 3


    # Task 8
    # Найдите максимальную разницу между медианами суммы транзакций, посчитанными
    #       при заданных ниже условиях по полю amount из таблицы transactions (*):
    #   Медиана суммы транзакций;
    #   Медиана суммы транзакций по тем строкам, которые ни в одном из своих столбцов
    #       не содержат пустые значения;
    #   Медиана суммы транзакций по строкам, отсортированным по полю amount в порядке
    #       возрастания, и из которых удалены дублирующиеся по столбцам [mcc_code, tr_type]
    #       строки, причём при удалении соответстующих дублей остаются только последние из
    #       дублирующихся строк (keep='last').
    print('\n\nTask 8')

    # Медиана суммы транзакций
    median = transactions["amount"].median()
    print(f'\nМедиана суммы транзакций ->\n{median}')

    # Медиана суммы транзакций по тем строкам, которые ни в одном из своих столбцов не содержат пустые значения
    # .dropna() — Удаляет строки, в которых отсутствует хотя бы один элемент
    without_nan = transactions.dropna()
    median_no_nan = without_nan["amount"].median()
    print(f'Медиана суммы транзакций по тем строкам, которые ни в одном из своих столбцов не содержат пустые значения ->\n{median_no_nan}')

    # Медиана суммы транзакций по строкам, отсортированным по полю amount в порядке возрастания,
    sort = transactions.sort_values(by="amount")
    # и из которых удалены дублирующиеся по столбцам [mcc_code, tr_type] строки,
    # причём при удалении соответствующих дублей остаются только последние из дублирующихся строк (keep='last')
    # .drop_duplicates — возвращает DataFrame с удаленными повторяющимися строками (по умолчанию по всем столбцам)
    sorted_drop = sort.drop_duplicates(subset=["mcc_code", "tr_type"], keep="last")
    sort_median = sorted_drop["amount"].median()

    print(f'Медиана суммы транзакций по строкам, отсортированным по полю amount в порядке возрастания ->\n{sort_median}')

    # Найдите максимальную разницу между медианами суммы транзакций
    dif = np.ptp([median, median_no_nan, sort_median])
    print(f'Максимальная разницу между медианами суммы транзакций: {dif:.2f}')

