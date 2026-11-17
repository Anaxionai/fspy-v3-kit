# Mock exam: AWS Certified Cloud Practitioner (CLF-C02)

We wrote these 40 questions for this pack. We did not copy them from any question bank. They follow the weight of the real exam:

| Domain | Questions |
| --- | --- |
| 1 Cloud Concepts | 10 |
| 2 Security and Compliance | 12 |
| 3 Cloud Technology and Services | 13 |
| 4 Billing, Pricing, and Support | 5 |

## How to sit it

1. Sit it at the end of week 3 of the study plan, or when you think you are ready to book.
2. Set a timer for 55 minutes. The real exam gives you 90 minutes for 65 questions, so this is the same pace.
3. Use no notes, no browser, no phone and no AI tool. The real exam allows none of these.
4. Write your answers on paper: the question number and the letter, for example "7 C".
5. Each question has one right answer, unless it says "Choose two". For "Choose two", you need both letters right to get the mark.
6. Answer every question. On the real exam a blank answer counts as wrong, and a wrong answer costs nothing extra.
7. When the timer ends, stop. Then open `mock-exam-answers.md` and mark your paper.

---

**1.** A ticket-booking start-up in Pune expects ten times its normal traffic during a two-day festival sale. After the sale, traffic falls back to normal. The team wants to add servers for the sale and remove them afterwards. Which benefit of the AWS Cloud does this describe?

- A. Elasticity
- B. Economies of scale
- C. Data sovereignty
- D. Fault isolation

**2.** A company runs its web app on Amazon EC2 instances. The Linux vendor releases a security patch for the operating system on those instances. Who is responsible for applying the patch?

- A. AWS, because AWS owns the physical servers
- B. The customer
- C. The AWS Partner who sold the instances
- D. No one, because EC2 patches the guest operating system for you

**3.** A company runs its web app on two EC2 instances in one Availability Zone. It wants the app to keep running if that whole Availability Zone fails. What should it do?

- A. Change both instances to a larger instance type
- B. Add a third instance in the same Availability Zone
- C. Run the instances in two or more Availability Zones in the Region
- D. Store the app's images in an edge location

**4.** A website in the Mumbai Region serves product images to users in many countries. Users far from India say the images load slowly. Which service caches the images in edge locations close to the users?

- A. Amazon Route 53
- B. Amazon CloudFront
- C. AWS Direct Connect
- D. Elastic Load Balancing

**5.** An auditor asks a fintech start-up for AWS's ISO certificates and SOC reports. Where can the start-up download these documents at no cost?

- A. AWS Config
- B. Amazon Inspector
- C. AWS Trusted Advisor
- D. AWS Artifact

**6.** A food-delivery company in Chennai wants to launch its app for customers in Europe next week. The European customers need low delay. The company does not want to build or rent a data centre in Europe. Which advantage of cloud computing helps most?

- A. Trade fixed expense for variable expense
- B. Go global in minutes
- C. Benefit from massive economies of scale
- D. Stop spending money running and maintaining data centres

**7.** A media company converts thousands of videos every night. The job needs high-performance processors more than extra memory or extra storage. Which EC2 instance family fits best?

- A. Compute optimized
- B. Memory optimized
- C. Storage optimized
- D. Burstable performance (the T family)

**8.** A company has one standalone AWS account. The account is not part of AWS Organizations. Which task requires a person to sign in as the root user?

- A. Create an IAM user for a new developer
- B. Create an AWS Budgets alert
- C. Close the AWS account
- D. Update the account's alternate contacts

**9.** A company has two workloads. A web app runs all day, every day, and will do so for the next three years. A nightly batch job can stop and restart at any time without harm. Which two choices give the lowest compute cost? (Choose two.)

- A. A three-year Savings Plan for the web app
- B. On-Demand Instances for both workloads
- C. Spot Instances for the batch job
- D. Dedicated Hosts for the batch job
- E. Spot Instances for the web app

**10.** A team wants its workload to recover from failure automatically. It also wants to test its recovery steps on a regular schedule. Which pillar of the AWS Well-Architected Framework covers these goals?

- A. Performance efficiency
- B. Cost optimization
- C. Sustainability
- D. Reliability

**11.** A team wants to run its Docker containers on Amazon ECS. It does not want to choose, patch or scale any EC2 instances. Which option should it use?

- A. AWS Fargate
- B. Amazon EC2 Auto Scaling
- C. AWS Outposts
- D. Amazon Lightsail

