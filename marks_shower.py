import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
my_norm = Normalize(vmin=0, vmax=20)
my_cmap = cm.get_cmap('jet')


ut_marksheet = pd.read_csv('UT2.csv')
ut_marksheet = ut_marksheet.fillna(0)
st.set_page_config(layout='wide')
st.title("TE UT1 and UT2 analysis")
plt.style.use('dark_background')
st.sidebar.header('Marksheet')


def get_hi_low(df, ut="UT1"):
    sub = ['DWM', 'TCS', 'SE', 'CN']
    diction = {}
    for x in sub:
        column_name = x + ut
        data = df[column_name]
        diction[x] = (data.max(), data.min())
    return diction


def all_sub_hi_low_plot(df, ut="UT1", figsize=(10, 10)):
    fig, ax = plt.subplots(figsize=figsize)
    plt.title('All Subjects High and Low Marks')
    marks = get_hi_low(df, ut)
    marks = pd.DataFrame(marks, index=['High', 'Low'])
    ax = plt.boxplot(marks.values, labels=marks.keys())
    plt.xticks(rotation=90)
    plt.show()
    return fig


def get_diction(values):
    diction = {}
    # count the number of occurances of each value
    for i in values:
        if i in diction:
            diction[i] += 1
        else:
            diction[i] = 1
    return diction


def plot_overall_sub(df, subject, UT_no='UT1', figsize=(10, 10)):
    fig, ax = plt.subplots(figsize=figsize)
    column_name = subject + UT_no
    plt.title('overall students and the marks')
    data = sorted(df[column_name])
    diction = get_diction(data)
    ax = plt.bar(x=diction.keys(), height=diction.values(),
                 color=my_cmap(my_norm([int(x) for x in diction.keys()])))
    plt.xlabel(f'{subject} marks')
    plt.ylabel('Number of students')
    plt.legend()
    return fig


def plot_marks(roll_no, df, show_avg=True, display_only_avg=False, figsize=(10, 10)):
    data = df[df['Roll No'] == roll_no]
    if show_avg == True:
        drop_cols = ['Roll No', 'Name of Student']
    else:
        drop_cols = ['Roll No', 'Name of Student',
                     'CNAvg', 'DWMAvg', 'TCSAvg', 'SEAvg']
    fig, ax = plt.subplots(figsize=figsize)

    if display_only_avg == True:
        show_cols = ['CNAvg', 'DWMAvg', 'TCSAvg', 'SEAvg']
        plt.title(f'Marks of {data["Name of Student"].values[0]}')
        ax = plt.bar(show_cols, data[show_cols].values[0], color=my_cmap(
            my_norm(data.drop(drop_cols, axis=1).values[0])))
        # plt.legend(['CNAvg', 'DWMAvg', 'TCSAvg', 'SEAvg'])
        return fig

    plt.title(f'Marks of {data["Name of Student"].values[0]}')
    plt.xticks(rotation=90)
    ax = plt.bar(data.drop(drop_cols, axis=1).columns,
                 data.drop(drop_cols, axis=1).values[0], color=my_cmap(
        my_norm(data.drop(drop_cols, axis=1).values[0])))
    plt.xlabel('Subjects')
    plt.ylabel('Marks')
    return fig


def show_marksheet():
    return st.container(st.table(ut_marksheet))


def show_individual_marks():
    st.subheader("Individual Marks")
    st.write("Enter the roll number of the student whose marks you want to see")
    rolls = st.slider('Roll No', 1, 77)
    show_avg = st.checkbox("Show average marks")
    display_only_avg = st.checkbox("Display only average marks")
    width = st.sidebar.slider("plot width", 0.1, 25., 13.53)
    height = st.sidebar.slider("plot height", 0.1, 25., 5.54)
    figs = plot_marks(rolls, ut_marksheet, show_avg,
                      display_only_avg, figsize=(width, height))
    st.pyplot(figs, use_container_width=False)


def view_sub_stats():
    st.subheader('Subject statistics')
    subject = st.selectbox('Subject', ['CN', 'DWM', 'TCS', 'SE'])
    UTNO = st.selectbox('UT NO', ['UT1', 'UT2', 'Avg'])
    width = st.sidebar.slider("plot width", 0.1, 25., 13.53)
    height = st.sidebar.slider("plot height", 0.1, 25., 5.54)
    fig = plot_overall_sub(
        ut_marksheet, subject, UT_no=UTNO, figsize=(width, height))
    st.pyplot(fig, use_container_width=False)


def show_all_high_low():
    st.subheader('All high and low marks')
    UTNO = st.selectbox('UT NO', ['UT1', 'UT2', 'Avg'])
    width = st.sidebar.slider("plot width", 0.1, 25., 13.53)
    height = st.sidebar.slider("plot height", 0.1, 25., 5.54)
    fig = all_sub_hi_low_plot(ut_marksheet, ut=UTNO, figsize=(width, height))
    return st.pyplot(fig, use_container_width=False)


subject = st.sidebar.radio("Select subject", [
    'show_marks_individual_marks', 'show_all_subjects_high_low', 'view_subject_statistics', 'show_data'])

if subject == 'show_data':
    show_marksheet()
elif subject == 'show_marks_individual_marks':
    show_individual_marks()
elif subject == 'view_subject_statistics':
    view_sub_stats()
elif subject == 'show_all_subjects_high_low':
    show_all_high_low()
