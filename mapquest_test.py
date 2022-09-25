import urllib.parse
import requests
from tkinter import *

#Create an instance of tkinter window or frame
win=Tk()
win.resizable(False, False)
win.title("Map Quest with Gas Calculator")
startloc,destloc,gas = "","",""
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "MhvbvH6lJAKgMu9wisKM5iSoZWOFFPQJ"
traffic_api = "http://www.mapquestapi.com/search/v2/radius?"
alternative_api = "http://www.mapquestapi.com/directions/v2/alternateroutes?"

#function to get the direction from starting location to destination city
def get_direction():
        url = main_api + urllib.parse.urlencode({"key":key, "from":startloc, "to":destloc})
        alt_url = alternative_api + urllib.parse.urlencode({"key":key, "from":startloc, "to":destloc})
        json_data = requests.get(url).json()
        json_data_alt = requests.get(alt_url).json()

        json_status = json_data["info"]["statuscode"]

        # if successfull, display the result
        if json_status == 0:

                navigate.destroy()
                Label( win, text="Destination City Location").pack()
                Label( win, text="Here are the Directions from " + (startloc) + " to " + (destloc)).pack()

                Label( win, text="Total Trip Duration: " + (json_data["route"]["formattedTime"])).pack()
                Label( win, text="Kilometers: " + str("{:.2f}".format(json_data["route"]["distance"] * 1.6))).pack()
                Label( win, text="Fuel Used (Ltr): " + str("{:.3f}".format(json_data["route"]["fuelUsed"]*3.78))).pack()
                Label( win, text="Amount of Money to be Spent on Fuel: " + str("{:.3f}".format(json_data["route"]["fuelUsed"]*3.78 *int(gas)))).pack()

                Label( win, text="Alternative Route: Total Trip Duration: " + (json_data_alt["route"]["formattedTime"])).pack()
                Label( win, text="Alternative route: Kilometers: " + str("{:.2f}".format(json_data_alt["route"]["distance"] * 1.6))).pack()
                Label( win, text="Alternative Route: Fuel Used (Ltr): " + str("{:.3f}".format(json_data_alt["route"]["fuelUsed"]*3.78))).pack()
                Label( win, text="Alternative Route: Amount of Money to be Spent on Fuel: " + str("{:.3f}".format(json_data_alt["route"]["fuelUsed"]*3.78 *int(gas)))).pack()
        
                #display the route result with scrollbar
                scrollbar.pack(side=RIGHT, fill = Y)
                myList = Listbox(win,  yscrollcommand=scrollbar.set, width=100)

                for each in json_data["route"]["legs"][0]["maneuvers"]:
                        narrative = each["narrative"] + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)")
                        myList.insert(END, narrative)

                myList.pack(side=LEFT, fill=BOTH)
                scrollbar.config(command=myList.yview)

                #display the route result with scrollbar
                scrollbar.pack(side=RIGHT, fill = Y)
                myList = Listbox(win,  yscrollcommand=scrollbar.set, width=100)

                for each in json_data_alt["route"]["legs"][0]["maneuvers"]:
                        narrative = each["narrative"] + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)")
                        myList.insert(END, narrative)
                        
                myList.pack(side=LEFT, fill=BOTH)
                scrollbar.config(command=myList.yview)

                #display the route result iwith scrollbar
                scrollbar.pack(side=RIGHT, fill = Y)
                myList = Listbox(win,  yscrollcommand=scrollbar.set, width=100)

                #create button to close the application
                Button(win, height=1, width=10, fg="white", bg='#4C6793',text="Close application", command=destroy).pack()
                lbl.destroy()

        elif json_status == 402:
                msg.set("You have entered an Invalid Location!")
                lbl.pack(padx=5, pady=5)
        elif json_status == 611:
                msg.set("You have entered an Invalid Location!")
                lbl.pack(padx=5, pady=5)
        else:
                msg.set("Something went wrong! PLEASE TRY AGAIN")
                lbl.pack(padx=5, pady=5)

#function that will get the value of text box
def get_input():
   global startloc
   global destloc
   global gas
   startloc = startloc_txt.get(1.0, "end-1c")
   destloc = destloc_txt.get(1.0, "end-1c")
   gas = gas_txt.get(1.0, "end-1c")
   if(startloc and destloc and gas):
       if(gas.isdigit()):
        get_direction()
       else:
        msg.set("The Gas Price must be an integer!")
        lbl.pack(padx=5, pady=5)    
   else:
       msg.set("Please fill up completely!")
       lbl.pack(padx=5, pady=5)

#creating a result label that will be displayed on the window
msg = StringVar()
lbl = Label( win, textvariable=msg)

#function to close the window
def destroy():
        win.destroy()

#Creating a text box and label widget for Starting Location
startloc_lbl = Label( win, text="Starting Location: ")
startloc_txt=Text(win, height=2, width=40)
startloc_lbl.pack(padx=5, pady=5)
startloc_txt.pack()

#Creating a scrollbar 
scrollbar = Scrollbar(win)

#Creating a text box and label widget for destination city
destloc_lbl = Label( win, text="Destination City: ")
destloc_txt=Text(win, height=2, width=40)
destloc_lbl.pack(padx=5, pady=5)
destloc_txt.pack()

#Creating a text box and label widget for gas price
gas_lbl = Label( win, text="Enter Gas Price: ")
gas_txt=Text(win, height=2, width=40,)
gas_lbl.pack(padx=5, pady=5)
gas_txt.pack()

#Create a button to navigate directions
navigate= Button(win, height=1, width=10, fg="white", bg='#4C6793', text="Let's Go!", command=get_input)
navigate.pack(padx=5, pady=5)

win.mainloop() 
