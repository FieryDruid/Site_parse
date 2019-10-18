from django.http import HttpResponse
from list_org import SiteData_list
from habr import SiteData_habr
from django.shortcuts import render


def index(request):
    if request.method == "GET":
        site = request.GET.get("url")
        print(site)
        count = request.GET.get("c")
        print(count)
        if site:
            if "list-org.com" in site:
                list_object = SiteData_list(site)
                list_object.import_html()
                list_object.data_parse()
                data = list_object.return_data()
                print(data[0])
                context = {'Название компании': data[0], 'Руководитель' : data[1], 'Дата регистрации': data[2], 'Статус': data[3], 'ИНН / КПП': data[4], 'ОРГН': data[5]}
                return render(request, 'index_list.html', context = {'data': context})
        if count:
            habr_object = SiteData_habr(count)
            context = habr_object.dict_return()
            print(context)
            return render(request, 'index_habr.html', context={'data': context})
        else:
            return HttpResponse(status=400)

