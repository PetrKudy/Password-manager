
import argparse
import pyAesCrypt
import sys
import os
import json



class PWManager():
    def __init__(self,args):
        self.args = args

    def _checking_super_pw(foo):
        def wrapper(self):
            try:
                pyAesCrypt.decryptFile("data.HAX", "data.txt", self.args.super_password, 64*1024) #if incorrect create empty data.txt
                foo(self)
                pyAesCrypt.encryptFile("data.txt", "data.HAX", self.args.super_password, 64*1024)
                os.remove('data.txt')
            except:
                print('sorry your super password is not correct')
        return wrapper

    @_checking_super_pw
    def add_record(self):
        with open("data.txt","r+") as file:
            records = json.load(file)
            if self.args.add_record[0] not in records.keys(): # check if exist
                records[self.args.add_record[0]] = self.args.add_record[1]
                json_records = json.dumps(records)
                file.seek(0) # overwriting file
                file.write(json_records)
                file.truncate()
            else:
                print('sorry this record already exist')

    @_checking_super_pw
    def delete_record(self):
        with open("data.txt","r+") as file:
            records = json.load(file)
            if self.args.delete_record in records.keys():
                records.pop(args.delete_record)# popping out
                json_records = json.dumps(records)
                file.seek(0)# overwriting file
                file.write(json_records)
                file.truncate()
            else:
                print('sorry record not found')

    @_checking_super_pw
    def edit_record(self):
        with open("data.txt","r+") as file:
            records = json.load(file)

            if self.args.edit_record[0] in records.keys(): # check if exist
                records[self.args.edit_record[0]] = self.args.edit_record[1]
                json_records = json.dumps(records)
                file.seek(0) # overwriting file
                file.write(json_records)
                file.truncate()
            else:
                print('sorry record not found ')

    @_checking_super_pw
    def show_password(self):
        with open("data.txt","r") as file:
            records = json.load(file)
            if self.args.show_password in records.keys():
                print(records[args.show_password])
            else:
                print('sorry record not found')

    @_checking_super_pw
    def show_all_records(self):
        with open("data.txt","r") as file:
            records = json.load(file)
            for key in records.keys():
                print(key)

    def change_super_password(self):
            if args.change_super_password[0] == args.change_super_password[1]:
                try:
                    pyAesCrypt.decryptFile("data.HAX", "data.txt", self.args.super_password, 64*1024)#if incorrect create empty data.txt

                    pyAesCrypt.encryptFile("data.txt", "data.HAX", self.args.change_super_password[0], 64*1024)
                    os.remove('data.txt')
                    print('password was changed')
                except:
                    print('sorry your super password is not correct')
            else:
                print('second password doesnt match first password')


def Control(args): # controling inputs and call method from PWManager
    ## checking if file for storing exist....
    if os.path.isfile('data.HAX') == False:
        with open("data.txt","w") as file:
            file.write('{}')
        pyAesCrypt.encryptFile("data.txt", "data.HAX",args.super_password, 64*1024)
        print('Password manager file was created!')

    # controler
    if args.add_record is not None:
        PWManager(args).add_record()

    elif args.delete_record is not None:
        PWManager(args).delete_record()

    elif args.edit_record is not None:
        PWManager(args).edit_record()

    elif args.show_password is not None:
        PWManager(args).show_password()

    elif args.show_all_records is True:
        PWManager(args).show_all_records()

    elif args.change_super_password is not None:
        PWManager(args).change_super_password()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'PassWordManager2019 - storying passwords in formate JSON ... {email:****,pornhub:*****,etc}')
    parser.add_argument("-a","--add_record",nargs=2, help ="add record to list, values:record password")
    parser.add_argument("-d","--delete_record", help ="delete record from list, value:record")
    parser.add_argument("-e","--edit_record",nargs=2, help ="edit record in list, values:record new_password")
    parser.add_argument("-s","--show_password", help ="show password of record, value:record")
    parser.add_argument("-all","--show_all_records",action='store_true', help ="show all records")
    parser.add_argument("-pass","--super_password",required = True, help ="super password to your record list")
    parser.add_argument("-chp","--change_super_password",nargs=2, help ="change super password values: new_password new_password")
    args = parser.parse_args()
    Control(args)
