#!/usr/bin/env python3

from aws_cdk import core

from sports_event_manager.sports_event_manager_stack import SportsEventManagerStack


app = core.App()
SportsEventManagerStack(app, "sports-event-manager")

app.synth()
