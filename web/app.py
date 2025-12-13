from flask import Flask, render_template, request
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
import io
import base64
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

import tempfile

# Cache directory
CACHE_DIR = os.path.join(tempfile.gettempdir(), 'f1_cache')
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

ff1.Cache.enable_cache(CACHE_DIR)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            year = int(request.form.get('year', 2021))
            gp = request.form.get('gp', 'British GP')
            session = request.form.get('session', 'Q')
            driver1 = request.form.get('driver1', 'HAM')
            driver2 = request.form.get('driver2', 'VER')
            dist_min = int(request.form.get('dist_min', 4800))
            dist_max = int(request.form.get('dist_max', 5500))

            # --- Analysis Logic ---
            plt.clf() # Clear previous plot
            plt.rcParams["figure.figsize"] = [13, 4]
            plt.rcParams["figure.autolayout"] = True
            
            # Load session
            race_session = ff1.get_session(year, gp, session)
            race_session.load()
            laps = race_session.laps

            # Get driver data
            laps_d1 = laps.pick_driver(driver1)
            laps_d2 = laps.pick_driver(driver2)

            tel_d1 = laps_d1.pick_fastest().get_car_data().add_distance()
            tel_d2 = laps_d2.pick_fastest().get_car_data().add_distance()

            team_d1 = laps_d1.reset_index().loc[0, 'Team']
            team_d2 = laps_d2.reset_index().loc[0, 'Team']

            # Process telemetry
            for tel in [tel_d1, tel_d2]:
                tel.loc[tel['Brake'] > 0, 'CurrentAction'] = 'Brake'
                tel.loc[tel['Throttle'] == 100, 'CurrentAction'] = 'Full Throttle'
                tel.loc[(tel['Brake'] == 0) & (tel['Throttle'] < 100), 'CurrentAction'] = 'Cornering'
                tel['ActionID'] = (tel['CurrentAction'] != tel['CurrentAction'].shift(1)).cumsum()

            actions_d1 = tel_d1[['ActionID', 'CurrentAction', 'Distance']].groupby(['ActionID', 'CurrentAction']).max('Distance').reset_index()
            actions_d2 = tel_d2[['ActionID', 'CurrentAction', 'Distance']].groupby(['ActionID', 'CurrentAction']).max('Distance').reset_index()

            actions_d1['Driver'] = driver1
            actions_d2['Driver'] = driver2

            for actions in [actions_d1, actions_d2]:
                actions['DistanceDelta'] = actions['Distance'] - actions['Distance'].shift(1)
                actions.loc[0, 'DistanceDelta'] = actions.loc[0, 'Distance']

            all_actions = pd.concat([actions_d1, actions_d2])

            # Speed comparison
            avg_speed_d1 = np.mean(tel_d1['Speed'].loc[(tel_d1['Distance'] >= dist_min) & (tel_d1['Distance'] >= dist_max)])
            avg_speed_d2 = np.mean(tel_d2['Speed'].loc[(tel_d2['Distance'] >= dist_min) & (tel_d2['Distance'] >= dist_max)])
            
            # Helper to safely get value or 0 if nan
            def safe_val(val):
                return val if not np.isnan(val) else 0

            avg_speed_d1 = safe_val(avg_speed_d1)
            avg_speed_d2 = safe_val(avg_speed_d2)

            if avg_speed_d1 > avg_speed_d2:
                speed_text = f"{driver1} {round(avg_speed_d1 - avg_speed_d2, 2)}km/h faster"
            else:
                speed_text = f"{driver2} {round(avg_speed_d2 - avg_speed_d1, 2)}km/h faster"

            # Plotting
            fig, ax = plt.subplots(2)
            
            # Speed Trace
            color_d1 = ff1.plotting.get_team_color(team_d1, session=race_session)
            color_d2 = ff1.plotting.get_team_color(team_d2, session=race_session)

            ax[0].plot(tel_d1['Distance'], tel_d1['Speed'], label=driver1, color=color_d1)
            ax[0].plot(tel_d2['Distance'], tel_d2['Speed'], label=driver2, color=color_d2)
            ax[0].text(dist_min + 15, 200, speed_text, fontsize=15)
            ax[0].set(ylabel='Speed')
            ax[0].legend(loc="lower right")
            ax[0].set_xlim(dist_min, dist_max)

            # Telemetry Bar
            telemetry_colors = {'Full Throttle': 'green', 'Cornering': 'grey', 'Brake': 'red'}
            
            for driver in [driver1, driver2]:
                driver_actions = all_actions.loc[all_actions['Driver'] == driver]
                previous_action_end = 0
                for _, action in driver_actions.iterrows():
                    ax[1].barh(
                        [driver], 
                        action['DistanceDelta'], 
                        left=previous_action_end, 
                        color=telemetry_colors[action['CurrentAction']]
                    )
                    previous_action_end += action['DistanceDelta']

            plt.xlabel('Distance')
            plt.gca().invert_yaxis()
            ax[1].spines['top'].set_visible(False)
            ax[1].spines['right'].set_visible(False)
            ax[1].spines['left'].set_visible(False)
            
            labels = list(telemetry_colors.keys())
            handles = [plt.Rectangle((0,0),1,1, color=telemetry_colors[label]) for label in labels]
            ax[1].legend(handles, labels)
            ax[1].set_xlim(dist_min, dist_max)

            # Save to buffer
            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            
            return render_template('index.html', plot_url=plot_url, 
                                   year=year, gp=gp, session=session, 
                                   driver1=driver1, driver2=driver2, 
                                   dist_min=dist_min, dist_max=dist_max)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
