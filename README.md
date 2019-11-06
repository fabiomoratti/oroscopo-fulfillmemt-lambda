# Simple Chatbot Demo - Oroscopo 
This repo briefly describes the steps to setup a (very) simple chatbot demo using DialogFlow for 
the chatbot and AWS Lambda for the fulfillment function.
 
You will need both GoogleCloud and AWS accounts to configure che chatbot and deploy the lambda. 
Details on how to obtain these account are not covered here, go find te official documentation
on AWS and GoogleCloud.

## Fulfillment web service
First let's build and deploy the fulfillment function.

### Prerequisites & setup 
You need `python 3.7`, `aws-cli` and `aws-sam-cli` to build and deploy the Lambda function.

Create a `venv` for the project:

```bash
python -m venv oroscopo-fulfillment-lambda-venv
```

Activate the `venv` Windows / Liunx:

```bash
oroscopo-fulfillment-lambda-venv\Scripts\activate
```
```bash
source oroscopo-fulfillment-lambda-venv/Scripts/activate
```

Install `awscli` and `aws-sam-cli`:

```bash
pip install awscli aws-sam-cli
```

**Note:** AWS credentials need to be configured in order to make che aws / sam cli work. 
Refer to the official documentation on how to do this.


### Build & deploy
To deploy the application you need a S3 Bucket, create it with the command:

```bash
aws s3 mb s3://<your bucket name>
```
Once setup the environment you can build the function:

```bash
sam build
```

package it:
```bash
sam package --output-template-file packaged.yaml --s3-bucket <your-bucket-name>
```

and deploy it:
```bash
aws cloudformation deploy --capabilities CAPABILITY_IAM --template-file packaged.yaml --stack-name oroscopo-stack
```

The API endpoint can be found on the AWS API Gateway console, you will need to copy-paste this
endpoint in the fulfillment configuration of the chatbot.
**Note:** the function logs will be written on CloudWatch.

## Create chatbot
Head to the DialogFlow console and create a new chatbot (let's call it Oroscopo).
We will create three intents (Nome, DataDiNascita, SegnoZodiacale) to get user's zodiacal sign;
we will also need a custom entity to manage the zodiacal signs.

### Default Intent
Modify "Default Welcome Intent" text response:

```
Ciao sono AstroChatBot e sono il tuo astrologo digitale. Come ti chiami?
```

### Intent "Nome"
Create a new intent called "Nome" and add the following training phrases:
 
 * Giovanni
 * Francesca
 * Mi chiamo Fabio
 * Il mio nome e' Fabio
 * ...
 
Set the names in the phrase as the pre-defined system entity  `@sys.given-name`.

Then add a response:

```
Ciao $given-name, sei pronto per il tuo oroscopo? 
Dimmi la tua data di nascita o il tuo segno zodiacale
```

### Entity "SegnoZodiacale"
Create a new entity: "SegnoZodiacale" and add the following entries:
 * ariete
 * toro
 * gemelli
 * cancro
 * leone
 * vergine
 * bilancia
 * scorpione
 * sagittario
 * capricorno
 * acquario
 * pesci

### Intent SegnoZodiacale
Create a new Intent: "SegnoZodiacale" and add the following training phrases:

 * sono del saggittario
 * pesci
 * il mio segno e' acquario
 - ...
 
Set webhook fulfillment for this intent.

### Intent DataDiNascita
Create a new Intent: "DataDiNascita" and add the following training phrases:

 * La mia data di nasciata e' 4 ottobre
 * 12 marzo
 * Sono nato il 4 aprile
 - ...
 
Set webhook fulfillment for this intent.

### Fulfillment
Set the fulfillment URL to the AWS lambda endpoint and ***voila'*** you are ready to use your chatbot.

# Credits
Dialogflow request / response JSON payloads are managed using the classes developed by 
[Emmarex](https://github.com/Emmarex); the original can be found
[here](https://github.com/Emmarex/dialogflow-fulfillment-python).
In this project I use a slightly modified version of the original classes.
