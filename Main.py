# import module
import streamlit as st
import pandas as pd
if __name__ == '__main__':
    path = Users/Sree.Pothula/hvrtracking.xlsx'
    df = pd.read_excel(path,sheet_name='Request Details Tracking - PROD', dtype=str)
    # Getting Outstanding Request Dataframe
    OutStandingfilteredDf = df[(df['Request Status'] == 'Requested') |
                               (df['Request Status'] == 'Clarify') |
                               (df['Request Status'] == 'Truncate') |
                               (df['Request Status'] == 'Ready for HVR') |
                               (df['Request Status'] == 'Validation Failed')]
    # Setting Page to Wide - Note: Must be first in code
    st.set_page_config(layout="wide")
    # Creating Multiple Tabs
    tab1, tab2 = st.tabs(['HVR Request Tab', 'HVR Tracking'])
    with tab1:
        col1, col2 = st.columns([3,8],gap='small')
        with col1:
            st.header("Make a Request")
            request_form = st.form("request_form")
            # User Inputs
            requester = request_form.text_input("Requester")
            project = request_form.selectbox("Project", ["CAMP", "GPD2", "misc high", "TBD", "Other: in comments"])
            object_type = request_form.selectbox("Object", ["table", "view"])
            source_server = request_form.selectbox("Source Server", ["BSB", "SQLPROD01", "SQLPROD106"])
            source_database = request_form.selectbox("Source Database", ["BSB", "FOP", "ProductCenter"])
            source_schema = request_form.selectbox("Source Schema", ["dbo", "productcenter", "cde"])
            source_table_name = request_form.text_input("Source Table Name")  # can also do select box
            target_server = request_form.selectbox("Target Server", ["Dev", "Prod"])
            target_schema = request_form.selectbox("Target Schema",
                                                   ["bsb", "fop", "product_center", "Other: in comments"])
            target_table_name = request_form.text_input("Target Table Name")  # can also do select box
            comments = request_form.text_area("Comments")
            # Form Submit Button
            add_data = request_form.form_submit_button()
            # Appends Entry and Writes to Excel
            if add_data:
                new_data = {
                    "Requester": requester,
                    "Project": project,
                    "Priority": "",
                    "SrcTABLENAME": source_table_name,
                    "OBJTYPE": object_type,
                    "SrcServer": source_server,
                    "SrcDATABASE": source_database,
                    "SrcSCHEMA": source_schema,
                    "TgtServer": target_server,
                    "TgtSchema": target_schema,
                    "TgtTableName": target_table_name,
                    "Request Status": "Requested",
                    "Comments": comments
                }
                df = df.append(new_data, ignore_index=True)
                df.to_excel(path, sheet_name='Request Details Tracking - PROD', index=False)
        # Displays Updated Request Sheet
        with col2:
            st.header("Request Sheet")
            st.dataframe(df, None, 700)
    with tab2:
        with st.container():
            st.title("HVR Tracking")
            col1, col2, col3 = st.columns(3,gap='small')
            with col1:
                # Creating Bar Charts
                st.header('Status of Open Requests')
                by_request_type = OutStandingfilteredDf.groupby(['Request Status'])["Requester"].count()
                st.bar_chart(by_request_type)
            with col2:
                st.header('Open Request Project')
                by_request_type = OutStandingfilteredDf.groupby(['Project'])["Requester"].count()
                st.bar_chart(by_request_type)
            with col3:
                st.header('Source Server Open Reqeust')
                by_request_type = OutStandingfilteredDf.groupby(['SrcServer'])["Requester"].count()
                st.bar_chart(by_request_type)
        # Displaying DataFrame
        st.header('HVR Open Requests')
        st.write(OutStandingfilteredDf)
