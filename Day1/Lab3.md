# Lab 3: Run a Pipeline

**Objective:**
The objective of this lab is to run the pipeline created in Lab 2 and monitor its execution status.

**Pre-requisites:**
*   An Azure Data Factory pipeline created in Lab 2.
*   Linked Service and datasets are set up correctly for all the data sources.

**Detailed Steps:**
1.  **Open Pipeline:** Open the Azure Data Factory Studio and open the pipeline that you have created in the previous lab.
2.  **Trigger Pipeline:** Click on the "Add Trigger" button then click "Trigger now" to trigger the pipeline manually and you should see various trigger options available.
3.  **Monitor Execution:** Go to the "Monitor" tab and click on pipeline runs to track the status of your pipeline execution, and see detailed status of each of the activity runs, and the different logs.
4. **Activity Run Details:** Verify the status of each of the activity and the copy activity to ensure it was executed successfully. Check the error messages if there are any failed activities and their corresponding log messages.
5. **Validate Output:** Verify that the data is moved from source to destination by checking the destination data source or location.
6. You can run a SQL query in the database to check that the data has been moved.

**Expected Output:**
You will have run the pipeline successfully. You will be able to see the successful execution of the pipeline and activity runs in the monitoring tab. And you can also see that the data was moved successfully from the source to destination.

Your pipeline copies data from the storage file into the Azure Database for PostgreSQL table. You can verify the output by running the following command in pgAdmin 4:
```sql
SELECT * FROM public.sample_data
```

**Troubleshooting:**
*   **Pipeline Run Failure:** Check the error messages in the pipeline runs to identify issues and troubleshoot the failure, you can also look at the activity run details.
*   **Activity Failures:** Check activity details for configuration issues or connection issues and use the detailed logs for debugging.
