import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Advanced Data Visualizer", layout="wide")

st.title("📊 Interactive Data Visualizer")
st.write(
    "Upload a CSV file, explore the data, filter it, and generate correct statistical visualizations."
)

# ------------------ FILE UPLOAD ------------------
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ------------------ DATA PREVIEW ------------------
    st.subheader("📄 Dataset Preview")
    st.dataframe(df)

    # ------------------ DATASET SUMMARY ------------------
    st.subheader("📌 Dataset Summary")
    col1, col2 = st.columns(2)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    st.write("**Column Names:**")
    st.write(df.columns.tolist())

    st.subheader("📊 Statistical Summary")
    st.dataframe(df.describe(include="all"))

    # ------------------ DATA FILTERING ------------------
    st.subheader("🔍 Data Filtering")

    filter_column = st.selectbox("Select column to filter", df.columns)

    if df[filter_column].dtype == "object":
        values = df[filter_column].unique()
        selected = st.multiselect("Select values", values, default=values)
        filtered_df = df[df[filter_column].isin(selected)]
    else:
        min_val, max_val = float(df[filter_column].min()), float(df[filter_column].max())
        selected_range = st.slider("Select range", min_val, max_val, (min_val, max_val))
        filtered_df = df[
            (df[filter_column] >= selected_range[0]) &
            (df[filter_column] <= selected_range[1])
        ]

    st.write("### Filtered Data")
    st.dataframe(filtered_df)

    # ------------------ VISUALIZATION ------------------
    st.subheader("📈 Data Visualization")

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Line Chart",
            "Bar Chart",
            "Area Chart",
            "Scatter Plot",
            "Histogram",
            "Box Plot",
            "Pie Chart"
        ]
    )

    numeric_cols = filtered_df.select_dtypes(include="number").columns.tolist()
    categorical_cols = filtered_df.select_dtypes(exclude="number").columns.tolist()

    fig, ax = plt.subplots()

    try:
        # -------- Line / Bar / Area --------
        if chart_type in ["Line Chart", "Bar Chart", "Area Chart"]:
            x_col = st.selectbox("Select X-axis", filtered_df.columns)
            y_col = st.selectbox("Select Y-axis (Numeric)", numeric_cols)

            if chart_type == "Line Chart":
                ax.plot(filtered_df[x_col], filtered_df[y_col])

            elif chart_type == "Bar Chart":
                ax.bar(filtered_df[x_col], filtered_df[y_col])

            elif chart_type == "Area Chart":
                ax.fill_between(
                    range(len(filtered_df[y_col])),
                    filtered_df[y_col],
                    alpha=0.5
                )
                ax.set_xticks(range(len(filtered_df[x_col])))
                ax.set_xticklabels(filtered_df[x_col], rotation=45)

            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)

        # -------- Scatter Plot --------
        elif chart_type == "Scatter Plot":
            x_col = st.selectbox("Select X-axis (Numeric)", numeric_cols)
            y_col = st.selectbox("Select Y-axis (Numeric)", numeric_cols)
            ax.scatter(filtered_df[x_col], filtered_df[y_col])
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)

        # -------- Histogram --------
        elif chart_type == "Histogram":
            col = st.selectbox("Select Numeric Column", numeric_cols)
            bins = st.slider("Number of bins", 5, 50, 20)
            ax.hist(filtered_df[col], bins=bins, edgecolor="black")
            ax.set_xlabel(col)
            ax.set_ylabel("Frequency")

        # -------- Box Plot --------
        elif chart_type == "Box Plot":
            col = st.selectbox("Select Numeric Column", numeric_cols)
            ax.boxplot(filtered_df[col], vert=True)
            ax.set_ylabel(col)

        # -------- Pie Chart --------
        elif chart_type == "Pie Chart":
            cat_col = st.selectbox("Select Category Column", categorical_cols)
            num_col = st.selectbox("Select Value Column (Numeric)", numeric_cols)

            pie_data = filtered_df.groupby(cat_col)[num_col].sum()
            ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")

        st.pyplot(fig)

    except Exception:
        st.error("❌ Please select appropriate fields for this chart.")

    # ------------------ DOWNLOAD ------------------
    st.subheader("⬇ Download Results")

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Filtered Data as CSV",
        csv,
        "filtered_data.csv",
        "text/csv"
    )
