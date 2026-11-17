# Study plan: three weeks to the AWS Cloud Practitioner exam

This plan has 18 study days over three weeks. Each day is one block of 1 to 2 hours. The whole plan takes about 29 hours.

Study six days a week and rest one day. If you miss a day, move the plan back by one day. Do not squeeze two days into one.

"CPE" means the AWS Cloud Practitioner Essentials course on AWS Skill Builder: <https://skillbuilder.aws/learn/94T2BEN85A/aws-cloud-practitioner-essentials/8D79F3AVR7>. "MAP" means the map weeks of FSPY-V3.

## Before you start: your AWS account

Some days have a short hands-on part in the AWS console (the AWS website where you manage your account). Read these rules first.

- **Use an account on the AWS Free plan.** On this plan, AWS does not charge you. The plan ends after six months or when your credits run out, and the account then closes. See <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html>.
- **Do not create or join an organisation in AWS Organizations, and do not set up AWS Control Tower.** Either action moves a Free plan account to the Paid plan.
- **If your account is on the Paid plan**, AWS bills any usage that your credits do not cover. Keep your budget alarm on and follow every teardown line.
- **Sign in as your IAM admin user, not the root user.** For the AWS CLI, use `aws login`, as you did in P13.
- **Work in Asia Pacific (Mumbai), `ap-south-1`,** unless a step names another Region.
- **Do not turn on paid security services**, such as Amazon GuardDuty, AWS Security Hub, Amazon Inspector or Amazon Macie. Read about them instead.
- **Every hands-on step ends with a teardown line.** Do the teardown the same day. Never leave anything running.

## Week 1: cloud concepts, global infrastructure and shared responsibility

Week 1 covers exam domain 1 (Cloud Concepts) and starts domains 2 and 3. Total: about 10 hours.

### Day 1: your starting point (1.5 hours)

Read:
- `README.md` in this folder: the exam facts and the "What you already know" tables.
- The exam guide's four domain pages, from the links on <https://docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/cloud-practitioner-02.html>.

Do:
1. Create a free AWS Skill Builder account. Open the Exam Prep Plan at <https://skillbuilder.aws/category/exam-prep/cloud-practitioner-foundational-CLF-C02>.
2. Take the Official Practice Question Set (20 questions) from step 1 of the plan. Do not study first. Write down your score. This is your starting point.
3. Enrol in CPE. Do not start it yet.

Hands-on (10 minutes):
1. If your account still has the $5 budget alarm from P13, check that its email address is right, and skip step 2.
2. Otherwise, open AWS Budgets in the console. Choose Create budget, then the "Zero spend budget" template (a budget that emails you when spending goes above the Free Tier limits). Enter your email address and create it. See <https://docs.aws.amazon.com/cost-management/latest/userguide/budget-templates.html>.

Teardown: none today. A budget only watches your spending. If you made the zero-spend budget, you delete it on Day 18.

### Day 2: why companies use the cloud (1.5 hours)

Watch: CPE module 1, "Introduction to the Cloud".

Read:
- Six advantages of cloud computing: <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/six-advantages-of-cloud-computing.html>
- Types of cloud computing (cloud, hybrid and on-premises): <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/types-of-cloud-computing.html>

