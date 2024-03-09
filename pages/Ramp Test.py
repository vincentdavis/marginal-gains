import plotly.express as px
import streamlit as st
from cycling_dynamics.critical_power import make_zwo_from_ramp, ramp_test_activity

st.set_page_config(
    page_title="Worst Ramp Ever",
    page_icon="\u1F6B2",
    layout="wide",
    initial_sidebar_state="auto",
)

"""
## The Worst Ramp Test Ever
For questions or comments, contact me on Discord: [Vincent.Davis](discordapp.com/users/vincent.davis)

My goal for this project was to take a rider's power curve, sometimes called Critical Power curve, and build a workout 
to produce that power curve. My initial question was, "Can I build a 20min workout that will produce my 20min 
power profile?" The answer is yes.

As you can imagine, a 20min workout that will produce your 20min profile will never be easy. What this looks like 
will surprise you.

### How the problem is solved:
1. Define a power profile, it must start with 1-second power and end with 20min and contain as many intermediate points 
are desired. Something like: `(sec, power) (1, 1000), (2, 900) (3, 875), (5, 800), (30, 500), (60, 450), (300, 400), (1200, 350)`
2. Interperlate the power profile for each second. Keep in mind that (5, 800) means 800 watts(average) for 5 seconds.
3. We are now ready to calculate the workout.

### The workout:
1. We start from the end of the workout and work toward the start.
2. The workout's end power and last second will be the riders 1 sec critical power = 1000.
3. The next (second to last) will need to satisfy `(1000w + x)/2sec = 900w. x = 800w` To make sense of this, if you did 
1000w for 1 second, then to have a 2-second average power of 900watts, you only need to do 800watts for the second 
second.
4. The third is than, `(1000w + 800w + x)/3sec = 875w. x = 825w`
5. Continue this process until the workout is complete.
6. Now we have ramp power defined for each second of duration from 1-1200seconds
7. The last 30 seconds is a 1-second ramp.
8. Average the power for the second to last 30 seconds. as a segment. 
9. The first 19min is are converted to 1-minute segments, setting the the average power for each segment.

### Corner cases:
. This calculation will sometimes result in the need to do negative power. The power is set to 0 in these cases. Usually 
it is only slightly negative.
. If ridden, the per-second ramp power workout should match the critical power profile. (except for this issue above)
. The workout created with the 1min segments is a close approximation of the critical power profile.

## Get a workout:
. Zwift workouts are defined as a % of FTP. You will get three workouts,
  . Ftp = The value you define below will override your Zwift value during the workout.
  . Ftp = 1. In this case, the workout will define the power you must ride, i.e., 120% of ftp == 120 watts. It's kind of a hack to 
  set the watts.
  . ftp = user, Zwift,  defined ftp. The workout will be defined as a % of the provided FTP, but it will use 
  your Zwift FTP when you ride.
. You can define as many (second, watts) points as you like. Starting with 1 sec and ending with 1200 sec.(20 min) or more.
. Result: 4 files, the three workouts, and the complete data as a CSV file.

"""

with st.form(key="ramp_test"):
    st.markdown("#### Rider Profile")
    name = st.text_input("Name", value="John and Jill")
    ftp = st.number_input("FTP", min_value=10.0, max_value=1000.0, value=250.0)
    st.markdown("##### Profile")
    prof = st.text_area(
        label="Profile [sec, watts]", value="1, 1000\n5, 800\n30, 500\n60, 450\n300, 400\n1200, 350", height=200
    )
    submit = st.form_submit_button("Submit")

if submit:
    with st.spinner("Processing..."):
        profile = prof.split("\n")
        profile = [x.split(",") for x in profile]
        profile = [(int(x[0]), int(x[1])) for x in profile]
        print(profile)
        df, dfwko = ramp_test_activity(profile, ftp=ftp)
        wko1 = make_zwo_from_ramp(dfwko, filename=None, name=f"{name}_ftp_{ftp}", ftp=ftp)
        wko2 = make_zwo_from_ramp(dfwko, filename=None, name=f"{name}_ftp_1", ftp=1)
        wko_user = make_zwo_from_ramp(dfwko, filename=None, name=f"{name}_ftp_1", ftp=None)

        st.download_button(
            label="Full data as CSV",
            data=df[[c for c in df.columns if "power_seconds" not in c]].to_csv(index=False).encode("utf-8"),
            file_name=f"ramp_test_{name}.csv",
            mime="text/csv",
        )
        st.download_button(
            label=f"Download WKO with ftp set to {ftp}",
            data=wko1.encode("utf-8"),
            file_name=f"ramp_test_{name}_ftp_{ftp}.zwo",
            mime="text/csv",
        )
        st.download_button(
            label="Download WKO with ftp set to 1",
            data=wko2.encode("utf-8"),
            file_name=f"ramp_test_{name}_ftp_1.zwo",
            mime="text/csv",
        )
        st.download_button(
            label="Download WKO with ftp set to in game ftp",
            data=wko_user.encode("utf-8"),
            file_name=f"ramp_test_{name}_ftp_user.zwo",
            mime="text/csv",
        )

    power_curve = px.line(df, x="seconds", y=["power", "ramp_power"], title="Critical Power and Ramp test power")
    st.plotly_chart(power_curve, theme="streamlit", use_container_width=True)
    bined_curve = px.line(df, x="seconds", y=["power", "bin_power"], title="Critical Power and Workout power")
    st.plotly_chart(bined_curve, theme="streamlit", use_container_width=True)
    result_curve = px.line(
        df, x="seconds", y=["power", "WKO Critical Power"], title="Critical Power VS Workout Critical Power"
    )
    st.plotly_chart(result_curve, theme="streamlit", use_container_width=True)