# ==========================================
# LIBRARIES
# ==========================================

import math as m
import random as r
import datetime as d
from pyscript import document


# ==========================================
# GLOBAL VARIABLES
# These are filled when Generate is clicked.
# ==========================================

NUM_OF_SUBJECTS = 0
NUM_OF_PERIODS = 0

subjects = []
period_allocation = {}
time_table = []

TOTAL_PERIODS = 0
ALLOCATED_PERIODS = 0
subject_pool = []

MAX_SUBJECTS_PER_DAY = 2
MAX_ATTEMPTS = 10000

NUMBER_OF_PAIRS = 5
SAMPLES_PER_PAIR = 2

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
]


# ==========================================
# HELPER: SHOW TEXT IN THE WEBPAGE
# ==========================================

def show_result(message):
    document.getElementById("result").innerText = message


# ==========================================
# FUNCTION: READ INPUTS AND GENERATE
# Called by the Generate button in index.html
# ==========================================

def generateTimeTable(event=None):
    global NUM_OF_SUBJECTS, NUM_OF_PERIODS
    global subjects, period_allocation, time_table
    global TOTAL_PERIODS, ALLOCATED_PERIODS, subject_pool

    result = document.getElementById("result")
    result.innerText = ""

    try:
        NUM_OF_SUBJECTS = int(document.getElementById("numOfSubs").value)
        NUM_OF_PERIODS = int(document.getElementById("numOfSessions").value)

        if NUM_OF_SUBJECTS < 1 or NUM_OF_PERIODS < 1:
            show_result("Please enter a number of subjects and periods greater than 0.")
            return

        subjects = []
        period_allocation = {}
        time_table = []

        # Read subject names and their weekly period allocations.
        for i in range(NUM_OF_SUBJECTS):
            subject_input = document.getElementById(f"subject{i + 1}")
            allocation_input = document.getElementById(f"sub{i + 1}Sessions")

            if subject_input is None or allocation_input is None:
                show_result("Please click Next and enter all subject details first.")
                return

            subject = subject_input.value.strip()

            if not subject:
                show_result(f"Please enter a name for Subject {i + 1}.")
                return

            if not allocation_input.value:
                show_result(f"Please enter the number of sessions for {subject}.")
                return

            allocation = int(allocation_input.value)

            if allocation < 0:
                show_result(f"Sessions for {subject} cannot be negative.")
                return

            subjects.append(subject)
            period_allocation[subject] = allocation

        # ==========================================
        # CHECK TOTAL PERIOD ALLOCATION
        # ==========================================

        TOTAL_PERIODS = 6 * NUM_OF_PERIODS
        ALLOCATED_PERIODS = sum(period_allocation.values())

        if ALLOCATED_PERIODS != TOTAL_PERIODS:
            show_result(
                "ERROR: Your period allocation does not match the available periods.\n"
                f"Available periods: {TOTAL_PERIODS}\n"
                f"Allocated periods: {ALLOCATED_PERIODS}"
            )
            return

        # ==========================================
        # CREATE SUBJECT POOL
        # ==========================================

        subject_pool = []

        for subject in subjects:
            for i in range(period_allocation[subject]):
                subject_pool.append(subject)

        # ==========================================
        # GENERATE SAMPLE PAIRS
        # ==========================================

        sample_pairs = []

        for pair_number in range(NUMBER_OF_PAIRS):
            sample1 = generate_timetable()

            if sample1 is None:
                continue

            sample2 = None

            for attempt in range(MAX_ATTEMPTS):
                possible_sample2 = generate_timetable()

                if possible_sample2 is None:
                    continue

                if check_pair(sample1, possible_sample2):
                    sample2 = possible_sample2
                    break

            if sample2 is None:
                continue

            sample_pairs.append([sample1, sample2])

        # ==========================================
        # DISPLAY ALL SAMPLE PAIRS IN THE PAGE
        # ==========================================

        if not sample_pairs:
            show_result(
                "Could not generate any valid timetable pairs. "
                "Try changing the number of sessions allocated to subjects."
            )
            return

        output = [
            "GENERATED TIME TABLE SAMPLE PAIRS",
            "=" * 50
        ]

        for pair_number, pair in enumerate(sample_pairs, start=1):
            output.append(f"\n{'=' * 50}\nPAIR {pair_number}\n{'=' * 50}")

            for sample_number, table in enumerate(pair, start=1):
                output.append(f"\n--- SAMPLE {sample_number} ---")

                for day in range(6):
                    output.append(f"\n=== {days[day]} ===")

                    for period in range(NUM_OF_PERIODS):
                        output.append(
                            f"Period {period + 1}: {table[day][period]}"
                        )

        output.append("\n" + "=" * 50)
        output.append(f"Generated {len(sample_pairs)} valid pair(s).")
        output.append("=" * 50)

        show_result("\n".join(output))

    except ValueError:
        show_result("Please enter valid numbers in all number fields.")
    except Exception as error:
        show_result(f"An error occurred: {error}")


# ==========================================
# FUNCTION: CHECK TIMETABLE RULES
# ==========================================

def check_rules(table):
    for day in range(6):
        daily_subjects = table[day]

        # Rule 1: No same subject consecutively.
        for period in range(1, NUM_OF_PERIODS):
            if daily_subjects[period] == daily_subjects[period - 1]:
                return False

        # Count subjects for the day.
        subject_count = {}

        for subject in daily_subjects:
            if subject not in subject_count:
                subject_count[subject] = 0
            subject_count[subject] += 1

        # Rule 2: Maximum subject occurrences per day.
        for subject in subject_count:
            if subject_count[subject] > MAX_SUBJECTS_PER_DAY:
                return False

    return True


# ==========================================
# FUNCTION: GENERATE ONE TIMETABLE
# ==========================================

def generate_timetable():
    for attempt in range(MAX_ATTEMPTS):
        shuffled_pool = subject_pool.copy()
        r.shuffle(shuffled_pool)

        test_table = []
        index = 0

        for day in range(6):
            test_table.append([])

            for period in range(NUM_OF_PERIODS):
                test_table[day].append(shuffled_pool[index])
                index += 1

        if check_rules(test_table):
            return test_table

    return None


# ==========================================
# FUNCTION: CHECK TWO SAMPLES
# ==========================================

def check_pair(sample1, sample2):
    for day in range(6):
        for period in range(NUM_OF_PERIODS):
            if sample1[day][period] == sample2[day][period]:
                return False

    return True