On paper:
1. Write the six advantages from memory. Check them against the page.
2. For each advantage, write one example from FSPY-V3. For example, the MAP lesson "How cloud billing works, and how bills surprise people" showed pay-as-you-go.
3. Write one line on elasticity (adding and removing resources as demand changes). Then write one line on economies of scale (lower prices from combining many customers' usage).

### Day 3: the AWS Well-Architected Framework (2 hours)

Watch: CPE module 13, "Well-Architected Solutions".

Read:
- The six pillars: <https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html>
- Reliability design principles: <https://docs.aws.amazon.com/wellarchitected/latest/framework/rel-dp.html>
- Sustainability design principles: <https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-design-principles.html>

On paper: draw a table with one row for each pillar. Write what the pillar cares about, and one thing Shortly did for it in P13.

Hands-on (20 minutes): the AWS Well-Architected Tool (a console tool that reviews a workload against the pillars). AWS offers it at no charge, as the AWS CAF overview says: <https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/welcome.html>. Its user guide is <https://docs.aws.amazon.com/wellarchitected/latest/userguide/>.
1. Open the Well-Architected Tool and choose Define workload.
2. Name it `shortly-exam-practice`, choose the Mumbai Region, and save.
3. Start the review and answer the first three questions of the Reliability pillar for Shortly.
4. If the tool is not available on your account plan, answer the same questions on paper from the reliability page.

Teardown: delete the `shortly-exam-practice` workload.

### Day 4: moving to the cloud (1.5 hours)

Watch: CPE module 12, "Migrating to the AWS Cloud".

Read:
- AWS Cloud Adoption Framework (AWS CAF) perspectives: <https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/foundational-capabilities.html>
- The seven migration strategies (the "7 Rs"): <https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html>
- Licensing: the Bring Your Own License (BYOL) model, on <https://docs.aws.amazon.com/license-manager/latest/userguide/license-manager.html>

On paper:
1. List the six CAF perspectives. Write one person who cares about each, for example "People: the head of HR".
2. Invent four small apps at a college. Choose one of the 7 Rs for each and say why in one sentence.

### Day 5: Regions, Availability Zones and edge locations (2 hours)

Watch: CPE module 4, "Going Global".

Read:
- AWS Regions: <https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html>
- AWS Availability Zones: <https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-availability-zones.html>
- Regions and Zones for EC2: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html>
- Edge locations, through Amazon CloudFront: <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html>

Hands-on (15 minutes, read-only):
1. Sign in with `aws login`.
2. Run this command. It lists the Availability Zones of the Mumbai Region and creates nothing.

   ```bash
   aws ec2 describe-availability-zones --region ap-south-1 --filters Name=zone-type,Values=availability-zone --query "AvailabilityZones[].{ZoneName:ZoneName,ZoneId:ZoneId}"
   ```

3. In the console, open the Region menu. Find Asia Pacific (Hyderabad). It is an opt-in Region (a Region you must turn on before use). Do not turn it on.

Teardown: you created nothing.

On paper: draw one Region with three Availability Zones. Put Shortly's server in one zone. Then redraw it so that Shortly survives the loss of one zone.

### Day 6: the shared responsibility model and the week 1 self-check (1.5 hours)

Read:
- The shared responsibility model: <https://aws.amazon.com/compliance/shared-responsibility-model/>
- The table that compares on-premises, Amazon EC2 and Amazon RDS: <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html>
- What AWS Lambda manages for you: <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>

On paper: draw three columns, EC2, RDS and Lambda. List who patches the operating system, who backs up data, and who writes the code.

#### Week 1 self-check

Answer in writing, without notes. Then check each answer on the linked page.

1. Name the six advantages of cloud computing.
2. Name the six pillars of the Well-Architected Framework.
3. A company moves an app to AWS with no changes. Which of the 7 Rs is this? Which R means switching to a software-as-a-service product?
4. What is an Availability Zone? Why run an app in more than one?
5. Who patches the guest operating system on Amazon EC2? Who patches the operating system under AWS Lambda?

Answers:
1. Trade fixed expense for variable expense; benefit from massive economies of scale; stop guessing capacity; increase speed and agility; stop spending money running and maintaining data centres; go global in minutes. [Six advantages](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/six-advantages-of-cloud-computing.html)
2. Operational excellence, security, reliability, performance efficiency, cost optimization, sustainability. [The pillars](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html)
3. Rehost ("lift and shift"). Repurchase ("drop and shop"). [Migration strategies](https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html)
4. One or more separate data centres in a Region, with redundant power, networking and connectivity, in separate buildings. More than one zone protects you from the failure of one location. [Global infrastructure](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/global-infrastructure.html)
5. On EC2, you do. Under Lambda, AWS does. [Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) and [What is AWS Lambda?](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)

If you got fewer than four right, repeat the day that covers each missed question before you start week 2.

## Week 2: security, compute and databases

Week 2 covers exam domain 2 (Security and Compliance) and the compute and database parts of domain 3. Total: about 10 hours.

### Day 7: IAM and the root user (2 hours)

Watch: CPE module 9, "Security".

Read:
- The root user, and the tasks only it can do: <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html>
- Root user best practices: <https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html>
- IAM groups: <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html>
- Managed and inline policies: <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html>
- AWS IAM Identity Center (one sign-in for many accounts): <https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html>

Hands-on (30 minutes). IAM has no additional charge: <https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html>.
1. In the IAM console, create a user group named `exam-readers`. Attach the AWS managed policy `ReadOnlyAccess`.
2. Create a user named `exam-test-user` with no console access. Add it to `exam-readers`.
3. Open the IAM policy simulator for `exam-test-user`. Test `s3:ListAllMyBuckets`, which the group allows, and `s3:CreateBucket`, which it does not. See <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html>.
4. Compare this with the P8 lesson "Cloud identity: IAM users, roles and policies". Write one line on why a group is better than a policy on each user.

Teardown: delete `exam-test-user`, then delete the `exam-readers` group.

### Day 8: logs, audits and compliance (1.5 hours)

Watch: CPE module 10, "Monitoring, Compliance, and Governance in the AWS Cloud".

Read:
- AWS CloudTrail (who did what): <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html>
- AWS Config (how resources were set up over time): <https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html>
- AWS Artifact (AWS compliance reports): <https://docs.aws.amazon.com/artifact/latest/ug/what-is-aws-artifact.html>
- Amazon CloudWatch (metrics, logs and alarms): <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html>

Hands-on (20 minutes, read-only):
1. Open CloudTrail and choose Event history. Event history is free to view.
2. Switch the console Region to US East (N. Virginia). CloudTrail records IAM events there. See <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html>.
3. Filter by event name `CreateUser`. Find the event for `exam-test-user` from Day 7. Note who created it and when.
4. Open AWS Artifact and choose Reports. Find one ISO report and one SOC report. You do not need to download them.

Teardown: you created nothing. Switch the console Region back to Mumbai.

On paper: write one sentence on how CloudTrail differs from AWS Config, and one on how both differ from CloudWatch.

### Day 9: security services (2 hours)

Read:
- The security services overview, which covers AWS Shield and AWS WAF: <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/security-services.html>
- Amazon GuardDuty: <https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html>
- Amazon Inspector: <https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html>
- AWS Key Management Service (AWS KMS): <https://docs.aws.amazon.com/kms/latest/developerguide/overview.html>
- AWS Secrets Manager: <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>
- AWS Trusted Advisor: <https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html>
- The "Domain 2" table in `README.md`, for every other security service.

On paper: make a table with three columns: the job, the AWS service, and the FSPY-V3 lesson that did a similar job. For example: "scan images for known weaknesses", "Amazon Inspector", "P11 task 'Scan the image with Trivy and fail on critical issues'". Fill in at least 12 rows.

Hands-on (10 minutes, read-only):
1. Open Trusted Advisor in the console and look at the security checks. With Basic Support you see a selection of them.
2. If the "MFA on root account" check is in your list, confirm that it passes.

Teardown: you created nothing.

### Day 10: compute (2 hours)

Watch: CPE module 2, "Compute in the Cloud", and module 3, "Exploring Compute Services".

Read:
- EC2 instance types: <https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-types.html>
- Compute optimized instances: <https://docs.aws.amazon.com/ec2/latest/instancetypes/co.html>
- Amazon EC2 Auto Scaling: <https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html>
- Elastic Load Balancing: <https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html>
- AWS Fargate: <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html>

On paper:
1. Reread your notes from the P13 lesson "Where to run a container: a VM, a managed service or Kubernetes".
2. Add four rows to them: AWS Elastic Beanstalk, Amazon Lightsail, AWS Batch and AWS Outposts. Use the `README.md` gap list.
3. Write which instance family suits each job: video encoding, an in-memory database, a small test web server.

No hands-on today. Do not launch EC2 instances or load balancers for this plan.

### Day 11: databases (1.5 hours)

Watch: CPE module 7, "Databases".

Read:
- Amazon RDS, including the responsibility table: <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html>
- Amazon DynamoDB: <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html>
- AWS Database Migration Service (AWS DMS): <https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html>

Hands-on (20 minutes):
1. In the DynamoDB console, create a table named `exam-players`. Use `player_id` (String) as the partition key. Keep the default settings.
2. Add two items, each with a `player_id` and a `score` (Number).
3. Scan the table and see both items. Compare this with the P9 lesson "MongoDB basics: collections, queries and indexes".

Teardown: delete the `exam-players` table.

On paper: write which AWS database fits each case: PostgreSQL with less admin work, a key-value store at any scale, a cache in front of a database, a graph of friends.

### Day 12: review and the week 2 self-check (1 hour)

Reread your Day 9 table. Then do the self-check.

#### Week 2 self-check

1. Name two tasks that only the root user can do in a standalone account.
2. How does AWS CloudTrail differ from AWS Config?
3. Name the service for each job. (a) It scans EC2 instances and container images for software weaknesses. (b) It detects threats from CloudTrail, VPC flow logs and DNS logs. (c) It finds sensitive data in Amazon S3.
4. Which EC2 instance family suits media transcoding? What do Elastic Load Balancing and EC2 Auto Scaling each do?
5. When would you choose Amazon RDS over PostgreSQL on EC2? When would you choose DynamoDB?

Answers:
1. Any two of: close the account; change the root user's email address, password or access keys; restore IAM user permissions; register as a seller in the Reserved Instance Marketplace. [AWS account root user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html)
2. CloudTrail records actions by users, roles and services. Config records the configuration of resources over time and checks them against rules. [CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) and [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)
3. (a) Amazon Inspector, (b) Amazon GuardDuty, (c) Amazon Macie. [Inspector](https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html), [GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html), [Macie](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
4. Compute optimized. Elastic Load Balancing spreads traffic across healthy targets. EC2 Auto Scaling adds and removes instances as demand changes. [Compute optimized](https://docs.aws.amazon.com/ec2/latest/instancetypes/co.html) and [Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html)
5. Choose RDS when you want AWS to handle backups, patching and failover. Choose DynamoDB for a serverless NoSQL database with fast responses at any scale. [Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html) and [DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)

If you got fewer than four right, repeat the day that covers each missed question before you start week 3.

## Week 3: network, storage, other services, billing and the mock exam

Week 3 finishes domain 3, covers domain 4 (Billing, Pricing, and Support) and ends with the mock exam. Total: about 9 hours.

### Day 13: networking (1.5 hours)

Watch: CPE module 5, "Networking".

Read:
- Amazon VPC: <https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html>
- Security groups compared with network ACLs: <https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html>
- Amazon Route 53: <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html>
- AWS Direct Connect: <https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html>
- AWS Site-to-Site VPN: <https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html>

Hands-on (15 minutes, read-only):
1. Open the VPC console in the Mumbai Region. Find the default VPC.
2. Look at its subnets. Note which Availability Zone each subnet is in.
3. Look at its route table, its internet gateway, its default security group and its default network ACL.
4. Do not create a NAT gateway. AWS charges for each hour that a NAT gateway is available, even when idle: <https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html>.

Teardown: you created nothing.

On paper: draw the default VPC. Mark where a security group applies and where a network ACL applies.

### Day 14: storage (1.5 hours)

Watch: CPE module 6, "Storage".

Read:
- S3 storage classes: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html>
- S3 Lifecycle rules: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>
- Instance store data loss: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-store-lifetime.html>
- Amazon EFS: <https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html>
- AWS Backup: <https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html>

Hands-on (20 minutes):
1. Create an S3 bucket in Mumbai with a unique name, such as `exam-pack-yourname-1311`. Keep Block Public Access turned on.
2. Upload one small text file.
3. On the bucket's Management tab, create a lifecycle rule for all objects. Move objects to S3 Glacier Flexible Retrieval after 30 days, and expire them after 365 days.
4. Open the object and note its storage class today.

Teardown: delete the object, then delete the bucket. The rule never runs, because you delete the bucket today.

On paper: write which storage fits each case: an EC2 boot disk, scratch data you can lose, files shared by many servers, seven-year archives.

### Day 15: AI/ML, analytics and other services (1.5 hours)

Watch: CPE module 8, "AI/ML and Data Analytics".

Read:
- The machine learning services overview: <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/machine-learning.html>
- The analytics services overview: <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/analytics.html>
- Amazon SNS: <https://docs.aws.amazon.com/sns/latest/dg/welcome.html>
- Amazon EventBridge: <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html>
- The "Domain 3" table in `README.md`, for developer tools, end-user computing, AWS Amplify and AWS IoT Core.

On paper:
1. Make flash cards, one service per card: Amazon SageMaker AI, Lex, Polly, Transcribe, Translate, Comprehend, Rekognition, Textract, Q, Athena, Kinesis, Glue, Redshift, EMR, OpenSearch Service and Quick.
2. Write the job on the back of each card, in five words or fewer.
3. Write one sentence each on when to use SNS, SQS and EventBridge. Use your P8 notes on queues.

No hands-on today.

### Day 16: pricing models and billing tools (1.5 hours)

Watch: CPE module 11, "Pricing and Support", up to the part on support.

Read:
- EC2 purchasing options: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html>
- Savings Plans: <https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html>
- Consolidated billing in AWS Organizations: <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing.html>
- Cost allocation tags: <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>
- Data transfer as a cost driver: <https://docs.aws.amazon.com/whitepapers/latest/how-aws-pricing-works/key-principles.html>

Hands-on (30 minutes):
1. Open AWS Pricing Calculator at <https://calculator.aws/>. You do not need to sign in.
2. Price one Linux t3.small instance in Mumbai, the server from the P13 task "Set the budget alarm, then create the server with OpenTofu".
3. Compare On-Demand with a one-year Compute Savings Plan. Write both monthly figures in your notes.
4. Open Cost Explorer in your account and look at the last month. On a new account it may show little or nothing.

Teardown: the calculator creates nothing in your account. Close the estimate without saving it.

On paper: write when to use On-Demand, Savings Plans, Reserved Instances, Spot Instances and Dedicated Hosts. One line each.

### Day 17: support and AWS resources (1 hour)

Watch: the rest of CPE module 11.

Read:
- AWS Support plans: <https://docs.aws.amazon.com/awssupport/latest/user/aws-support-plans.html>
- AWS Health: <https://docs.aws.amazon.com/health/latest/ug/what-is-aws-health.html>
- AWS re:Post and the AWS Knowledge Center: <https://repost.aws/knowledge-center>
- Reporting abuse to AWS Trust & Safety: <https://repost.aws/knowledge-center/report-aws-abuse>
- The "Domain 4" table in `README.md`, for the AWS Partner Network, AWS Marketplace and AWS Professional Services.

Hands-on (5 minutes, read-only): open AWS Health in the console and look at your account's health events.

Teardown: you created nothing.

On paper: write what Basic Support includes. Then write one feature that only a paid plan gives.

### Day 18: self-check, mock exam and final teardown (2 hours)

#### Week 3 self-check (10 minutes)

1. Give two differences between a security group and a network ACL.
2. What does an S3 Lifecycle rule do? Give one example.
3. Name the AWS service for each job: speech to text, text to speech, translation, image analysis, SQL queries on files in S3.
4. Which purchasing option suits a steady workload for three years? Which suits a batch job that can stop and restart at any time?
5. What does Basic Support include? Which tool estimates cost before you build anything?

Answers:
1. Any two: a security group works at the instance level and a network ACL at the subnet level; security groups are stateful and network ACLs are stateless; security groups have allow rules only, and network ACLs have allow and deny rules. [Compare security groups and network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html)
2. It moves objects to a lower-cost storage class, or deletes them, on a schedule. Example: move objects to S3 Glacier Flexible Retrieval one year after creation. [S3 Lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
3. Amazon Transcribe, Amazon Polly, Amazon Translate, Amazon Rekognition, Amazon Athena. [Machine learning services](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/machine-learning.html) and [Athena](https://docs.aws.amazon.com/athena/latest/ug/what-is.html)
4. A Savings Plan (or Reserved Instances) for the steady workload. Spot Instances for the batch job. [Purchasing options](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html)
5. Basic Support gives every customer 24x7 answers to account and billing questions, documentation, technical papers and support forums. AWS Pricing Calculator estimates cost before you build. [Support plans](https://docs.aws.amazon.com/awssupport/latest/user/aws-support-plans.html) and [Pricing Calculator](https://docs.aws.amazon.com/pricing-calculator/latest/userguide/what-is-pricing-calculator.html)

#### Mock exam (1.5 hours)

1. Sit `mock-exam.md` under exam rules: 55 minutes, no notes, no AI.
2. Mark it with `mock-exam-answers.md` and use its scoring guide by domain.
3. Write down the three topics you missed most. Restudy them over the next two or three days.
4. When you reach your target, take the Official Practice Question Set again and compare it with your Day 1 score.

#### Final teardown (5 minutes)

1. Check that the `exam-test-user` user, the `exam-readers` group, the `exam-players` table, your S3 bucket and the `shortly-exam-practice` workload are all gone.
2. If you made a zero-spend budget on Day 1, delete it.
3. Leave nothing running in the account.

## After the plan

- If you passed your targets, book the exam with the steps in `README.md`. Ask for the ESL +30 extra time before you book.
- Read the exam guide again in the week you book. AWS publishes guide updates about one month before they reach the exam.
- After you pass, look in the Benefits section of your AWS Certification Account for your 50% discount voucher for your next AWS exam.
