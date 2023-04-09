## ARJ-Stack: Cognito User pool setup using AWS CDK

This repository is a walkthrough (along with code) on end-to-end setup of how to provision Cognito User Pool along with User Pool Client and with Lambda Triggers.

### Requirements

| Name | Version |
|------|---------|
| <a name="requirement_awscli"></a> [awscli](#requirement\_awscli) | 2.9.21 |
| <a name="requirement_python"></a> [python](#requirement\_python) | 3.11.1 |
| <a name="requirement_poetry"></a> [poetry](#requirement\_poetry) | 1.4.1 |

### Pre-requisites?

There are few steps that we need to follow to setup/configure the environment on local system. Refer [AWS Cloud Development Kit (AWS CDK) - Setup](https://github.com/ankit-jn/devops-aws-cdk-setup) for detailed instruction.

### How to setup the project (if doing it from start rather cloning it)

- Create a directory named `aws-cdk-cognito`
- Run the following commands withint the directory:

```
poetry init
poetry add antlr4-python3-runtime
poetry add pytest
```

### How to run it?

#### Create Python Virual Environment 

Run the following command to create python virual environment:

```
python -m venv .venv
```

#### Activate/Prapare the environment

Run the following command to activate the virtualenv:

```
.venv\Scripts\activate.bat
```

Run the following command to prepare the virtualenv for CDK references:

```
python -m pip install aws-cdk-lib 
```

#### Delete the executable directory (if any)

```
rmdir /S layer
```

#### Setup the executable directory

```
mkdir layer\python
xcopy core layer\python\core /E/H
```

#### Export dependencies

```
poetry export --without-hashes --format=requirements.txt > requirements-poetry.txt
```

#### Install dependencies

```
python -m pip install -r requirements-poetry.txt --target .\layer\python\ --upgrade
```

#### Synthesize the stack

```
cdk synth --profile <AWS Credential Profile Name>
```

#### Stack deployment

```
cdk deploy --profile <AWS Credential Profile Name>
```


#### How to test it programmatically?

Change the following values in example/login.py and run the program:

- PROFILE_NAME: Your AWS profile name
- COGNITO_IDP_REGION: AWS Region Code
- USER_POOL_ID: Cognito User Pool ID
- CLIENT_ID: Client ID
- CLIENT_SECRET: Client Secret
- USER_NAME: Your User Name which you have choosen while signed-up with Cognito User Pool
- PASSWORD: Password

### Authors

Module is maintained by [Ankit Jain](https://github.com/ankit-jn) with help from [these professional](https://github.com/ankit-jn/aws-cdk-cognito/graphs/contributors).
