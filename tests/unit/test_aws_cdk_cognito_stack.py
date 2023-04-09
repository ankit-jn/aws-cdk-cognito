import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_cognito.aws_cdk_cognito_stack import AwsCdkCognitoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_cdk_cognito/aws_cdk_cognito_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsCdkCognitoStack(app, "aws-cdk-cognito")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
