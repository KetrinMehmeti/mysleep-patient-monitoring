"""Selected data-processing helpers adapted from the original MySleep database script.

The original MySleepdb.py contained database creation, test records and an
absolute development-machine path. This module keeps selected general helpers
without running demo database modifications at import time.
"""

import os
import random
import sqlite3 as sql
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def generate_windowed_avgs(parametro): #function which generates hours from 9PM to 9AM, with a pace of 30 mins
    valori = []
    if parametro == "HR":
        valori = [round(random.uniform(55, 75), 1) for _ in range(24)]
    elif parametro == "PO2":
        valori = [round(random.uniform(93, 99), 1) for _ in range(24)]
    elif parametro == "BP":
        valori = [round(random.uniform(100, 125), 1) for _ in range(24)]
    return valori


def generate_hours_windowed(start_h="21:00"): #function which generates the .txt files for the windowed avgs and 
    #creates the associated path
    base_time = datetime.strptime(start_h, "%H:%M")
    return [(base_time + timedelta(minutes=30*i)).strftime("%H:%M") for i in range(24)]


def save_windowed_avgs(device_id, date, po2_data, hr_data, bp_data, start_h="21:00"):
    base_dir = os.path.join("data", "synthetic", f"device_{device_id}")
    os.makedirs(base_dir, exist_ok=True)

    hours = generate_hours_windowed(start_h)

    def salva(nome, valori):
        path = f"{base_dir}/report_{date}_{nome}.txt"
        with open(path, 'w') as f:
            f.write(" ".join(hours) + "\n")
            f.write(" ".join(str(v) for v in valori) + "\n")
        return path

    po2_path = salva("PO2", po2_data)
    hr_path = salva("HR", hr_data)
    bp_path = salva("BP", bp_data)

    return po2_path, hr_path, bp_path


def leggi_report(path): #funzione che legge i report e li trasforma in un formato leggibile per python
    with open(path, 'r') as f:
        righe = f.readlines()
    # Prima riga: orari (es. "22:00 22:30 ...")
    ore = righe[0].strip().split()
    # Seconda riga: valori
    valori = list(map(float, righe[1].strip().split()))
    return ore, valori


def filtra_dati(ore, valori, start_time_str, end_time_str):
    fmt = "%H:%M:%S" if len(start_time_str.split(":")) == 3 else "%H:%M"
    start = datetime.strptime(start_time_str, fmt).time()
    end = datetime.strptime(end_time_str, fmt).time()

    filtrati_ore = []
    filtrati_valori = []

    for o, v in zip(ore, valori):
        ora = datetime.strptime(o, "%H:%M").time()
        # Considero anche il caso addormentamento oltre la mezzanotte
        if start <= end:
            if start <= ora <= end:
                filtrati_ore.append(o)
                filtrati_valori.append(v)
        else:  # periodo notturno che passa la mezzanotte
            if ora >= start or ora <= end:
                filtrati_ore.append(o)
                filtrati_valori.append(v)
    return filtrati_ore, filtrati_valori


def crea_plot(device_id, summary_date, db_path='MySleep.db', base_dir="plots"):
    import sqlite3 as sql
    conn = sql.connect(db_path)
    c = conn.cursor()

    c.execute("""
    SELECT PO2Path, HRPath, BPPath, FallAsleepTime, WakingUpTime
    FROM DataSummary
    WHERE DeviceID = ? AND SummaryDate = ?
    """, (device_id, summary_date))
    row = c.fetchone()
    conn.close()

    if not row:
        print(" No data found for specified DeviceID and SummaryDate.")
        return

    po2_path, hr_path, bp_path, fall_asleep, wake_up = row

    po2_ore, po2_valori = leggi_report(po2_path)
    hr_ore, hr_valori = leggi_report(hr_path)
    bp_ore, bp_valori = leggi_report(bp_path)

    po2_ore_f, po2_valori_f = filtra_dati(po2_ore, po2_valori, fall_asleep, wake_up)
    hr_ore_f, hr_valori_f = filtra_dati(hr_ore, hr_valori, fall_asleep, wake_up)
    bp_ore_f, bp_valori_f = filtra_dati(bp_ore, bp_valori, fall_asleep, wake_up)

    parametri = [
        ("PO2", po2_ore_f, po2_valori_f, "blue", "%"),
        ("HR", hr_ore_f, hr_valori_f, "red", "bpm"),
        ("BP", bp_ore_f, bp_valori_f, "green", "mmHg")
    ]

    for nome, ore, valori, colore, unita in parametri:
        folder = os.path.join(base_dir, f"device_{device_id}", f"report{nome}")
        os.makedirs(folder, exist_ok=True)

        plt.figure(figsize=(10, 6))
        plt.plot(ore, valori, label=nome, color=colore)
        plt.xlabel("Time")
        plt.ylabel(f"{nome} ({unita})")
        plt.title(f"{nome} trend for Device {device_id} on {summary_date}")
        plt.xticks(rotation=45)
        plt.tight_layout()

        path_grafico = os.path.join(folder, f"{summary_date}_{nome}.png")
        plt.savefig(path_grafico)
        plt.close()
