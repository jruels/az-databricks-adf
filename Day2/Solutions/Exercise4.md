### **Step-by-Step Guide: Create a Pipeline to Process Files Based on Modification Date**

This guide describes how to create an Azure Data Factory (ADF) pipeline to read a file, check if it was modified in the last 24 hours, and process it conditionally based on its properties.

---

### **1. Prerequisites**
- An **Azure Storage Account** with the file to be processed.
- An **Azure Data Factory (ADF)** instance.
- A database or storage location to log errors and activity status.

---

### **2. Pipeline Design**

#### **2.1 Overview**
1. **Get Metadata**: Retrieve the file's properties, including the last modified date and file size.
2. **If Condition**: Check if the file's last modified date is within the last 24 hours.
3. **Data Processing**: Perform transformations only if the condition is met.
4. **Error Logging**: Use Set Variable and logging mechanisms to capture errors and exceptions.

---

### **3. Implementation Steps**

#### **Step 1: Set Up the Pipeline**
1. Go to **Author** in ADF Studio and create a new pipeline named `File_Processing_Pipeline`.

---

#### **Step 2: Add Get Metadata Activity**
1. **Drag and Drop Get Metadata Activity**:
   - Name it `Get_File_Metadata`.
   - Configure the activity:
     - **Dataset**: Create a dataset pointing to the file in your Azure Blob Storage container.
     - **Field List**: Select `Last Modified` and `Size`.

2. **Output of Get Metadata**:
   - The activity outputs metadata, including `lastModified` and `size`.

---

#### **Step 3: Add If Condition Activity**
1. **Drag and Drop If Condition Activity**:
   - Name it `Check_Modified_Time`.

2. **Condition Expression**:
   - Use the `lastModified` property from the `Get_File_Metadata` activity.
   - Compare it to the current time minus 24 hours:
     ```text
     @greaterOrEquals(activity('Get_File_Metadata').output.lastModified, addHours(utcnow(), -24))
     ```

3. **If True**: Add processing steps for files modified in the last 24 hours.
4. **If False**: Skip processing or log a message indicating no new file was found.

---

#### **Step 4: Add Processing Activities**
1. **Inside True Condition**:
   - Add the activities to process the file. This could include:
     - **Data Flow Activity**: Transform and process the file.
     - **Copy Data Activity**: Move the file to a processed folder or another storage account.

2. **Pass Parameters**:
   - Use the file path and metadata as parameters for downstream activities.

---

#### **Step 5: Add Error Logging**
1. **Set Variable Activity for Errors**:
   - Drag a **Set Variable** activity after each critical step to capture errors if any.
   - Example:
     ```text
     @concat('Error in activity: ', activity('ActivityName').Error.Message)
     ```

2. **Write Logs**:
   - Use a **Stored Procedure Activity** to log the errors to a database, or use a **Copy Data Activity** to write logs to Azure Blob Storage.

---

### **4. Combine Activities and Create Dependencies**

- **Control Flow**:
  - Use dependencies to ensure activities execute in sequence.
  - Example: Data processing starts only if the `If Condition` evaluates to true.

- **Retry Policies**:
  - Set retry policies on activities to handle transient errors.

- **Error Paths**:
  - Configure **On Failure** paths for activities to capture and log exceptions.

---

### **5. Validate and Publish**
1. **Validate Pipeline**:
   - Use the **Validate All** button to check for errors in the pipeline.
2. **Publish Pipeline**:
   - Click **Publish All** to deploy the pipeline.

---

### **6. Execution and Monitoring**
1. Trigger the pipeline manually or via a schedule.
2. Monitor execution using the **Monitor** tab in ADF to track activity runs and view logs.

---

### **Discussion: Workflow Design and Dependencies**

1. **Get Metadata and Conditional Processing**:
   - The `Get Metadata` activity provides file-level details like modification time, size, and more.
   - The `If Condition` ensures processing happens only when necessary, reducing unnecessary resource usage.

2. **Error Handling and Logging**:
   - Use the `Set Variable` and `Stored Procedure` activities to centralize error logging.
   - Ensure error handling paths capture exceptions from all critical activities.

3. **Control Flow Activities**:
   - ADF's control flow activities like `If Condition`, `For Each`, and `Set Variable` enable flexible workflows.
   - Dependencies between activities ensure the pipeline executes in the desired sequence.

4. **Scalability**:
   - This pipeline design is scalable for multiple files or dynamic file paths by incorporating the `For Each` activity.

---
