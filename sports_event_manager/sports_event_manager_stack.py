from aws_cdk import (core,
                    aws_apigateway as apigateway,
                    aws_lambda as _lambda,
                    aws_dynamodb as dynamodb,
                    aws_s3 as s3,
                    aws_iam as iam,
                    aws_lambda_event_sources as lambda_event_sources,
                    aws_sqs as sqs               
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

        ###Queue###
        queue_facilities = sqs.Queue(self, "QueueFacilities", 
        visibility_timeout = core.Duration.minutes(3)
        )

        ###Enviroment###
        env_ = {
            "BUCKET" : bucket.bucket_name,
            "TABLE_PLAYERS" : table_players.table_name,
            "TABLE_TEAMS" : table_teams.table_name,
            "TABLE_SPORT_FACILITIES" : table_sport_facilities.table_name, 
            "TABLE_EVENTS" : table_events.table_name, 
            "TABLE_RESERVATIONS" : table_reservations.table_name,
            "QUEUE_FACILITIES_URL" : queue_facilities.queue_url,
            "QUEUE_FACILITIES" : queue_facilities.queue_name
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

        #sport_facilities
        get_sport_facilities = _lambda.Function(self,'get_sport_facilities',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='sportFacilitiesDBhandler.get_sport_facilities',
            environment=env_)
        table_sport_facilities.grant_read_write_data(get_sport_facilities)

        get_sport_facility = _lambda.Function(self,'get_sport_facility',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='sportFacilitiesDBhandler.get_sport_facility',
            environment=env_)
        table_sport_facilities.grant_read_write_data(get_sport_facility)
        bucket.grant_read(get_sport_facility)

        add_sport_facility = _lambda.Function(self,'add_sport_facility',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='sportFacilitiesDBhandler.add_sport_facility',
            environment=env_)
        table_sport_facilities.grant_read_write_data(add_sport_facility)
        bucket.grant_read_write(add_sport_facility)
        queue_facilities.grant_send_messages(add_sport_facility)

        process_new_sport_facility = _lambda.Function(self,'process_new_sport_facility',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='sportFacilitiesDBhandler.process_new_sport_facility',
            environment=env_)
        table_sport_facilities.grant_read_write_data(process_new_sport_facility)
        bucket.grant_read_write(process_new_sport_facility)
        process_new_sport_facility.add_event_source(lambda_event_sources.SqsEventSource(queue_facilities,batch_size=1))

        update_sport_facility = _lambda.Function(self,'update_sport_facility',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='sportFacilitiesDBhandler.update_sport_facility')
        table_sport_facilities.grant_read_write_data(update_sport_facility)

        delete_sport_facility = _lambda.Function(self,'delete_sport_facility',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='sportFacilitiesDBhandler.delete_sport_facility')
        table_sport_facilities.grant_read_write_data(delete_sport_facility)

        #reservations
        get_reservations = _lambda.Function(self,'get_reservations',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='reservation_handler.get_reservations',
            environment=env_)
        table_reservations.grant_read_write_data(get_reservations)

        get_reservation = _lambda.Function(self,'get_reservation',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='reservation_handler.get_reservation',
            environment=env_)
        table_reservations.grant_read_write_data(get_reservation)
        bucket.grant_read(get_reservation)

        add_reservation = _lambda.Function(self,'add_reservation',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='reservation_handler.add_reservation',
            environment=env_)
        table_reservations.grant_read_write_data(add_reservation)
        bucket.grant_read_write(add_reservation)
        table_players.grant_read_data(add_reservation)
        table_sport_facilities.grant_read_data(add_reservation)
        
        update_reservation = _lambda.Function(self,'update_reservation',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='reservation_handler.update_reservation')
        table_reservations.grant_read_write_data(update_reservation)

        delete_reservation = _lambda.Function(self,'delete_reservation',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='reservation_handler.delete_reservation')
        table_reservations.grant_read_write_data(delete_reservation)

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

        # /facilities
        facilities = api.root.add_resource("facilities")
        facilities.add_method("GET", apigateway.LambdaIntegration(get_sport_facilities), 
            authorization_type=apigateway.AuthorizationType.NONE)
        facilities.add_method("POST", apigateway.LambdaIntegration(add_sport_facility),
            authorization_type=apigateway.AuthorizationType.NONE)
        
        facility = facilities.add_resource("{facility_id}")
        facility.add_method("GET", apigateway.LambdaIntegration(get_sport_facility),
            authorization_type=apigateway.AuthorizationType.NONE)
        facility.add_method("PUT", apigateway.LambdaIntegration(update_sport_facility),
            authorization_type=apigateway.AuthorizationType.NONE)
        facility.add_method("DELETE", apigateway.LambdaIntegration(delete_sport_facility),
            authorization_type=apigateway.AuthorizationType.NONE)

        # /reservations
        reservations = api.root.add_resource("reservations")
        reservations.add_method("GET", apigateway.LambdaIntegration(get_reservations), 
            authorization_type=apigateway.AuthorizationType.NONE)
        reservations.add_method("POST", apigateway.LambdaIntegration(add_reservation),
            authorization_type=apigateway.AuthorizationType.NONE)
        
        reservation = reservations.add_resource("{reservation_id}")
        reservation.add_method("GET", apigateway.LambdaIntegration(get_reservation),
            authorization_type=apigateway.AuthorizationType.NONE)
        reservation.add_method("PUT", apigateway.LambdaIntegration(update_reservation),
            authorization_type=apigateway.AuthorizationType.NONE)
        reservation.add_method("DELETE", apigateway.LambdaIntegration(delete_reservation),
            authorization_type=apigateway.AuthorizationType.NONE)

       
