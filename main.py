import json, requests, logging, simpleaudio, wave, string
from show_chars import Show
from pwinput import pwinput
from time import sleep
from os import path, mkdir
from numpy import random
import random as rd
from jsmin import jsmin


def token_gen():
    """
    Generates a random token string for FakeYou requests
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


if __name__ == '__main__':

    #  Open the json config file
    with open('userinfo.json') as json_file:
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
        username = input("FakeYou Username or email (Press enter/return to skip this step, but the processing will be "
                         "slower without a premium account)")
        if username != '':
            password = pwinput()
    else:
        username = config_dict["Fakeyou"]["User"]
        if config_dict["FakeYou"]["Pass"] == "default":
            password = pwinput(prompt=f'FakeYou Password for {username}: ')
        else:
            password = config_dict["Fakeyou"]["Pass"]

    #  Define global variables for wave files
    sample_rate = 16000
    num_channels = 2
    bytes_per_sample = 2

    #  Define the ID Keys for The OpenAI and FakeYou APIs
    if username == '' or password == '':
        print("FakeYou Login Credentials Skipped\n")
        pass
    else:
        ljson = {"username_or_email": username, "password": password}
        # login payload

        logging.debug("Sending Login request")

        loginHandler = requests.Session().post("https://api.fakeyou.com/login", json=ljson)
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
                sjson = requests.Session().get("https://api.fakeyou.com/session").json()
                print("Success!")

            elif lrjson["success"] is False and lrjson["error_type"] == "InvalidCredentials":
                # login failed
                logging.critical("FALSE email/password, raising error.")

        elif loginHandler.status_code == 429:
            # ip ban !
            logging.critical("IP IS BANNED (caused by login request)")

    #  Prompt the command line to ask for a script
    show = Show(config_dict['Show'], config_dict['Characters'][f'{config_dict["Show"]}'])
    prompt = input(f"Write a '{show.show}' prompt: ")
    script = show.write(openai_key, prompt)
    print(script)
    print("\nGeneration Started")
    model_dict = show.voice_ids
    name_bank = show.characters
    scene_bank = []
    if script == ['Bad_prompt']:
        print("Bad Prompt, BOZO")
        pass
    else:
        line_list = []
        for i, x in enumerate(script):
            if x in name_bank:
                line_list.append(x)
        count = 0
        lines = []
        for i, x in enumerate(script):
            line = ""
            if x in name_bank:
                if x not in scene_bank:
                    scene_bank.append(x)
                count += 1
                line = script[i+1]
                lines.append(f"{x}")
                lines.append(f"{script[i+1]}")
                # send the line to FakeYou api
                voicemodel_uuid = model_dict[x]
                text = line
                id_tok = token_gen()
                audio_uuid = requests.post("https://api.fakeyou.com/tts/inference",
                                           json=dict(uuid_idempotency_token=id_tok, tts_model_token=voicemodel_uuid,
                                                     inference_text=text)).json()['inference_job_token']
                print("\n")
                audio_url = None
                for t in range(1200):
                    sleep(1)  # check status every second for up to 20 minutes.
                    output = requests.get(
                        f"https://api.fakeyou.com/tts/job/{audio_uuid}").json()
                    if (t % 10) == 0:
                        print(f"\r", end="")
                        print(f"LINE {count} of {len(line_list)}:\tTIME: {t}s, ", "OUTPUT: ", output["state"]["status"],
                              end="")
                    if output["state"]["status"] == "complete_success":
                        audio_url = output["state"]["maybe_public_bucket_wav_audio_path"]
                        break
                    elif output["state"]["status"] == "dead" or output["state"]["status"] == "complete_failure":
                        break
                if audio_url is None:
                    print("\n", "Production Failed")
                else:
                    print(f"\r", end="")
                    print(f"LINE {count} of {len(line_list)}:\tTIME: {t}s, ", "OUTPUT: ", output["state"]["status"])
                    total = sample_rate * num_channels * bytes_per_sample

                    logging.basicConfig(level=logging.INFO)

                    audio_url = f"https://storage.googleapis.com/vocodes-public{audio_url}"

                    logging.info(f"Downloading audio file from: {audio_url}")
                    content = requests.get(audio_url).content
                    if not path.exists(f"scene/line_{count}.wav"):
                        if not path.isdir("scene"):
                            mkdir("scene")
                        with open(f"scene/line_{count}.wav", "x") as file:
                            pass
                    with wave.open(f"scene/line_{count}.wav", "wb") as file:
                        file.setframerate(sample_rate)
                        file.setnchannels(num_channels)
                        file.setsampwidth(bytes_per_sample)
                        file.writeframesraw(content)
        play = None
        while play != "N":
            play = input("Play the script?(Y/N)")
            if play == "Y":
                for x in range(0, count):
                    with wave.open(f"scene/line_{x+1}.wav", "rb") as file:
                        n = file.getnframes()
                        content = file.readframes(n)
                    print(lines[2 * x], ":\t\t", lines[(2 * (x + 1)) - 1])
                    sample = simpleaudio.WaveObject(audio_data=content,
                                                    sample_rate=sample_rate,
                                                    num_channels=num_channels,
                                                    bytes_per_sample=bytes_per_sample)
                    control = sample.play()
                    control.wait_done()
                    sleep(1)
            else:
                pass
