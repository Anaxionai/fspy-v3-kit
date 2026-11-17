# AZ-900 study plan: three weeks

This plan takes about 30 hours over three weeks. You study six days a week, for 1 to 2 hours a day. Take the seventh day off.

Each day has three parts:

- **Learn:** one free Microsoft Learn module, or part of one. Read every unit and take the module assessment (the short quiz at the end).
- **Try:** a short activity that needs no Azure account. It links the new Azure words to work you did in FSPY-V3.
- **Done when:** how you know the day is finished.

Keep one notebook for the whole plan. Give it two sections:

1. **Glossary:** each new Azure term, with a definition of ten words or fewer.
2. **AWS to Azure:** a two-column table. Write the AWS name you used in the course on the left. Write the Azure name on the right.

Sign in to Microsoft Learn with a personal Microsoft account before Day 1. Signing in saves your progress and module assessment results.

## Hands-on practice and safety rules

Microsoft Learn no longer offers free sandboxes. The [Microsoft Learn FAQ](https://learn.microsoft.com/en-us/training/support/faq) says exercises now need your own Azure subscription. This plan works without one. Every "Try" step below needs no Azure account.

Some steps list an **optional** guided project that runs in a real Azure account. Do them only if you already have a subscription, or you choose to open a free account with a card. If you do, follow these rules every time:

1. Before you create anything, write down the name of one new resource group for the session, for example `rg-az900-yourname-0113`.
2. Create every resource inside that resource group.
3. Finish the guided project in one sitting. Never leave anything running overnight.
4. If you added a resource lock, remove it first. A lock blocks deletion, even for an owner.
5. End the session by deleting the resource group. In Cloud Shell, run `az group delete --name rg-az900-yourname-0113 --yes`. In the portal, open the resource group and select **Delete resource group**.
6. If the project created something outside the resource group, such as a budget or a policy assignment, delete it too. The guided projects in this plan end with a "Clean up resources" unit. Follow it.
7. Check **All resources** in the portal. It must be empty before you close the browser.

The `az group delete` command is documented on the [az group reference page](https://learn.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest).

## Week 1: cloud concepts and the shape of Azure (about 10 hours)

### Day 1 (1.5 hours): set a baseline

- **Learn:** read `README.md` in this pack. Then read the skills list in the [AZ-900 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900).
- **Try:** open the [exam sandbox](https://aka.ms/examdemo) for 15 minutes. Learn how to move between questions and mark one for review.
- **Try:** take Microsoft's free [practice assessment](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/practice/assessment?assessment-type=practice&assessmentId=23&practice-assessment-type=certification) once, without studying. Write your score in your notebook. A low score today is normal.
- **Done when:** you have a baseline score and an empty glossary ready.

### Day 2 (2 hours): what the cloud is

- **Learn:** [Describe cloud computing](https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/).
- **Try:** find your table from MAP: "What a cloud is: IaaS, PaaS and serverless". Add three rows that are always yours: data, devices and identities. Check them against the [shared responsibility unit](https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/4-describe-shared-responsibility-model).
- **Try:** write one sentence each for public, private, hybrid and multicloud. Use a bank, a startup, a hospital and a company moving between providers as examples.
- **Done when:** you pass the module assessment and can explain CapEx and OpEx in one sentence each.

### Day 3 (1.5 hours): the benefits vocabulary

- **Learn:** [Describe the benefits of using cloud services](https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/).
- **Try:** P12 TiffinTrack scaled the WebSocket server by adding pods. Write whether that was vertical or horizontal scaling, and why.
- **Try:** write one line each for high availability, scalability, reliability, predictability, security, governance and manageability. Use an example from P12 or P13 where you can.
- **Done when:** you pass the module assessment and your seven lines are in the glossary.

### Day 4 (1.5 hours): IaaS, PaaS and SaaS

- **Learn:** [Describe cloud service types](https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/).
- **Try:** open your work from MAP: "Fill in the four-cloud map for six common jobs". Label each Azure service on it as IaaS, PaaS or serverless. Then name two SaaS products you use every day.
- **Done when:** you pass the module assessment and can give one use case for each service type.

### Day 5 (2 hours): regions, zones and the resource hierarchy

- **Learn:** [Describe the core architectural components of Azure](https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/).
- **Try:** open the [Azure pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/) and add a Virtual Machines estimate. Open its region list and find the regions in India. The calculator creates nothing and charges nothing.
- **Try:** draw the hierarchy for an imaginary training centre. Show one management group and two subscriptions (Dev and Prod). Add resource groups to each subscription, and resources to each group.
- **Done when:** you pass the module assessment and can say what happens to the resources when you delete a resource group.

### Day 6 (1.5 hours): review week 1

- **Learn:** reread your glossary. Reread any unit where you got a module assessment question wrong.
- **Try:** start your AWS to Azure table with the pairs you can already make. AWS region and Azure region is the first pair.
- **Done when:** you have answered the week 1 self-check below without notes.

### Week 1 self-check

Answer in writing, without notes. Then check your answers against the key.

1. Name the three things you are always responsible for, whatever cloud service type you use.
2. What is the difference between scaling up and scaling out?
3. Why is cloud spending classed as OpEx and not CapEx?
4. In an Azure region that supports availability zones, what is the smallest number of zones?
5. Put these in order, from the largest to the smallest: resource group, management group, resource, subscription.

**Key:**

1. The information and data stored in the cloud, the devices allowed to connect, and the accounts and identities. ([Shared responsibility](https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/4-describe-shared-responsibility-model))
2. Scaling up (vertical) adds CPU or RAM to one resource. Scaling out (horizontal) adds more resources, such as more VMs or containers. ([Scalability](https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/2-high-availability-scalability-cloud))
3. You pay for cloud services over time as you use them, with no up-front hardware purchase. ([Consumption-based model](https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/6-describe-consumption-based-model))
4. Three. Not every region supports availability zones. ([Physical infrastructure](https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/5-describe-azure-physical-infrastructure))
5. Management group, subscription, resource group, resource. ([Management infrastructure](https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/6-describe-azure-management-infrastructure))

## Week 2: Azure services and security (about 10.5 hours)

### Day 1 (2 hours): compute and hosting

- **Learn:** [Describe Azure compute services](https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/).
- **Try:** redo the Azure column of your four-cloud map with exact names. Choose between Azure Container Instances, Azure Container Apps, AKS, Azure Functions, App Service and Virtual Machines for each job. Databases are not in the current AZ-900 skills list, so skip that row.
- **Try:** P13 asked where to run a container: a VM, a managed service or Kubernetes. Write the Azure service for each of those three answers.
- **Done when:** you pass the module assessment and can explain when you would pick a scale set.

### Day 2 (1.5 hours): networking

- **Learn:** [Describe Azure networking services](https://learn.microsoft.com/en-us/training/modules/describe-azure-networking-services/).
- **Try:** draw a diagram on paper. Show an office connected to a virtual network by VPN Gateway, and a second office connected by ExpressRoute. Add two subnets, a peered virtual network in another region, and one public and one private endpoint.
- **Done when:** you pass the module assessment and can say which connection avoids the public internet.

### Day 3 (2 hours): storage

- **Learn:** [Describe Azure storage services](https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/).
- **Try:** open your ReelPipe project from P8: "Add an Azure backend on Azurite". Find where your code names the storage account, the container and the blob. Add those three terms to your glossary.
- **Try:** in the [pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/), add a Storage Accounts estimate in a region in India. Change the redundancy from LRS to GRS, then the access tier from Hot to Cool. Note how the estimate moves each time.
- **Done when:** you pass the module assessment and can name the six redundancy options in order of protection.

### Day 4 (2 hours): identity and access

- **Learn:** [Describe Azure identity, access, and security](https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/), units 1 to 6 (from the introduction to role-based access control).
- **Try:** in P5 you built "Sign in with Google" with OpenID Connect. Write two lines on how Microsoft Entra ID plays the same part for apps that use Microsoft accounts.
- **Try:** in P5 you wrote a permission matrix. Rewrite one row as an Azure role assignment: who, which role (Owner, Contributor or Reader) and which scope.
- **Done when:** you can explain the difference between authentication and authorisation, and name the three passwordless options.

### Day 5 (1.5 hours): security models and Defender for Cloud

- **Learn:** the same module, from "Describe Zero Trust model" to the end. Take the module assessment.
- **Try:** list the seven defence in depth layers from outside to inside. Next to each layer, write one control you used in FSPY-V3. For example, P13 MFA on the cloud account belongs to the identity and access layer.
- **Done when:** you pass the module assessment.

### Day 6 (1.5 hours): review week 2

- **Learn:** reread the units where you made mistakes this week.
- **Try:** add at least eight new pairs to your AWS to Azure table. Examples: S3 to Blob Storage, SQS to Queue Storage, Lambda to Azure Functions, IAM roles to Azure RBAC roles.
- **Done when:** you have answered the week 2 self-check below without notes.

### Week 2 self-check

1. Which Azure service gives remote staff Windows desktops that run in Azure?
2. How does a VPN Gateway connection differ from ExpressRoute?
3. Which blob access tier has the lowest storage cost but the highest cost and delay to read data back?
4. What does Conditional Access look at to make a decision, and what can it decide?
5. Name the three Zero Trust principles.

**Key:**

1. Azure Virtual Desktop. ([Azure Virtual Desktop](https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/4-virtual-desktop))
2. A VPN Gateway sends encrypted traffic over the public internet. ExpressRoute is a private connection through a connectivity provider that does not use the public internet. ([VPN Gateway](https://learn.microsoft.com/en-us/training/modules/describe-azure-networking-services/3-virtual-private-networks), [ExpressRoute](https://learn.microsoft.com/en-us/training/modules/describe-azure-networking-services/4-expressroute))
3. Archive. ([Storage services](https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/4-describe-azure-storage-services))
4. It looks at signals such as the user, their location, their device and the app. It can allow access, require MFA or block access. ([Conditional Access](https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/5-conditional-access))
5. Verify explicitly, use least privilege access, and assume breach. ([Zero Trust](https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/7-describe-zero-trust-model))

## Week 3: management, governance and exam practice (about 9.5 hours)

### Day 1 (2 hours): cost management

- **Learn:** [Describe cost management in Azure](https://learn.microsoft.com/en-us/training/modules/describe-cost-management-azure/).
- **Try:** open `cloud.md` from P8 ReelPipe. Build the same estimate for Azure in the [pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/): a storage account, a queue and Azure Functions. Write two lines on what changes the Azure price most.
- **Try:** in MAP you learned that a budget does not stop spending. Check whether that is still true for an Azure budget, using the Cost Management unit.
- **Done when:** you pass the module assessment and can name the three types of cost alert.

### Day 2 (1.5 hours): governance and compliance

- **Learn:** [Describe features and tools in Azure for governance and compliance](https://learn.microsoft.com/en-us/training/modules/describe-features-tools-azure-for-governance-compliance/).
- **Try:** imagine one shared subscription for the next FSPY-V3 batch. Write three Azure Policy rules you would set and one resource lock. For each, say what mistake it prevents.
- **Optional, real account:** the guided project [Organize and protect resources with tags and locks](https://learn.microsoft.com/en-us/training/modules/guided-project-organize-resources-tags-locks/). Follow the safety rules above.
- **Done when:** you pass the module assessment and can say how Azure Policy differs from Azure RBAC.

### Day 3 (1.5 hours): tools and infrastructure as code

- **Learn:** [Describe features and tools for managing and deploying Azure resources](https://learn.microsoft.com/en-us/training/modules/describe-features-tools-manage-deploy-azure-resources/).
- **Try:** open your OpenTofu files from P11. Write which parts are declarative (you describe the end state). Then write what an ARM template or a Bicep file would do in their place.
- **Optional, real account:** the guided project [Manage Azure resources with Cloud Shell and the Azure CLI](https://learn.microsoft.com/en-us/training/modules/guided-project-manage-resources-cloud-shell-cli/). Follow the safety rules above.
- **Done when:** you pass the module assessment and can say which tool you would use with no local install.

### Day 4 (1 hour): monitoring

- **Learn:** [Describe monitoring tools in Azure](https://learn.microsoft.com/en-us/training/modules/describe-monitoring-tools-azure/).
- **Try:** open the public [Azure status page](https://azure.status.microsoft/en-us/status). This is the global view inside Azure Service Health. Write what the other two Service Health views add.
- **Try:** in P12 you used OpenTelemetry, Prometheus and Grafana. Write the Azure Monitor feature that plays a similar part for each one.
- **Done when:** you pass the module assessment.

### Day 5 (1.5 hours): mock exam

- **Learn:** sit `mock-exam.md` in this pack under exam rules: 45 minutes, no notes, no AI.
- **Try:** mark it with `mock-exam-answers.md`. Fill in the scoring table at the end of that file.
- **Done when:** you have a score for each skill area and a list of units to restudy.

### Day 6 (2 hours): close the gaps and decide

- **Learn:** restudy the units that the scoring guide sends you to.
- **Try:** take Microsoft's [practice assessment](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/practice/assessment?assessment-type=practice&assessmentId=23&practice-assessment-type=certification) again. Compare the score with your Day 1 baseline.
- **Done when:** you have decided whether to book. A good rule: book when you score 80% or more on both the mock exam and the practice assessment. If you are not there yet, add one more week of review.

### Week 3 self-check

1. When spending passes a budget's alert level, what happens? Does the budget stop resources by itself?
2. You add a tag to a resource group. Do the resources inside it get the tag too?
3. Which type of resource lock lets people change a resource but not delete it?
4. Which service lets you manage servers in your own datacenter and in another cloud from Azure?
5. Which tool tells you whether an Azure outage affects the services and regions you use?

**Key:**

1. Azure raises a budget alert in cost alerts and emails the people on the alert list. A budget changes or stops resources only if you set up automation for it. ([Cost Management](https://learn.microsoft.com/en-us/training/modules/describe-cost-management-azure/6-describe-azure-tool))
2. No. Resources do not inherit tags from resource groups or subscriptions. Azure Policy can add or enforce tags. ([Tags](https://learn.microsoft.com/en-us/training/modules/describe-cost-management-azure/7-describe-purpose-of-tags))
3. A Delete lock. A ReadOnly lock blocks changes and deletion. ([Resource locks](https://learn.microsoft.com/en-us/training/modules/describe-features-tools-azure-for-governance-compliance/4-describe-purpose-resource-locks))
4. Azure Arc. ([Azure Arc](https://learn.microsoft.com/en-us/training/modules/describe-features-tools-manage-deploy-azure-resources/3-describe-purpose-of-azure-arc))
5. Service Health, one of the three views in Azure Service Health. ([Service Health](https://learn.microsoft.com/en-us/training/modules/describe-monitoring-tools-azure/3-describe-azure-service-health))
