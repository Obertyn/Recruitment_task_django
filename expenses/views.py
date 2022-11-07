from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_all, summary_per_year, summary_per_month, data_for_category_list
import datetime


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5
    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        def get_start_date(self):
            start_date = self.request.GET.get('start_date')
            return start_date

        def get_end_date(self):
            start_date = self.request.GET.get('end_date')
            return start_date
        start_date = get_start_date(self)
        end_date = get_end_date(self)

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            if name:
                queryset = queryset.filter(name__icontains=name)

        start_date2 = ''
        end_date2 = ''
        if(start_date):
            for i in ('%d-%m-%Y', '%d.%m.%Y', '%d/%m/%Y'):
                try:
                    start_date2 = datetime.datetime.strptime(start_date, i).date()
                except:  # obsługa błędu polegającego na tym, że użytkownik wpisze coś co nie jest datą
                    pass  # w takim przypadku wpisana wartość nie zostanie wzięta pod uwagę, przy wyszukiwaniu
                          # a text input zostanie wyzerowany, żeby użytkownik wiedział że popełnił błąd
        if(end_date):
            for i in ('%d-%m-%Y', '%d.%m.%Y', '%d/%m/%Y'):
                try:
                    end_date2 = datetime.datetime.strptime(end_date, i).date()
                except:
                    pass

        if (start_date2 != "" and end_date2 != ""):
            queryset = queryset.filter(date__range=[start_date2, end_date2])
        elif(start_date2 != ""):
            queryset = queryset.filter(date__range=[start_date2, "9000-01-01"])
            end_date = ""
        elif(end_date2 != ""):
            queryset = queryset.filter(date__range=["1000-01-01", end_date2])
            start_date = ""
        else:
            end_date = ""
            start_date = ""

        if end_date == None:
            end_date = ""

        if start_date == None:
            start_date = ""

        def get_sorting(self):
            select = self.request.GET.get('select')
            return select

        select = get_sorting(self)

        if (select == "sort_category_a"):
            queryset = queryset.order_by('category')
        if (select == "sort_category_d"):
            queryset = queryset.order_by('-category')
        if (select == "sort_date_a"):
            queryset = queryset.order_by('date')
        if (select == "sort_date_d"):
            queryset = queryset.order_by('-date')

        return super().get_context_data(
            sort_category_a="sort_category_a",
            form=form,
            end_date=end_date,
            start_date=start_date,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_all=summary_all(queryset),
            summary_per_year=summary_per_year(queryset),
            summary_per_month=summary_per_month(queryset),
            **kwargs,)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):

        return super().get_context_data(
            data_for_category_list=data_for_category_list,
            **kwargs,)
