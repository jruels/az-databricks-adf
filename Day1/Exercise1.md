# Exercise: Data Movement

## Objective
Create from scratch:
1. An Azure Storage Account and container for source data.  
2. An Azure SQL Database for the sink.  
3. A pipeline to copy data from Storage to SQL.  
4. Experiment with different settings to observe performance changes.

## Steps

1. **Create Azure Storage as Source**  
   - In the Azure Portal, click "+ Create a resource" → "Storage account."  
   - Assign a unique name, region, and resource group.  
   - After deployment, go to the storage account → "Containers" → "+ Container" to create a container (e.g., "inputdata").  
   - Upload a CSV or other data file to use as the source data.

2. **Create Azure SQL Database as Sink**  
   - Click "+ Create a resource" → "SQL Database."  
   - Choose or create a new SQL Server.  
   - Provide database name (e.g., "ExperimentDB").  
   - After deployment, go to your SQL Database and set firewall rules to allow Azure services and your IP.  
   - Create a table for the incoming data (e.g., "ExperimentTable").

3. **Configure Linked Services in Data Factory**  
   - In Azure Data Factory (ADF), open "Manage."  
   - Under "Linked services," click "+ New" to create:  
     - A linked service for your Storage account.  
     - A linked service for your SQL Database (using server name, credentials).

4. **Create Datasets**  
   - In ADF "Author" panel, create datasets for Source (CSV in Storage) and Sink (SQL Database table).  
   - Ensure your dataset schema is correct; adjust field mappings if necessary.

5. **Build the Pipeline**  
   - Create a new pipeline (e.g., "StorageToSQLExperiment").  
   - Add a "Copy data" activity.  
   - Set the Source dataset (pointing to your container and CSV).  
   - Set the Sink dataset (pointing to your SQL table).  
   - Adjust schema mapping or data type conversions as needed.

6. **Configure Performance & Settings**  
   - In the Copy activity "Settings," configure staging or different DIU levels.  
   - Experiment with parallelism, batch size, or compression.  
   - Compare run times with different configurations.

7. **Publish & Run**  
   - Click "Publish all."  
   - Trigger the pipeline manually ("Trigger now").  
   - Monitor the pipeline in the "Monitor" pane to compare performance metrics and discover issues.

## Exploration
- Change file format (CSV, Parquet), compression, or partition settings.  
- Adjust table schema, column mappings, data type conversions.  
- Observe how each change affects speed and resource usage.  

**Outcome:** You have learned how to set up both source (Storage) and sink (SQL) from scratch, configure copy activities, and tweak performance parameters for efficient data movement in Azure Data Factory.