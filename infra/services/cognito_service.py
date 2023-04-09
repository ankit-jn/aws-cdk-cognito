from aws_cdk import (
    aws_cognito,
    aws_lambda,
    RemovalPolicy,
    Duration,
)
from constructs import Construct
from typing import Dict, List, Tuple
from configs.deployment_config import DeploymentConfig
from infra.services.lambda_service import LambdaService

class CognitoService(Construct):

    DEFAULT_LAMBDA_TIMEOUT = Duration.seconds(15)
    DEFAULT_LAMBDA_MEMORY_USAGE = 512

    def __init__(self, scope: Construct, configs: DeploymentConfig, lambda_service: LambdaService, **kwargs) -> None:
        super().__init__(scope, f"{configs.deployment_name}-cognito")
        
        # Cognito [User Pool]
        self.user_pool = self.__createUserPool(
            deployment_name=configs.deployment_name,
            pre_sign_up_lambda=lambda_service.pre_sign_up_lambda,
            post_confirmation_lambda=lambda_service.post_confirmation_lambda,
            pre_authentication_lambda=lambda_service.pre_authentication_lambda,
            pre_token_generation_lambda=lambda_service.pre_token_generation_lambda,
            post_authentication_lambda=lambda_service.post_authentication_lambda
        )

        # Cognito [User Pool Domain]
        self.user_pool_domain = self.__createUserPoolDomain(
            deployment_name=configs.deployment_name,
            user_pool=self.user_pool
        )

        # Cognito [User Pool Cient]
        self.user_pool_client = self.__createUserPoolClient(
            deployment_name=configs.deployment_name,
            user_pool=self.user_pool,
            callback_urls=configs.app_parameters["callback_urls"]
        )
    
    def __createUserPool(
        self: Construct,
        deployment_name: str,
        pre_sign_up_lambda: aws_lambda.Function,
        post_confirmation_lambda: aws_lambda.Function,
        pre_authentication_lambda: aws_lambda.Function,
        pre_token_generation_lambda: aws_lambda.Function,
        post_authentication_lambda: aws_lambda.Function
    ) -> Tuple[
        aws_cognito.UserPool, aws_cognito.UserPoolDomain, aws_cognito.UserPoolClient
    ]:
        user_pool = aws_cognito.UserPool(
            self,
            id=f"{deployment_name}-user-pool",
            sign_in_case_sensitive=False,
            auto_verify=aws_cognito.AutoVerifiedAttrs(
                email=True,
            ),
            user_pool_name=f"{deployment_name}-user-pool",
            self_sign_up_enabled=True,
            standard_attributes=aws_cognito.StandardAttributes(
                email=aws_cognito.StandardAttribute(
                    required=True,
                ),
                given_name=aws_cognito.StandardAttribute(
                    required=True,
                ),
                family_name=aws_cognito.StandardAttribute(required=True),
            ),
            removal_policy=RemovalPolicy.DESTROY,
            lambda_triggers=aws_cognito.UserPoolTriggers(
                pre_sign_up=pre_sign_up_lambda,
                post_confirmation=post_confirmation_lambda,
                pre_authentication=pre_authentication_lambda,
                pre_token_generation=pre_token_generation_lambda,
                post_authentication=post_authentication_lambda,
            ),
        )
        
        aws_cognito.UserPoolResourceServer(
            self,
            id=f"{deployment_name}-user-pool-resource-server",
            user_pool=user_pool,
            identifier="com.example.photos",
            scopes=[],
            user_pool_resource_server_name=f"{deployment_name}-user-pool-resource-server",
        )

        return user_pool
    
    def __createUserPoolDomain(
        self: Construct,
        deployment_name: str,
        user_pool: aws_cognito.UserPool
    ) -> Tuple[
        aws_cognito.UserPool, aws_cognito.UserPoolDomain, aws_cognito.UserPoolClient
    ]:
        user_pool_domain = aws_cognito.UserPoolDomain(
            self,
            id=f"{deployment_name}-user-pool-domain",
            user_pool=user_pool,
            cognito_domain=aws_cognito.CognitoDomainOptions(
                domain_prefix=f"{deployment_name}-user-pool-domain",
            ),
        )
        return user_pool_domain
    
    def __createUserPoolClient(
        self: Construct,
        deployment_name: str,
        user_pool: aws_cognito.UserPool,
        callback_urls: List[str]
    ) -> Tuple[
        aws_cognito.UserPool, aws_cognito.UserPoolDomain, aws_cognito.UserPoolClient
    ]:
        user_pool_client = aws_cognito.UserPoolClient(
            self,
            id=f"{deployment_name}-user-pool-client",
            user_pool=user_pool,
            generate_secret=True,
            auth_flows=aws_cognito.AuthFlow(
                admin_user_password=True, custom=True, user_srp=True
            ),
            o_auth=aws_cognito.OAuthSettings(
                flows=aws_cognito.OAuthFlows(
                    authorization_code_grant=True, implicit_code_grant=True
                ),
                callback_urls=callback_urls,
                scopes=[
                    aws_cognito.OAuthScope.EMAIL,
                    aws_cognito.OAuthScope.OPENID,
                    aws_cognito.OAuthScope.COGNITO_ADMIN,
                    aws_cognito.OAuthScope.PROFILE,
                ],
            ),
        )
        return user_pool_client
