# Django-shop-manager
## Django app to manage a shop / warehouse

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
Web application created with Python and Django to manage a shop or warehouse.\
Application have three types of users: owner (admin), seller, warehouseman.
Every user have special functions which he can use, for example:
* You can login as:
    * owner -> Username: `admin` Password: `admin`
    * seller -> Username: `user1` Password: `Django1234`
    * warehouseman -> Username: `user2` Password: `Django1234`

* owner:

    * Can create new user (owner/seller/warehouseman)
    * Have access to seller and warehouse panel
* warehouseman:
    * Add new product or edit existing products
    * Create new categories or edit existing
    * Search for product (by title or description), category
    * Receives notifications when product quantity on stock is lower than 5
    * Complete order
* seller:
    * create new order
    * edit orders with status 'waiting'
    * search for orders
    * display available products in their categories
    * increase / reduce quantity of products in active order
    * change status to paid / unpaid
    * send order to warehouse to finalize 

## Technologies
Project is created with:
* Python 3.8
* Django 3.1.2
* Bootstrap 4

## Setup
To run this project on Windows:
* pip install virtualvenv (for keep order)
* py -m venv myvenv
* myvenv\scripts\activate
* pip install -r requirements.txt
* py manage.py runserver

On Linux/Ubuntu:
* sudo apt install python-pip
* sudo apt install virtualenv (for keep order)
* virtualenv myvenv
* source myvenv/bin/activate
* pip install -r requirements.txt
* python manage.py runserver