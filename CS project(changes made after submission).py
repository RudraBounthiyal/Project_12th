import random as r
import mysql.connector as M
my=M.connect(host='localhost', user='root', passwd='Rudra@123',database='event_management')

myc=my.cursor()

def Menu():
    print("****Welcome To Dreamsmith Events****")
    y="c"
    while y in "cC":
        print("Enter 1 to organise an event\n"
          "Enter 2 to book tickets for an event\n"
          "Enter 3 to view the details of the booked tickets\n"
          "Enter 4 to view the details of all the events\n"
          "Enter 5 to cancel your tickets\n"
          "Enter 6 to remove an event")
        print()
        f=input("Enter your choice:")
        if f=="1":
            CreateEvent()
        elif f=="2":
            BookTicket()
        elif f=="3":
            ViewTickets()
        elif f=="4":
            ViewEvents()
        elif f=="5":
            DeleteTicket()
        elif f=="6":
            DeleteEvent()
        else:
            print("Invalid Function!!!")
        y=input("Enter c to continue and x to exit:")
        print()

def CreateEvent():
    e = "CREATE Table if not exists pro (event_name varchar(40) , event_date varchar(40), event_time varchar(20), event_duration varchar(40),Number_of_tickets integer,price_of_tickets varchar(40),Organiser Varchar(40),event_id bigint)"
    myc.execute(e)
    print("Types Of Events We Manage Are:-")    
    event = ("Conferences","Fair","Party","Tournaments","Award Ceremony","Wokshops","Product Launch","Festival Celebration","Trade Shows","Theatrical Performance")
    for l in event:
        print(l)
    ch = input("Enter the type of your event:").title()
    if ch in event:
        event_name =input("Enter event name:")
        event_date = input("Enter event date(DD/MM/YYYY):")
        event_time = input("Enter event time(HH:MM):")
        event_duration = input("Enter event duration(In Hours):")
        no=int(input("Enter number of tickets:"))
        price=input("Enter ticket price(In Rupees):")
        o = input("Enter the organiser's name:")
        event_id= r.randint(1,10000)
        myc.execute("INSERT INTO pro(event_name, event_date, event_time, event_duration,Number_of_tickets,price_of_tickets,Organiser,event_id) VALUES ('{}','{}','{}','{}',{},'{}','{}',{})".format (event_name, event_date, event_time, event_duration,no,price,o,event_id))
        my.commit()
    else:
        print("Sorry, We Do Not Provide Services For Such Events")
        print()

    
def BookTicket():
    t = "create table if not exists ticket (customer_name varchar(40), event_name varchar(40),number_of_booked integer,event_id bigint)"
    myc.execute(t)

    myc.execute("select * from pro")
    event = myc.fetchall()
    if event!=[]:
        customer_name =input("Enter customer's name:")
        print("Choose one event from the list given below:-")
        for i  in event:
            print("Event name:-",i[0])
            print("Price per ticket:-",i[5])
            
        event_name =input("Enter event name:")
        myc.execute("select event_id from pro where event_name='{}'".format(event_name))
        f=myc.fetchall()
        for j in f:
            event_id=j[0]
        
        p="select Number_of_tickets from pro where event_name='{}'".format(event_name)
        myc.execute(p)
        e=myc.fetchall()
        for k in e:
            for j in k:
                if j!=0:
                    o=int(input("Number of tickets to book:"))
                    in1="INSERT INTO ticket (customer_name,event_name,number_of_booked,event_id) values ('{}','{}',{},{})".format (customer_name,event_name,o,event_id)
                    myc.execute(in1)
                    my.commit()
                    n="update pro set Number_of_tickets =Number_of_tickets-{} where event_name = '{}'".format(o,event_name)
                    myc.execute(n)
                    my.commit()
                    print("Ticket Booked")
                else:
                    print("No Tickets Available")
    else:
        print("No Event Alloted")  
            
def ViewTickets():
    
    print("Choose one event from the list given below:-")
    myc.execute("select * from pro")
    event = myc.fetchall()
    if event!=[]:
        for i in event:
            print("Event name:-",i[0])
            
        myc.execute("select B.customer_name, A.event_name, A.event_date, A.event_time, A.event_duration, B.number_of_booked FROM ticket B, pro A WHERE A.event_id = B.event_id")
        ticket = myc.fetchall()

        e_name = input("Choose the event:")

        for j in ticket:
            if j[5]!=0:
                if e_name.upper() == j[1].upper():
                    print("Customer name:-",j[0])
                    print("Event name:-",j[1])
                    print("Event date:-",j[2])
                    print("Event time:-",j[3])
                    print("Event duration:-",j[4])
                    print("Number of tickets booked:-",j[5])
                    print()
            else:
                print("No Ticket Booked")
    else:
        print("No Event Alloted")
            
def ViewEvents():
    myc.execute("select * from pro")
    event = myc.fetchall()
    if event !=[]:
        for i  in event:
            print("Event name:-",i[0])
            print("Event date:-",i[1])
            print("Event time:-",i[2])
            print("Event duration:-",i[3])
            print("Number Of Tickets:-",i[4])
            print("Price Of Tickets:-",i[5])
            print("Name Of The Organiser:-",i[6])
            print()
    else:
        print("No Event Alloted")
def DeleteTicket():
    myc.execute("select * from pro")
    event = myc.fetchall()
    if event !=[]:
        cust_name =input("Enter the name of the customer:")
        eve_name = input("Enter the name of the event:")
        myc.execute("select number_of_booked from ticket where customer_name ='{}' and event_name='{}'".format(cust_name,eve_name))
        t=myc.fetchall()
        myc.execute("DELETE FROM ticket WHERE customer_name ='{}' and event_name='{}'".format(cust_name,eve_name))
        my.commit()
        for i in t:
            for j in i:
                n="update pro set Number_of_tickets =Number_of_tickets+{} where event_name='{}'".format(j,eve_name)
                myc.execute(n)
                my.commit()
        print("Ticket Cancelled")
    else:
        print("No Event Alloted")
def DeleteEvent():

    print("The list of event given below:-")
    myc.execute("select * from pro")
    event = myc.fetchall()
    if event!=[]:
        for i  in event:
            print("Event name:-",i[0])
        ev_name=input("Enter the name of the event:")
        myc.execute("DELETE FROM pro where event_name='{}'".format(ev_name))
        my.commit()
        myc.execute("DELETE FROM ticket where event_name='{}'".format(ev_name))
        my.commit()
        print("Event Cancelled")
    else:
        print("No Event Alloted")

Menu()
