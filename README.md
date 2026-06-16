# CST8919 Lab 2: Building a Web App with Threat Detection using Azure Monitor and KQL

## YouTube Video Demo

[https://youtu.be/0Dvo2835EIs]

The video demonstrates:

- The Flask application deployed to Azure App Service
- Generating login activity using the REST Client
- Viewing application logs in Azure Monitor and Log Analytics
- Running the KQL query to identify failed login attempts
- Creating and testing an Azure Monitor alert rule
- Receiving the email notification after the alert is triggered

---

# Application Testing

I used a REST Client `test-app.http` file to generate both successful and failed login attempts.

---

# KQL Query

```kusto
AppServiceConsoleLogs
| where ResultDescription has "LOGIN_FAILED"
| project TimeGenerated, ResultDescription
| order by TimeGenerated desc
```

## Query Explanation

- Searches the `AppServiceConsoleLogs` table.
- Filters log entries containing the text `LOGIN_FAILED`.
- Displays the timestamp and log message.
- Sorts the results from newest to oldest.

---

# What I Learned

This lab helped me better understand how application monitoring works in Azure.

I learned how to deploy a Flask application to Azure App Service and connect it to Azure Monitor for logging and analysis. I also learned how KQL can be used to search and filter logs stored in a Log Analytics Workspace.

Another useful part of the lab was creating alert rules. Instead of manually checking logs, Azure Monitor can automatically detect suspicious activity and send notifications when a threshold is reached.

---

# Challenges Faced

## HTTPS Redirection

One issue I encountered was receiving HTTP 301 redirect responses when testing the application.

Initially, the requests in my `.http` file were using the HTTP endpoint. Azure App Service automatically redirects traffic to HTTPS, so I updated the base URL to use HTTPS and the issue was resolved.

## Log Ingestion Delay

Another challenge was the delay between generating logs and seeing them appear in Log Analytics.

After generating failed login attempts, it usually took a few minutes before the logs became available. Because of this delay, testing the KQL query and alert rule required some patience.

## KQL Query Testing

At first, I used the `contains` operator when searching log messages. Later, I learned that the `has` operator is generally more efficient because Azure can use indexing to search the logs faster.

---

# Real-World Improvements

1. Track failed login attempts by IP address instead of counting all failed logins together.
2. Implement account lockout or rate limiting after a certain number of failed attempts.
3. Integrate Azure Logic Apps or Azure Functions to automatically respond to suspicious activity.
4. Use Azure Web Application Firewall (WAF) to block malicious IP addresses automatically.

---

