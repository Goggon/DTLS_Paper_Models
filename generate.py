import subprocess
import pathlib
import os
import argparse
import pyparsing as pp
from plotresults import plot_base_case_vs_case_5, plot_malicious_user, plot_malicious_sheartbeat
from uppaal_variable_modifier import modify_variables, reset_variables, \
                                     add_new_line_under_marks, remove_changed_lines        


parser = argparse.ArgumentParser(description="Run Uppaal models")
parser.add_argument("--uppaal", "-u", help="Path to Uppaal installation", required=True)
args = parser.parse_args()

uppaal_path = pathlib.Path(args.uppaal)
model_folder = pathlib.Path("./Models")
verifyta_path = uppaal_path / "bin" / "verifyta"
base_command = [verifyta_path, "-s", "-q"]


# parser to extract value from E(max) queries
parser = (  pp.Literal("(")+
            pp.pyparsing_common.number+
            pp.Literal(f"runs) E(max) = ")+
            pp.pyparsing_common.number+
            pp.Literal("±")+
            pp.pyparsing_common.number+
            pp.Literal("(")+
            pp.pyparsing_common.number+
            pp.Literal("% CI)")).setParseAction(lambda s,l,t: (t[3]))

def run_model_2_E_max(command):
    res = subprocess.run(command, capture_output=True)
    stdout = res.stdout.decode()
    lines = [r for r in stdout.split('\n') if r != ""]
    lines = [r for r in lines if r != "\r"]
    if "Formula is satisfied" in stdout:
        client = lines[2]
        server = lines[6]
        if "≈" in client:
            client_power = 0
        else:
            client_power = parser.parseString(client)[0]
        server_power = parser.parseString(server)[0]
        return (client_power, server_power)
    raise Exception("Model did not satisfy formula")

def gen_base_case_vs_case_5():
    try:
        results: dict = {}
        base_case = ("NoHeartbeat.xml", "NoHeartBeatPower.q")
        case_5_day = ("ServerHeartbeat.xml", "SimFor12h.q")
        case_5_night = ("noHeartbeat.xml", "SimFor12h.q")

        # run base case
        base_case_command = base_command + [str((model_folder / base_case[0]).absolute()), str((model_folder / base_case[1]).absolute())]
        results["base_case"] = run_model_2_E_max(base_case_command)
        
        # run case 5
        # day
        case_5_day_command = base_command + [str((model_folder / case_5_day[0]).absolute()), str((model_folder / case_5_day[1]).absolute())]
        results["case_5_day"] = run_model_2_E_max(case_5_day_command)

        #night
        variables = {"psk": "bool psk[N] = {true};",
                    "requestInterval": "const int requestInterval = 40000;"}
        cl = modify_variables(model_folder / case_5_night[0], variables)

        case_5_night_command = base_command + [str((model_folder / case_5_night[0]).absolute()), str((model_folder / case_5_night[1]).absolute())]
        results["case_5_night"] = run_model_2_E_max(case_5_night_command)

        #combine night and day
        results["case_5"] = (results["case_5_day"][0] + results["case_5_night"][0],
                            results["case_5_day"][1] + results["case_5_night"][1])

        results.pop("case_5_day")
        results.pop("case_5_night")
        print(results)
        plot_base_case_vs_case_5(results["base_case"], results["case_5"])
    except:
        print("No good")
    finally:
        reset_variables(model_folder / case_5_night[0], cl)

