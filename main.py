#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

header = st.beta_container()
FIGURE_1 = st.beta_container()
FIGURE_2 = st.beta_container()
FIGURE_3 = st.beta_container()
DESCRIPTION_DATA = st.beta_container()

@st.cache
def load_data():
    df = pd.read_csv('Data/data_prepared')
    return df
df=load_data()

with header:
    st.title('Gender in economics journals')

    anzeige=st.selectbox('What features do you want to explore?', ('Publication', 'Citations', 'JEL Codes'))

with st.sidebar:
    st.title('Journals')
    lst_journals =[]

    if st.checkbox('Average over all journals (All)'):
        lst_journals.append('All')

    if st.checkbox('American Economic Review (AER)'):
        lst_journals.append('AER')

    if st.checkbox('Journal of Political Economy (JPE)'):
        lst_journals.append('JPE')

    if st.checkbox('Quarterly Journal of Economics (QJE)'):
        lst_journals.append('QJE')

    if st.checkbox('Econometrica (ECO)'):
        lst_journals.append('ECO')

    if st.checkbox('Review of Economic Studies (REStud)'):
        lst_journals.append('REStud')

    if st.checkbox('Economic Journal (EJ)'):
        lst_journals.append('EJ')

    if st.checkbox('Journal of the European Economic Association (JEEA)'):
        lst_journals.append('JEEA')

    if st.checkbox('Review of Economics and Statistics (REStat)'):
        lst_journals.append('REStat')

    if st.checkbox('European Economic Review (EER)'):
        lst_journals.append('EER')

    if st.checkbox('Journal of Public Economics (JPubE)'):
        lst_journals.append('JPubE')

    if st.checkbox('Journal of Finance (JoF)'):
        lst_journals.append('JoF')

    if st.checkbox('Journal of Monetary Economics (JME)'):
        lst_journals.append('JME')

    if st.checkbox('Review of Financial Studies (RFS)'):
        lst_journals.append('RFS')

    if st.checkbox('Journal of Labor Economics (JOLE)'):
        lst_journals.append('JOLE')

    if st.checkbox('Journal of Human Ressources (JHR)'):
        lst_journals.append('JHR')

    if st.checkbox('Labour Economics (Labour)'):
        lst_journals.append('Labour')

    if st.checkbox('International Economic Review (IER)'):
        lst_journals.append('IER')

    if len(lst_journals)==0: lst_journals.append('All')
