# Mock exam answers: AWS Certified Cloud Practitioner (CLF-C02)

Mark your paper first. Then read the reason for every question you got wrong, and open its official page.

Each answer below has the right letter, a short reason, the exam domain and task statement, and an official AWS page. We opened every page on 13 November 2026.

For a "Choose two" question, you get the mark only if both letters are right.

## Answers

**1. A. Elasticity**
You add resources when demand rises and remove them when it falls, so capacity follows demand. AWS calls this elasticity.
Domain 1, task 1.1. <https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-your-workload-to-adapt-to-changes-in-demand.html>

**2. B. The customer**
On Amazon EC2, the customer manages the guest operating system, including its updates and security patches. AWS looks after the hardware and the facilities.
Domain 2, task 2.1. <https://aws.amazon.com/compliance/shared-responsibility-model/>

**3. C. Run the instances in two or more Availability Zones in the Region**
Availability Zones are isolated locations inside a Region. Instances in more than one zone protect the app from the failure of a single location.
Domain 3, task 3.2. <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html>

**4. B. Amazon CloudFront**
CloudFront delivers content through edge locations and serves cached copies from the edge location with the lowest latency for each user.
Domain 3, task 3.2. <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html>

**5. D. AWS Artifact**
AWS Artifact gives on-demand downloads of AWS compliance documents, such as ISO and SOC reports. AWS provides them free of charge.
Domain 2, task 2.2. <https://docs.aws.amazon.com/artifact/latest/ug/what-is-aws-artifact.html>

**6. B. Go global in minutes**
AWS describes this advantage as deploying to Regions around the world in a few clicks, which gives customers lower latency.
Domain 1, task 1.1. <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/six-advantages-of-cloud-computing.html>

**7. A. Compute optimized**
AWS says compute optimized instances suit work that needs high-performance processors, such as batch processing and media transcoding.
Domain 3, task 3.3. <https://docs.aws.amazon.com/ec2/latest/instancetypes/co.html>

**8. C. Close the AWS account**
A standalone account outside AWS Organizations needs root user credentials to close the account. Alternate contacts do not need the root user.
Domain 2, task 2.3. <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html>

**9. A and C**
A Savings Plan lowers the price in return for a one- or three-year commitment, which suits steady use. Spot Instances suit work that can stop at any time.
Domain 4, task 4.1. <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html>

**10. D. Reliability**
"Automatically recover from failure" and "Test recovery procedures" are two of the five design principles of the reliability pillar.
Domain 1, task 1.2. <https://docs.aws.amazon.com/wellarchitected/latest/framework/rel-dp.html>

**11. A. AWS Fargate**
Fargate runs containers with Amazon ECS without servers or clusters of EC2 instances for you to manage.
Domain 3, task 3.3. <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html>

**12. B. AWS CloudTrail**
CloudTrail records actions taken by a user, role or AWS service as events. You can see who did what, to which resource, and when.
Domain 2, task 2.2. <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html>

**13. D. Amazon RDS for PostgreSQL**
Amazon RDS runs PostgreSQL and manages backups, software patching, failure detection and recovery. On EC2, the customer does these tasks.
Domain 3, task 3.4. <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html>

**14. A. People**
The People perspective of AWS CAF focuses on culture, organisational structure, leadership and workforce during the move to the cloud.
Domain 1, task 1.3. <https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/foundational-capabilities.html>

**15. B and D**
Lambda manages the underlying infrastructure, including server maintenance, capacity, scaling and patching. This leaves you to focus on your own code.
Domain 2, task 2.1. <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>

**16. C. Amazon DynamoDB**
DynamoDB is a serverless NoSQL database with single-digit millisecond performance at any scale. AWS lists game state and player data as a use case.
Domain 3, task 3.4. <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html>

**17. B. AWS does not charge for data transferred in to AWS**
AWS says that in most cases there is no charge for inbound data transfer. Outbound data transfer is one of the three main drivers of cost.
Domain 4, task 4.1. <https://docs.aws.amazon.com/whitepapers/latest/how-aws-pricing-works/key-principles.html>

