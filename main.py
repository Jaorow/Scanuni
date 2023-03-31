import paramiko
import json
import datetime
from dotenv import load_dotenv
import os


class ssh_client:
    def __init__(self):
        load_dotenv()

        # Define the SSH connection parameters
        hostupi = "login.cs.auckland.ac.nz"
        port = 22
        userupi = os.getenv("USERUPI")
        password = os.getenv("PASSWORD")

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostupi, port, userupi, password)

        self.alpha = [
                    "a","b","c","d","e","f","g","h","i",
                    "j","k","l","m","n","o","p","q","r",
                    "s","t","u","v","w","x","y","z"
                    ]
        self.path = "/afs/ec.auckland.ac.nz/users/"
        self.logger = ""

    def get_root(self):
        for _ in range(3):
            self.cmd("cd ..")
    
    def loop_aplha(self):
        count = 0 
        upis_count = 0
        for first_letter in self.alpha:
            for second_letter in self.alpha:
                count += 1
                message = (f"combo.NO : {count} -- combo : {first_letter}/{second_letter}\n")
                self.logger += message
                print(message)
                upis = self.cmd(f"ls {self.path}{first_letter}/{second_letter}").strip()

                for upi in upis.split("\n"):
                    print(f"NO : {upis_count} UPI : {upi}")
                    upis_count += 1

                self.write_out(upis,first_letter,second_letter)
        print(f"{count} loops with {upis_count} upis")

    def write_out(self,data,fl,sl):
        # text file output
        with open("output.txt","a") as out:
            out.write(data+"\n")

        # json output
        with open('output.json', 'r') as f:
            json_data = json.load(f)

        json_data[f"{fl+sl}"] = data.split("\n")

        with open("output.json","w") as out:
            json.dump(json_data, out)

    def cmd(self,cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        output =  stdout.read().decode()
        stdout.close()
        return output

    def close(self):
        self.client.close()
        self.log()
    
    def log(self):
        with open("DEBUG_log.txt", "a") as log:
            log.write(datetime.datetime.now)
            log.write(self.logger)


client = ssh_client()
client.loop_aplha()
client.close()