with FIGURE_1:
    st.write('')

    ### First Figure Publishing Success
    if anzeige=='Publication':

        st.write('Figure 1: Share of articles with at least one female author')
        df_fem_share = pd.DataFrame(df.groupby(['Year', 'Journal']).women.mean()).reset_index(level=['Year', 'Journal'])
        mitelwert = pd.DataFrame(df.groupby(['Year']).women.mean()).reset_index(level=['Year'])
        mitelwert['Journal'] = 'All'
        df_fem_share = df_fem_share.append(mitelwert)
        df_fem_share.women=np.round(df_fem_share.women, 2)

        for i in lst_journals:
            try:
                df_draw = df_draw.append(df_fem_share[df_fem_share.Journal == i])
            except:
                df_draw = df_fem_share[df_fem_share.Journal == i]

        fig_1 = px.line(df_draw, x='Year', y='women', color='Journal', labels={'women':'Share of Articles with at least one female author'})
        fig_1.update_layout(xaxis=dict(tickmode='linear', tick0=1991, dtick=3))
        fig_1.update_traces(mode="markers+lines", hovertemplate=None)
        fig_1.update_layout(hovermode="x unified", height=600, width=800)
        st.plotly_chart(fig_1)

    ### First Figure Citations
    if anzeige == 'Citations':
        st.write('Figure 1: Mean number of citations by gender')
        df_cit_gender = pd.DataFrame(df.groupby(['Year', 'Journal', 'women']).WoS.mean()).reset_index(level=['Year', 'Journal', 'women'])
        mitelwert = pd.DataFrame(df.groupby(['Year', 'women']).WoS.mean()).reset_index(level=['Year', 'women'])
        mitelwert['Journal'] = 'All'
        df_cit_gender = df_cit_gender.append(mitelwert)
        df_cit_gender.WoS = np.round(df_cit_gender.WoS, 0)
        df_cit_gender['Journal_gender'] = ""
        for i in range(df_cit_gender.shape[0]):
            if df_cit_gender.iloc[i, df_cit_gender.columns.get_loc('women')] == 1.0:
                df_cit_gender.iloc[i, df_cit_gender.columns.get_loc('Journal_gender')] = df_cit_gender.iloc[
                                                                                             i, df_cit_gender.columns.get_loc(
                                                                                                 'Journal')] + ' Women'
            else:
                df_cit_gender.iloc[i, df_cit_gender.columns.get_loc('Journal_gender')] = df_cit_gender.iloc[
                                                                                             i, df_cit_gender.columns.get_loc(
                                                                                                 'Journal')] + ' Men'

        for i in lst_journals:
            try:
                df_draw_1 = df_draw_1.append(df_cit_gender[df_cit_gender.Journal == i])
            except:
                df_draw_1 = df_cit_gender[df_cit_gender.Journal == i]

        fig_1_cit = px.line(df_draw_1, x='Year', y='WoS', color='Journal_gender', labels={'WoS':'Mean WoS citations'})
        fig_1_cit.update_layout(xaxis=dict(tickmode='linear', tick0=1991, dtick=3))
        fig_1_cit.update_traces(mode="markers+lines", hovertemplate=None)
        fig_1_cit.update_layout(hovermode="x unified", height=600, width=800)
        st.plotly_chart(fig_1_cit)

    ### First Figure JEL
    if anzeige == 'JEL Codes':
        st.write('Figure 1: Share of articles in JEL code by gender')
        df_JEL = df[['Journal', 'women', 'JEL_A', 'JEL_B', 'JEL_C', 'JEL_D', 'JEL_E', 'JEL_F', 'JEL_G', 'JEL_H', 'JEL_I',
                     'JEL_J', 'JEL_K', 'JEL_L', 'JEL_M', 'JEL_N', 'JEL_O', 'JEL_P', 'JEL_Q', 'JEL_R', 'JEL_Y', 'JEL_Z']]
        df_JEL_d = pd.DataFrame(df_JEL.groupby(['Journal', 'women']).mean()).reset_index(level=['Journal', 'women'])
        df_JEL_d = pd.melt(df_JEL_d, id_vars=['Journal', 'women'], var_name='JEL', value_name='share_JEL')
        mitelwert = pd.DataFrame(df_JEL.groupby(['women']).mean()).reset_index(level=['women'])
        mitelwert = pd.melt(mitelwert, id_vars=['women'], var_name='JEL', value_name='share_JEL')
        mitelwert['Journal'] = 'All'
        df_JEL_d = df_JEL_d.append(mitelwert)
        for i in lst_journals:
            try:
                df_draw_JEL_1 = df_draw_JEL_1.append(df_JEL_d[df_JEL_d.Journal == i])
            except:
                df_draw_JEL_1 = df_JEL_d[df_JEL_d.Journal == i]
        df_draw_JEL_1 = df_draw_JEL_1[['women', 'JEL', 'share_JEL']]
        df_draw_JEL_1 = pd.DataFrame(df_draw_JEL_1.groupby(['women', 'JEL']).mean()).reset_index(level=['women', 'JEL'])
        df_draw_JEL_1.share_JEL = np.round(df_draw_JEL_1.share_JEL, 2)

        fig_JEL_1 = go.Figure(data=[
            go.Bar(name='Women', x=df_draw_JEL_1[df_draw_JEL_1.women == 1].JEL.value_counts().sort_index().index,
                   y=df_draw_JEL_1[df_draw_JEL_1.women == 1].share_JEL),
            go.Bar(name='Men', x=df_draw_JEL_1[df_draw_JEL_1.women == 1].JEL.value_counts().sort_index().index,
                   y=df_draw_JEL_1[df_draw_JEL_1.women == 0].share_JEL)
        ])
        # Change the bar mode
        fig_JEL_1.update_layout(barmode='group', height=600, width=800)
        st.plotly_chart(fig_JEL_1)

