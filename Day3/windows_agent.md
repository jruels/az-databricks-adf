## Download and configure the agent



### Azure Pipelines

1. In your web browser, sign in to Azure Pipelines, and navigate to the **Agent pools** tab:

   1. Sign in to your organization (`https://dev.azure.com/{yourorganization}`).

   2. Choose **Azure DevOps**, **Organization settings**.

      ![Choose Organization settings.](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/media/agent-pools-tab/organization-settings.png?view=azure-devops)

   3. Choose **Agent pools**.

      ![Choose Agent pools tab.](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/media/agent-pools-tab/agent-pools.png?view=azure-devops)

2. Select the **Default** pool, select the **Agents** tab, and choose **New agent**.

3. On the **Get the agent** dialog box, choose **Windows**.

4. On the right pane, click the **Download** button.

5. Follow the instructions on the page to download the agent.

6. Unpack the agent into the directory of your choice. Make sure that the path to the directory contains no spaces because tools and scripts don't always properly escape spaces. A recommended folder is `C:\agents`. Extracting in the download folder or other user folders may cause permission issues.



## Install the agent

1. Start a PowerShell window and set the location to where you unpacked the agent.

   ```ps
   cd C:\agents 
   ```

2. Run `config.cmd`. This will ask you a series of questions to configure the agent.

   ```ps
   .\config.cmd
   ```

- When prompted:
  - Server URL: `https://dev.azure.com/{your-organization}`
  - Authentication type: `AAD`
  - Complete device code flow authentication in browser
  - Select "Default" for agent pool
  - Select No for service mode 
  - Select No for auto start



## Run the agent



### Run interactively

Run the following command to start the agent.

```ps
.\run.cmd
```

To restart the agent, press Ctrl+C to stop the agent, and then run `run.cmd` to restart it.