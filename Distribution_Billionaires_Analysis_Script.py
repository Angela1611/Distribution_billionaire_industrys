import streamlit as st
import pandas as pd
import folium
import plotly.express as px
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import branca.colormap as cm
import geopandas as gpd
from folium import plugins


#Page Settings
st.set_page_config(page_title="Distribution_Billionaires - Analysis",
                   page_icon="bar_chart:",
                   layout="wide")


# Read the CSV file into a DataFrame
richest_people = pd.read_csv("500_richest_people_2021_clean.csv")

# Create a new DataFrame with the count of each value in the 'Country' column
country_counts = richest_people['Country'].value_counts().reset_index()
country_counts.columns = ['Country', 'Count']

# Create the country_money DataFrame
country_money = richest_people.groupby('Country')['Total_Networth_Billions'].sum().reset_index()
country_money.columns = ['Country', 'Total_Networth_Billions']
# Sort the DataFrame in descending order by 'Total_Networth_Billions'
country_money = country_money.sort_values(by='Total_Networth_Billions', ascending=False)
# Reset the index and add a column numbered from 1
country_money.reset_index(drop=True, inplace=True)
country_money.index += 1
# Show the country_money DataFrame
print(country_money)

#______________ Side bar _________
st.sidebar.title("Distribution of Billionaire People and Industrys")
st.sidebar.header("Please filter here:")
category = st.sidebar.selectbox(
    "Category",
    [" ", "Countrys", "Industrys"]
)

feature = st.sidebar.selectbox(
    "Feature",
    [" ", "With more Billionaires", "With more money"]
)


if category == "Countrys" and feature == "With more Billionaires":
    st.header("Countrys with more Billionaires")

    ###MAP COUNTRYS WITH MORE BILLIONAIRES
    # Create a map centered at a specific location with zoom level 1.45
    map = folium.Map(location=[30, -20], zoom_start=1.45)

    # Add a choropleth layer with custom style and tooltip
    folium.Choropleth(
        geo_data="countries.geojson",
        name="choropleth",
        data=country_counts,
        columns=["Country", "Count"],
        key_on="feature.properties.ADMIN",
        fill_color="YlOrRd",  # Yellow to Red color palette
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_color="gray",
        nan_fill_opacity=0.4,
        legend_name="Count",
        highlight=True,
        threshold_scale=country_counts['Count'].quantile([i/20 for i in range(21)]).tolist(),  # Define 20 quantiles
        tooltip=folium.features.GeoJsonTooltip(fields=['ADMIN', 'Count'], aliases=['Country', 'Count'], labels=True, sticky=False)
    ).add_to(map)

    # Display the map
    folium_static(map, width=600, height=400)

    ##BAR CHART COUNTRYS WITH MORE BILLIONAIRES
    # Sort the DataFrame by 'Count' in descending order and get the top 15 countries
    top_countries = country_counts.sort_values('Count', ascending=False).head(15)


    # Create an interactive line chart with points using Plotly

    # Create a bar chart
    fig = px.bar(top_countries, x='Country', y='Count', title='Top 15 Countries with more billionaires')

    # Update the layout to change the y-axis label
    fig.update_layout(yaxis_title='Number of Billionaires')

    # Display the chart
    st.plotly_chart(fig)


    country_counts

if category == "Countrys" and feature == "With more money":
    st.header("Countrys with more money from Billionaires")

    ###MAP COUNTRYS WITH MORE MONEY 
    # Create a map centered at a specific location with zoom level 1.45
    map = folium.Map(location=[30, -20], zoom_start=1.45)

    # Add a choropleth layer with custom style and tooltip
    folium.Choropleth(
        geo_data="countries.geojson",
        name="choropleth",
        data=country_money,
        columns=["Country", "Total_Networth_Billions"],
        key_on="feature.properties.ADMIN",
        fill_color="YlOrRd", 
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_color="gray",
        nan_fill_opacity=0.4,
        legend_name="Total Net Worth (Billions)",
        highlight=True,
        threshold_scale=country_money['Total_Networth_Billions'].quantile([i/50 for i in range(51)]).tolist(),  
        tooltip=folium.features.GeoJsonTooltip(fields=['ADMIN', 'Total_Networth_Billions'], aliases=['Country', 'Total_Networth_Billions'], labels=True, sticky=False)
    ).add_to(map)
    
    # Display the map
    folium_static(map, width=600, height=400)

    ###Bar Chart 

    # Filter the top 15 countries
    top_15_countries = country_money.head(15)

    # Create a bar chart for the top 15 countries
    fig = px.bar(top_15_countries, x='Country', y='Total_Networth_Billions',
                title='Top 15 Countries by Total Net Worth from Billionaires',
                labels={'Total_Networth_Billions': 'Total Net Worth (Billions)', 'Country': 'Country'},
                )

    # Update the layout to customize the chart appearance
    fig.update_layout(xaxis_title='Country', yaxis_title='Total Net Worth (Billions)',
                    yaxis_tickformat='$.2f',  # Format y-axis as currency with 2 decimal places
                    )

    # Display the chart
    st.plotly_chart(fig)

    country_money

if category == "Industrys" and feature == "With more Billionaires":

    # Count the number of occurrences of each value in the "Industry" column
    industry_counts = richest_people['Industry'].value_counts()

    # Create a bar chart
    fig = px.bar(x=industry_counts.index, y=industry_counts.values,
                labels={'y': 'Number of Billionaires', 'x': 'Industry'},
                title='Number of Billionaires by Industry')

    # Display the chart in your Streamlit app
    st.plotly_chart(fig)

    # Create a donut chart
    fig = px.pie(names=industry_counts.index, values=industry_counts.values,
                title='Percentage of Billionaires by Industry',
                hole=0.5)  # Set the size of the hole in the middle to create a donut chart

    # Display the chart
    st.plotly_chart(fig)



if category == "Industrys" and feature == "With more money":

    # Sum the "Total_Networth_Billions" column grouped by "Industry"
    industry_total_networth = richest_people.groupby('Industry')['Total_Networth_Billions'].sum().reset_index()

    # Create a bar chart
    fig = px.bar(industry_total_networth, x='Industry', y='Total_Networth_Billions',
                title='Total Net Worth by Industry',
                labels={'Total_Networth_Billions': 'Total Net Worth (Billions)', 'Industry': 'Industry'},
                )

    # Update the layout to customize the chart appearance
    fig.update_layout(xaxis_title='Industry', yaxis_title='Total Net Worth (Billions)',
                    yaxis_tickformat='$.2f',  # Format y-axis as currency with 2 decimal places
                    )

    # Display the chart in your Streamlit app
    st.plotly_chart(fig)




    # Sum the "Total_Networth_Billions" column grouped by "Industry"
    industry_total_networth = richest_people.groupby('Industry')['Total_Networth_Billions'].sum().reset_index()

    # Create a donut chart
    fig = px.pie(industry_total_networth, names='Industry', values='Total_Networth_Billions',
                title='Total Net Worth by Industry',
                hole=0.5)  # Set the size of the hole in the middle to create a donut chart

    # Display the chart in your Streamlit app
    st.plotly_chart(fig)
