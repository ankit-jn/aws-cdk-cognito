from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
)
from constructs import Construct
from typing import Dict, List, Tuple
from configs.deployment_config import DeploymentConfig

from infra.services.network_service import NetworkService
from infra.services.lambda_service import LambdaService
from infra.services.cognito_service import CognitoService

class InfraStack(Stack):

    DEFAULT_LAMBDA_TIMEOUT = Duration.seconds(15)
    DEFAULT_LAMBDA_MEMORY_USAGE = 512

    def __init__(self, scope: Construct, construct_id: str, configs: DeploymentConfig, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        aws_region = configs.app_parameters["aws_region"]
        
        network_service = NetworkService(scope=self, configs=configs)
        lambda_service = LambdaService(scope=self, configs=configs, network_service=network_service)
        cognito_service = CognitoService(scope=self, configs=configs, lambda_service=lambda_service)

        CfnOutput(
            self, 
            "vpc",
            value=network_service.vpc.vpc_id,
            export_name=f"{configs.deployment_name}-vpc-id",
        )

        CfnOutput(
            self,
            "cognitouserpoolid",
            value=cognito_service.user_pool.user_pool_id,
            export_name=f"{configs.deployment_name}-cognito-userpool-id",
        )
        CfnOutput(
            self,
            "cognitoclientid",
            value=cognito_service.user_pool_client.user_pool_client_id,
            export_name=f"{configs.deployment_name}-cognito-clientid",
        )
        CfnOutput(
            self,
            "cognitoclientsecret",
            value=cognito_service.user_pool_client.user_pool_client_secret.unsafe_unwrap(),
            export_name=f"{configs.deployment_name}-cognito-client-secret",
        )
        CfnOutput(
            self,
            "cognitobaseurl",
            value=f"https://{cognito_service.user_pool_domain.domain_name}.auth.{aws_region}.amazoncognito.com",
            export_name=f"{configs.deployment_name}-cognito-baseurl",
        )
        CfnOutput(
            self,
            "cognitotokenurl",
            value=f"https://{cognito_service.user_pool_domain.domain_name}.auth.{aws_region}.amazoncognito.com/oauth2/token",
            export_name=f"{configs.deployment_name}-cognito-token-url",
        )
        CfnOutput(
            self,
            "cognitoauthurl",
            value=f"https://{cognito_service.user_pool_domain.domain_name}.auth.{aws_region}.amazoncognito.com/oauth2/authorize",
            export_name=f"{configs.deployment_name}-cognito-auth-url",
        )