**12.** Someone deleted an Amazon S3 bucket yesterday. The security team needs to know which IAM user deleted it, and at what time. Which service records this information?

- A. Amazon Inspector
- B. AWS CloudTrail
- C. AWS Trusted Advisor
- D. Amazon Macie

**13.** A company runs PostgreSQL on an EC2 instance. The team spends hours each month on backups, patching and failover. It wants to keep using PostgreSQL and let AWS handle these tasks. Which service fits?

- A. Amazon DynamoDB
- B. Amazon ElastiCache
- C. Amazon Redshift
- D. Amazon RDS for PostgreSQL

**14.** A bank is moving to AWS. Its leaders worry that staff lack cloud skills and that teams resist the change. Which perspective of the AWS Cloud Adoption Framework (AWS CAF) focuses on this concern?

- A. People
- B. Platform
- C. Governance
- D. Operations

**15.** A team moves a small job from an EC2 instance to an AWS Lambda function. Which two tasks does AWS now handle for this job? (Choose two.)

- A. Writing secure code for the function
- B. Patching the operating system that runs the code
- C. Choosing which IAM permissions the function needs
- D. Adding capacity as more requests arrive
- E. Deciding what customer data the function may store

**16.** A mobile game stores each player's profile and score, looked up by player ID. It needs a serverless database that answers in single-digit milliseconds, even with millions of players. Which service fits best?

- A. Amazon RDS for MySQL
- B. Amazon Redshift
- C. Amazon DynamoDB
- D. Amazon Neptune

**17.** A company uploads 2 TB of video files from its office to an Amazon S3 bucket. Which statement about data transfer charges is true in most cases?

- A. AWS charges the outbound data rate for every gigabyte that you upload.
- B. AWS does not charge for data transferred in to AWS.
- C. Uploads are free only for accounts on the AWS Free plan.
- D. AWS charges for data transfer only on Amazon EC2, never on Amazon S3.

**18.** A company must leave its data centre in four months. It plans to move its applications to Amazon EC2 without changing any code, and to improve them later. Which migration strategy is this?

- A. Refactor
- B. Repurchase
- C. Rehost
- D. Retire

**19.** Which statement about security groups and network ACLs in a VPC is correct?

- A. Security groups work at the subnet level and support deny rules.
- B. Network ACLs are stateful, so they allow return traffic automatically.
- C. Security groups check rules in number order and stop at the first match.
- D. Network ACLs work at the subnet level, and security groups work at the instance level.

**20.** A company has 60 employees and six AWS accounts in AWS Organizations. It wants each employee to sign in once and reach only the accounts and permissions they need. Which service should it use?

- A. AWS IAM Identity Center
- B. Amazon Cognito
- C. AWS Resource Access Manager (AWS RAM)
- D. A separate IAM user for each employee in every account

**21.** A team must build the same network, servers and database in three Regions. It wants a repeatable process with no manual clicks, using an AWS service. What should it use?

- A. The AWS Management Console
- B. AWS Config
- C. AWS Trusted Advisor
- D. AWS CloudFormation

**22.** A company used to buy servers every three years. It paid a large amount before it knew how much it would use them. Now it pays each month only for the computing it uses. Which advantage of cloud computing describes this change?

- A. Go global in minutes
- B. Trade fixed expense for variable expense
- C. Increase speed and agility
- D. Benefit from massive economies of scale

**23.** A company must show auditors how its security group rules looked at any time in the past six months. It also wants a warning when a rule breaks company policy. Which service fits?

- A. AWS Artifact
- B. AWS Shield
- C. AWS Config
- D. Amazon Macie

**24.** A web app runs on four EC2 instances. The team wants to spread incoming traffic across the healthy instances. It also wants to add or remove instances as demand changes. Which two services should it use? (Choose two.)

- A. Elastic Load Balancing
- B. AWS Backup
- C. Amazon Athena
- D. Amazon EC2 Auto Scaling
- E. AWS Artifact

**25.** A company has six AWS accounts, one for each team. Its finance team wants one monthly bill. It also wants the usage of all six accounts combined for volume discounts. What should the company use?

- A. Six separate AWS Budgets budgets
- B. AWS Organizations with consolidated billing
- C. AWS Pricing Calculator
- D. AWS Cost and Usage Reports in each account

**26.** A graduate creates a new AWS account for a side project. Which two actions follow AWS's best practices for the root user? (Choose two.)

