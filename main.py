import json, requests, logging, simpleaudio, wave, string, sys, curses, re, io, os
from show_chars import Show
from PIL import Image
from pwinput import pwinput
from time import sleep
from os import path, mkdir
from numpy import random
import random as rd
from jsmin import jsmin
from multiprocessing import Process

# menu function source: https://stackoverflow.com/a/70520442 user:15887215


def menu(title, classes, color='white'):
    # define the curses wrapper
    def character(stdscr, ):
        attributes = {}
        # stuff i copied from the internet that i'll put in the right format later
        icol = {
            0: 'black',
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

        # declare the background colors

        bc = curses.COLOR_BLACK
        hbc = curses.COLOR_WHITE

        # make the 'normal' format
        curses.init_pair(1, 7, bc)
        attributes['normal'] = curses.color_pair(1)

        # make the 'highlighted' format
        curses.init_pair(2, col[color], hbc)
        attributes['highlighted'] = curses.color_pair(2)

        # handle the menu
        c = 0
        option = 0
        stdscr.scrollok(True)
        stdscr.idlok(1)
        while c != 10:

            stdscr.erase()  # clear the screen (you can erase this if you want)
            # for eventual better navigation: stdscr.move(option, 0)
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
    logging.basicConfig()
    user_choice1 = 1  # change user_choice var names?

    # main menu while loop
    while user_choice1 != 2:
        user_choice1 = menu('Show Script Generation Program\n',
                            ['Create a Script', 'Add/Edit a Show and Characters', "Exit"], 'black')

        # adding/editing new show and characters
        if user_choice1 == 1:
            user_choice2 = 0

            # edit show menu while loop
            while user_choice2 != 2:
                user_choice2 = menu('Add or Edit new Show\n',
                                    ['Add New Show', 'Edit Show and Characters', "Exit"], 'black')

                # opening config json file to edit as dictionary
                with open("userinfo.json", "r") as jsonfile:
                    data = json.load(jsonfile)

                # add new show option
                if user_choice2 == 0:
                    new_show_title = input("Show Title: ")
                    data["Characters"][new_show_title] = {}  # creates new show title dict entry, with empty characters

                # edit show and characters option
                elif user_choice2 == 1:
                    user_list3 = [x for x in data["Characters"]]  # list of available shows to edit
                    user_list3.append("Exit")
                    user_choice3 = 0

                    # edit show menu while loop
                    while user_choice3 != len(user_list3) - 1:
                        user_choice3 = menu('Edit Show\n', user_list3, 'black')
                        user_choice4, user_choice5 = 1, 1
                        if user_choice3 != len(user_list3) - 1:  # person has chosen to edit a show

                            # edit or delete show or characters menu while loop
                            while user_choice4 != 3 and (not (user_choice4 == 2 or user_choice5 == 0)):
                                user_choice4 = menu('Edit or Delete Show or Characters:\n',
                                                    ["Edit Show Title", "Edit Characters", "Delete Show", "Exit"],
                                                    "black")
                                for i, x in enumerate(data["Characters"]):
                                    if i == user_choice3:
                                        x_global = x
                                if user_choice4 == 2:
                                    user_choice5 = menu("Are you sure?\n", ["No", "Yes"], "black")
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
                                                            user_list6, "black")
                                        if user_choice6 == len(data["Characters"][x_global]):
                                            loop = 0
                                            while loop != 1:
                                                show_char_val = input(
                                                    f"Add Character's FakeYou Voice Model Key or Search Character by "
                                                    f"Name: ")
                                                characters = requests.get(
                                                    "https://api.fakeyou.com/tts/list").json()["models"]
                                                show_character = None
                                                character_search = None
                                                if show_char_val[:3] == "TM:":
                                                    for x in characters:
                                                        if x["model_token"] == show_char_val:
                                                            length = len(x["title"])
                                                            for i, y in enumerate(x["title"]):
                                                                if y == "(":
                                                                    length = i-1
                                                            show_character = x["title"][0:length]
                                                            break
                                                else:
                                                    for x in characters:
                                                        if show_char_val.lower() in x["title"].lower() and \
                                                                character_search is None:
                                                            character_search = [x]
                                                        elif show_char_val.lower() in x["title"].lower():
                                                            character_search.append(x)
                                                    if character_search is not None:
                                                        def rating_calc(character):
                                                            if character['user_ratings']['total_count'] > 0:
                                                                return round((character['user_ratings']['positive_count']
                                                                              / character['user_ratings']['total_count'])
                                                                             * 5, 2)
                                                            else:
                                                                return 0
                                                        character_search.sort(key=rating_calc, reverse=True)
                                                        selection = menu(
                                                            f"Which {show_char_val} do you want?", 
                                                            [f"{y['title']},  Rating: "
                                                             f"{rating_calc(y)}/5, "
                                                             f"Popularity:{y['user_ratings']['total_count']} Ratings" 
                                                             for y in character_search],
                                                            "black")
                                                        chosen_character = character_search[selection]
                                                        length = len(chosen_character["title"])
                                                        for i, y in enumerate(chosen_character["title"]):
                                                            if y == "(":
                                                                length = i - 1
                                                        show_character = chosen_character["title"][0:length]
                                                        show_char_val = chosen_character["model_token"]
                                                if show_character is None and character_search is None:
                                                    loop = menu("Voice model does not exist! Try again? \n",
                                                                ["Yes", "No"], "black")
                                                else:    
                                                    loop = menu(f"{show_character} added, add another? \n",
                                                                ["Yes", "No"], "black")
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
                                                                             "Exit"], 'black')
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
                                                                                "black")
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

                # save all information put in/taken out of dictionary to jsonfile
                with open("userinfo.json", "w") as jsonfile:
                    json.dump(data, jsonfile, indent=4)

        # creating a script
        if user_choice1 == 0:
            #  Open the JSON config file
            with open('userinfo.json') as json_file:
                # Remove comments in JSON
                user_info = jsmin(json_file.read(), quote_chars="/*")
            config_dict = json.loads(user_info)
            if config_dict["OpenAI_Key"].lower() == "default":
                temp_var = pwinput(prompt='OpenAI API Key: ')
                openai_key = temp_var
            else:
                openai_key = config_dict["OpenAI_Key"]

            username = ''
            password = ''
            if config_dict["FakeYou"]["User"].lower() == "default":
                username = input("FakeYou Username or email (Press enter/return to skip this step, "
                                 "but the processing will be slower without a premium account)")
                if username != '':
                    password = pwinput()
            else:
                username = config_dict["FakeYou"]["User"]
                if config_dict["FakeYou"]["Pass"].lower() == "default":
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
            if config_dict['Show'].lower() == "default":
                user_choice3 = menu('Choose a Show', [x for x in config_dict["Characters"]], 'black')
                for i, x in enumerate(config_dict["Characters"]):
                    if i == user_choice3:
                        show = Show(x, config_dict['Characters'][x], openai_key)
                        break
            else:
                show = Show(config_dict['Show'], config_dict['Characters'][config_dict["Show"]], openai_key)

            # Start while loop to allow continuation of the script
            contin = 2
            while contin != 1:

                #  Prompt the command line to ask for a script
                if contin == 2:
                    prompt = input(f"Write a '{show.show}' prompt: ")
                    script_str = show.write(prompt)
                elif contin == 0:
                    prompt = input(f"Add an additional prompt: ")
                    script_str = show.contn(prompt)
                script = list(script_str.split("\n"))

                if not path.isdir("scene"):
                    mkdir("scene")

                if not path.isdir(f"scene/{show.show}"):
                    mkdir(f"scene/{show.show}")

                if path.isdir(f"scene/{show.show}/{show.global_prompt}"):
                    cool_count = 0
                    cool_prompt = f"{show.global_prompt}"
                    while path.isdir(f"scene/{show.show}/{cool_prompt}") and contin == 2:
                        cool_count += 1
                        cool_prompt = f"{show.global_prompt}_{cool_count}"
                    if contin == 0:
                        pass
                    else:
                        mkdir(f"scene/{show.show}/{cool_prompt}")
                        scene_path = f"scene/{show.show}/{cool_prompt}"
                else:
                    mkdir(f"scene/{show.show}/{show.global_prompt}")
                    scene_path = f"scene/{show.show}/{show.global_prompt}"

                if path.exists(f"{scene_path}/script.txt"):
                    with open(f"{scene_path}/script.txt", "w") as script_text:
                        script_text.write(script_str)
                else:
                    with open(f"{scene_path}/script.txt", "x") as script_text:
                        script_text.write(script_str)

                print("\nScript Generated")
                sleep(1)
                print("\nVoice Generation Started")
                model_dict = show.voice_ids
                name_bank = show.characters
                scene_bank = []
                if script == ['Bad_prompt']:
                    print("Bad Prompt")
                    pass
                else:
                    line_list = []
                    for i, x in enumerate(script):

                        # split_name variable created to detect with lines like "CHARACTER (action)" and change them to
                        # "CHARACTER" for voice assignment
                        split_name = re.split(":| ", x)
                        if (split_name[0] in name_bank) \
                                or ((len(split_name)) > 1
                                    and ((split_name[0] + " " + split_name[1]) in name_bank)):
                            line_list.append(x)
                            char_name = split_name[0]
                            if char_name not in scene_bank:
                                scene_bank.append(char_name)
                    while not line_list:
                        print("\n\nScript Could Not Be Generated :(\n\n")
                        script_str = show.contn('')
                        script = list(script_str.split("\n"))
                        for i, x in enumerate(script):

                            # split_name variable created to detect with lines like "CHARACTER (action)" and change them to
                            # "CHARACTER" for voice assignment
                            split_name = re.split(":| ", x)
                            if (split_name[0] in name_bank) \
                                    or ((len(split_name)) > 1
                                        and ((split_name[0] + " " + split_name[1]) in name_bank)):
                                line_list.append(x)
                                char_name = split_name[0]
                                if char_name not in scene_bank:
                                    scene_bank.append(char_name)
                    else:
                        image_url = show.generate_set(scene_bank)
                        if image_url is None:
                            pass
                        else:
                            script_set = requests.get(image_url).content
                            r = requests.get(image_url)
                            if r.status_code == 200:
                                i = Image.open(io.BytesIO(r.content))
                                i.save(os.path.join(f"{scene_path}", "image.jpg"))
                    count = 0
                    lines = []
                    action_bank = {}
                    audio_uuids = []
                    # Request all voices for loop
                    for i, x in enumerate(script):
                        line = ""
                        char_name = ""
                        if (i + 1 < len(script)) and (script[i-1] == "" and script[i+1] == ""):
                            # this line is an action
                            action_bank[count] = x

                            ##
                            ## ADD CODE TO SEND ACTION TO VIDEO API AND RECIEVE VIDEO
                            ##

                        # split_name variable created to detect with lines like "CHARACTER (action)" and change them to
                        # "CHARACTER" for voice assignment
                        split_name = re.split(":| ", x)

                        # Character line conditional statement
                        if (split_name[0] in name_bank)\
                                or ((len(split_name)) > 1
                                    and ((split_name[0] + " " + split_name[1]) in name_bank)):
                            if split_name[0] in name_bank:
                                char_name = split_name[0]
                            elif ((len(split_name)) > 1) and ((split_name[0] + " " + split_name[1]) in name_bank):
                                char_name = split_name[0] + " " + split_name[1]
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
                            sleep(0.5)
                            audio_uuid = {}
                            text_to_vid_gen = f"{char_name} is talking to the characters in this list: {scene_bank}, " \
                                              f"with the line: {text}"
                            while 'inference_job_token' not in audio_uuid:
                                logging.debug("Error: Could not find inference_job_token key, retrying")
                                audio_uuid = session.post("https://api.fakeyou.com/tts/inference",
                                                          json=dict(uuid_idempotency_token=id_tok,
                                                                    tts_model_token=voicemodel_uuid,
                                                                    inference_text=text)).json()
                                sleep(2)

                            logging.debug("Success: found inference_job_token key")
                            print(f"\r", end="")
                            print(f"Sent {count}/{len(line_list)} ({round(count*100/len(line_list), 0)}% done)", end="")
                            audio_uuid = audio_uuid['inference_job_token']
                            audio_uuids.append(audio_uuid)
                    print("\n")
                    if contin == 2:
                        count = 0
                        prev_length = 0
                    elif contin == 0:
                        count = prev_length
                    # prompt for finish all voices
                    for token in audio_uuids:
                        count += 1
                        audio_url = None
                        for t in range(12000):
                            sleep(0.1)  # check status every second for up to 20 minutes.

                            output = session.get(
                                f"https://api.fakeyou.com/tts/job/{token}").json()
                            if (t % 10) == 0:            # Change the number after modulo (x) to make
                                                        # it print progress every x times
                                print(f"\r", end="")
                                print(f"LINE {count} of {prev_length + len(line_list)}:\tTIME: {t / 10}s, ", "OUTPUT: ",
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
                            print(f"LINE {count} of {prev_length + len(line_list)}:\tTIME: {round(t / 10, 0)}s, ", "OUTPUT: ",
                                  output["state"]["status"])
                            total = sample_rate * num_channels * bytes_per_sample

                            logging.basicConfig(level=logging.INFO)

                            audio_url = f"https://storage.googleapis.com/vocodes-public{audio_url}"

                            logging.info(f"Downloading audio file from: {audio_url}")
                            content = session.get(audio_url).content
                            if not path.exists(f"{scene_path}/line_{count}.wav"):
                                with open(f"{scene_path}/line_{count}.wav", "x") as file:
                                    pass
                            with wave.open(f"{scene_path}/line_{count}.wav", "wb") as file:
                                file.setframerate(sample_rate)
                                file.setnchannels(num_channels)
                                file.setsampwidth(bytes_per_sample)
                                file.writeframesraw(content)
                    play = None
                    while play != 1:
                        play = menu("Play the script?", ["Yes", "No"], 'black')
                        if play == 0:
                            if contin == 0:
                                print(show.old_gen_script)
                            for x in range(prev_length, count):
                                with wave.open(f"{scene_path}/line_{x+1}.wav", "rb") as file:
                                    n = file.getnframes()
                                    content = file.readframes(n)
                                sample = simpleaudio.WaveObject(audio_data=content,
                                                                sample_rate=sample_rate,
                                                                num_channels=num_channels,
                                                                bytes_per_sample=bytes_per_sample)
                                print("{:<30s} ".format(lines[2 * (x-prev_length)]), end="")
                                run_parallel(play_audio, stream_print,
                                             (sample, ), (f"{lines[(2 * ((x-prev_length) + 1)) - 1]}", ))
                                print("\n")
                                sleep(0.5)
                    prev_length = count
                    # print("prev length:", prev_length)
                contin = menu("Continue the script?", ["Yes", "No"], 'black')

