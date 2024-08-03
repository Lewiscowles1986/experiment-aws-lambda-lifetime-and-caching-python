# AWS Lambda experiment, Python cachetools

This is an experiment aimed at showcasing cachetools in AWS Lambda

It comes from a conversation with Engineer Megan List.

I Asserted that AWS Lambda can:

- [X] cache values for more than 15 minute maximum runtime
- [X] take memory snapshots of VM to get faster warm boot times
- [ ] I was wrong when I said it reaps warm lambdas over 1 hour old.

To check this, I'm monitoring the PID, as well as the time, and trying to call serially, avoiding parallel calls.

I have no dependencies on SSM or anything else, because this is a simple app. YMMV as we do not control the scheduler, re-balancing of machines etc. That is part of what is good about serverless.

As stated above, I was wrong about lambdas over 1 hour old being reaped. Perhaps this is part of AWS coordination, which in a prior test run had looked like it happened. Honestly I cannot remember if it's a day, or they just run forever; but it's definitely over 1 hour.

## Pre-requisites

- Curl 8.6+
- Terraform 1.5+
- cli `zip` command compatible with:
  - `zip <zipfile-path.zip> <list of file names>`
  - `zip -ur ../<zipfile-path.zip> ./*`

## Usage

1. Initialize terraform and apply
```
terraform init
terraform apply
```

2. Record the URL output. Mine and the one given below was https://msxbosdarhxhgoxzcyeo2xjtdu0yhkzz.lambda-url.us-east-1.on.aws/

3. Run the test
```
for i in {1..60}
do
    curl https://msxbosdarhxhgoxzcyeo2xjtdu0yhkzz.lambda-url.us-east-1.on.aws/ > logs/$(date +"%Y-%m-%dT%H%M%S").json
    sleep 60
done
```

## Sample output

I've saved the output of the logs in the logs-example.zip by using `zip logs-example.zip logs/` in the hopes it might help budget strained folks interested in the output.

Note that the sample output was manual commands, until it became the loop example above at 11:33:00
The loop iterated a few times, which is why you see it go back to 00 in seconds. There is no magic there, just fast fingers, and restarting with `<CTRL>`+`<C>`, then `<Cursor (Up)>` then `<Return / Enter>`.

## Further thoughts

I wonder if I could exploit this property for other cool demo's. Like fan-out, fan-in data using Lambda, or sequential flows in a single lambda-lith.
