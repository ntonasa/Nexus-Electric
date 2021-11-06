from argparse import ArgumentParser, FileType

def generate_parser():
    main_parser = ArgumentParser(
        prog='energy_group11',
        description="NexusElectric API CLI client"
    )
    scope_subparsers = main_parser.add_subparsers(
        metavar="scope",
        dest="scope"
    )

    scope_subparsers.required = True

    configure_parser_health(scope_subparsers)
    configure_parser_reset(scope_subparsers)
    configure_parser_login(scope_subparsers)
    configure_parser_logout(scope_subparsers)
    configure_parser_actual(scope_subparsers)
    configure_parser_aggregated(scope_subparsers)
    configure_parser_day_ahead(scope_subparsers)
    configure_parser_actual_vs_forecast(scope_subparsers)
    configure_parser_admin(scope_subparsers)

    return main_parser

# Health Check Parser
def configure_parser_health(scope_subparsers):
    health_check_subparser = scope_subparsers.add_parser('HealthCheck', help="check database connectivity")
    health_check_subparser.set_defaults(func=health_check)

# Reset Parser
def configure_parser_reset(scope_subparsers):
    reset_subparser = scope_subparsers.add_parser('Reset', help="reset database")
    reset_subparser.set_defaults(func=reset)

# Login Parser
def configure_parser_login(scope_subparsers):
    login_subparser = scope_subparsers.add_parser(
        'Login', 
        help="authenticate user using credentials and obtain token"
    )
    login_subparser.add_argument(
        '--username', 
        metavar="username", 
        required=True
    )
    login_subparser.add_argument(
        '--password', 
        metavar="password", 
        required=True
    )

    login_subparser.set_defaults(func=login)

# Logout Parser
def configure_parser_logout(scope_subparsers):
    logout_subparser = scope_subparsers.add_parser(
        'Logout', 
        help="remove authentication token"
    )

    logout_subparser.set_defaults(func=logout)

# Actual Total Load Parser
def configure_parser_actual(scope_subparsers):
    p = scope_subparsers.add_parser(
        'ActualTotalLoad', 
        help="query ActualTotalLoad dataset"
    )

    add_dataset_patameters(p)
    p.set_defaults(func=actual_total_load)

# Aggregated Generation Per Type
def configure_parser_aggregated(scope_subparsers):
    p = scope_subparsers.add_parser(
        'AggregatedGenerationPerType', 
        help="query AggregatedGenerationPerType dataset"
    )

    add_dataset_patameters(p)
    p.set_defaults(func=aggregated_generation_per_type)

# Day Ahead Total Load Forecast
def configure_parser_day_ahead(scope_subparsers):
    p = scope_subparsers.add_parser(
        'DayAheadTotalLoadForecast', 
        help="query DayAheadTotalLoadForecast dataset"
    )

    add_dataset_patameters(p)
    p.set_defaults(func=day_ahead_total_load_forecast)

# Actual vs Forecast
def configure_parser_actual_vs_forecast(scope_subparsers):
    p = scope_subparsers.add_parser(
        'ActualvsForecast', 
        help="query ActualvsForecast dataset"
    )

    add_dataset_patameters(p)
    p.set_defaults(func=actual_vs_forecast)

# Admin Parser
def configure_parser_admin(scope_subparsers):
    p = scope_subparsers.add_parser(
        'Admin',
        help="Application & User Management"
    )

    newuser_group = p.add_argument_group("Newuser options")
    newuser_group.add_argument('--newuser', metavar="username", required=True)
    newuser_group.add_argument('--passwd', metavar="password", required=True)
    newuser_group.add_argument('--email', metavar="email", required=True)
    newuser_group.add_argument('--quota', type=int, metavar="quota", required=True)

    moduser_group = p.add_argument_group("Moduser options")
    moduser_group.add_argument('--newuser', metavar="username", required=True)
    moduser_group.add_argument('--passwd', metavar="password", required=True)
    moduser_group.add_argument('--email', metavar="email", required=True)
    moduser_group.add_argument('--quota', type=int, metavar="quota", required=True)

    userstatus_group = p.add_argument_group("Userstatus options")
    userstatus_group.add_argument('--userstatus', metavar="username")

    newdata_group = p.add_parser('Newdata options')
    newdata_group.add_argument('--newdata', metavar="username", choices=['ActualTotalLoad', 'AggregatedGenerationPerType', 'DayAheadTotalLoadForecast'], required=True)
    newdata_group.add_argument('--source', type=FileType('r', encoding='UTF-8'), metavar="filename", required=True)

    p.set_defaults(func=admin)

# Dataset Arguments
def add_dataset_patameters(p):
    dataset_params = p.add_argument_group("Dataset filtering parameters")
    date_params = dataset_params.add_mutually_exclusive_group()
    dataset_params.add_argument(
        '--area', 
        metavar="area_name", 
        required=True
    )
    dataset_params.add_argument(
        '--timeres', 
        choices=['PT15M', 'PT30M', 'PT60M'], 
        required=True, 
        help="resolution type description"
    )
    date_params.add_argument(
        '--date', 
        metavar="YYYY-MM-DD", 
        help="date in YYYY-MM-DD format to filter dataset"
    )
    date_params.add_argument(
        '--month', 
        metavar="YYYY-MM", 
        help="date in YYYY-MM format to filter dataset"
    )
    date_params.add_argument(
        '--year', 
        metavar="YYYY", 
        help="date in YYYY format to filter dataset"
    )
    dataset_params.add_argument(
        '--format', 
        metavar="type", 
        choices=['json', 'csv'], 
        default="json"
    )

    return dataset_params




args = main_parser.parse_args()
params = vars(args)
if 'func' in params:
    args.func(params)