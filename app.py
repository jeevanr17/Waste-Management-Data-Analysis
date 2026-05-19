import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="AutoInsight Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

/* Main Background */
.main {
    background-color: #ffffff;
    color: #000000;
}

/* Smooth Fade Animation */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

/* Main App Animation */
.block-container {
    animation: fadeIn 0.6s ease-in-out;
    padding-top: 2rem;
}

/* Headings */
h1, h2, h3 {
    color: #000000;
    font-weight: 700;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f8f8f8;
    border-right: 1px solid #e5e5e5;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: black !important;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e5e5e5;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    box-shadow: 0px 10px 25px rgba(0,0,0,0.12);
}

/* Buttons */
.stButton > button {
    background-color: black;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 18px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: #222222;
    transform: scale(1.02);
}

/* File Uploader */
[data-testid="stFileUploader"] {
    border: 1px dashed #888;
    border-radius: 16px;
    padding: 14px;
    transition: all 0.3s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: black;
}

/* Tabs */
.stTabs [role="tab"] {
    border-radius: 10px;
    transition: 0.3s ease;
}

.stTabs [role="tab"]:hover {
    background-color: #f0f0f0;
}

/* DataFrame */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    animation: fadeIn 0.5s ease;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

/* Success / Info / Warning */
.stSuccess, .stInfo, .stWarning {
    border-radius: 10px;
}

