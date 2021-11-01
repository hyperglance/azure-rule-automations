<img src="https://github.com/hyperglance/azure-rule-automations/blob/master/files/b5dfbb6c-75c8-493b-8c5d-d68b3272cf0f.png" alt="Hyperglance Logo" />

# Hyperglance Rule Automations for Azure

> Enable Hyperglance to automate, fix and optimize your cloud.

This repository contains terraform configurations, that deploy a Azure Storage Account and Azure Function that you connect with your Hyperglance VM. Giving you the power to automate your cloud and fix configuration issues quickly & easily.

## Pre-Requisites

Before you can deploy automations you will need:
1. Terraform CLI - [Install instructions](https://learn.hashicorp.com/tutorials/terraform/install-cli)
2. Azure CLI - [Install instructions](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
3. Func CLI - [Install instructions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
4. A Python (3) Interpreter

### Azure role assignments

This deployment utilizes system assigned managed identities to limit the scope of the Azure function to the subscription it is deployed in. 

To [assign Azure roles to a managed identity](https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal-managed-identity), you must have:

* Microsoft.Authorization/roleAssignments/write permissions

## Storage account permissions

The account under which Hyperglance run needs to be able to write to the Storage Account used by the automations. This may be achieved by granting Hyperglance the ```Storage Account Contributor``` built-in role.

## Quick Start

1. Follow the pre-requisite steps above. If you are deploying to Azure Government [see the notes the below](#azure-government).

2. Connect the Azure CLI to the Azure account that you wish to deploy the function in and set the subscription to use: `az login`

	__Note:__ Guidance on authenticating to Azure can be found [here](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli)
	
	Example:
	```bash
	 az login
	 az account set --subscription <subscription name>
	```

3. Clone our repo or  [download the zip](https://github.com/hyperglance/azure-rule-automations/archive/refs/heads/master.zip)
	```bash
	 git clone https://github.com/hyperglance/azure-rule-automations.git
	```

4.  Navigate to the terraform deployment directory 
	
	```
	cd azure-rule-automations/deployment/terraform/automations
    ```

	Create a a file ```subscriptions.csv``` with the subscriptions you want to act on separated by a comma.

	```
	MySubscription, AnotherSubscriptionOfMine, ...
	```

5a (_Optional_).  To use the automations accross __multiple subscriptions__, generate the correct terraform configuration for your environment. 
 
	_Windows_
	```
	py -3 provision.py
	```

	_Unix_	
	```
	python3 provision.py
	```

5b. Deploy the stack:
	> Terraform will prompt for the region you wish to deploy to and for final confirmation.
	```
	 terraform init
	 terraform apply
	```

6. Once complete, the storage account ID and  will be returned:
	```bash
	Apply complete! Resources: 11 added, 0 changed, 0 destroyed.

	Outputs:

    func_command = "func azure functionapp publish hyperglance-automations-legible-buffalo"
    storage_account_resource_id = "/subscriptions/<subscription ID>/resourceGroups/hyperglance-automations-legible-buffalo/providers/Microsoft.Storage/storageAccounts/rii5it09y343"
	```
 
   *The storage account ID is required to configure automations in Hyperglance*
   *The func command is required to deploy the function code to the Azure function*
	
	Copy the storage account ID into the Hyperglance UI:  __Settings ➔ Automations ➔ Azure ➔ Storage Account Resource ID__
	or visit this URL: https://your-hyperglance-ip/#/admin/automations

7. Deploy the function code to the function

    Change directory to the root of the repo and execute the func command generated by Terraform:

	```bash
     cd azure-rule-automations
	 func azure functionapp publish <The unique name generated by terraform>
	```

8. __That's it - Automations are now enabled against this subscription!__
	* Within Hyperglance click on any rule or visit the Advanced Search page to start exploring automations features.

# Azure Government

To deploy Hyperglance automations to Azure Government a couple of extra steps must be taken.

Before login issue azure the following command 

```az cloud set --name AzureUSGovernment```

Then set an appropriate Government region location in:

`<azure-automations-dir>/deployment/terraform/automations/main.tf`

_for example, the contents of the file may look like_

```
module "hyperglance-automations" {
  region = "usgovvirginia"
  source = "../modules/hyperglance-automations"
  utilised-subscriptions-script = "../../metadata/parse_subscriptions.py"
}
```

## Contributions
Are welcome!
