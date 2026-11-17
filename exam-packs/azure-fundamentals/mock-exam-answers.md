# AZ-900 mock exam: answers and scoring guide

Open this file only after you finish `mock-exam.md`. Each answer gives the correct letter, a short reason, the skill area and one official Microsoft Learn page that supports it. We checked every page on 13 November 2026.

Score one point per question. A "Choose two" question scores one point only when both letters are right. The maximum is 40.

## Answers

### Question 1

- **Answer:** D
- **Why:** You always own the accounts and identities in your environment, whatever the service type. The provider always owns the physical datacenter, network and hosts, with their power and cooling.
- **Skill area:** Describe cloud concepts
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/4-describe-shared-responsibility-model>

### Question 2

- **Answer:** A
- **Why:** An availability zone is one or more physically separate datacenters in a region, each with independent power, cooling and networking. Option B describes a region pair, and option C describes a sovereign region.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/5-describe-azure-physical-infrastructure>

### Question 3

- **Answer:** C
- **Why:** Some inbound data transfers into Azure datacenters are free, and outbound transfers are priced by billing zone. A billing zone is a group of regions for pricing, not an availability zone.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-cost-management-azure/2-describe-factors-affect-costs-azure>

### Question 4

- **Answer:** A
- **Why:** A private cloud is used by a single organisation and gives its IT team much greater control. It still needs hardware, and a third party can host it offsite.
- **Skill area:** Describe cloud concepts
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/5-define-cloud-models>

### Question 5

- **Answer:** B
- **Why:** Every resource must belong to exactly one resource group at a time. Resource groups cannot be nested, and they cannot be renamed after you create them.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/6-describe-azure-management-infrastructure>

### Question 6

- **Answer:** D
- **Why:** Spot Virtual Machines use unused Azure capacity at reduced prices, but Azure can reclaim that capacity. That suits interruptible work, such as batch jobs that can restart.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-cost-management-azure/7a-describe-cost-optimization-options>

### Question 7

- **Answer:** C
- **Why:** A hybrid cloud connects public and private clouds. Microsoft gives this exact use: a private cloud surges into public cloud resources for a temporary rise in demand.
- **Skill area:** Describe cloud concepts
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/5-define-cloud-models>

### Question 8

- **Answer:** C
- **Why:** Azure Container Instances is the fastest and simplest way to run a container in Azure, with no virtual machines to manage. AKS is an orchestration service for managing a fleet of containers.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/5-containers>

### Question 9

- **Answer:** B
- **Why:** When the alert condition is met, Azure shows a budget alert in cost alerts and emails the people on the alert list. A budget suspends or changes resources only if you configure automation for it.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-cost-management-azure/6-describe-azure-tool>

### Question 10

- **Answer:** D
- **Why:** Up-front spending on servers and datacenter space is capital expenditure. Paying for cloud services as you use them is classed as operational expenditure.
- **Skill area:** Describe cloud concepts
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/6-describe-consumption-based-model>

### Question 11

- **Answer:** D
- **Why:** In an extensive outage, Azure prioritises one region out of every pair. Planned updates roll out one region at a time, most pairs share a geography, and some regions have no pair.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/5-describe-azure-physical-infrastructure>

### Question 12

- **Answer:** A
- **Why:** The pricing calculator estimates the cost of Azure resources, including storage redundancy options, before you provision them. Nothing is created and nothing is charged when you use it.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-cost-management-azure/3-compare-pricing-total-cost-of-ownership-calculators>

### Question 13

- **Answer:** A
- **Why:** Adding or removing resources, such as virtual machines, is horizontal scaling. Vertical scaling changes the CPU or RAM of one resource.
- **Skill area:** Describe cloud concepts
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/2-high-availability-scalability-cloud>

### Question 14

- **Answer:** D
- **Why:** Scale sets manage groups of identical, load-balanced VMs and can scale out or in based on demand. Availability sets group VMs to reduce the impact of one maintenance event or hardware failure.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/2-virtual-machines>

### Question 15

- **Answer:** C
- **Why:** A tag is a name and value pair on a resource. Tags let you group resources to report costs and allocate internal cost centres.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-cost-management-azure/7-describe-purpose-of-tags>

### Question 16

- **Answer:** B
- **Why:** Microsoft defines reliability as the ability of a system to recover from failures and continue to function.
- **Skill area:** Describe cloud concepts
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/3-reliability-predictability-cloud>

### Question 17

- **Answer:** A and C
- **Why:** Azure generates separate billing reports and invoices for each subscription. Subscriptions inherit conditions from their management group, each has only one parent, and management groups sit above subscriptions.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/6-describe-azure-management-infrastructure>

