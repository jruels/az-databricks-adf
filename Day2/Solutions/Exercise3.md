### Step-by-Step Guide to Design the Data Pipeline

---

#### **1. Prerequisites**
- **Azure Storage Account**: Store source files in a Blob Storage container.
- **Azure Data Factory (ADF)**: Use ADF to orchestrate the pipeline.
- **Logging System**: Use Azure Blob Storage, Azure SQL Database, or another system for logging.

---

### **Step 1: Set Up Azure Resources**

1. **Create an Azure Storage Account**
   - Set up a storage account and container for source files (e.g., `source-data`).
   - Create another container (e.g., `processed-data`) for processed output.

2. **Set Up Logging**
   - Decide on a logging system (e.g., a separate container in Azure Blob Storage or a table in Azure SQL Database).
   - Create a storage container or database table to store logs.

---

### **Step 2: Create the ADF Pipeline**

#### **2.1 Set Up the Pipeline**
1. In the ADF Studio, create a new pipeline and name it `File_Processing_Pipeline`.

---

#### **2.2 Add the Get Metadata Activity**
1. **Add Get Metadata Activity**
   - Drag the **Get Metadata** activity into the pipeline.
   - Configure the **Dataset** to point to your source Blob Storage container.
   - Add **Field List** properties like `Child Items` and `Last Modified`.

2. **Output of Get Metadata**
   - This activity will output a list of files and their last modified timestamps.

---

#### **2.3 Add If Condition Activity**
1. **Add If Condition**
   - Drag the **If Condition** activity below the Get Metadata activity.
   - Define the condition to check for new files:
     ```text
     @greater(length(activity('Get Metadata').output.childItems), 0)
     ```
   - This condition checks if any files exist in the source folder.

2. **Inside the If Condition**
   - If the condition is true, proceed to execute the data flow.
   - If false, end the pipeline.

---

#### **2.4 Add For Each Activity**
1. **Add For Each**
   - Inside the `If` activity, add a **For Each** activity.
   - Configure it to iterate over the `childItems` output from the Get Metadata activity.

---

#### **2.5 Inside For Each**
1. **Add Data Flow Activity**
   - Add a **Data Flow** activity inside the For Each loop.
   - Pass the current file name as a parameter to the data flow.

2. **Configure Data Flow**
   - Create a data flow to process the files:
     - **Source**: Use the parameterized file path to read the current file.
     - **Transformations**:
       - **Filter**: Remove invalid or null values.
       - **Derived Column**: Add calculated fields and perform data type conversions.
       - **Aggregate**: Summarize data if needed.
     - **Sink**: Write transformed data to the `processed-data` container.

---

#### **2.6 Add Logging**
1. **Append Variables for Logging**
   - Inside the For Each loop, after the Data Flow, add an **Append Variable** activity.
   - Log the processed file names and timestamps:
     ```text
     @concat('Processed file: ', item().name, ' at ', pipeline().TriggerTime)
     ```

2. **Log Errors**
   - Add an **Error Handling** path for the Data Flow activity.
   - Use another **Append Variable** activity to log errors:
     ```text
     @concat('Error processing file: ', item().name, ' - Error: ', activity('Data Flow').Error.Message)
     ```

---

### **Step 3: Validate and Publish**
1. **Validate Pipeline**
   - Ensure all parameters, conditions, and paths are correctly configured.
   - Test the pipeline with a sample dataset.

2. **Publish the Pipeline**
   - Publish the pipeline to make it available for execution.

---

### **Step 4: Execution**
1. **Trigger the Pipeline**
   - Run the pipeline manually or set up a trigger to execute it periodically.
2. **Monitor Execution**
   - Use the **Monitor** tab in ADF to track progress and check for errors.

---

### **Logging System Example**
- **Blob Storage**: Save logs as a JSON or CSV file.
- **SQL Database**: Write logs into a table with columns like `FileName`, `Status`, `Timestamp`, and `ErrorMessage`.

---

### **Pipeline Summary**
1. **Get Metadata**: Retrieve file names and timestamps.
2. **If Condition**: Check if there are new files.
3. **For Each**: Iterate through the files.
4. **Data Flow**: Process and transform the files.
5. **Logging**: Capture status and error information for each file.