/* Smooth Plot Animation */
.element-container {
    animation: fadeIn 0.5s ease;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown("""
# AutoInsight Pro
### Intelligent CSV Analytics Dashboard
Analyze, visualize, and generate insights from datasets instantly.
""")

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("Dashboard Menu")

menu = st.sidebar.radio(
    "Navigate",
    [
        "Dataset Overview",
        "Missing Value Handling",
        "Visualizations",
        "Correlation Analysis",
        "Outlier Detection",
        "Smart Insights"
    ]
)

# -----------------------------------
# FILE UPLOADER
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

# -----------------------------------
# MAIN APPLICATION
# -----------------------------------

if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

        st.success("CSV File Uploaded Successfully")

        # ===================================
        # DATASET OVERVIEW
        # ===================================

        if menu == "Dataset Overview":

            st.subheader("Dataset Overview")

            total_rows = df.shape[0]
            total_columns = df.shape[1]
            missing_values = df.isnull().sum().sum()
            duplicates = df.duplicated().sum()

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Rows", total_rows)

            with col2:
                st.metric("Columns", total_columns)

            with col3:
                st.metric("Missing Values", missing_values)

            with col4:
                st.metric("Duplicate Rows", duplicates)

            tab1, tab2, tab3 = st.tabs(
                [
                    "Dataset Preview",
                    "Data Types",
                    "Statistical Summary"
                ]
            )

            with tab1:
                st.dataframe(
                    df,
                    use_container_width=True
                )

            with tab2:

                datatype_df = pd.DataFrame({
                    "Column": df.columns,
                    "Data Type": df.dtypes.astype(str)
                })

                st.dataframe(
                    datatype_df,
                    use_container_width=True
                )

            with tab3:
                st.dataframe(
                    df.describe(include='all'),
                    use_container_width=True
                )
                
               
        # ===================================
        # MISSING VALUE HANDLING
        # ===================================

        elif menu == "Missing Value Handling":

            st.subheader("Missing Value Handling")

            missing_data = df.isnull().sum()

            missing_df = missing_data[
                missing_data > 0
            ]

            if not missing_df.empty:

                st.write("Columns with Missing Values")

                st.dataframe(
                    missing_df.reset_index().rename(
                        columns={
                            "index": "Column Name",
                            0: "Missing Count"
                        }
                    ),
                    use_container_width=True
                )

                st.markdown("### Select Missing Value Strategy")

                strategy = st.selectbox(
                    "Choose Method",
                    [
                        "Drop Missing Values",
                        "Fill with Mean",
                        "Fill with Median",
                        "Fill with Mode",
                        "Fill with Custom Value"
                    ]
                )

                # DROP VALUES

                if strategy == "Drop Missing Values":

                    if st.button("Apply Changes"):

                        df = df.dropna()

                        st.success(
                            "Missing values dropped successfully."
                        )

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                # FILL WITH MEAN

                elif strategy == "Fill with Mean":

                    if st.button("Apply Changes"):

                        numeric_cols = df.select_dtypes(
                            include=['number']
                        ).columns

                        df[numeric_cols] = df[
                            numeric_cols
                        ].fillna(
                            df[numeric_cols].mean()
                        )

                        st.success(
                            "Missing values filled using mean."
                        )

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                # FILL WITH MEDIAN

                elif strategy == "Fill with Median":

                    if st.button("Apply Changes"):

                        numeric_cols = df.select_dtypes(
                            include=['number']
                        ).columns

                        df[numeric_cols] = df[
                            numeric_cols
                        ].fillna(
                            df[numeric_cols].median()
                        )

                        st.success(
                            "Missing values filled using median."
                        )

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                # FILL WITH MODE

                elif strategy == "Fill with Mode":

                    if st.button("Apply Changes"):

                        for column in df.columns:

                            if df[column].isnull().sum() > 0:

                                df[column].fillna(
                                    df[column].mode()[0],
                                    inplace=True
                                )

                        st.success(
                            "Missing values filled using mode."
                        )

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                # CUSTOM VALUE

                elif strategy == "Fill with Custom Value":

                    custom_value = st.text_input(
                        "Enter Custom Value"
                    )

                    if st.button("Apply Changes"):

                        df = df.fillna(custom_value)

                        st.success(
                            "Missing values filled successfully."
                        )

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

            else:

                st.success(
                    "No missing values found in dataset."
                )

        # ===================================
        # VISUALIZATIONS
        # ===================================

        elif menu == "Visualizations":

            st.subheader("Data Visualization")

            chart_type = st.selectbox(
                "Select Chart Type",
                [
                    "Histogram",
                    "Bar Chart",
                    "Scatter Plot",
                    "Pie Chart",
                    "Distribution Plot"
                ]
            )

            # HISTOGRAM

            if chart_type == "Histogram":

                numeric_columns = df.select_dtypes(
                    include=['number']
                ).columns.tolist()

                if not numeric_columns:

                    st.warning(
                        "No numerical columns available."
                    )

                else:

                    column = st.selectbox(
                        "Select Numerical Column",
                        numeric_columns
                    )

                    fig = px.histogram(
                        df,
                        x=column,
                        template="plotly_white",
                        title=f"Histogram of {column}"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            # BAR CHART

            elif chart_type == "Bar Chart":

                categorical_columns = df.select_dtypes(
                    exclude=['number']
                ).columns.tolist()

                if not categorical_columns:

                    st.warning(
                        "No categorical columns available."
                    )

                else:

                    column = st.selectbox(
                        "Select Category Column",
                        categorical_columns
                    )

                    count_df = df[column].value_counts().reset_index()

                    count_df.columns = [column, "Count"]

                    fig = px.bar(
                        count_df,
                        x=column,
                        y="Count",
                        template="plotly_white",
                        title=f"Bar Chart of {column}"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            # SCATTER PLOT

            elif chart_type == "Scatter Plot":

                numeric_columns = df.select_dtypes(
                    include=['number']
                ).columns.tolist()

                if len(numeric_columns) < 2:

                    st.warning(
                        "At least 2 numerical columns are required."
                    )

                else:

                    x_column = st.selectbox(
                        "Select X-axis",
                        numeric_columns
                    )

                    y_column = st.selectbox(
                        "Select Y-axis",
                        numeric_columns
                    )

                    fig = px.scatter(
                        df,
                        x=x_column,
                        y=y_column,
                        template="plotly_white",
                        title=f"{x_column} vs {y_column}"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            # PIE CHART

            elif chart_type == "Pie Chart":

                categorical_columns = df.select_dtypes(
                    exclude=['number']
                ).columns.tolist()

                if not categorical_columns:

                    st.warning(
                        "No categorical columns available."
                    )

                else:

                    column = st.selectbox(
                        "Select Category Column",
                        categorical_columns
                    )

                    pie_data = df[column].value_counts().reset_index()

                    pie_data.columns = [column, "Count"]

                    fig = px.pie(
                        pie_data,
                        names=column,
                        values="Count",
                        template="plotly_white",
                        title=f"Pie Chart of {column}"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )
            # Distribution Plot
            elif chart_type == "Distribution Plot":

                numeric_columns = df.select_dtypes(
                    include=['number']
                ).columns

                column = st.selectbox(
                    "Select Numerical Column",
                    numeric_columns
                )

            # Create Figure
                fig, ax = plt.subplots(
                    figsize=(10, 5)
                )
                sns.set_style("darkgrid")


            # Distribution Plot
                sns.histplot(
                    df[column],
                    kde=True,
                    bins=20,
                    color="skyblue",
                    edgecolor="black",
                    ax=ax
                )
                sns.rugplot(
                    df[column],
                    color="black",
                    ax=ax
                )

                ax.set_title(
                    f"Distribution Plot of {column}",
                    fontsize=16,
                    fontweight='bold'
                )

                ax.set_xlabel(column)
                ax.set_ylabel("Frequency")


                st.pyplot(fig)
                # Statistical Insights

                st.subheader("Distribution Insights")

                skewness = df[column].skew()

                if skewness > 1:
                    st.warning(
                        "Highly Right-Skewed Distribution"
                    )

                elif skewness < -1:
                    st.warning(
                        "Highly Left-Skewed Distribution"
                    )

                else:
                    st.success(
                        "Approximately Normal Distribution"
                    )

                st.write(
                    f"Skewness Value: {skewness:.2f}"
                )
        # ===================================
        # CORRELATION ANALYSIS
        # ===================================

        elif menu == "Correlation Analysis":

            st.subheader("Correlation Heatmap")

            numeric_df = df.select_dtypes(
                include=['number']
            )

            if not numeric_df.empty:

                correlation = numeric_df.corr()

                fig, ax = plt.subplots(
                    figsize=(12, 7)
                )

                sns.heatmap(
                    correlation,
                    annot=True,
                    cmap="coolwarm",
                    linewidths=0.5,
                    fmt=".2f",
                    ax=ax
                )

                st.pyplot(fig)

            else:

                st.warning(
                    "No numerical columns available for correlation analysis."
                )
        # -----------------------------------
        # Missing Value Heatmap
        # -----------------------------------

            st.subheader("Missing Value Heatmap")

            fig2, ax2 = plt.subplots(
                figsize=(10, 5)
            )

            msno.heatmap(
                df,
                ax=ax2
            )

            st.pyplot(fig2)

            # ===================================
            # OUTLIER DETECTION
            # ===================================

        elif menu == "Outlier Detection":

            st.subheader("📦 Outlier Detection")

        # Select Numerical Columns
            numeric_columns = df.select_dtypes(
                include=['number']
            ).columns

        # Check Numerical Columns
            if len(numeric_columns) > 0:

            # Select Column
                column = st.selectbox(
                    "Select Numerical Column",
                    numeric_columns
                )

            # Box Plot
                fig = px.box(
                    df,
                    y=column,
                    title=f"Outlier Detection for {column}"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # IQR Method
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)

                IQR = Q3 - Q1

                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = df[
                    (df[column] < lower_bound) |
                    (df[column] > upper_bound)
                ]

                st.write(
                    f"Detected Outliers: {len(outliers)}"
                )

                st.dataframe(outliers)

            else:

                st.warning(
                    "No numerical columns available."
                )       

        # ===================================
        # SMART INSIGHTS
        # ===================================

        elif menu == "Smart Insights":

            st.subheader("Smart Insights")

            insights = []

            total_rows = df.shape[0]
            total_columns = df.shape[1]

            missing_values = df.isnull().sum().sum()
            duplicates = df.duplicated().sum()

            # Missing Values

            if missing_values > 0:

                missing_percent = (
                    missing_values /
                    (total_rows * total_columns)
                ) * 100

                insights.append(
                    f"Dataset contains {missing_values} missing values "
                    f"({missing_percent:.2f}% of total data)."
                )

            else:

                insights.append(
                    "Dataset has no missing values."
                )

            # Duplicates

            if duplicates > 0:

                duplicate_percent = (
                    duplicates / total_rows
                ) * 100

                insights.append(
                    f"Dataset contains {duplicates} duplicate rows "
                    f"({duplicate_percent:.2f}% of dataset)."
                )

            else:

                insights.append(
                    "Dataset has no duplicate rows."
                )

            # Numerical Insights

            numeric_columns = df.select_dtypes(
                include=['number']
            ).columns.tolist()

            if numeric_columns:

                correlation_matrix = df[
                    numeric_columns
                ].corr()

                for col in numeric_columns:

                    column_data = df[col].dropna()

                    if len(column_data) == 0:
                        continue

                    mean_value = column_data.mean()
                    median_value = column_data.median()

                    if abs(mean_value - median_value) > 0.1 * abs(mean_value):

                        insights.append(
                            f"{col} may contain skewed distribution "
                            f"(Mean: {mean_value:.2f}, "
                            f"Median: {median_value:.2f})."
                        )

                    q1 = column_data.quantile(0.25)
                    q3 = column_data.quantile(0.75)

                    iqr = q3 - q1

                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr

                    outliers = column_data[
                        (column_data < lower_bound) |
                        (column_data > upper_bound)
                    ]

                    if len(outliers) > 0:

                        insights.append(
                            f"{col} contains "
                            f"{len(outliers)} potential outliers."
                        )

                    if column_data.std() < 1:

                        insights.append(
                            f"{col} has very low variance."
                        )

                # Correlation Detection

                for i in range(len(numeric_columns)):

                    for j in range(i + 1, len(numeric_columns)):

                        corr_value = correlation_matrix.iloc[i, j]

                        if abs(corr_value) > 0.8:

                            insights.append(
                                f"{numeric_columns[i]} and "
                                f"{numeric_columns[j]} are highly correlated "
                                f"({corr_value:.2f})."
                            )

            # Categorical Insights

            categorical_columns = df.select_dtypes(
                exclude=['number']
            ).columns.tolist()

            if categorical_columns:

                for col in categorical_columns:

                    unique_count = df[col].nunique()

                    if unique_count == total_rows:

                        insights.append(
                            f"{col} contains unique values "
                            f"for every row."
                        )

                    elif unique_count == 1:

                        insights.append(
                            f"{col} contains only one unique value."
                        )

                    most_common = df[col].mode()

                    if not most_common.empty:

                        insights.append(
                            f"Most common value in {col}: "
                            f"{most_common[0]}"
                        )

            # DISPLAY INSIGHTS

            if insights:

                st.markdown("### Generated Insights")

                for insight in insights:

                    st.success(insight)

            else:

                st.info(
                    "No major insights detected."
                )

    except Exception as e:

        st.error(
            f"Error loading file: {e}"
        )

# -----------------------------------
# NO FILE UPLOADED
# -----------------------------------

else:

    st.info(
        "Please upload a CSV file to begin analysis."
    )