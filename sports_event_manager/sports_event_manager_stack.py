from aws_cdk import (core,
                    aws_apigateway as apigateway,
                    aws_lambda as _lambda,
)

class SportsEventManagerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        #lambda
        ###players###
        get_players = _lambda.Function(self,'get_players',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='playersDBHandler.get_players')

        get_player = _lambda.Function(self,'get_player',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='playersDBHandler.get_player')

        add_player = _lambda.Function(self,'add_player',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='playersDBHandler.add_player')

        update_player = _lambda.Function(self,'update_player',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='playersDBHandler.update_player')

        delete_player = _lambda.Function(self,'delete_player',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='playersDBHandler.delete_player')

        ###teams###


        #api
        api = apigateway.RestApi(self, "SportsEventManagerApi")

        # /pla
        players = api.root.add_resource("players")
        players.add_method("GET", apigateway.LambdaIntegration(get_players))
        players.add_method("POST", apigateway.LambdaIntegration(add_player))

        player = players.add_resource("{player_id}")
        player.add_method("GET", apigateway.LambdaIntegration(get_player))
        player.add_method("PUT", apigateway.LambdaIntegration(update_player))
        player.add_method("DELETE", apigateway.LambdaIntegration(delete_player))




