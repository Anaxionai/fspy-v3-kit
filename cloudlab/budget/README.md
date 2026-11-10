# A $5 budget with alerts

A budget (an AWS Budgets rule) compares your spending with an amount you choose. When the spending passes a threshold, AWS emails you an alert. You set one before you start anything on a real account.

You practise on Floci first (part 1), then do the same on your real AWS account in P13 (part 2). Run every command in Git Bash, in a folder of your own.

## Budgets alert. They never stop spending

- A budget only sends an alert. It does not stop, pause or delete anything. A server keeps running, and keeps costing money, after the 100% alert.
- The alert comes late. AWS updates budget data up to three times a day, usually 8 to 12 hours apart. You can pass $5 hours before the email arrives.
- Budget actions can apply an IAM policy or stop EC2 and RDS instances. They are still not a cap: storage, data transfer and other services keep costing money.
- The only way to stop spending is to delete what you made. Tear everything down on the same day.

## The two files

`budget.json`: a monthly cost budget of 5 US dollars.

```json
{
  "BudgetName": "monthly-5-usd",
  "BudgetLimit": {"Amount": "5", "Unit": "USD"},
  "BudgetType": "COST",
  "TimeUnit": "MONTHLY",
  "CostTypes": {"IncludeCredit": false}
}
```

`"IncludeCredit": false` makes the budget count your usage before credits. Part 2 explains why.

`notifications.json`: three alerts, at 50%, 80% and 100% of the budget, on actual cost.

```json
[
  {
    "Notification": {"NotificationType": "ACTUAL", "ComparisonOperator": "GREATER_THAN", "Threshold": 50, "ThresholdType": "PERCENTAGE"},
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "student@example.com"}]
  },
  {
    "Notification": {"NotificationType": "ACTUAL", "ComparisonOperator": "GREATER_THAN", "Threshold": 80, "ThresholdType": "PERCENTAGE"},
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "student@example.com"}]
  },
  {
    "Notification": {"NotificationType": "ACTUAL", "ComparisonOperator": "GREATER_THAN", "Threshold": 100, "ThresholdType": "PERCENTAGE"},
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "student@example.com"}]
  }
]
```

`ACTUAL` alerts on money already spent. `FORECASTED` alerts when AWS predicts that the month will pass the threshold. The map-week task and P13 ask for two alerts, 80% actual and 100% forecast. That file looks like this:

```json
[
  {
    "Notification": {"NotificationType": "ACTUAL", "ComparisonOperator": "GREATER_THAN", "Threshold": 80, "ThresholdType": "PERCENTAGE"},
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "student@example.com"}]
  },
  {
    "Notification": {"NotificationType": "FORECASTED", "ComparisonOperator": "GREATER_THAN", "Threshold": 100, "ThresholdType": "PERCENTAGE"},
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "student@example.com"}]
  }
]
```

Check a file for mistakes with `python -m json.tool budget.json`. It shows the line of the first mistake.

## Part 1: practise on Floci

Start Floci and set up the `floci` profile as `../aws/README.md` shows. Then check the fake account:

```bash
aws sts get-caller-identity --profile floci
```

Floci's account ID is `000000000000`. Create the budget with its alerts:

```bash
aws budgets create-budget --account-id 000000000000 --budget file://budget.json --notifications-with-subscribers file://notifications.json --profile floci
```

It prints nothing when it works. Read the budget back:

```bash
aws budgets describe-budgets --account-id 000000000000 --profile floci
```

Find `"Amount": "5"`, `"Unit": "USD"`, `"TimeUnit": "MONTHLY"` and `"IncludeCredit": false`. Then read the alerts back:

```bash
aws budgets describe-notifications-for-budget --account-id 000000000000 --budget-name monthly-5-usd --profile floci
```

It lists your alerts with their type and threshold.

### Why the alert never fires on Floci

Floci stores the budget and its alerts, but it has no spending data. Nothing on your laptop costs money, so `CalculatedSpend` stays at `0` and no threshold is ever reached. Floci also sends no email.

