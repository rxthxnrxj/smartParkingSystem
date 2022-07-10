from django.shortcuts import render
import torch
from requests import Response
from django.shortcuts import render, redirect, reverse

from PIL import Image as im
import socket
import json
from pathlib import Path
from django.core.files import File
import base64
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .forms import *
import requests
from math import radians, cos, sin, asin, sqrt
from django.contrib import messages

# Create your views here.


def distance(lat1, lon1, lat2, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return(c * r)


# def slotChecker(request):
#     a = 5
#     b = 3
#     c = a*b
#     slots = parkingInformation.objects.get(name='demoLocation')
#     context = {'slot': slots}
#     print(slots)
#     return render(request, 'base/home.html', context)


def user(request):
    form = AddressForm()
    if request.method == 'POST':
        address = request.POST.get("address")
        API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
        URL = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}'
        results = requests.get(URL)
        if results.status_code == 200:
            # getting data in the json format
            data = results.json()
            # getting the main dict block
            lat_val = data['results'][0]['geometry']['location']['lat']
            lon_val = data['results'][0]['geometry']['location']['lng']
            print("Latitude:", lat_val, "\t Longitude:", lon_val)

        data = imageData.objects.all()
        for i in data:
            dis = distance(i.latitude, i.longitude, lat_val, lon_val)
            if dis < 1:
                if i.availableSlots > 0:
                    print("\n\nParking slot Available! \nFound at a distance of: ", round(
                        dis, 2), " kms from your destination\n\n")
                    messages.success(
                        request, f"Found at: {round(dis, 2)} kms from your destination")
                    response = redirect('/test/home')
                    return response
                else:
                    print("No parking slots avaible!")
                    messages.error(request, f"No slots found at {address}!")
            else:
                print("No parking slots avaible!")
                messages.error(request, f"No slots found at {address}")

    context = {'form': form}
    return render(request, 'base/user.html', context)


def slotUpdater(request):

    data = imageData.objects.all().last()
    print(data)
    slots = data.slots
    if data:
        f_name = str(data.capture)
        torch.hub.download_url_to_file(
            'http://127.0.0.1:8000/static/images/' + f_name, f_name)
        img = im.open(f_name)
        width, height = img.size
    path_hubconfig = 'D:/COLLEGE/SEM 6/OPENLAB/project/parking/base/yolov5'
    path_weightfile = 'D:/COLLEGE/SEM 6/OPENLAB/project/parking/base/yolov5/yolov5s.pt'
    model = torch.hub.load(
        path_hubconfig, 'custom', path=path_weightfile, source='local')
    results = model(img, size=640)
    df = results.pandas().xyxy[0]
    count = 0
    for i in df['name']:
        if i == 'car':
            count += 1
    ans = slots-count
    if ans > 0:
        imageData.objects.filter(_id=1).update(
            availableSlots=ans
        )
    else:
        imageData.objects.filter(_id=1).update(
            availableSlots=0
        )
    print("/////", ans)

    response = redirect('/test/home')
    return response


def bookSlot(request):
    data = imageData.objects.all().last()
    avail = data.availableSlots
    print("\nBooking Slot...")
    imageData.objects.filter(_id=1).update(
        availableSlots=avail-1
    )
    print("Done.\n")
    messages.info(request, "Slot booked successfully !")

    response = redirect('/test/home')
    return response


def home(request):
    parking = imageData.objects.all().last()
    context = {'parking': parking}
    return render(request, 'base/home.html', context)


def adminPage(request):
    return render(request, 'base/admin.html')


# if slotUpdater():
#         print("\n Slot updation by Admin successsful")
#         response = redirect('/home/')
#         return response
#     else:
#         print("Error Updating Database !")


@csrf_exempt
def saveImage(request):
    data = imageData.objects.all().last()
    print("VIEW TRIGGERED")
    if request.method == "POST":
        path = Path("image.jpeg")
        pic = request.POST.get("media")
        print(pic)
        with open("image.jpeg", "wb") as new_file:
            new_file.write(base64.decodebytes(bytes(pic, encoding='utf-8')))

        with path.open(mode='rb') as f:
            data.capture = File(f, name=path.name)
            data.save()
    else:
        print("No Image received")
    response = redirect('/test/home')
    return response


# def sendInfo(request):
#     #Create a socket object
#     s = socket.socket()
#     print ("Socket object successfully created")
#     print("\n")

#     HOST = "172.20.10.2"
#     PORT = 65000  # Port to listen

#     # Bind to the port
#     s.bind((HOST,PORT))
#     print ("socket binded to %s" %(PORT))
#     print("\n")

#     # Socket in listening mode
#     s.listen()
#     print ("socket is listening")
#     print("\n")

#     #Write your application code here
#     while True:
#     #c connection obj
#     # Establish connection with client.
#         c, addr = s.accept()
#         print ('Got connection from', addr )
#         print("\n")
#         c.sendall(b'Thank you for connecting')
#         print("\n")
#         data=c.recv(1024)
#         print(data)
#     # Close the connection with the client
#         c.close()
#     # Breaking once connection closed
#         break
