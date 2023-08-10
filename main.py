import json, requests, logging, simpleaudio, wave, string, sys, curses, re
from show_chars import Show
from pwinput import pwinput
from time import sleep
from os import path, mkdir
from numpy import random
import random as rd
from jsmin import jsmin
from multiprocessing import Process

# menu function source: https://stackoverflow.com/a/70520442 user:15887215

def menu(title: str, classes: list[str], color: str = 'white') -> int:
    """
    Wrapper for command line menu screen,
    :param title: Title of menu screen
    :param classes: Options user can choose from
    :param color: color of selected option
    :return: option choice as index of classes
    """
    def character(stdscr, ):
        attributes = {}
        icol = {
            1: 'red',
            2: 'green',
            3: 'yellow',
            4: 'blue',
            5: 'magenta',
            6: 'cyan',
            7: 'white'
        }
        # put the stuff in the right format
        col = {v: k for k, v in icol.items()}

        # declare the background color

        bc = curses.COLOR_BLACK

        # make the 'normal' format
        curses.init_pair(1, 7, bc)
        attributes['normal'] = curses.color_pair(1)

        # make the 'highlighted' format
        curses.init_pair(2, col[color], bc)
        attributes['highlighted'] = curses.color_pair(2)

        # handle the menu
        c = 0
        option = 0
        while c != 10:

            stdscr.erase()  # clear the screen (you can erase this if you want)

            # add the title
            stdscr.addstr(f"{title}\n", curses.color_pair(1))

            # add the options
            for i in range(len(classes)):
                # handle the colors
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']

                # actually add the options

                stdscr.addstr(f'> ', attr)
                stdscr.addstr(f'{classes[i]}' + '\n', attr)
            c = stdscr.getch()

            # handle the arrow keys
            if c == curses.KEY_UP and option > 0:
                option -= 1
            elif c == curses.KEY_DOWN and option < len(classes) - 1:
                option += 1
        return option

    return curses.wrapper(character)


def token_gen() -> str:
    """
    Generates a random token string for FakeYou requests
    :return: string in the format of "A12345B-C67891D-E01112F-G13141H"
    """
    seed_1 = random.randint(10000, 99999)
    let_seed1 = rd.choice(string.ascii_letters)
    let_seed2 = rd.choice(string.ascii_letters)
    let_seed3 = rd.choice(string.ascii_letters)
    seed_2 = random.randint(10000, 99999)
    let_seed4 = rd.choice(string.ascii_letters)
    let_seed5 = rd.choice(string.ascii_letters)
    let_seed6 = rd.choice(string.ascii_letters)
    seed_3 = random.randint(10000, 99999)
    let_seed7 = rd.choice(string.ascii_letters)
    let_seed8 = rd.choice(string.ascii_letters)
    let_seed9 = rd.choice(string.ascii_letters)
    return f"{let_seed1}{seed_1}{let_seed2}-{let_seed3}{seed_2}{let_seed4}-{let_seed5}{seed_3}{let_seed6}-" \
           f"{let_seed7}{let_seed8}{let_seed9}"


def stream_print(line: str) -> None:
    """
    prints line as a stream of characters one at a time
    :param line: string to print
    :return: None
    """
    for c in line:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep(0.03)


def run_parallel(fn1, fn2, arg1, arg2):
    p1 = Process(target=fn1, args=arg1)
    p1.start()
    p2 = Process(target=fn2, args=arg2)
    p2.start()
    p1.join()
    p2.join()


def play_audio(audio) -> None:
    """

    :param audio: WaveObject that will be played
    :return: None
    """
    start = audio.play()
    start.wait_done()


