import argparse
import pathlib
import os
import subprocess
from uppaal_variable_modifier import modify_variables, reset_variables

parser = argparse.ArgumentParser(description="Run Uppaal models")
parser.add_argument("--uppaal", "-u", help="Path to Uppaal installation", required=True)
args = parser.parse_args()

uppaal_path = pathlib.Path(args.uppaal)
model_folder = pathlib.Path("./Models")
verifyta_path = str(uppaal_path / "bin" / "verifyta")
base_command = [verifyta_path, "-s", "-q"]

model = "NoHeartbeat.xml"
query = "NoHeartBeatSymbolic.q"

command = base_command + [str((model_folder / model).absolute()), str((model_folder / query).absolute())]

variables = {"EPM": "const bool enablePerformanceMeasures = false;"}
cl = modify_variables((model_folder / model).absolute(), variables)
try:
    subprocess.run(command)
finally:
    reset_variables(model_folder / model, cl)