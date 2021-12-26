# GCS-Credencial_harvest [Python 3.5]

**Your best friend in credential reuse attacks.**

### Some of the scenarios GCS-Credencial_harvestcan be used in it
- Check if the targeted email is in any leaks and then use the leaked password to check it against the websites.
- Check if the target credentials you found is reused on other websites/services.
- Checking if the old password you got from the target/leaks is still used in any website.

# Usage
```
usage: GCS-Credencial_harvest.py [-h] [-p] [-np] [-q] email

positional arguments:
  email       Email/username to check

optional arguments:
  -h, --help  show this help message and exit
  -p          Don't check for leaks or plain text passwords.
  -np         Don't check for plain text passwords.
  -q          Quiet mode (no banner).

```

## Installing and requirements
### To make the tool work at its best you must have :
- Python 3.x or 2.x (preferred 3).
- Linux or Windows system.
- Worked on some machines with MacOS and python3.
- The requirements mentioned in the next few lines.
###installation
cd GCS-Credencial_harvest
python -m pip install -r win_requirements.txt or python -m pip install -r requirements.txt 
python GCS-Credencial_harvest.py -h
```
**+For Linux :**
```
git clone https://github.com/GCSCOUNCIL/GCS-Credencial_harvest
cd GCS-Credencial_harvest
python3 -m pip install -r requirements.txt
python3 GCS-Credencial_harvest.py -h
```