### Question 18

- **Answer:** D
- **Why:** Azure Policy can prevent noncompliant resources from being created. It also evaluates resources that existed before the policy, and it can require allowed locations.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-features-tools-azure-for-governance-compliance/3-describe-purpose-azure-policy>

### Question 19

- **Answer:** B and D
- **Why:** Management in the cloud is how you manage resources: through a web portal, a command-line interface, APIs or PowerShell. Automatic scaling and replacing failing resources are management of the cloud.
- **Skill area:** Describe cloud concepts
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/5-manageability-cloud>

### Question 20

- **Answer:** B
- **Why:** App Service hosts web apps and REST APIs in languages that include Python, without managing infrastructure. It offers automatic scaling and automated deployment from GitHub.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/7-describe-application-hosting-options>

### Question 21

- **Answer:** A
- **Why:** Resource locks apply regardless of RBAC permissions. Even an owner must remove the lock before the blocked action can happen.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-features-tools-azure-for-governance-compliance/4-describe-purpose-resource-locks>

### Question 22

- **Answer:** C
- **Why:** Microsoft says cloud providers are typically well suited to handle DDoS attacks. With IaaS you manage your own operating system patches, and templates let you update resources at scale.
- **Skill area:** Describe cloud concepts
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/4-security-governance-cloud>

### Question 23

- **Answer:** B and C
- **Why:** A private endpoint has a private IP address from the virtual network's address space. Traffic between peered virtual networks travels on the Microsoft backbone and never enters the public internet.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-networking-services/2-virtual-network>

### Question 24

- **Answer:** B
- **Why:** Microsoft Purview gives a unified view of data on-premises, in multiple clouds and in SaaS apps, including Amazon S3. It offers sensitive data classification and end-to-end data lineage.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-features-tools-azure-for-governance-compliance/2-describe-purpose-microsoft-purview>

### Question 25

- **Answer:** A
- **Why:** In PaaS, the provider maintains the operating systems, middleware and development tools. You do not handle licensing or patching for operating systems and databases.
- **Skill area:** Describe cloud concepts
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/3-describe-platform-service>

### Question 26

- **Answer:** C
- **Why:** Zone-redundant storage copies data synchronously across three availability zones in the primary region. Locally redundant storage keeps all copies in one datacenter, and the geo options add a second region.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/3-redundancy>

### Question 27

- **Answer:** D
- **Why:** Azure Cloud Shell runs in the browser with no local installation. It supports both the Azure CLI and Azure PowerShell, and it knows who you are when you sign in.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-features-tools-manage-deploy-azure-resources/2-describe-interacting-azure>

### Question 28

- **Answer:** B
- **Why:** With SaaS you use a fully developed application, and the provider manages almost all of the application stack. Email is one of Microsoft's own SaaS examples.
- **Skill area:** Describe cloud concepts
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/4-describe-software-service>

### Question 29

- **Answer:** D
- **Why:** The archive tier suits data that is rarely accessed, with flexible latency needs. It has the lowest storage cost, but the highest rehydration delay and access cost.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/4-describe-azure-storage-services>

### Question 30

- **Answer:** C
- **Why:** Azure Arc extends Azure compliance and monitoring to hybrid and multicloud configurations. It can manage servers and Kubernetes clusters that run outside Azure.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-features-tools-manage-deploy-azure-resources/3-describe-purpose-of-azure-arc>

### Question 31

- **Answer:** D
- **Why:** An event wakes an Azure function, so no resources stay provisioned between events. Azure charges only for the CPU time used while the function runs.
- **Skill area:** Describe cloud concepts
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/6-functions>

### Question 32

- **Answer:** A
- **Why:** Azure Data Box ships a physical storage device to you for large transfers. It suits very large data sets, often tens of terabytes or more, when network bandwidth is limited.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/6-identify-azure-data-migration-options>

### Question 33

- **Answer:** A and C
- **Why:** ARM templates describe the resources you want in declarative JSON. Azure Resource Manager receives, authenticates and authorises every request from Azure tools before the service acts.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-features-tools-manage-deploy-azure-resources/4-describe-azure-resource-manager-azure-arm-templates>

### Question 34

- **Answer:** C
- **Why:** Microsoft Entra Domain Services provides domain join, group policy, LDAP and Kerberos authentication without domain controllers to manage. It suits older apps that cannot use modern authentication.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/2-directory-services>

### Question 35

- **Answer:** B
- **Why:** Azure Advisor evaluates your resources and recommends changes for reliability, security, performance, operational excellence and cost. Microsoft calls it a personalised best-practices guide.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-monitoring-tools-azure/2-describe-purpose-of-azure-advisor>