- A. Turn on multi-factor authentication (MFA) for the root user
- B. Create root user access keys for the AWS CLI
- C. Use the root user for daily work, so that no permission ever stops you
- D. Create an administrative user for everyday tasks
- E. Share the root password with the team, so anyone can recover the account

**27.** A company stores invoices in Amazon S3. Staff read them often for 30 days, then almost never. The law says the company must keep them for seven years. What is the most cost-effective approach?

- A. Keep the invoices in S3 Standard for seven years
- B. Create an S3 Lifecycle rule that moves the invoices to an S3 Glacier storage class after 30 days
- C. Copy the invoices to an instance store volume after 30 days
- D. Move the invoices to an Amazon EBS volume after 30 days

**28.** A company sets a goal to cut the energy that its cloud workloads use. It plans to raise the use of each instance and to remove idle resources. Which Well-Architected pillar does this goal belong to?

- A. Operational excellence
- B. Security
- C. Sustainability
- D. Reliability

**29.** A company must encrypt its data at rest in Amazon S3 and Amazon EBS. It wants to create the encryption keys and control who can use them. Which service should it use?

- A. AWS Key Management Service (AWS KMS)
- B. AWS Certificate Manager (ACM)
- C. Amazon Macie
- D. AWS WAF

**30.** Which two are good reasons to run a workload in more than one AWS Region? (Choose two.)

- A. To remove the need for backups
- B. To give users on another continent lower latency
- C. To make each Availability Zone larger
- D. To meet a law that says customer data must stay in a certain country
- E. To move all security duties to AWS

**31.** A company already owns licences for a commercial database engine. It wants to use these licences on AWS, instead of paying for licence-included instances. What is this model called?

- A. A Compute Savings Plan
- B. Bring Your Own License (BYOL)
- C. Licence-included pricing
- D. A Spot Instance request

**32.** A developer has written a database password inside the application's source code. Which service lets the app fetch the password when it runs, and rotate the password on a schedule?

- A. AWS Artifact
- B. AWS Certificate Manager (ACM)
- C. Amazon Cognito
- D. AWS Secrets Manager

**33.** A call centre records its customer calls. It wants to turn each recording into text. Then it wants to find whether each text shows a positive, negative or neutral sentiment. Which two services should it use? (Choose two.)

- A. Amazon Polly
- B. Amazon Transcribe
- C. Amazon Rekognition
- D. Amazon Textract
- E. Amazon Comprehend

**34.** Before building anything, a team wants an estimate of the monthly cost of a new design. The design uses Amazon EC2, Amazon S3 and Amazon RDS. Which tool should the team use?

- A. AWS Pricing Calculator
- B. AWS Cost Explorer
- C. AWS Budgets
- D. AWS Cost and Usage Reports

**35.** An online shop runs behind Amazon CloudFront. It wants to block SQL injection attempts in web requests. It also wants protection against large DDoS (distributed denial of service) attacks. Which two services help? (Choose two.)

- A. Amazon Macie
- B. AWS WAF
- C. AWS Artifact
- D. Amazon Inspector
- E. AWS Shield

**36.** Which two business outcomes does AWS say cloud adoption can help a company achieve? (Choose two.)

- A. Reduced business risk
- B. No further need for security controls
- C. A guarantee that every workload costs less
- D. Improved operational efficiency
- E. No further need to train staff

**37.** A customer places an order. The app must then send the same message to an email address, a phone by SMS and an Amazon SQS queue. Which service fits best?

- A. Amazon SQS
- B. Amazon SNS
- C. Amazon SES
- D. AWS Step Functions

**38.** A company wants a service that watches AWS CloudTrail events, VPC flow logs and DNS logs for signs of threats. It does not want to install agents or turn on those logs itself. Which service fits?

- A. Amazon Inspector
- B. AWS Config
- C. Amazon GuardDuty
- D. AWS Artifact

**39.** Reports show that an EC2 instance has used less than 10% of its CPU for the past month. Which action follows the idea of rightsizing?

- A. Buy a three-year Savings Plan for the current instance
- B. Add a second instance of the same size in another Availability Zone
- C. Move the instance to a Dedicated Host
- D. Move the workload to a smaller instance type that still meets its needs

**40.** Which of these does every AWS customer get with Basic Support, at no extra cost?

- A. A designated Technical Account Manager (TAM)
- B. 24x7 phone access to Cloud Support Engineers
- C. 24x7 answers to account and billing questions, plus documentation, technical papers and support forums
- D. Critical workload reviews and personalised runbooks

---

Stop here. Mark your paper with `mock-exam-answers.md`.