if __name__ == '__main__':
    user_choice1 = 1
    while user_choice1 != 2:
        user_choice1 = menu('Show Script Generation Program\n',
                            ['Create a Script', 'Add/Edit a Show and Characters', "Exit"], 'blue')

        # Adding new show and characters
        if user_choice1 == 1:
            user_choice2 = 0
            while user_choice2 != 2:
                user_choice2 = menu('Add or Edit new Show\n',
                                    ['Add New Show', 'Edit Show and Characters', "Exit"], 'blue')
                with open("userinfo.json", "r") as jsonfile:
                    data = json.load(jsonfile)
                if user_choice2 == 0:
                    new_show_title = input("Show Title: ")
                    data["Characters"][new_show_title] = {}
                elif user_choice2 == 1:
                    user_list3 = [x for x in data["Characters"]]
                    user_list3.append("Exit")
                    user_choice3 = 0
                    while user_choice3 != len(user_list3) - 1:
                        user_choice3 = menu('Edit Show\n', user_list3, 'blue')
                        user_choice4 = 1
                        user_choice5 = 1
                        if user_choice3 != len(user_list3) - 1:
                            while user_choice4 != 3 and (not (user_choice4 == 2 or user_choice5 == 0)):
                                user_choice4 = menu('Edit or Delete Show or Characters:\n',
                                                    ["Edit Show Title", "Edit Characters", "Delete Show", "Exit"], "blue")
                                for i, x in enumerate(data["Characters"]):
                                    if i == user_choice3:
                                        x_global = x
                                if user_choice4 == 2:
                                    user_choice5 = menu("Are you sure?\n", ["No", "Yes"], "blue")
                                    if user_choice5 == 1:
                                        del data["Characters"][x_global]
                                        user_list3.remove(x_global)
                                elif user_choice4 == 1:
                                    user_choice6 = 0
                                    while user_choice6 != len(data["Characters"][x_global]) + 1:
                                        user_list6 = [x for x in data["Characters"][x_global]]
                                        user_list6.append("Add New Character")
                                        user_list6.append("Exit")
                                        user_choice6 = menu('Pick a Character to Edit:\n',
                                                            user_list6, "blue")
                                        if user_choice6 == len(data["Characters"][x_global]):
                                            loop = 0
                                            while loop != 1:
                                                show_character = input("Add Character: ")
                                                show_char_val = input(f"Add {show_character}'s FakeYou Voice Model Key: ")
                                                loop = menu(f"{show_character} added, add another? \n",
                                                            ["Yes", "No"], "blue")
                                                show_character = show_character.upper()
                                                data["Characters"][x_global][show_character] = show_char_val

                                        elif user_choice6 < len(data["Characters"][x_global]):
                                            count3 = 0
                                            for i, x in enumerate(data["Characters"][x_global]):
                                                if i == user_choice6:
                                                    user_choice7 = 0
                                                    count2 = 0
                                                    while user_choice7 != 2 and user_choice7 != 3:
                                                        if count2 == 0:
                                                            new_name = x
                                                        user_choice7 = menu(f"Edit {new_name}'s name or Voice ID?",
                                                                            ["Name", "Voice ID", "Delete Character",
                                                                             "Exit"], 'blue')
                                                        if user_choice7 == 0:
                                                            count3 += 1
                                                            new_name = input(f"Change {new_name}'s name to: ").upper()
                                                            old_name = x
                                                            new_val = data["Characters"][x_global][x]
                                                        elif user_choice7 == 1:
                                                            count3 += 1
                                                            new_val = input(f"Change {new_name}'s "
                                                                            f"FakeYou Voice ID to: ")
                                                            new_name = x
                                                            old_name = new_name
                                                        elif user_choice7 == 2:
                                                            user_choice8 = menu("Are you sure?\n", ["No", "Yes"],
                                                                                "blue")
                                                            if user_choice8 == 1:
                                                                old_name = x
                                                            else:
                                                                user_choice7 = 0
                                                        count2 += 1
                                            if count3 > 0:
                                                del data["Characters"][x_global][old_name]
                                                data["Characters"][x_global][new_name] = new_val
                                            elif user_choice7 == 2:
                                                del data["Characters"][x_global][old_name]

                                elif user_choice4 == 0:
                                    new_title = input(f"Enter the new title for {x_global}: ")
                                    data["Characters"][new_title] = data["Characters"][x_global]
                                    del data["Characters"][x_global]
                with open("Userinfo.json", "w") as jsonfile:
                    json.dump(data, jsonfile, indent=4)

        # Creating a script
        if user_choice1 == 0:
            #  Open the JSON config file
            with open('userinfo.json') as json_file:
                # Remove comments in JSON
                user_info = jsmin(json_file.read(), quote_chars="/*")
            config_dict = json.loads(user_info)
            if config_dict["OpenAI_Key"] == "default":
                temp_var = pwinput(prompt='OpenAI API Key: ')
                openai_key = temp_var
            else:
                openai_key = config_dict["OpenAI_Key"]

            username = ''
            password = ''
            if config_dict["FakeYou"]["User"] == "default":
                username = input("FakeYou Username or email (Press enter/return to skip this step, "
                                 "but the processing will be slower without a premium account)")
                if username != '':
                    password = pwinput()
            else:
                username = config_dict["FakeYou"]["User"]
                if config_dict["FakeYou"]["Pass"] == "default":
                    password = pwinput(prompt=f'FakeYou Password for {username}: ')
                else:
                    password = config_dict["FakeYou"]["Pass"]

            #  Define global variables for wave files
            sample_rate = 16000
            num_channels = 2
            bytes_per_sample = 2

            #  Define the ID Keys for The OpenAI and FakeYou APIs
            if username == '' or password == '':
                print("FakeYou Login Credentials Skipped\n")
                session = requests.Session()
                pass
            else:

                # Original code below written by shards-7 in FakeYou.py, Source Link:
                # https://github.com/shards-7/fakeyou.py
                # BEGIN CODE

                ljson = {"username_or_email": username, "password": password}
                # login payload

                logging.debug("Sending Login request")
                session = requests.Session()
                loginHandler = session.post("https://api.fakeyou.com/login", json=ljson)
                # sending the login request, this will return cookies and status
                logging.debug("Login request sent")

                lrjson = loginHandler.json()
                # our response from 'login request'
                if loginHandler.status_code == 200:
                    # this means we're in without 'ERRORS'

                    logging.debug("Processing the response (login)")
                    if lrjson["success"]:
                        # login success
                        logging.debug("Login has been done successfully")
                        sjson = session.get("https://api.fakeyou.com/session").json()
                        print("\nFakeYou Login Success!\n")

                    elif lrjson["success"] is False and lrjson["error_type"] == "InvalidCredentials":
                        # login failed
                        logging.critical("FALSE email/password, raising error.")

                elif loginHandler.status_code == 429:
                    # ip ban !
                    logging.critical("IP IS BANNED (caused by login request)")

                # END CODE

            # Create the show object using the shaw name and character bank given in the JSON file
            if config_dict['Show'] == "Default":
                user_choice3 = menu('Choose a Show', [x for x in config_dict["Characters"]], 'blue')
                for i, x in enumerate(config_dict["Characters"]):
                    if i == user_choice3:
                        show = Show(x, config_dict['Characters'][x])
                        break
            else:
                show = Show(config_dict['Show'], config_dict['Characters'][config_dict["Show"]])

            #  Prompt the command line to ask for a script
            prompt = input(f"Write a '{show.show}' prompt: ")
            script_str = show.write(openai_key, prompt)
            script = list(script_str.split("\n"))

            if not path.isdir("scene"):
                mkdir("scene")

            if path.exists("scene/script.txt"):
                with open("scene/script.txt", "w") as script_text:
                    script_text.write(script_str)
            else:
                with open("scene/script.txt", "x") as script_text:
                    script_text.write(script_str)

            print("\nScript Generated")
            sleep(0.3)
            print("\nVoice Generation Started")
            model_dict = show.voice_ids
            name_bank = show.characters
            scene_bank = []
            if script == ['Bad_prompt']:
                print("Bad Prompt, BOZO")
                pass
            else:
                line_list = []
                for i, x in enumerate(script):

                    # split_name variable created to detect with lines like "CHARACTER (action)" and change them to
                    # "CHARACTER" for voice assignment
                    split_name = re.split(":| ", x)
                    # print(split_name)
                    if (split_name[0] in name_bank) \
                            or ((len(split_name)) > 1
                                and ((split_name[0] + " " + split_name[1]) in name_bank)):
                        line_list.append(x)
                if line_list == []:
                    print("\n\nScript Could Not Be Generated :(\n\n")
                    sleep(2)
                    exit()
                count = 0
                lines = []
                for i, x in enumerate(script):
                    line = ""
                    char_name = ""

                    # split_name variable created to detect with lines like "CHARACTER (action)" and change them to
                    # "CHARACTER" for voice assignment
                    split_name = re.split(":| ", x)

                    if (split_name[0] in name_bank)\
                            or ((len(split_name)) > 1
                                and ((split_name[0] + " " + split_name[1]) in name_bank)):
                        if split_name[0] in name_bank:
                            char_name = split_name[0]
                        elif ((len(split_name)) > 1) and ((split_name[0] + " " + split_name[1]) in name_bank):
                            char_name = split_name[0] + " " + split_name[1]
                        if char_name not in scene_bank:
                            scene_bank.append(char_name)
                        # Keeps track of total lines rendered
                        count += 1
                        line = script[i+1]

                        # Append the single voice lines generated to list to print later
                        lines.append(f"{x}")
                        lines.append(f"{line}")

                        # Send the line to FakeYou api
                        voicemodel_uuid = model_dict[char_name]
                        text = line
                        id_tok = token_gen()
                        audio_uuid = {}
                        while 'inference_job_token' not in audio_uuid:
                            sleep(1)
                            logging.debug("Error: Could not find inference_job_token key, retrying")
                            audio_uuid = session.post("https://api.fakeyou.com/tts/inference",
                                                       json=dict(uuid_idempotency_token=id_tok,
                                                                 tts_model_token=voicemodel_uuid,
                                                                 inference_text=text)).json()
                        logging.debug("Success: found inference_job_token key")
                        audio_uuid = audio_uuid['inference_job_token']
                        print("\n")
                        audio_url = None
                        for t in range(1200):
                            sleep(1)  # check status every second for up to 20 minutes.
                            output = session.get(
                                f"https://api.fakeyou.com/tts/job/{audio_uuid}").json()
                            if (t % 1) == 0:            # Change the number after modulo (x) to make
                                                        # it print progress every x times
                                print(f"\r", end="")
                                print(f"LINE {count} of {len(line_list)}:\tTIME: {t}s, ", "OUTPUT: ",
                                      output["state"]["status"], end="")
                            if output["state"]["status"] == "complete_success":
                                audio_url = output["state"]["maybe_public_bucket_wav_audio_path"]
                                break
                            elif output["state"]["status"] == "dead" or output["state"]["status"] == "complete_failure":
                                break
                        if audio_url is None:
                            print("\nProduction Failed")
                        else:
                            print(f"\r", end="")
                            print(f"LINE {count} of {len(line_list)}:\tTIME: {t-1}s, ", "OUTPUT: ",
                                  output["state"]["status"])
                            total = sample_rate * num_channels * bytes_per_sample

                            logging.basicConfig(level=logging.INFO)

                            audio_url = f"https://storage.googleapis.com/vocodes-public{audio_url}"

                            logging.info(f"Downloading audio file from: {audio_url}")
                            content = session.get(audio_url).content
                            if not path.exists(f"scene/line_{count}.wav"):
                                with open(f"scene/line_{count}.wav", "x") as file:
                                    pass
                            with wave.open(f"scene/line_{count}.wav", "wb") as file:
                                file.setframerate(sample_rate)
                                file.setnchannels(num_channels)
                                file.setsampwidth(bytes_per_sample)
                                file.writeframesraw(content)
                play = None
                while play != "N":
                    play = input("\nPlay the script?(Y/N)")
                    if play == "Y":
                        for x in range(0, count):
                            with wave.open(f"scene/line_{x+1}.wav", "rb") as file:
                                n = file.getnframes()
                                content = file.readframes(n)
                            sample = simpleaudio.WaveObject(audio_data=content,
                                                            sample_rate=sample_rate,
                                                            num_channels=num_channels,
                                                            bytes_per_sample=bytes_per_sample)
                            print("{:<30s} ".format(lines[2 * x]), end="")
                            run_parallel(play_audio, stream_print,
                                         (sample, ), (f"{lines[(2 * (x + 1)) - 1]}", ))
                            print("\n")
                            sleep(1)
                    else:
                        pass
