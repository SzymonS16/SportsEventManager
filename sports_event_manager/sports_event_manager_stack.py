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
        bucket = s3.Bucket(self, "Bucket",)
        
         ###Tables###
        table_players = dynamodb.Table(self, "Players",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        table_teams = dynamodb.Table(self, "Teams",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        table_sport_facilities = dynamodb.Table(self, "SportFacilities",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        table_events = dynamodb.Table(self, "Events",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        table_reservations = dynamodb.Table(self, "Reservation",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        ###Enviroment###
        env_ = {
            "BUCKET" : bucket.bucket_name,
            "TABLE_PLAYERS" : table_players.table_name,
            "TABLE_TEAMS" : table_teams.table_name,
            "TABLE_SPORT_FACILITIES" : table_sport_facilities.table_name, 
            "TABLE_EVENTS" : table_events.table_name, 
            "TABLE_RESERVATIONS" : table_reservations.table_name 
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
        table_players.grant_read_write_data(update_player)

        delete_player = _lambda.Function(self,'delete_player',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='playersDBhandler.delete_player')
        table_players.grant_read_write_data(delete_player)

        #teams
        get_teams = _lambda.Function(self,'get_teams',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='teamsDBhandler.get_teams',
            environment=env_)
        table_teams.grant_read_write_data(get_teams)

        get_team = _lambda.Function(self,'get_team',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='teamsDBhandler.get_team',
            environment=env_)
        table_teams.grant_read_write_data(get_team)
        bucket.grant_read(get_team)

        add_team = _lambda.Function(self,'add_team',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='teamsDBhandler.add_team',
            environment=env_)
        table_teams.grant_read_write_data(add_team)
        bucket.grant_read_write(add_team)
        
        update_team = _lambda.Function(self,'update_team',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='teamsDBhandler.update_team')
        table_teams.grant_read_write_data(update_team)

        delete_team = _lambda.Function(self,'delete_team',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='teamsDBhandler.delete_team')
        table_teams.grant_read_write_data(delete_team)


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
        teams = api.root.add_resource("teams")
        teams.add_method("GET", apigateway.LambdaIntegration(get_teams), 
            authorization_type=apigateway.AuthorizationType.NONE)
        teams.add_method("POST", apigateway.LambdaIntegration(add_team),
            authorization_type=apigateway.AuthorizationType.NONE)
        
        team = teams.add_resource("{team_id}")
        team.add_method("GET", apigateway.LambdaIntegration(get_team),
            authorization_type=apigateway.AuthorizationType.NONE)
        team.add_method("PUT", apigateway.LambdaIntegration(update_team),
            authorization_type=apigateway.AuthorizationType.NONE)
        team.add_method("DELETE", apigateway.LambdaIntegration(delete_team),
            authorization_type=apigateway.AuthorizationType.NONE)
       



