from enum import Enum
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

from src.scrape.scrape_utils import ScrapeUtils

URI = "https://termine.staedteregion-aachen.de/auslaenderamt/"
# Page 1
BUTTON_REPORTING_PRESENCE_ID = "buttonfunktionseinheit-1"

# Page 2
STAY_HEADER_ID = "concerns_accordion-340"
TEAM_1_APPOINTMENTS_ID = "input-264"
TEAM_2_APPOINTMENTS_ID = "input-267"
TEAM_3_APPOINTMENTS_ID = "input-268"

# Page 3
SELECT_LOCATION_NAME = "select_location"
LOCATION_XPATH = "//input[@type='submit' and @aria-label='Ausländeramt Aachen, 2. Etage auswählen' and @name='select_location' and @value='Ausländeramt Aachen, 2. Etage auswählen' and @class='btn btn-primary onehundred pull-right']"

# Page 4
NO_APPOINTMENT_TEXT = "Keine Zeiten verfügbar"

# GENERAL
BUTTON_OK_TEXT = "OK"
BUTTON_OK_ID = "OKButton"
NEXT_BUTTON_ID = "WeiterButton"
TITLE_TEXT = "title"
BUTTON_BACK_ID = "zurueck"


class RegistrationTeam(str, Enum):
    Team1 = "Team1"
    Team2 = "Team2"
    Team3 = "Team3"


class ResidencePermitAachen:
    _TEAM_REGISTRATION_ID_MAPPING = {
        RegistrationTeam.Team1: TEAM_1_APPOINTMENTS_ID,
        RegistrationTeam.Team2: TEAM_2_APPOINTMENTS_ID,
        RegistrationTeam.Team3: TEAM_3_APPOINTMENTS_ID,
    }

    def __init__(
            self,
            appointments: int,
            team: RegistrationTeam,
            timeout: int,
            browser=webdriver.Chrome(),
            scrape_utils=ScrapeUtils()
    ) -> None:
        self._appointments = appointments
        self._team = team
        self._timeout = timeout
        self._scrape_utils = scrape_utils
        self._browser = browser
        self._browser.get(URI)

    def book_residence_permit(self) -> bool:
        found_appointment = False
        self._process_residence_permit_page_1()
        self._process_residence_permit_page_2()

        while not found_appointment:
            self._process_residence_permit_page_3()
            print("Trying to find an appointment.")
            if self._process_residence_permit_page_4():
                found_appointment = True
            else:
                print("Unable to find an appointment. Waiting for '{seconds}' seconds.".format(
                    seconds=self._timeout))
                sleep(self._timeout)
                self._scrape_utils.find_button_and_click(self._browser, By.ID, BUTTON_BACK_ID)
        return found_appointment

    def _process_residence_permit_page_1(self) -> None:
        self._scrape_utils.find_button_and_click(
            self._browser,
            By.ID,
            BUTTON_REPORTING_PRESENCE_ID)

    def _process_residence_permit_page_2(self) -> None:
        team_appointment_id = self._TEAM_REGISTRATION_ID_MAPPING.get(self._team)
        self._scrape_utils.find_button_and_click(self._browser, By.ID, STAY_HEADER_ID)
        self._scrape_utils.find_field_and_enter(
            self._browser,
            By.ID,
            team_appointment_id,
            self._appointments)
        # self._find_button_and_click(self._browser, By.ID, NEXT_BUTTON_ID) why no next?
        self._scrape_utils.find_button_and_click(self._browser, By.ID, BUTTON_OK_ID)

    def _process_residence_permit_page_3(self) -> None:
        self._scrape_utils.find_by_xpath_and_click(self._browser, By.XPATH, LOCATION_XPATH)

    def _process_residence_permit_page_4(self) -> bool:
        return self._scrape_utils.field_contains_text(
            self._browser,
            By.TAG_NAME,
            TITLE_TEXT,
            NO_APPOINTMENT_TEXT)