with FIGURE_2:
    ### Second Figure Publishing Success
    if anzeige == 'Publication':
        st.write('Figure 2: Share of female authors')
        df_h = df[['Year', 'Journal', 'number_authors', 'number_fem_aut']]
        share_fem_aut = pd.DataFrame(df_h.groupby(['Year', 'Journal']).sum()).reset_index(level=['Year', 'Journal'])
        share_fem_aut['share_fem_aut'] = share_fem_aut.number_fem_aut / share_fem_aut.number_authors
        mitelwert = pd.DataFrame(df_h.groupby(['Year']).mean()).reset_index(level=['Year'])
        mitelwert['share_fem_aut'] = mitelwert.number_fem_aut / mitelwert.number_authors
        mitelwert['Journal'] = 'All'
        share_fem_aut = share_fem_aut.append(mitelwert)
        share_fem_aut.share_fem_aut = np.round(share_fem_aut.share_fem_aut, 2)
        for i in lst_journals:
            try:
                df_draw = df_draw.append(share_fem_aut[share_fem_aut.Journal == i])
            except:
                df_draw = share_fem_aut[share_fem_aut.Journal == i]

        fig_2 = px.line(df_draw, x='Year', y='share_fem_aut', color='Journal', labels={'share_fem_aut':'Share of female authors'})
        fig_2.update_layout(xaxis=dict(tickmode='linear', tick0=1991, dtick=3))
        fig_2.update_traces(mode="markers+lines", hovertemplate=None)
        fig_2.update_layout(hovermode="x unified", height=600, width=800)
        st.plotly_chart(fig_2)

    ### Second Figure Citations
    if anzeige == 'Citations':
        st.write('Figure 2: Median number of citations by gender')
        df_cit_gender = pd.DataFrame(df.groupby(['Year', 'Journal', 'women']).WoS.median()).reset_index(level=['Year', 'Journal', 'women'])
        mitelwert = pd.DataFrame(df.groupby(['Year', 'women']).WoS.median()).reset_index(level=['Year', 'women'])
        mitelwert['Journal'] = 'All'
        df_cit_gender = df_cit_gender.append(mitelwert)
        df_cit_gender.WoS = np.round(df_cit_gender.WoS, 0)
        df_cit_gender['Journal_gender'] = ""
        for i in range(df_cit_gender.shape[0]):
            if df_cit_gender.iloc[i, df_cit_gender.columns.get_loc('women')] == 1.0:
                df_cit_gender.iloc[i, df_cit_gender.columns.get_loc('Journal_gender')] = df_cit_gender.iloc[
                                                                                             i, df_cit_gender.columns.get_loc(
                                                                                                 'Journal')] + ' Women'
            else:
                df_cit_gender.iloc[i, df_cit_gender.columns.get_loc('Journal_gender')] = df_cit_gender.iloc[
                                                                                             i, df_cit_gender.columns.get_loc(
                                                                                                 'Journal')] + ' Men'

        for i in lst_journals:
            try:
                df_draw_5 = df_draw_5.append(df_cit_gender[df_cit_gender.Journal == i])
            except:
                df_draw_5 = df_cit_gender[df_cit_gender.Journal == i]

        fig_2_cit = px.line(df_draw_5, x='Year', y='WoS', color='Journal_gender', labels={'WoS':'Median WoS citations'})
        fig_2_cit.update_layout(xaxis=dict(tickmode='linear', tick0=1991, dtick=3))
        fig_2_cit.update_traces(mode="markers+lines", hovertemplate=None)
        fig_2_cit.update_layout(hovermode="x unified", height=600, width=800)
        st.plotly_chart(fig_2_cit)

with FIGURE_3:
    if anzeige == 'Publication':
        st.write('Figure 3: Share of articles with all authors being women')
        df_all_fem_share = pd.DataFrame(df.groupby(['Year', 'Journal']).all_female.mean()).reset_index(level=['Year', 'Journal'])
        mitelwert = pd.DataFrame(df.groupby(['Year']).all_female.mean()).reset_index(level=['Year'])
        mitelwert['Journal'] = 'All'
        df_all_fem_share = df_all_fem_share.append(mitelwert)
        for i in lst_journals:
            try:
                df_draw = df_draw.append(df_all_fem_share[df_all_fem_share.Journal == i])
            except:
                df_draw = df_all_fem_share[df_all_fem_share.Journal == i]

        fig_3 = px.line(df_draw, x='Year', y='all_female', color='Journal', labels={'all_female':'Share of articles with all authors being women'})
        fig_3.update_layout(xaxis=dict(tickmode='linear', tick0=1991, dtick=3))
        fig_3.update_traces(mode="markers+lines", hovertemplate=None)
        fig_3.update_layout(hovermode="x unified", height=600, width=800)
        st.plotly_chart(fig_3)


with DESCRIPTION_DATA:
    st.title('Data Description')
    st.write('The names of the authors and JEL codes were collected from EconLit. Data for the years 2019 and 2020 might be incomplete. The data is updated regularly')
    st.write('The gender of authors is determined using genderize.io. A gender is assigned when the probability >.90. Otherwise, the gender is determined by hand.')
    st.write('Citations are collected from Web of Science. The citations for all articles were collected in June 2020.')
    st.write('Paper published with the dataset: \'Male Gatekeepers: Gender Bias in the Publishing process\' Felix Bransch and Michael Kvasnicka, IZA Working Paper')
    st.write('Contact felix.bransch@ovgu.de if you have any questions or want to get access to the data!')