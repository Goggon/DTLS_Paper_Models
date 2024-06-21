# About
This repository is for reproduction of the figures 12, 13 and 14 from the article Modelling and Analysis of DTLS: Power
Consumption, and Attacks.

This repository also contains the student project report "IoT Power Consumption & DTLS Modeling" that the paper is based upon and references. Be aware that some aspects of the report do not mirror the later findings in the article.

## reproduction of figures
Firstly, the needed pip packages used in the scripts can be gotten via the command:
```
pip install -r requirements.txt
```

Then run the following command with the path to the UPPAAL installation directory as an argument:
```
generate.py --uppaal PATH_TO_UPPAAL
```

The figures will be generated in the `figures` directory.
- `Base_case_power.png` = figure 11
- `Chello_attack.png` = figure 12
- `SHeartbeat_attack.png` = figure 13

## run symbolic verification queries
Run the following command with the path to the UPPAAL installation directory as an argument:
```
run_symbolic.py --uppaal PATH_TO_UPPAAL
```

This runs the model `NoHeartBeat.xml` with the quries in `NoHeartbeatSymbolic.q`

## Info about the models
The models are located in the `models` directory. The models are the same as the ones used in the paper.

In the global declarations of the models, there is a variable called `enablePerformanceMeasures` which enables or disables the use of the symbolic model checking.
