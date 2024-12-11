from PyQt6.QtCore import QTimer
import csv
import os

header = ['ID', 'Vote Choice']


class Logic:
    """
    Handles the logic for the Voting Application, including submitting votes, checking for duplicates,
    writing results to a CSV file, and managing UI updates.
    """

    def __init__(self, ui: object) -> None:
        """
        Initializes the Logic class with the UI object.

        Args:
            ui (object): The UI object that contains the application interface elements.
        """
        self.ui = ui
        self.ui.Vote_Button.clicked.connect(self.on_submit)

    def on_submit(self) -> None:
        """
        Handles the submit action for the voting process.
        Validates the input, checks for duplicates, writes results to the CSV file,
        and updates the UI labels.

        Ensures that the vote is only cast if the ID is unique and valid.
        """
        storeID = self.ui.ID_Input.text()
        selected_button = self.ui.Voting_Options.checkedButton()

        # Check for invalid input or no candidate selection
        if not storeID.isdigit() or selected_button is None:
            self.ui.Error_Label.show()
            self.ui.Vote_Cast_Label.hide()
            self.ui.Already_Voted_Label.hide()
            return

        candidate = selected_button.text()

        # Open CSV file to append vote results
        with open('Vote Results.csv', 'a+', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_file.seek(0)
            first_line = csv_file.readline().strip()

            # Check if header is missing, write header if needed
            if not first_line or first_line.split(',') != header:
                csv_file.seek(0, os.SEEK_END)
                csv_writer.writerow(header)

            # Check if the ID has already voted
            is_duplicate = False
            for row in csv.reader(csv_file):
                if row[0] == storeID:
                    is_duplicate = True
                    break

            if is_duplicate:
                self.ui.Already_Voted_Label.show()
                self.ui.Error_Label.hide()
                self.clear_inputs()
                QTimer.singleShot(3000, self.clear_labels)
                return
            else:
                csv_writer.writerow([storeID, candidate])

        # Update UI if vote is cast successfully
        self.ui.Vote_Cast_Label.show()
        self.ui.Error_Label.hide()
        self.clear_inputs()
        QTimer.singleShot(3000, self.clear_labels)

    def clear_inputs(self) -> None:
        """
        Clears the input fields and unchecks the radio buttons.

        Ensures that the input fields and buttons are reset after submitting a vote.
        """
        self.ui.Voting_Options.setExclusive(False)  # Disable exclusivity for the group
        for button in self.ui.Voting_Options.buttons():
            button.setChecked(False)
        self.ui.Voting_Options.setExclusive(True)
        self.ui.ID_Input.clear()

    def clear_labels(self) -> None:
        """
        Hides the result and error labels after 3 seconds.

        This method is triggered by a timer to reset UI labels after a delay.
        """
        self.ui.Vote_Cast_Label.hide()
        self.ui.Already_Voted_Label.hide()
