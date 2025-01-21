# Lab 1: ADF Instance Creation

**Objective:**
The objective of this lab is to gain hands-on experience with creating a new Azure Data Factory instance in the Azure portal.

**Pre-requisites:**
*   An active Azure subscription.
*   Permissions to create resources in Azure.

**Detailed Steps:**
1.  **Go to the Azure Portal:** Navigate to the Azure Portal (portal.azure.com) and sign in with your Azure account.
2.  **Create a New Resource Group:** From the home page click "Resource Groups" under Azure Services, then click on "+ Create" to create a new resource group. Enter "rg-adf-{your-name}" as the name, select the appropriate subscription and region, and then click "Review + Create" followed by "Create". Once the resource group is created, navigate to it.
3.  **Add Data Factory:** Click on " + Create " and search for "Data Factory", then select the Data Factory Resource and click "Create".
4.  **Fill in Basic Details:** In the Data Factory instance creation page fill in all required information including, subscription, resource group, name, region etc..
5.  **Review and Create:** Click "Review + Create" to validate, and if validation is passed, then click "Create".
6.  **Navigate to Resource:** After the resource is deployed, click "Go to resource".
7.  **Open Studio:** Click on "Launch Studio" from the overview page to launch the user interface.

**Expected Output:**
You should have a working Azure Data Factory instance. You should see the ADF Overview page and can click on "Open Azure Data Factory Studio" which should launch the ADF UI.

**Troubleshooting:**
*   **Deployment Errors:** If the resource deployment fails, check the error messages for details on the problem. Also verify that the name you provided is unique.
*   **Permission Issues:** If you lack sufficient permissions to create resources, you may need to consult with your subscription administrator to get the required access.