# AZ-900 mock exam

This mock exam has 40 questions. We wrote every question for this pack. None comes from Microsoft's practice assessment or from any question bank. The answers are in `mock-exam-answers.md`. Do not open that file until you finish.

## How to sit it

- **Time:** 45 minutes, the same as the real exam. Set a timer before you read Question 1.
- **No help:** no notes, no books, no web search, no AI tool and no other person. The real exam allows none of these.
- **Phone:** put it in another room, or switch it off.
- **Answer every question.** A blank answer scores zero, so make your best guess.
- **"Choose two" questions:** pick exactly two options. You score the point only if both choices are right.
- **Write your answers** in the grid at the end of this file. Then mark them with `mock-exam-answers.md`.

Most questions have one right answer. Questions marked **Choose two** have two.

## Questions

### Question 1

A small company moves its accounting app onto virtual machines from a cloud provider. Under the shared responsibility model, which task always stays with the company?

- A. Replacing failed disks in the datacenter
- B. Providing power and cooling for the servers
- C. Protecting the physical network cables
- D. Managing the accounts of the people who sign in

### Question 2

What is an Azure availability zone?

- A. One or more physically separate datacenters in a region, with independent power, cooling and networking
- B. A second Azure region in the same geography, used for disaster recovery
- C. An isolated instance of Azure for government use
- D. A logical container for resources that share the same life cycle

### Question 3

A video app stores its files in Azure. Users upload and download many files every day. Which statement about Azure data transfer costs is true?

- A. All data that leaves Azure datacenters is free.
- B. Moving data between any two regions in the world costs the same.
- C. Some data going into Azure datacenters is free, but data leaving them is priced by billing zone.
- D. A billing zone is another name for an availability zone.

### Question 4

Which statement describes a private cloud?

- A. One organisation uses it, and it gives that organisation more control over resources and security.
- B. Anyone who wants to buy cloud services can use its resources.
- C. It removes all hardware costs for the organisation that uses it.
- D. It must always be hosted inside the organisation's own building.

### Question 5

Which statement about Azure resource groups is true?

- A. A resource can belong to two resource groups at the same time.
- B. Every resource must belong to exactly one resource group.
- C. You can nest one resource group inside another.
- D. You can rename a resource group at any time after you create it.

### Question 6

A team runs a nightly batch job that converts videos. The job can stop at any time and start again later without harm. The team wants the lowest compute price. Which pricing option fits best?

- A. Reservations for a three-year term
- B. Azure savings plan for compute
- C. Pay-as-you-go virtual machines
- D. Azure Spot Virtual Machines

### Question 7

A hospital keeps patient records on servers it owns and controls. During a vaccination drive, it needs extra capacity for six weeks. Which cloud model lets it add public cloud resources for the busy period and keep its own servers?

- A. Public cloud
- B. Private cloud
- C. Hybrid cloud
- D. Multicloud

### Question 8

A developer wants to run one container in Azure as fast as possible. They do not want to manage virtual machines or set up an orchestration service. Which service fits best?

- A. Azure Kubernetes Service (AKS)
- B. Azure Virtual Machine Scale Sets
- C. Azure Container Instances
- D. Azure Virtual Desktop

### Question 9

Your team creates a monthly budget in Microsoft Cost Management, with an alert at 80%. On day 20, spending reaches 80%. You set up nothing else. What happens?

- A. Azure deletes the most expensive resource in the subscription.
- B. A budget alert appears in cost alerts, and the people on the alert list get an email.
- C. Azure stops every virtual machine in the subscription.
- D. Nothing happens until the end of the billing month.

### Question 10

A college stops buying its own servers and starts paying a monthly cloud bill instead. How does its spending change?

- A. It moves from operational expenditure (OpEx) to capital expenditure (CapEx).
- B. It stays capital expenditure, because the college still uses servers.
- C. It stays operational expenditure, because the college still pays for IT.
- D. It moves from capital expenditure (CapEx) to operational expenditure (OpEx).

### Question 11

Your app runs in an Azure region that has a region pair. Which statement about region pairs is true?

- A. Planned Azure updates roll out to both regions of the pair at the same time.
- B. Every Azure region has a region pair.
- C. The two regions of a pair are always in different geographies.
- D. In a very large outage, Azure prioritises restoring one region of each pair.

### Question 12

Before you deploy anything, you want to estimate the monthly cost of a storage account with GRS redundancy in a region in India. Which tool should you use?