**18. C. Rehost**
Rehost, also called "lift and shift", moves applications to AWS without changing them. AWS suggests improving them after the move.
Domain 1, task 1.3. <https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html>

**19. D. Network ACLs work at the subnet level, and security groups work at the instance level**
AWS's comparison table also shows that security groups are stateful with allow rules only. Network ACLs are stateless with allow and deny rules.
Domain 3, task 3.5. <https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html>

**20. A. AWS IAM Identity Center**
IAM Identity Center manages workforce access to many AWS accounts from one place. Users sign in once through the AWS access portal.
Domain 2, task 2.3. <https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html>

**21. D. AWS CloudFormation**
A CloudFormation template describes your resources once. You reuse it to create the same resources in many Regions in a repeatable way.
Domain 3, task 3.1. <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html>

**22. B. Trade fixed expense for variable expense**
Instead of investing heavily in servers before you know your use, you pay only when you consume computing resources.
Domain 1, task 1.4. <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/six-advantages-of-cloud-computing.html>

**23. C. AWS Config**
AWS Config keeps the configuration history of resources, including security group rules. Config rules flag resources that break your rules.
Domain 2, task 2.2. <https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html>

**24. A and D**
Elastic Load Balancing sends traffic only to healthy targets. EC2 Auto Scaling adds or removes instances as demand changes.
Domain 3, task 3.3. <https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html>

**25. B. AWS Organizations with consolidated billing**
Consolidated billing gives one bill for many accounts and combines their usage, which shares volume discounts. It costs nothing extra.
Domain 4, task 4.2. <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing.html>

**26. A and D**
AWS recommends MFA for the root user, and an administrative user for everyday tasks. It says not to create root access keys or share root credentials.
Domain 2, task 2.3. <https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html>

**27. B. Create an S3 Lifecycle rule that moves the invoices to an S3 Glacier storage class after 30 days**
Lifecycle rules move objects to lower-cost storage classes on a schedule. AWS gives archiving for regulations as an example use.
Domain 3, task 3.6. <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>

**28. C. Sustainability**
"Maximize utilization" is a sustainability design principle. It asks you to right-size workloads and reduce idle resources to save energy.
Domain 1, task 1.2. <https://docs.aws.amazon.com/wellarchitected/latest/framework/sus-design-principles.html>

**29. A. AWS Key Management Service (AWS KMS)**
AWS KMS creates and controls the keys that encrypt your data. Key policies decide who can use each key.
Domain 2, task 2.2. <https://docs.aws.amazon.com/kms/latest/developerguide/overview.html>

**30. B and D**
AWS says a Region close to your users lowers latency. You also choose Regions to meet legal requirements about where you keep data.
Domain 3, task 3.2. <https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html>

**31. B. Bring Your Own License (BYOL)**
With BYOL, you reuse licences you already own on AWS resources. AWS License Manager helps you track them.
Domain 1, task 1.4. <https://docs.aws.amazon.com/license-manager/latest/userguide/license-manager.html>

**32. D. AWS Secrets Manager**
Secrets Manager replaces hard-coded credentials with a call at run time. It can rotate secrets on an automatic schedule.
Domain 2, task 2.3. <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>

**33. B and E**
Amazon Transcribe converts speech to text. Amazon Comprehend finds the sentiment of a text: positive, negative, neutral or mixed.
Domain 3, task 3.7. <https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html> and <https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html>

**34. A. AWS Pricing Calculator**
AWS Pricing Calculator is a free planning tool that models solutions before you build them. Cost Explorer shows costs you have already had.
Domain 4, task 4.2. <https://docs.aws.amazon.com/pricing-calculator/latest/userguide/what-is-pricing-calculator.html>

**35. B and E**
AWS WAF blocks common attack patterns such as SQL injection. AWS Shield is a managed DDoS protection service.
Domain 2, task 2.4. <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/security-services.html>

