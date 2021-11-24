# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 15:34:48 2021

@author: kcnab
"""

def GetConnectionString():

    driver = "{ODBC Driver 17 for SQL Server}"
    #server = "LAPTOP-ITLUQC4Q\SQLEXPRESS"
    server = "tempdatanabin.database.windows.net"
    database = "AirHeaterTemp"
    username = "nabin"
    password = "Mymilk4654@"
    connectionString = "DRIVER=" + driver + ";SERVER=" + server + ";DATABASE=" + database + ";UID=" + username + ";PWD=" + password
    return connectionString