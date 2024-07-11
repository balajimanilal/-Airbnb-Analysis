import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu


df = pd.read_csv("/Users/balajibm/New Folder/AirbnbDataset.csv")

st.set_page_config(
                    page_title="Airbnb Analysis",
                    page_icon="https://static-00.iconduck.com/assets.00/airbnb-icon-512x512-d9grja5t.png",
                    layout="wide",
                    initial_sidebar_state="collapsed"
                    )

row1 = st.columns(2)
with row1[0]:
    sub_columns = st.columns(3)

    with sub_columns[0]:
        menu = option_menu("Menu", ["Home","Analysis", "About"], 
                            icons=["house", "graph-up", "exclamation-triangle"],
                            menu_icon="cast",
                            default_index=0,
                            styles={"icon": {"color": "orange", "font-size": "20px"}}
                            )

if menu == 'Home':
    st.markdown(f""" <style>
                    .stApp {{
                        background: url('https://www.spinxdigital.com/app/uploads/2022/11/image-airbnb.jpg');
                        background-size: cover;
                    }}
                    
                    </style>""", unsafe_allow_html=True)

    st.markdown("<style>h1, h2, h3, p { color: black; font-size: 20px; background-color: lightgrey;}</style>", unsafe_allow_html=True)

    with row1[1]:
        st.markdown("<div class='home-text'>", unsafe_allow_html=True)  # Add custom CSS class for styling
    
        st.write("# Welcome to Airbnb Data Analysis")

        st.write("This Streamlit web app allows you to explore Airbnb listing data through interactive visualizations.")

        st.write("You can select different analysis options from the sidebar to gain insights into various aspects of Airbnb listings.")

        st.write("To learn more about this app and its features, visit the 'About' section.")

        st.markdown("</div>", unsafe_allow_html=True)


