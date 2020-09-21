RMIT University Vietnam
Course: COSC2790 Programming Internet of Things
Semester: 2020B
Assessment 2: Car Share IoT application
Group: 10
Members: Pham Nguyen Thanh Nhan, Nguyen Khang Duy , Vu Duy Khoi , Nguyen Trung Duc, Le Nguyen Thien Phu, 
Student ID: s3563953, S3636076, s3694615, s3695504 , s3639855

1. INTRODUCTION
The aim of this assignment is to develop a automatic car share system. To be specific, this system can be used to search, book, unlock and lock cars. 
Moreover, car's issues can be reported by customers which would help the company for car maintainance. There are totally 4 types of users which are company manager, 
engineers, system administrator and customer. Moreover, to finish this assignment, we used python as the main programming language and flask as website building tool. 
The system is divided into 2 parts: Master pi and Agent pi. The former would contain all python console for user registration, user features and flask website as well as
cloud database while the latter has facial recognition for car unlock and python console authentication. These 2 parts would be connected and worked properly by 
socket programming.

2. ACCOUNTS FOR ALL TYPES OF USER
- Customer:
    Username:customer
    Password:customer
- System admin:
    Username:admin
    Password:admin
- Company manager:
    Username:manager
    Password:manager
- Engineer:
    Username:engineer
    Password:engineer

3. FEATURES
All in formation would be stored in the google cloud mySQL database including all user account, cars' information, booking history as well as system data
There are several features for all types of user in this system:
- For customer: 
    Log in page: 
        + Log in in case customer already has an account or register when it is their first access to the system
    Customer's home page:
        + Show a list of available cars with their information such as Make, Body Type, Colour, Seats, Location, Cost per hours
        + Search for cars based on their feature
        + View booking history made by the current customer
        + Book a car, then customer will be asked to input booking details such as the duration.
        + Cancel a booking
        + Logout their account  
        
- For system admin: 
    Log in page:
        + Log in to access home page.
    Admin's home page:
        + View car booking history
        + Search and view users or cars details
        + Add, remove, modify information of users and cars
        + Report cars with issues by sending an email so that engineer can get it repaired.
        + Logout
- For company manager:
    Log in page:
        + Log in to access home page.
    Manager's home page:
        + Contain 3 charts which is useful for company manager in terms of decision making in business such as daily active user, all bookings by cars in this month, 
total number of bookings by months in the current year.
        + Logout

- For engineer:
    Log in page:
        + Log in to access home page
    Engineer's home page:
        + Show location of reported cars in google map
        + Logout
Unit tests for all features of the system

4. INSTALLATION	INSTRUCTION
- Download folder and unzip the downloaded folder.

5. REPOSITORY USEAGE IN GITHUB 
- Screenshots:

6. KNOWN BUGS AND LIMITATION
Unknown

7. ACKNOWLEDGEMENT

GITHUB
 https://github.com/nguyenkhangduy298/car-share-system-iot
 
DESCRIPTION BY MODULE
Part A
Part B
Part C
Part D
 UNIT TESTING AND DOCUMENTS 
 DOCUMENTATION:
 GITHUB
 https://github.com/nguyenkhangduy298/car-share-system-iot