- A. The Azure pricing calculator
- B. Cost analysis in Microsoft Cost Management
- C. Azure Advisor
- D. Azure Service Health

### Question 13

During a festival sale, an online shop adds four more virtual machines behind its load balancer. After the sale, it removes them. What is this an example of?

- A. Horizontal scaling
- B. Vertical scaling
- C. A region pair failover
- D. A capital expenditure

### Question 14

Your web tier runs on identical virtual machines. You want Azure to add or remove machines as demand changes, and to spread traffic across them. What should you use?

- A. An availability set
- B. Azure Virtual Desktop
- C. A region pair
- D. A virtual machine scale set

### Question 15

Finance wants a cost report that splits Azure spending by department. Each department's resources sit in many resource groups. What should you add to each resource?

- A. A resource lock
- B. A management group
- C. A tag
- D. An availability zone

### Question 16

Which cloud benefit describes a system's ability to recover from failures and continue to work?

- A. Scalability
- B. Reliability
- C. Manageability
- D. Predictability

### Question 17

Which two statements about subscriptions and management groups are true? **Choose two.**

- A. Azure produces a separate invoice for each subscription.
- B. A subscription can have two parent management groups.
- C. A policy assigned to a management group applies to the subscriptions under it.
- D. Management groups sit below resource groups in the hierarchy.

### Question 18

Your company allows Azure resources only in two regions in India. You want Azure to block new resources in other regions, and to flag older resources that break the rule. What should you use?

- A. Azure role-based access control (RBAC)
- B. A ReadOnly resource lock
- C. Microsoft Purview
- D. Azure Policy

### Question 19

Microsoft splits cloud manageability into "management of the cloud" and "management in the cloud". Which two are examples of management in the cloud? **Choose two.**

- A. Azure adds resources automatically when demand rises.
- B. An engineer changes resources through a web portal.
- C. Azure replaces a failing resource automatically.
- D. An engineer runs a script with a command-line interface.

### Question 20

A team wants to host a Python REST API on Azure. They want built-in scaling and deployment from GitHub, and they do not want to manage servers. Which service fits best?

- A. Azure Virtual Machines
- B. Azure App Service
- C. Azure Virtual Desktop
- D. Azure Data Box

### Question 21

A user has the Owner role on a resource group. The resource group has a Delete lock. The user tries to delete the resource group. What happens?

- A. The deletion fails until someone removes the lock.
- B. The deletion works, because the Owner role overrides locks.
- C. Azure deletes the resources but keeps the empty resource group.
- D. Azure changes the lock to ReadOnly and then deletes the group.

### Question 22

Which statement about security and governance in the cloud is true?

- A. With IaaS, the cloud provider patches your virtual machine's operating system for you.
- B. Templates cannot change resources after they are deployed.
- C. Cloud providers are well placed to handle distributed denial of service (DDoS) attacks.
- D. Cloud-based auditing works only for private clouds.

### Question 23

Which two statements about Azure networking are true? **Choose two.**

- A. ExpressRoute traffic travels over the public internet inside an encrypted tunnel.
- B. A private endpoint has a private IP address from the virtual network's address space.
- C. Traffic between peered virtual networks stays on the Microsoft backbone network.
- D. You can buy a new domain name directly in Azure DNS.

### Question 24

A company wants one view of where its sensitive data is stored. The data sits in Azure, on its own servers and in Amazon S3. It also wants data classification and data lineage. Which service fits best?

- A. Azure Policy
- B. Microsoft Purview
- C. Azure Arc
- D. Azure Monitor

### Question 25

A team wants to write and deploy its own web app code. It does not want to patch operating systems or manage database software licences. Which cloud service type fits best?

- A. Platform as a service (PaaS)
- B. Infrastructure as a service (IaaS)
- C. Software as a service (SaaS)
- D. An on-premises datacenter

### Question 26

A company wants copies of its storage data spread across three availability zones in one region. It does not need a copy in a second region. Which redundancy option should it choose?

- A. Locally redundant storage (LRS)
- B. Geo-redundant storage (GRS)
- C. Zone-redundant storage (ZRS)
- D. Read-access geo-zone-redundant storage (RA-GZRS)

### Question 27

You are on a library computer where you cannot install any software. You need to run Azure CLI commands against your subscription. What should you use?

- A. Azure Storage Explorer
- B. Azure Arc
- C. Azure Advisor
- D. Azure Cloud Shell