if menu == 'Analysis':
    st.markdown(f""" <style>.stApp {{
                background: url('https://news.airbnb.com/wp-content/uploads/sites/4/2023/11/PJMPHOTO18Q436_SNYA72_0609.jpg?fit=2500%2C1667');   
                background-size: cover}}
                </style>""",unsafe_allow_html=True)

    with row1[1]:
        analysis = st.selectbox("Exploratory Analysis of Airbnb Listing Data", ["Distribution of Listings by Country",
                                                                        "Price Variation by Selected Feature",
                                                                        "Frequency of Selected Feature",
                                                                        "Sum of Price and Beds by Number of Bedrooms",
                                                                        "Average Price by Cancellation Policy",
                                                                        "Sum of Price and Beds by Property Type",
                                                                        "Sum of Price and Guests Included by Cancellation Policy",
                                                                        "Sum of Price and Average Review Scores Rating by Number of Bathrooms"
                                                                        ])
        
    if analysis == "Distribution of Listings by Country":

        sub_columns = st.columns(2)

        with sub_columns[0]:

            country_counts = df['country'].value_counts().reset_index()
            country_counts.columns = ['country', 'count']

            fig = px.pie(country_counts, values='count', names='country', title='Country Distribution')
            fig.update_layout(title_x=0.3)
            st.plotly_chart(fig)

    if analysis == "Price Variation by Selected Feature":

        sub_columns = st.columns(2)

        with sub_columns[1]:
                    sub_columns_1 = st.columns(2)

                    with sub_columns_1[1]:
                        yaxis = st.selectbox("", ['price',
                                                  'security_deposit',
                                                  'cleaning_fee',
                                                  'extra_people_fee',
                                                ])

        with sub_columns[0]:
            fig = px.bar(df, x='country', y = yaxis, title=f"{yaxis} by Country")
            fig.update_layout(xaxis_title='Country', yaxis_title = yaxis , xaxis_tickangle=-45, title_x=0.35)
            st.plotly_chart(fig)

    if analysis == "Frequency of Selected Feature":

        sub_columns = st.columns(2)

        with sub_columns[1]:
                    sub_columns_1 = st.columns(2)

                    with sub_columns_1[1]:
                        yaxis = st.selectbox("", ['property_type',
                                                  "country",
                                                  "bed_type",
                                                ])

        with sub_columns[0]:
            property_type_counts = df[yaxis].value_counts().reset_index()
            property_type_counts.columns = [yaxis, 'count']

            fig = px.bar(property_type_counts, x='count', y=yaxis, title=f'Frequency of {yaxis}', orientation='h')
            fig.update_layout(xaxis_title='Frequency', yaxis_title= yaxis, xaxis_tickangle=-45, title_x=0.35)
            st.plotly_chart(fig)

    if analysis == "Sum of Price and Beds by Number of Bedrooms":

        agg_df = df.groupby('bedrooms').agg({'price': 'sum', 'beds': 'sum'}).reset_index()

        # Create a bar-line chart with Plotly Express
        fig = px.bar(agg_df, x='bedrooms', y='price', title='Sum of Price and Sum of Beds by Number of Bedrooms')
        fig.add_scatter(x=agg_df['bedrooms'], y=agg_df['beds'], mode='lines', name='Sum of Beds', yaxis='y2')

        # Update layout
        fig.update_layout(
            xaxis_title='Number of Bedrooms',
            yaxis=dict(title='Sum of Price', side='left', color='blue'),
            yaxis2=dict(title='Sum of Beds', side='right', overlaying='y', color='green')
        )
        st.plotly_chart(fig)

    if analysis == "Average Price by Cancellation Policy":
        avg_price_by_cancellation = df.groupby('cancellation_policy')['price'].mean().reset_index()
        bar_fig = px.bar(avg_price_by_cancellation, x='cancellation_policy', y='price', title='Average Price by Cancellation Policy')
        bar_fig.update_xaxes(title='Cancellation Policy')
        bar_fig.update_yaxes(title='Average Price')
        st.plotly_chart(bar_fig)
    
    if analysis == "Sum of Price and Beds by Property Type":
        # Aggregate the data by property type
        agg_property_df = df.groupby('property_type').agg({'price': 'sum', 'beds': 'sum'}).reset_index()

        # Create a bar-line chart for property type
        property_fig = px.bar(agg_property_df, x='property_type', y='price', title='Sum of Price and Sum of Beds by Property Type')
        property_fig.add_scatter(x=agg_property_df['property_type'], y=agg_property_df['beds'], mode='lines', name='Sum of Beds', yaxis='y2')

        # Update layout for property type
        property_fig.update_layout(
            xaxis_title='Property Type',
            yaxis=dict(title='Sum of Price', side='left', color='blue'),
            yaxis2=dict(title='Sum of Beds', side='right', overlaying='y', color='green')
        )
        st.plotly_chart(property_fig)

    if analysis == "Sum of Price and Guests Included by Cancellation Policy":
        # Aggregate the data by cancellation policy
        agg_cancel_df = df.groupby('cancellation_policy').agg({'price': 'sum', 'guests_included': 'sum'}).reset_index()

        # Create a bar-line chart for cancellation policy
        cancel_fig = px.bar(agg_cancel_df, x='cancellation_policy', y='price', title='Sum of Price and Sum of Guests Included by Cancellation Policy')
        cancel_fig.add_scatter(x=agg_cancel_df['cancellation_policy'], y=agg_cancel_df['guests_included'], mode='lines', name='Sum of Guests Included', yaxis='y2')

        # Update layout for cancellation policy
        cancel_fig.update_layout(
            xaxis_title='Cancellation Policy',
            yaxis=dict(title='Sum of Price', side='left', color='blue'),
            yaxis2=dict(title='Sum of Guests Included', side='right', overlaying='y', color='green')
        )
        st.plotly_chart(cancel_fig)

    if analysis == "Sum of Price and Average Review Scores Rating by Number of Bathrooms":
        # Aggregate the data by number of bathrooms
        agg_bathroom_df = df.groupby('bathrooms').agg({'price': 'sum', 'review_scores_rating': 'mean'}).reset_index()

        # Create a bar-line chart for number of bathrooms
        bathroom_fig = px.bar(agg_bathroom_df, x='bathrooms', y='price', title='Sum of Price and Average Review Scores Rating by Number of Bathrooms')
        bathroom_fig.add_scatter(x=agg_bathroom_df['bathrooms'], y=agg_bathroom_df['review_scores_rating'], mode='lines', name='Average Review Scores Rating', yaxis='y2')

        # Update layout for number of bathrooms
        bathroom_fig.update_layout(
            xaxis_title='Number of Bathrooms',
            yaxis=dict(title='Sum of Price', side='left', color='blue'),
            yaxis2=dict(title='Average Review Scores Rating', side='right', overlaying='y', color='green')
        )

        st.plotly_chart(bathroom_fig)

if menu == "About":

    st.markdown(f""" <style>.stApp {{
                    background: url('https://blog.artonemfg.com/hubfs/airbnb-3399753_1920.jpg');   
                    background-size: cover}}
                    </style>""",unsafe_allow_html=True)
    
    with row1[1]:
        st.write("# About")
    
        st.write("This Streamlit web app provides an exploratory analysis of Airbnb listing data. The analysis includes various visualizations to understand different aspects of the dataset.")
        
        st.write("The app allows users to select from the following analysis options:")
        
        st.markdown("""
        <ul>
            <li style='color:red; font-size:20px; background-color: lightgrey;'>Distribution of Listings by Country</li>
            <li style='color:red; font-size:20px; background-color: lightgrey;'>Price Variation by Selected Feature</li>
            <li style='color:red; font-size:20px; background-color: lightgrey;'>Frequency of Selected Feature</li>
            <li style='color:red; font-size:20px; background-color: lightgrey;'>Sum of Price and Beds by Number of Bedrooms</li>
            <li style='color:red; font-size:20px; background-color: lightgrey;'>Average Price by Cancellation Policy</li>
            <li style='color:red; font-size:20px; background-color: lightgrey;'>Sum of Price and Beds by Property Type</li>
            <li style='color:red; font-size:20px; background-color: lightgrey;'>Sum of Price and Guests Included by Cancellation Policy</li>
            <li style='color:red; font-size:20px; background-color: lightgrey;'>Sum of Price and Average Review Scores Rating by Number of Bathrooms</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.write("Users can select an analysis option from the sidebar to view the corresponding visualization.")

    # Styling the text
    st.markdown("<style>h1, h2, h3, p { color: black; font-size: 20px; background-color: lightgrey;}</style>", unsafe_allow_html=True)