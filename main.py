import argparse
import concurrent.futures

from src.aachen.residence_permit_aachen import ResidencePermitAachen, RegistrationTeam
from src.notification.sound import Sound


def _create_arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process input parameters.")
    parser.add_argument(
        "teams",
        type=int,
        default=1,
        nargs='?',
        help="Number of registration teams. This might not be available for all registrations.")
    parser.add_argument(
        "appointments",
        type=int,
        default=1,
        nargs='?',
        help="Number of appointments to book")
    parser.add_argument(
        "timeout",
        type=int,
        default=5,
        nargs='?',
        help="Timeout duration in seconds if an appointment is not available")
    return parser.parse_args()


def _find_residence_permit_appointment(
        team: RegistrationTeam,
        args: argparse.Namespace) -> None:
    try:
        success = ResidencePermitAachen(
            appointments=args.appointments,
            team=team,
            timeout=args.timeout).book_residence_permit()
        if success:
            print("Found an appointment slot!!")
            Sound().notify()
    except Exception as ex:
        print(f"Residence permit lookup for team {team} failed.", ex)


if __name__ == '__main__':
    input_args = _create_arg_parser()
    teams = [RegistrationTeam.Team1, RegistrationTeam.Team2, RegistrationTeam.Team3][0: input_args.teams]
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(teams)) as executor:
        futures = [executor.submit(_find_residence_permit_appointment, team, input_args) for team in teams]
