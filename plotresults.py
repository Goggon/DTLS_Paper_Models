import matplotlib.pyplot as plt
import numpy as np
import pathlib



figure_path = pathlib.Path("./figures")

def plot_base_case_vs_case_5(base_case, case_5):
  # plot
  fig, ax = plt.subplots()
  ax.bar(1, base_case[0], width=1, edgecolor="white", linewidth=0.7, color="blue")
  ax.bar(2, case_5[0], width=1, edgecolor="white", linewidth=0.7, color="red")
  ax.bar(4, base_case[1], width=1, edgecolor="white", linewidth=0.7, color="blue")
  ax.bar(5, case_5[1], width=1, edgecolor="white", linewidth=0.7, color="red")
  ax.set_xticks([1.5, 4.5])
  ax.set_xticklabels(["Client Power", "Server Power"])
  ax.set_title('Average power consumption of the system')
  ax.legend(["Base Case", "Case 5"])
  ax.set(xlim=(0, 6))

  #save figure to file
  plt.savefig(figure_path / "Base_case_power.png")

def plot_malicious_user(Chello_power, Ccookie_power):
  # Data for plotting malicious user (Server
  # plot
  fig, ax = plt.subplots()
  ax.bar(1, Ccookie_power, width=1, edgecolor="white", linewidth=0.7, color="blue")
  ax.bar(2, Chello_power, width=1, edgecolor="white", linewidth=0.7, color="red")

  ax.set_xticks([1.5])
  ax.set_xticklabels(["Server Power Consumption"])
  ax.set_title('Malicious user using "Chello" attack')
  ax.legend(["No cookie required", "Cookie required"])
  ax.set(xlim=(0, 3))

  #save figure to file
  plt.savefig(figure_path / "Chello_attack.png")

def plot_malicious_sheartbeat(case_5, sleep, nosleep):
  # plot
  fig, ax = plt.subplots()
  ax.bar(1, case_5[0], width=1, edgecolor="white", linewidth=0.7, color="blue")
  ax.bar(2, nosleep[0], width=1, edgecolor="white", linewidth=0.7, color="red")
  ax.bar(3, sleep[0], width=1, edgecolor="white", linewidth=0.7, color="green")
  ax.bar(5, case_5[1], width=1, edgecolor="white", linewidth=0.7, color="blue")
  ax.bar(6, nosleep[1], width=1, edgecolor="white", linewidth=0.7, color="red")
  ax.bar(7, sleep[1], width=1, edgecolor="white", linewidth=0.7, color="green")

  ax.set_xticks([2, 6])
  ax.set_xticklabels(["Client Power", "Server Power"])
  ax.set_title('Power consumption of the system with malicious\n user using "SHeartbeat" to attack')
  ax.legend(["Case 5", "Sheartbeat without sleep", "SHeartbeat with sleep"])
  ax.set(xlim=(0, 8))

  #save figure to file
  plt.savefig(figure_path / "SHeartbeat_attack.png")

