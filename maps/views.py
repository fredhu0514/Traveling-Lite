from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from maps import TimeMap, one_path_algo, clustering
# Create your views here.

# Robots.txt for crawler engines
def robots(request):
    return render(request, "robots.txt")
def err_404(request):
    return render(request, "err_404.html")

def gaodeMap(request):
    return render(request, "map.html", {
        'FUNC' : 0
    })

def test(request):
    return render(request, "test.html", {
        'FUNC' : 0
    }) #测试
def tested(request):
    FUNC_indicator = [0]
    if request.method == 'POST':
        long_str = request.POST.get('positionsToReturn')
        lst_of_loc_str = [(str + '}') for str in long_str.split('}')]
        lst_of_loc_str.pop()
        lst_of_loc = [eval(str) for str in lst_of_loc_str]
        print(lst_of_loc)
        axes = [loc["location"] for loc in lst_of_loc]
        print(axes)
        a = TimeMap.TimeMap()
        time_list, guide_list = a.timeList(axes)
        print(time_list)
        cluster = request.POST.get('cluster')
        cluster = eval(cluster)
        if cluster == 0:
            FUNC_indicator[0] = 1
            paths = one_path_algo.one_path_algo.shortest_path(time_list)
            guides = []
            for i in range(len(paths[0]) - 1):
                guides.append(guide_list[paths[0][i]][paths[0][i + 1]])
            print(paths)
        else:
            FUNC_indicator[0] = 2
            paths = clustering.cluster.clustering(time_list, cluster)
            print(paths)
            # locs = [[lst_of_loc[i] for i in group] for group in paths.values()]
            try:
                tempAstr = [x["location"] for x in lst_of_loc]
                locs = []
                error_for_clustering = False
                for str in tempAstr:
                    str_lst_temp = str.split(',')
                    if len(str_lst_temp) == 2:
                        int_lst_temp = [eval(str_lst_temp[0]), eval(str_lst_temp[1])]
                        locs.append(int_lst_temp)
                    else:
                        error_for_clustering = True
                        break
                if error_for_clustering:
                    FUNC_indicator[0] = -1
                    print("高德地图location数值对长度不为2。file: view.py line 47-56")
            except:
                FUNC_indicator[0] = -1
                print("高德地图POI信息不含location key OR 无法interpret预期为double类型的string。file: view.py line 46 or 52")


            return render(request, "tested.html", {
                'positionsToReturn': request.POST.get('positionsToReturn'),
                'Paths': paths,
                'Locs': locs,
                'FUNC': FUNC_indicator[0]
            })

    return render(request, "tested.html", {
        'positionsToReturn': request.POST.get('positionsToReturn'),
        'Paths': paths[0],
        'Locs': [lst_of_loc[i] for i in paths[0]],
        'Time': paths[1],
        'Guides': guides,
        'FUNC' : FUNC_indicator[0]
    })
