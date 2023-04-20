from aws_cdk import (
    aws_lambda,
    aws_ec2,
    Duration,
)
from constructs import Construct
from configs.deployment_config import DeploymentConfig
from infra.services.network_service import NetworkService

LAMBDA_SOURCE_PATH = "./functions"

class LambdaService(Construct):

    DEFAULT_LAMBDA_TIMEOUT = Duration.seconds(15)
    DEFAULT_LAMBDA_MEMORY_USAGE = 512

    def __init__(self, scope: Construct, configs: DeploymentConfig, network_service: NetworkService, **kwargs) -> None:
        super().__init__(scope, f"{configs.deployment_name}-lambdas")

        vpc = network_service.vpc
        
        # Security Group for Lambda
        lambda_sg = aws_ec2.SecurityGroup(
            self,
            f"{configs.deployment_name}-lambda-sg",
            vpc=vpc,
            allow_all_outbound=False,
        )
        lambda_sg.add_egress_rule(
            aws_ec2.Peer.any_ipv4(), aws_ec2.Port.tcp(443)
        )

        # Provision lambda layer
        layer = aws_lambda.LayerVersion(
            self,
            id=f"{configs.deployment_name}-lambda-layer",
            code=aws_lambda.Code.from_asset("./layer"),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_9],
        )

        # Pre Signup Lambda
        self.pre_sign_up_lambda = aws_lambda.Function(
            self,
            id=f"{configs.deployment_name}-pre-sign-up",
            function_name=f"{configs.deployment_name}-pre-sign-up",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset(f"{LAMBDA_SOURCE_PATH}/pre_sign_up"),
            handler="lambda_function.lambda_handler",
            timeout=self.DEFAULT_LAMBDA_TIMEOUT,
            memory_size=self.DEFAULT_LAMBDA_MEMORY_USAGE,
            layers=[layer],
            environment={},
            security_groups=[lambda_sg],
            vpc=vpc,
            allow_all_outbound=False,
            vpc_subnets=aws_ec2.SubnetSelection(subnets=vpc.private_subnets),
            tracing=aws_lambda.Tracing.ACTIVE,
        )

        # Post Confirmation Lambda
        self.post_confirmation_lambda = aws_lambda.Function(
            self,
            id=f"{configs.deployment_name}-post-confirmation",
            function_name=f"{configs.deployment_name}-post-confirmation",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset(f"{LAMBDA_SOURCE_PATH}/post_confirmation"),
            handler="lambda_function.lambda_handler",
            timeout=self.DEFAULT_LAMBDA_TIMEOUT,
            memory_size=self.DEFAULT_LAMBDA_MEMORY_USAGE,
            layers=[layer],
            environment={},
            security_groups=[lambda_sg],
            vpc=vpc,
            allow_all_outbound=False,
            vpc_subnets=aws_ec2.SubnetSelection(subnets=vpc.private_subnets),
            tracing=aws_lambda.Tracing.ACTIVE,
        )

        # Pre Authentication Generation Lambda
        self.pre_authentication_lambda = aws_lambda.Function(
            self,
            id=f"{configs.deployment_name}-pre-authentication",
            function_name=f"{configs.deployment_name}-pre-authentication",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset(f"{LAMBDA_SOURCE_PATH}/pre_authentication"),
            handler="lambda_function.lambda_handler",
            timeout=self.DEFAULT_LAMBDA_TIMEOUT,
            memory_size=self.DEFAULT_LAMBDA_MEMORY_USAGE,
            layers=[layer],
            environment={},
            security_groups=[lambda_sg],
            vpc=vpc,
            allow_all_outbound=False,
            vpc_subnets=aws_ec2.SubnetSelection(subnets=vpc.private_subnets),
            tracing=aws_lambda.Tracing.ACTIVE,
        )

        # Pre Token Generation Lambda
        self.pre_token_generation_lambda = aws_lambda.Function(
            self,
            id=f"{configs.deployment_name}-pre-token-generation",
            function_name=f"{configs.deployment_name}-pre-token-generation",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset(f"{LAMBDA_SOURCE_PATH}/pre_token_generation"),
            handler="lambda_function.lambda_handler",
            timeout=self.DEFAULT_LAMBDA_TIMEOUT,
            memory_size=self.DEFAULT_LAMBDA_MEMORY_USAGE,
            layers=[layer],
            environment={},
            security_groups=[lambda_sg],
            vpc=vpc,
            allow_all_outbound=False,
            vpc_subnets=aws_ec2.SubnetSelection(subnets=vpc.private_subnets),
            tracing=aws_lambda.Tracing.ACTIVE,
        )

        # Post Authentication Lambda
        self.post_authentication_lambda = aws_lambda.Function(
            self,
            id=f"{configs.deployment_name}-post-authentication",
            function_name=f"{configs.deployment_name}-post-authentication",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset(f"{LAMBDA_SOURCE_PATH}/post_authentication"),
            handler="lambda_function.lambda_handler",
            timeout=self.DEFAULT_LAMBDA_TIMEOUT,
            memory_size=self.DEFAULT_LAMBDA_MEMORY_USAGE,
            layers=[layer],
            environment={},
            security_groups=[lambda_sg],
            vpc=vpc,
            allow_all_outbound=False,
            vpc_subnets=aws_ec2.SubnetSelection(subnets=vpc.private_subnets),
            tracing=aws_lambda.Tracing.ACTIVE,
        )
