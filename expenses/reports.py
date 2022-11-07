from collections import OrderedDict
from django.db.models import Sum, Value, Count
from django.db.models.functions import Coalesce
from django.db.models import CharField
from .models import Expense, Category

def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def summary_all(queryset):
    summary = queryset.aggregate(suma=Sum('amount'))
    print(summary)
    try:
        summary = round(summary['suma'], 2)
    except:  # obsługa błędu występującego gdy lista jest pusta
        summary = 0
    return summary


def summary_per_month(queryset):
    list1 = queryset.values('date__year', 'date__month').annotate(s=Sum('amount'))
    list1 = list(list1)
    summary_month = [[""]*2 for i in range(len(list1))]
    for j in range(len(list1)):
        summary_month[j][0] = str(list1[j]['date__month'])+"/"+str(list1[j]['date__year'])
    for j in range(len(list1)):
        summary_month[j][1] = list1[j]['s']
    return summary_month


def summary_per_year(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(aaaaa=Coalesce('date__year', Value('-'), output_field=CharField()))
        .order_by()
        .values('aaaaa')
        .annotate(s=Sum('amount'))
        .values_list('aaaaa', 's')
    ))


def data_for_category_list():

    data = Expense.objects.all()
    data = (data
            .annotate(categoryid=Coalesce('category__id', Value('-'), output_field=CharField()))
            .order_by('category__name')
            .values('categoryid')
            .annotate(s=Count('category'))
            .values_list('categoryid', 's'))
    count_without_count0 = [0] * len(data)
    id_without_count0 = [0] * len(data)
    for i in range(len(data)):
        count_without_count0[i] = data[i][1]
    for i in range(len(data)):
        id_without_count0[i] = data[i][0]

    data = Category.objects.all()
    data = (data.values('name'))
    data = list(data)
    # name_list i id_list są potrzebne do wyświetlenia danych w kolumnach "name" i "actions"
    name_list = [0] * len(data)
    for i in range(len(data)):
        name_list[i] = data[i]['name']
    data = Category.objects.all()
    data = (data.values('id'))
    data = list(data)
    id_list = [0] * len(data)
    for i in range(len(data)):
        id_list[i] = data[i]['id']

    count_list = []
    x = 0
    # w bazie z wydatkami nie znajdują się kategorię z przedmiotami, których nigdy nie zakupiono (np. transport)
    # powoduje to, że lista z sumą wydatków jest krótsza - nie zawiera wartości z zerem, w związku z tym,
    # powiększam listę z sumą wydatków, o kategorie z ilością zakupionych przedmiotów równą 0
    for i in range(len(id_list)):
        if id_list[i] in id_without_count0:
            count_list.append(count_without_count0[x])
            x = x + 1
        else:
            count_list.append(0)
    # łączę wszystkie 3 listy ze sobą
    data_for_category_list = [[None] * 3 for i in range(len(name_list))]
    for i in range(len(name_list)):
        data_for_category_list[i][0] = name_list[i]
        data_for_category_list[i][1] = count_list[i]
        data_for_category_list[i][2] = id_list[i]

    return data_for_category_list
