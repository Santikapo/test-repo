import os
import base64
from requests import get, post, put
import json
import webbrowser
import sched
import time
import spotifyrequests as sr
from userinfo import client_id, client_secret
import sys


clear = lambda: os.system('cls')
code='AQDqbaunI4EYKnLl1fH1tc7HC1O844NJkep9xRRz5L0k2bN5d-3C2gDJyFQGHFyQ_CbrTSof5LLt1gIePD6ypgE4kCaJNv6zewMluctV0mwsJ-YPUGODHFUBeNvBIrX2J22Dq8GdC2aXF183gtaRhJEEclcw_E5uZOlGI6yC-jlnTXVvmjzVotaTIAijaORtiHdhf--DNLTUivA0yA_MdR3eA5QP2MaF6yhZRmFoVZo732uMEZqAkU8aKjFBICQTyYtg0OyQaCS8sZHsGvGCG46punoigB6g8UmutXfUGuSpIg5BAb4m4_dEuGvhClYzhQjp0JJ9DAV9eEY2_94-n8T-Mrd2GT04qJP85mdGESnDNAtF7AbYzVYS2laP1RbemW88Vm-FT0JnSN3LQjGv2L5aperE2as9iooap24Obx6I8e4fBPbUTbRmnxWKdMtKg9irP75hBQtFTD1dLlcDqfDPK1K5iJk'
liked = []

def main():
    inp = 0
    checking = False
    f = open('tokens.txt', 'r')
    token = f.readline().rstrip('\n')
    f.close()
    
    if input('Download Liked?\n') == 'y':
        clear()
        sr.get_liked(token)

    while True:
        print(
        "option 1: Get Code\n"\
        "option 2: Get Access\n"\
        "option 3: Use Refresh\n"\
        "option 4: Listening Mode\n"\
        "option 5: Exit"
            )
        while inp not in range(1, 6):
            inp = int(input(""))
            clear()




        if inp == 1:
            sr.get_code()
        elif inp == 2:
            sr.get_access_token(code)
        elif inp == 3:
            token = sr.use_refresh()
        elif inp == 4:
            checking = True
            sr.skip_liked(token, checking)
        elif inp == 5:
            return 
        inp = 0



def do_something(token, checking):
    inp = 0
    while True:
        print(
            "option 1: Resume Song\n"\
            "option 2: Skip\n"\
            "option 3: Get List of Playlists\n"\
            "option 4: Skip Liked mode\n"\
            "option 5: Get Liked Songs\n"
            "option 6: Return to Menu"
                )
        while inp not in range(1, 7):
            inp = int(input(""))

        if inp == 1:
            sr.start_resume(token)
        elif inp == 2:
            sr.skip(token, checking)
        elif inp == 3:
            sr.get_playlists(token)
        elif inp == 4:
            checking = True
            sr.skip_liked(token, True)
        elif inp == 5:
            sr.get_liked(token)
        elif inp == 6:
            return
        inp = 0


def periodic(scheduler, interval, action, actionargs):

    scheduler.enter(interval, 1, periodic,
                    (scheduler, interval, action, actionargs))
    action(actionargs)


main()