To change the budget, delete it and create it again:

```bash
aws budgets delete-budget --account-id 000000000000 --budget-name monthly-5-usd --profile floci
```

Creating a budget with a name that exists gives `DuplicateRecordException`.

## Part 2: the same on your real AWS account (P13)

### Before you start

- To sign up for AWS, you need a card that allows international payments. No such card? Tell your mentor early: the centre provides one.
- Your root user has MFA, and you work as an IAM user, as P13 shows.
- To see Budgets in the console, your IAM user needs billing access. The root user switches it on once: **Account**, then **IAM user and role access to Billing information**, then **Edit**, then **Activate IAM Access**.

### Credits: exclude them

On the AWS Free plan, credits pay for what you use. A budget counts credits by default, so its spending can stay at $0 while your credits drain. The alert would never fire. Exclude credits, so the budget counts what you use before credits:

- In the JSON: `"CostTypes": {"IncludeCredit": false}`, as in `budget.json` above.
- In the console: in **Budget scope**, add a filter for **Charge type**, choose to exclude, and select **Credit**. (An older console shows a **Credits** box under **Advanced options** instead: clear it.)

### Console steps

1. Sign in as your IAM user and open https://console.aws.amazon.com/cost-management/.
2. In the left menu, choose **Budgets**, then **Create budget**.
3. Under **Budget setup**, choose **Customize (advanced)**. Under **Budget types**, choose **Cost budget**, then **Next**.
4. Name it, for example `shortly-5usd`. Set **Period** to **Monthly**, **Budget renewal type** to **Recurring budget** and **Budgeting method** to **Fixed**.
5. Enter `5.00` as the budgeted amount.
6. Exclude credits in **Budget scope**, as shown above. Choose **Next**.
7. Choose **Add an alert threshold**. Enter `80`, choose **% of budgeted amount** and **Actual**, and type your email under **Email recipients**.
8. Add a second threshold: `100`, **% of budgeted amount**, **Forecasted**, with the same email. Add a 50% actual alert too if you want an earlier warning.
9. Choose **Next** twice (no actions), check the summary, and choose **Create budget**.
10. Open the email from AWS (from an `@aws.com` address) and choose the link to verify your address. You get no alerts until you do. The link expires after 12 hours.

### CLI commands

Use your real profile, not `floci`. P13 names it `shortly`. Sign in as P13 shows, then check who you are:

```bash
aws sts get-caller-identity --profile shortly
```

The `Arn` ends with your IAM user name, not `root`. Keep the 12-digit account ID in a variable:

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --profile shortly --query Account --output text)
echo "$ACCOUNT_ID"
```

Set `"BudgetName": "shortly-5usd"` in `budget.json`, and your own email in `notifications.json`. Then:

```bash
aws budgets create-budget --account-id "$ACCOUNT_ID" --budget file://budget.json --notifications-with-subscribers file://notifications.json --profile shortly
aws budgets describe-budgets --account-id "$ACCOUNT_ID" --profile shortly
```

Budgets is a global service. The CLI sends these commands to the right AWS address whatever your region is.

Verify your email address from the AWS email, as in step 10 above. Read the spending later with:

```bash
aws budgets describe-budget --account-id "$ACCOUNT_ID" --budget-name shortly-5usd --profile shortly
```

`CalculatedSpend` can show `0` for up to a day after you start something.

## Troubleshooting

- **`Unable to locate credentials`**: add `--profile floci` (Floci) or `--profile shortly` (real account) to the command.
- **`AccessDeniedException`** on a real account: your IAM user needs the `budgets:ModifyBudget` and `budgets:ViewBudget` permissions. The `AdministratorAccess` policy includes both.
- **`InvalidParameterException`** about the JSON: run `python -m json.tool` on both files and fix the line it shows.
- **`DuplicateRecordException`**: a budget with that name exists. Delete it first, or use another name.
- **No alert email on a real account**: verify your email address first. The alert also comes hours after the spending.