### Question 36

- **Answer:** A
- **Why:** Conditional Access uses signals such as location to decide whether to allow access, ask for MFA or block. A user at a known location might not be asked for a second factor.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/5-conditional-access>

### Question 37

- **Answer:** D
- **Why:** Resource Health looks at individual resources, such as one virtual machine. It shows whether the issue is on Azure's side or yours.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-monitoring-tools-azure/3-describe-azure-service-health>

### Question 38

- **Answer:** B
- **Why:** A Reader assignment at subscription scope lets the user view every resource group and resource in that subscription. Access granted at a parent scope is inherited by all of its child scopes.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/6-role-based-access-control>

### Question 39

- **Answer:** C
- **Why:** Application Insights is an Azure Monitor feature for web apps that run in Azure, on-premises or in another cloud. It tracks request rates, response times and failure rates.
- **Skill area:** Describe Azure management and governance
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-monitoring-tools-azure/4-describe-azure-monitor>

### Question 40

- **Answer:** B and D
- **Why:** Defender for Cloud can protect resources in other clouds, including AWS. It groups its recommendations and calculates a secure score, so teams can prioritise improvements.
- **Skill area:** Describe Azure architecture and services
- **Source:** <https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/9-describe-microsoft-defender-for-cloud>

## Scoring guide

### Step 1: score each skill area

| Skill area | Questions | Points | Target | Your score |
| --- | --- | --- | --- | --- |
| Describe cloud concepts | 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31 | 11 | 9 | |
| Describe Azure architecture and services | 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 34, 36, 38, 40 | 15 | 12 | |
| Describe Azure management and governance | 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 35, 37, 39 | 14 | 11 | |
| **Total** | | **40** | **32** | |

Each target is 80% of the points, rounded down. This mock exam is not scored like the real exam. Do not convert your mark into Microsoft's pass mark of 700.

### Step 2: restudy where you fell short

For every area below its target, find the questions you missed in the table below. Reread the module for each one, then reread the source page in its answer.

| Skill area | Questions | Module to restudy |
| --- | --- | --- |
| Describe cloud concepts | 1, 4, 7, 10 | [Describe cloud computing](https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/) |
| Describe cloud concepts | 13, 16, 19, 22 | [Describe the benefits of using cloud services](https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/) |
| Describe cloud concepts | 25, 28 | [Describe cloud service types](https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/) |
| Describe cloud concepts | 31 | [Describe Azure compute services](https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/) |
| Describe Azure architecture and services | 2, 5, 11, 17 | [Describe the core architectural components of Azure](https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/) |
| Describe Azure architecture and services | 8, 14, 20 | [Describe Azure compute services](https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/) |
| Describe Azure architecture and services | 23 | [Describe Azure networking services](https://learn.microsoft.com/en-us/training/modules/describe-azure-networking-services/) |
| Describe Azure architecture and services | 26, 29, 32 | [Describe Azure storage services](https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/) |
| Describe Azure architecture and services | 34, 36, 38, 40 | [Describe Azure identity, access, and security](https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/) |
| Describe Azure management and governance | 3, 6, 9, 12, 15 | [Describe cost management in Azure](https://learn.microsoft.com/en-us/training/modules/describe-cost-management-azure/) |
| Describe Azure management and governance | 18, 21, 24 | [Describe features and tools in Azure for governance and compliance](https://learn.microsoft.com/en-us/training/modules/describe-features-tools-azure-for-governance-compliance/) |
| Describe Azure management and governance | 27, 30, 33 | [Describe features and tools for managing and deploying Azure resources](https://learn.microsoft.com/en-us/training/modules/describe-features-tools-manage-deploy-azure-resources/) |
| Describe Azure management and governance | 35, 37, 39 | [Describe monitoring tools in Azure](https://learn.microsoft.com/en-us/training/modules/describe-monitoring-tools-azure/) |

Then answer that week's self-check in `study-plan.md` again, without notes.

### Step 3: decide what to do next

| Total score | What to do |
| --- | --- |
| 32 to 40 | Take Microsoft's free [practice assessment](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/practice/assessment?assessment-type=practice&assessmentId=23&practice-assessment-type=certification). If you also score 80% or more there, you are ready to book. |
| 24 to 31 | Spend one more week on the modules from Step 2. Then take the practice assessment. |
| 0 to 23 | Repeat the study plan week for your weakest skill area. Then sit this mock exam again. |

Keep each restudy session to the modules this guide names. Rereading everything takes longer and helps less.
