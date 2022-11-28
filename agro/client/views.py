from django.shortcuts import render,HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import fetcher
import requests,random

districts=["Adilabad","Bhadradri Kothagudem","Hanumakkonda","Hyderabad","Jagtial","Jangaon","Jayashankar","Jogulamba Gadwal","Kamareddy","Karimnagar","Khammam","Kumuram Bheem","Mahabubabad","Mahabubnagar","Mancherial","Medak","Medchal-Malkajgiri","Mulugu","Nagarkurnool","Nalgonda","Narayanpet","Nirmal","Nizamabad","Peddapalli","Rajanna Sircilla","Rangareddy","Sangareddy","Siddipet","Suryapet","Vikarabad","Wanaparthy","Warangal","Yadadri Bhuvanagiri","Warangal Rural","Warangal Urban"]

# Create your views here.
@xframe_options_exempt
def home(request):
    data={"districts":districts}
    return render(request,"home.html",context=data)

def form(request):
    data={"nitrogen":0.0, "pottasium":0.0, "phosphorus":0.0, "ph":0.0, "temperature":0.0, "humidity":0.0, "rainfall":0.0}
    data["districts"]=districts
    if(request.method=='POST'):
        print("getting the data of dictrict:",request.POST["district"],"|| mandal:",request.POST["mandal"])
        res=fetcher.fetch(request.POST["district"],request.POST["mandal"])
        if(res!=None):
            print("fetch Successful!! Updating data")
            data["nitrogen"]=res["N"]
            data["pottasium"]=res["K"]
            data["phosphorus"]=res["P"]
            data["ph"]=res["pH"]
            data["temperature"]=res["temp"]
            data["humidity"]=res["humidity"]
            data["rainfall"]=res["rain"]
            print("Data Updated!")

    return render(request,"form.html",context=data)

def result(request):
    if request.method=='POST':
        res=fetcher.predictor([request.POST["N"],request.POST["P"],request.POST["K"],request.POST["temp"],request.POST["humidity"],request.POST["ph"],request.POST["rain"]])
    img_info=requests.get("https://pixabay.com/api/?key=31593177-fb0d545d7aa2804ff1a38ee60&q="+res[0]+"&image_type=photo")
    crop_img=img_info.json()["hits"][random.randint(0,10)]['largeImageURL'] if(img_info.json()["totalHits"]>10) else ""
    return render(request,"result.html",context={"crop_img":crop_img,"crops":len(set(res)),"data":res[0:len(set(res))],"districts":districts})
