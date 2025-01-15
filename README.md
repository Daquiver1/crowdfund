# crowdfund

This project

## Installation

Follow these steps to get your development environment set up:

### 1. Clone the Repository

Start by cloning this repository to your local machine:

```bash
git clone https://github.com/QuiverTech-Solutions/crowdfund.git
```

then change directory to the project folder

```bash
cd crowdfund
```

### 2. Start docker

```bash
docker-compose up
```

## Usage

Once the application is running, you can interact with the backend API on `http://localhost:8080/docs`.

# For getting local host

npx untun@latest tunnel http://localhost:8008

# High Urgency Todo

- [x] get thew answers via an sql join.,
- [x] The interactive buttons aren't working
- [x] serialize redis data past questions and answers,
- [x] Better error handling
- [x] Filter past question text. ugbs 101, returns false. It shouldn't same as ugbs 101
- [x] Refactor
- [x] Integrate Paystack and payment options
- [x] Centralize with telegram server
- [x] Make the states seamless
- [x] Update texts writeup
- [ ] Sometimes it sends the event twice.
- [x] Integrate sentry
- [x] Confirm that registration works.
- [x] Add that when there's an error it'll send a message to you.
- [x] When they start with the bot, it'll tell them that welcome to QT, they are the 300th person to use the bot.
- [x] If you haven't registered, it'll tell you and route you to register.
- [x] Tap on exit to terminate the registration flow.
- [x] Fix up alembic downgrading and upgrading issue.
- [x] Update db schema
- [x] Shorten length of strings.
- [ ] Raise your own errors. Those not found errors.
- [ ] Change from returning None to returning a message. You'd have to change from db and the callers. Should take max 2 hours.
- [x] Add the telegram routes to it.
- [x] Sync the db to it.
- [ ] Let the whatsapp message send before you update the state, keeps it neat, since that one has more chance of failure.
- [ ] Update s3 when it comes to storing questions and their path.
- [x] Find out what nai did that it only accepts from the bot not when a user taps the link.
- [ ] afTER TESTING CHANGE CPUS ON FLY TOML TO 2,
- [x] AFTER TESTING, INCREASE SENTRY SCORE TO 1.0 FOR PROD
- [x] Fix the bug where android users can't download the bot.
- [x] After you search for pastt question, and do some things, and tryr and select another one, it tdont' work.
- [ ] Upload questions into s3 and db.

# Low Urgency Todo

- [ ] Update stats route.
- [ ] Paystack use the base currency(pesewas)
- [ ] Refactor endpoints best practices.
- [ ] Getting the current user, should get from cache.
- [ ] Cache db queries from endpoint.

# Known issues

- Email not verified, potential security risk
- Instead of converting to string, update db and route to use uuid instead.

# To get db from fly io

1. flyctl sftp shell -a past-questions-bot-server
2. cd /data
3. get past_questions.db
4. exit
   it'll come to directory

try the rpesigned

use s3 to generate a presigned and that's what you'd use and make the buckets not accessible.
code is like this.
import boto3
from botocore.exceptions import NoCredentialsError

s3_client = boto3.client('s3')

try:
response = s3_client.generate_presigned_url('get_object',
Params={'Bucket': 'mypascobucket',
'Key': 'test/UGBS101_2023_Second.pdf'},
ExpiresIn=3600) # URL valid for 1 hour
print(response)
except NoCredentialsError:
print("Credentials not available")