**36. A and D**
AWS says the cloud can help you lower costs, reduce business risks and improve operational efficiency. AWS lists none of the other three options.
Domain 1, task 1.3. <https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/welcome.html>

**37. B. Amazon SNS**
SNS sends one message from a topic to many subscribers, including SQS queues, email addresses and SMS numbers. AWS calls this "fanout".
Domain 3, task 3.8. <https://docs.aws.amazon.com/sns/latest/dg/welcome.html>

**38. C. Amazon GuardDuty**
GuardDuty reads CloudTrail management events, VPC flow logs and DNS logs as soon as you turn it on. You do not need to enable anything else.
Domain 2, task 2.4. <https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html>

**39. D. Move the workload to a smaller instance type that still meets its needs**
Rightsizing means matching resource size to real use. AWS Compute Optimizer gives rightsizing recommendations to reduce cost.
Domain 1, task 1.4. <https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html>

**40. C. 24x7 answers to account and billing questions, plus documentation, technical papers and support forums**
These are Basic Support features for every customer. A TAM, phone access to engineers and workload reviews come with paid plans.
Domain 4, task 4.3. <https://docs.aws.amazon.com/awssupport/latest/user/aws-support-plans.html>

## Answer grid

| Q | Answer | Q | Answer | Q | Answer | Q | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | 11 | A | 21 | D | 31 | B |
| 2 | B | 12 | B | 22 | B | 32 | D |
| 3 | C | 13 | D | 23 | C | 33 | B, E |
| 4 | B | 14 | A | 24 | A, D | 34 | A |
| 5 | D | 15 | B, D | 25 | B | 35 | B, E |
| 6 | B | 16 | C | 26 | A, D | 36 | A, D |
| 7 | A | 17 | B | 27 | B | 37 | B |
| 8 | C | 18 | C | 28 | C | 38 | C |
| 9 | A, C | 19 | D | 29 | A | 39 | D |
| 10 | D | 20 | A | 30 | B, D | 40 | C |

## Scoring guide by domain

Count your marks in each domain with the table below. This mock exam is not scaled like the real one. Aim for 32 of 40 before you book, so you have a margin.

| Domain | Questions | Your target | If you score below the target, restudy |
| --- | --- | --- | --- |
| 1 Cloud Concepts | 1, 6, 10, 14, 18, 22, 28, 31, 36, 39 (10 questions) | 8 of 10 | CPE modules 1, 12 and 13. The six advantages of cloud computing. The six Well-Architected pillars and their design principles. AWS CAF perspectives. The seven migration strategies. Study plan days 2 to 4. |
| 2 Security and Compliance | 2, 5, 8, 12, 15, 20, 23, 26, 29, 32, 35, 38 (12 questions) | 10 of 12 | CPE modules 9 and 10. The shared responsibility model for EC2, RDS and Lambda. Root user tasks and best practices. The security services table in `README.md`. Study plan days 6 to 9. |
| 3 Cloud Technology and Services | 3, 4, 7, 11, 13, 16, 19, 21, 24, 27, 30, 33, 37 (13 questions) | 10 of 13 | CPE modules 2 to 8. Regions, Availability Zones and edge locations. Database, network and storage choices. The AI/ML service names. Study plan days 5, 10, 11, 13, 14 and 15. |
| 4 Billing, Pricing, and Support | 9, 17, 25, 34, 40 (5 questions) | 4 of 5 | CPE module 11. EC2 purchasing options. Consolidated billing. Which cost tool does which job. Support plans. Study plan days 16 and 17. |

### What your total means

| Total | What to do next |
| --- | --- |
| 32 to 40 | You are ready to try the AWS Official Practice Question Set. If you pass that too, book the exam. |
| 26 to 31 | Restudy every domain below its target for two or three days. Then sit this mock exam again. |
| 25 or fewer | Go back to week 1 of `study-plan.md` and finish the Cloud Practitioner Essentials course before you try again. |

When you sit this mock exam a second time, you will remember some answers. Read each reason again and say it in your own words. If you cannot, restudy that topic.
