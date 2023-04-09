from aws_cdk import (
    aws_ec2,
    Duration,
    Stack,
)
from constructs import Construct
from typing import Dict, List, Tuple
from configs.deployment_config import DeploymentConfig

class NetworkService(Construct):

    DEFAULT_LAMBDA_TIMEOUT = Duration.seconds(15)
    DEFAULT_LAMBDA_MEMORY_USAGE = 512

    def __init__(self, scope: Construct, configs: DeploymentConfig, **kwargs) -> None:
        super().__init__(scope, f"{configs.deployment_name}-network")

        # VPC
        self.vpc = self.__createVPC(configs.deployment_name,
                               configs.app_parameters["vpc"])
        
    def __createVPC(self: Construct, deployment_name: str, vpc_configs: Dict) -> aws_ec2.Vpc:
        vpc = aws_ec2.Vpc(self, f'{deployment_name}-vpc',
                          vpc_name=f'{deployment_name}-vpc',
                          ip_addresses=aws_ec2.IpAddresses.cidr(
                              vpc_configs["cidr"]),
                          enable_dns_hostnames=vpc_configs["enable_dns_hostnames"],
                          enable_dns_support=vpc_configs["enable_dns_support"],
                          subnet_configuration=[
                            aws_ec2.SubnetConfiguration(
                                name=f"{deployment_name}-public-subnet",
                                subnet_type=aws_ec2.SubnetType.PUBLIC,
                                cidr_mask=24,
                            ),
                            aws_ec2.SubnetConfiguration(
                                name=f"{deployment_name}-private-subnet",
                                subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS,
                                cidr_mask=24,
                            ),
                            aws_ec2.SubnetConfiguration(
                                name=f"{deployment_name}-isolated-subnet",
                                subnet_type=aws_ec2.SubnetType.PRIVATE_ISOLATED,
                                cidr_mask=24,
                            ),
                         ],
                         nat_gateways=1)
        return vpc