### Question 28

A school wants email for its staff. It does not want to manage servers, updates or the email application itself. Which cloud service type is this?

- A. Infrastructure as a service (IaaS)
- B. Software as a service (SaaS)
- C. Platform as a service (PaaS)
- D. A private cloud

### Question 29

A training centre must keep old exam papers for seven years. Staff almost never open them, and a long wait before reading one is acceptable. Which blob access tier has the lowest storage cost?

- A. Hot
- B. Cool
- C. Cold
- D. Archive

### Question 30

A company runs servers in its own datacenter and Kubernetes clusters in another cloud. It wants to manage them from Azure and apply the same Azure policies to them. Which service fits best?

- A. Azure Kubernetes Service (AKS)
- B. Azure Migrate
- C. Azure Arc
- D. Azure Virtual Desktop

### Question 31

Which statement about serverless computing with Azure Functions is true?

- A. You pay for the function's virtual machine every hour, even when no code runs.
- B. You must patch the operating system that runs your function.
- C. Your function must run all the time so that it can receive requests.
- D. An event starts your code, and Azure charges for the CPU time while it runs.

### Question 32

A film studio must move about 50 terabytes of video into Azure. Its internet connection is slow. Which service fits best?

- A. Azure Data Box
- B. AzCopy
- C. Azure File Sync
- D. Azure Storage Explorer

### Question 33

Which two statements about Azure Resource Manager and ARM templates are true? **Choose two.**

- A. ARM templates describe the resources you want in declarative JSON.
- B. ARM templates must list every deployment command in step-by-step order.
- C. Azure Resource Manager authenticates and authorises requests from the portal, the CLI and PowerShell.
- D. Bicep deploys resources without using Azure Resource Manager.

### Question 34

An old app needs domain join, LDAP and Kerberos authentication. The company does not want to run its own domain controllers in Azure. Which service fits best?

- A. Microsoft Entra Conditional Access
- B. Azure role-based access control (RBAC)
- C. Microsoft Entra Domain Services
- D. Microsoft Purview

### Question 35

Your manager wants personalised recommendations to cut costs and improve the reliability of your existing Azure resources. Which service gives these?

- A. Azure Service Health
- B. Azure Advisor
- C. Azure Policy
- D. Microsoft Purview

### Question 36

An administrator wants staff to sign in without MFA at the office, but to need MFA from unknown locations. What should the administrator use?

- A. Microsoft Entra Conditional Access
- B. Azure Policy
- C. A resource lock
- D. Azure Advisor

### Question 37

One virtual machine stops responding. You want to know whether the problem is on Azure's side or on yours. Which view should you check?

- A. Azure Status
- B. Cost analysis
- C. Azure Advisor
- D. Resource Health

### Question 38

You assign the Reader role to a user at the subscription scope. What can the user do?

- A. Delete any resource in the subscription
- B. View every resource group and resource in the subscription
- C. View resources in every subscription in the organisation
- D. Change role assignments for other users

### Question 39

Your FastAPI app runs on a server in your own datacenter. You want to track its request rates, response times and failure rates with Azure Monitor. Which feature should you use?

- A. Azure Advisor
- B. Azure Service Health
- C. Application Insights
- D. Microsoft Defender for Cloud

### Question 40

Which two statements about Microsoft security models and tools are true? **Choose two.**

- A. Zero Trust trusts any device that is inside the corporate network.
- B. Microsoft Defender for Cloud can protect resources in AWS as well as in Azure.
- C. Azure RBAC uses a deny model, so two role assignments never add their permissions together.
- D. Microsoft Defender for Cloud calculates a secure score to help you decide which security fixes come first.

## Your answers

Write one letter per question, or two letters for a "Choose two" question.

| Q | Answer | Q | Answer | Q | Answer | Q | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | 11 | | 21 | | 31 | |
| 2 | | 12 | | 22 | | 32 | |
| 3 | | 13 | | 23 | | 33 | |
| 4 | | 14 | | 24 | | 34 | |
| 5 | | 15 | | 25 | | 35 | |
| 6 | | 16 | | 26 | | 36 | |
| 7 | | 17 | | 27 | | 37 | |
| 8 | | 18 | | 28 | | 38 | |
| 9 | | 19 | | 29 | | 39 | |
| 10 | | 20 | | 30 | | 40 | |

Time used: ______ minutes. Now open `mock-exam-answers.md`.
