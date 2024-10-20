from dotenv import load_dotenv

from InGaTools.core.IP_check import IPCheck

load_dotenv()

if __name__ == "__main__":
    target = input("Enter target Website:\n> ")
    ip_check = IPCheck(target)
    ip_check.run_ip_check()