def gen_malicious_user_server():
    try:
        results: dict = {}
        malicious_case = ("NoHeartbeat.xml", "NoHeartBeatPower.q")
        malicious_user_command = base_command + [str((model_folder / malicious_case[0]).absolute()), str((model_folder / malicious_case[1]).absolute())]
        # change variables
        variables = {"MUser": "system Client0,Server0, Router0, User0, MUser;"}
        new_line = {"MTrans": """<label kind="synchronisation" x="-170" y="-136">Chello[id]!</label>"""}
        cl = modify_variables(model_folder / malicious_case[0], variables)
        al = add_new_line_under_marks(model_folder / malicious_case[0], new_line)

        # run
        results["Chello"] = run_model_2_E_max(malicious_user_command)

        # change variables
        other_variables = {"SentCookies": "bool SentCookies = true;",
                           "maxRT": "const int maxRT = 0;",
                           "RTTime": "const int RTTime = 100;",
                           "MUser": "system Server0, Router0, MUser;"}
        
        sent_cookie_line = {"SentCTrans": """<label kind="assignment" x="-10522" y="-11475">SentCookies = true</label>"""}
        Ccookie_line = {"MTrans": """<label kind="synchronisation" x="-170" y="-136">Ccookie[id]!</label>"""}
        al2 = add_new_line_under_marks(model_folder / malicious_case[0], sent_cookie_line)
        cl2 = modify_variables(model_folder / malicious_case[0], other_variables)
        modify_variables(model_folder / malicious_case[0], Ccookie_line)

        # run
        results["Ccookie"] = run_model_2_E_max(malicious_user_command)

        print(results)
        plot_malicious_user(results["Chello"][1], results["Ccookie"][1])
    except:
        print("No good")
    finally:
        pass
        # reset
        reset_variables(model_folder / malicious_case[0], cl2)
        remove_changed_lines(model_folder / malicious_case[0], al2)
        remove_changed_lines(model_folder / malicious_case[0], al)
        reset_variables(model_folder / malicious_case[0], cl)

def gen_malicious_sheartbeat():
    try:
        results: dict = {}
        case_5_day = ("ServerHeartbeat.xml", "SimFor12h.q")
        case_5_night = ("noHeartbeat.xml", "SimFor12h.q")
        case_malicious_sleep = ("ClientSleep.xml", "SimFor12h.q")
        case_malicious_nosleep = ("ServerHeartbeat.xml", "SimFor12h.q")
        
        # run case 5
        # day
        case_5_day_command = base_command + [str((model_folder / case_5_day[0]).absolute()), str((model_folder / case_5_day[1]).absolute())]
        results["case_5_day"] = run_model_2_E_max(case_5_day_command)

        #night
        variables = {"psk": "bool psk[N] = {true};",
                    "requestInterval": "const int requestInterval = 40000;"}
        case_5_cl = modify_variables(model_folder / case_5_night[0], variables)

        case_5_night_command = base_command + [str((model_folder / case_5_night[0]).absolute()), str((model_folder / case_5_night[1]).absolute())]
        results["case_5_night"] = run_model_2_E_max(case_5_night_command)

        variables = {"MUser": "system Client0,Server0, Router0, User0, MUser;"}
        #run sleep
        sleep_cl = modify_variables(model_folder / case_malicious_sleep[0], variables)
        case_malicious_sleep_command = base_command + [str((model_folder / case_malicious_sleep[0]).absolute()), str((model_folder / case_malicious_sleep[1]).absolute())]
        results["case_malicious_sleep"] = run_model_2_E_max(case_malicious_sleep_command)

        #run no sleep
        nosleep_cl = modify_variables(model_folder / case_malicious_nosleep[0], variables)
        case_malicious_nosleep_command = base_command + [str((model_folder / case_malicious_nosleep[0]).absolute()), str((model_folder / case_malicious_nosleep[1]).absolute())]
        results["case_malicious_nosleep"] = run_model_2_E_max(case_malicious_nosleep_command)

        results["case_5"] = (results["case_5_day"][0] + results["case_5_night"][0],
                             results["case_5_day"][1] + results["case_5_night"][1])
        
        results["case_malicious_sleep"] = (results["case_malicious_sleep"][0]+results["case_5_night"][0],
                                           results["case_malicious_sleep"][1]+results["case_5_night"][1])

        results["case_malicious_nosleep"] = (results["case_malicious_nosleep"][0]+results["case_5_night"][0],
                                             results["case_malicious_nosleep"][1]+results["case_5_night"][1])
        
        results.pop("case_5_day")
        results.pop("case_5_night")
        print(results)
        plot_malicious_sheartbeat(results["case_5"], results["case_malicious_sleep"], results["case_malicious_nosleep"])
    except:

        pass
    finally:
        reset_variables(model_folder / case_5_night[0], case_5_cl)
        reset_variables(model_folder / case_malicious_sleep[0], sleep_cl)
        reset_variables(model_folder / case_malicious_nosleep[0], nosleep_cl)
        pass

if __name__ == "__main__":
    # prepare directories
    if not os.path.exists("figures"):
        os.makedirs("figures")

    gen_base_case_vs_case_5()
    
    gen_malicious_user_server()

    gen_malicious_sheartbeat()