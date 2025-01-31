Here's a tailored version of the lab instructions, adjusted to use a `happiness.csv` file instead of `emp.txt` for your student's task:

---

**Quickstart: Create an Azure Data Factory using ARM Template**

This quickstart demonstrates how to create an Azure Data Factory using an Azure Resource Manager (ARM) template. The pipeline created in this Data Factory copies data from one folder to another within an Azure blob storage. 

An Azure Resource Manager (ARM) template is a JavaScript Object Notation (JSON) file that defines the infrastructure and configuration for your project. The template uses declarative syntax, allowing you to describe your intended deployment without specifying the sequence of commands.

### Prerequisites

1. The `happiness.csv` file.


### Template for Creating Azure Data Factory Resources

Below is the ARM template you will use to deploy your Azure resources. This template defines a storage account, a blob container, and a pipeline that moves data between two folders in Azure Blob Storage. You will use `happiness.csv`.

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "dataFactoryName": {
      "type": "string",
      "defaultValue": "[format('datafactory{0}', uniqueString(resourceGroup().id))]",
      "metadata": {
        "description": "Data Factory Name"
      }
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]",
      "metadata": {
        "description": "Location of the data factory."
      }
    },
    "storageAccountName": {
      "type": "string",
      "defaultValue": "[format('storage{0}', uniqueString(resourceGroup().id))]",
      "metadata": {
        "description": "Name of the Azure storage account that contains the input/output data."
      }
    },
    "blobContainerName": {
      "type": "string",
      "defaultValue": "[format('blob{0}', uniqueString(resourceGroup().id))]",
      "metadata": {
        "description": "Name of the blob container in the Azure Storage account."
      }
    }
  },
  "variables": {
    "dataFactoryLinkedServiceName": "AzureBlobLinkedService",
    "happinessDatasetIn": "happinessDatasetIn",
    "happinessDatasetOut": "happinessDatasetOut"
  },
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2023-01-01",
      "name": "[parameters('storageAccountName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "Standard_LRS"
      },
      "kind": "StorageV2",
      "properties": {
        "minimumTlsVersion": "TLS1_2",
        "supportsHttpsTrafficOnly": true,
        "allowBlobPublicAccess": false
      }
    },
    {
      "type": "Microsoft.DataFactory/factories",
      "apiVersion": "2018-06-01",
      "name": "[parameters('dataFactoryName')]",
      "location": "[parameters('location')]",
      "identity": {
        "type": "SystemAssigned"
      }
    },
    {
      "type": "Microsoft.DataFactory/factories/linkedservices",
      "apiVersion": "2018-06-01",
      "name": "[format('{0}/{1}', parameters('dataFactoryName'), variables('dataFactoryLinkedServiceName'))]",
      "properties": {
        "type": "AzureBlobStorage",
        "typeProperties": {
          "connectionString": "[concat('DefaultEndpointsProtocol=https;AccountName=', parameters('storageAccountName'), ';AccountKey=', listKeys(resourceId('Microsoft.Storage/storageAccounts', parameters('storageAccountName')), '2023-01-01').keys[0].value)]"
        }
      }
    },
    {
      "type": "Microsoft.DataFactory/factories/datasets",
      "apiVersion": "2018-06-01",
      "name": "[format('{0}/{1}', parameters('dataFactoryName'), variables('happinessDatasetIn'))]",
      "dependsOn": [
        "[resourceId('Microsoft.DataFactory/factories/linkedservices', parameters('dataFactoryName'), variables('dataFactoryLinkedServiceName'))]"
      ],
      "properties": {
        "linkedServiceName": {
          "referenceName": "[variables('dataFactoryLinkedServiceName')]",
          "type": "LinkedServiceReference"
        },
        "type": "Binary",
        "typeProperties": {
          "location": {
            "type": "AzureBlobStorageLocation",
            "container": "[parameters('blobContainerName')]",
            "folderPath": "input",
            "fileName": "happiness.csv"
          }
        }
      }
    },
    {
      "type": "Microsoft.DataFactory/factories/datasets",
      "apiVersion": "2018-06-01",
      "name": "[format('{0}/{1}', parameters('dataFactoryName'), variables('happinessDatasetOut'))]",
      "dependsOn": [
        "[resourceId('Microsoft.DataFactory/factories/linkedservices', parameters('dataFactoryName'), variables('dataFactoryLinkedServiceName'))]"
      ],
      "properties": {
        "linkedServiceName": {
          "referenceName": "[variables('dataFactoryLinkedServiceName')]",
          "type": "LinkedServiceReference"
        },
        "type": "Binary",
        "typeProperties": {
          "location": {
            "type": "AzureBlobStorageLocation",
            "container": "[parameters('blobContainerName')]",
            "folderPath": "output"
          }
        }
      }
    },
    {
      "type": "Microsoft.DataFactory/factories/pipelines",
      "apiVersion": "2018-06-01",
      "name": "[format('{0}/{1}', parameters('dataFactoryName'), 'CopyHappinessPipeline')]",
      "dependsOn": [
        "[resourceId('Microsoft.DataFactory/factories/datasets', parameters('dataFactoryName'), variables('happinessDatasetIn'))]",
        "[resourceId('Microsoft.DataFactory/factories/datasets', parameters('dataFactoryName'), variables('happinessDatasetOut'))]"
      ],
      "properties": {
        "activities": [
          {
            "name": "CopyHappinessData",
            "type": "Copy",
            "typeProperties": {
              "source": {
                "type": "BinarySource",
                "storeSettings": {
                  "type": "AzureBlobStorageReadSettings",
                  "recursive": true
                }
              },
              "sink": {
                "type": "BinarySink",
                "storeSettings": {
                  "type": "AzureBlobStorageWriteSettings"
                }
              },
              "inputs": [
                {
                  "referenceName": "[variables('happinessDatasetIn')]",
                  "type": "DatasetReference"
                }
              ],
              "outputs": [
                {
                  "referenceName": "[variables('happinessDatasetOut')]",
                  "type": "DatasetReference"
                }
              ]
            }
          }
        ]
      }
    }
  ]
}

```

### Steps to Deploy the Template

1. Sign in to the Azure portal.
2. Navigate to **Deploy to Azure**.
3. Fill in the parameters for the Azure resources, including your **Data Factory Name**, **Location**, **Storage Account Name**, and **Blob Container Name**.
4. Once the template is deployed, upload the `happiness.csv` file to the **input** folder in the created blob container.

### Running the Pipeline

1. Open your Data Factory from the Azure portal.
2. Select **Open Azure Data Factory Studio**.
3. Go to the **Author** tab.
4. Open the pipeline you created (`CopyHappinessPipeline`).
5. Click **Add Trigger > Trigger Now**.
6. Monitor the pipeline execution and check the **output** folder in the blob container to verify that the `happiness.csv` file has been copied.

### Clean Up

You can clean up the resources you created by deleting the resource group or just the Data Factory resource.
