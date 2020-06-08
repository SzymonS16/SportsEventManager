from aws_cdk import (core,
                    aws_apigateway as apigateway,
                    aws_lambda as _lambda,
                    aws_dynamodb as dynamodb,
                    aws_s3 as s3,
                    aws_iam as iam
                    
)

class SportsEventManagerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        ###Bucket###
        bucket = s3.Bucket(self, "Bucket",
        )
        
         ###Tables###
        table_players = dynamodb.Table(self, "Players",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        env_ = {
            "BUCKET" : bucket.bucket_name,
            "TABLE_PLAYERS" : table_players.table_name
        }

        ###Lambdas###
        #players
        get_players = _lambda.Function(self,'get_players',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='playersDBhandler.get_players',
            environment=env_)
        table_players.grant_read_write_data(get_players)

        get_player = _lambda.Function(self,'get_player',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='playersDBhandler.get_player',
            environment=env_)
        table_players.grant_read_write_data(get_player)
        bucket.grant_read(get_player)

        add_player = _lambda.Function(self,'add_player',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='playersDBhandler.add_player',
            environment=env_)
        table_players.grant_read_write_data(add_player)
        bucket.grant_read_write(add_player)
        add_player.add_to_role_policy(iam.PolicyStatement(
            resources=['*'],
            actions=["rekognition:DetectFaces"]
        ))

        update_player = _lambda.Function(self,'update_player',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='playersDBhandler.update_player')

        delete_player = _lambda.Function(self,'delete_player',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='playersDBhandler.delete_player')
        table_players.grant_read_write_data(delete_player)

        #teams

        ###API###
        api = apigateway.RestApi(self, "SportsEventManagerApi")

        # /players
        players = api.root.add_resource("players")
        players.add_method("GET", apigateway.LambdaIntegration(get_players), 
            authorization_type=apigateway.AuthorizationType.NONE)
        players.add_method("POST", apigateway.LambdaIntegration(add_player),
            authorization_type=apigateway.AuthorizationType.NONE)
        
        player = players.add_resource("{player_id}")
        player.add_method("GET", apigateway.LambdaIntegration(get_player),
            authorization_type=apigateway.AuthorizationType.NONE)
        player.add_method("PUT", apigateway.LambdaIntegration(update_player),
            authorization_type=apigateway.AuthorizationType.NONE)
        player.add_method("DELETE", apigateway.LambdaIntegration(delete_player),
            authorization_type=apigateway.AuthorizationType.NONE)

        # /teams

       



