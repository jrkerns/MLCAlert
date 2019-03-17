# Copyright 2019 James Kerns

VERSION = '1.0'  # major.patch

from datetime import datetime, timedelta
import os
import os.path as osp

import numpy as np
import pylinac
import yagmail

# **************FILL IN THE FOLLOWING*************************
LOG_FOLDER = r'path/to/log/folder'
MACHINE_NAME = 'TrueBeam 1'

LEAF_DEVIATION_THRESHOLD_MM = 0.1
LEAF_DEVIATION_NUMBER_PER_DAY = 10

ANALYSIS_WINDOW_DAYS = 10
DAYS_WITH_DEVIATIONS_WITHIN_WINDOW = 1


GMAIL_UN = 'mythrowaway@gmail.com'
GMAIL_PW = 'mypassword'
RECIPIENTS = [
    'recipient1@gmail.com',
    'recipient2@gmail.com'
]

# *****************************************************************

a_leaf_ids = {idx-1: 'A' + str(idx) for idx in range(1, 61)}
b_leaf_ids = {idx+59: 'B' + str(idx) for idx in range(1, 61)}
leaf_ids = {**a_leaf_ids, **b_leaf_ids}


class LeafCounter(dict):

    def __init__(self):
        super().__init__({idx: 0 for idx in range(120)})


def get_logs_from_date(date):
    all_logs = os.listdir(LOG_FOLDER)
    logs_within_window = []
    for log in all_logs:
        time_since_epoch = osp.getctime(osp.join(LOG_FOLDER, log))
        delta_from_date = datetime.fromtimestamp(time_since_epoch) - date
        if delta_from_date.days < 1:
            logs_within_window.append(log)
    return logs_within_window


def get_total_deviations_by_leaf_per_day(log_files):
    leaf_deviations = LeafCounter()
    leaf_over_threshold = LeafCounter()
    # count the number of deviations by summing over all Tlogs for that day
    for log in log_files:
        if pylinac.log_analyzer.is_tlog(osp.join(LOG_FOLDER, log)):
            tlog = pylinac.TrajectoryLog(osp.join(LOG_FOLDER, log))
            for idx, leaf in enumerate(tlog.axis_data.mlc.leaf_axes.values()):
                leaf_deviations[idx] += np.sum(np.abs(leaf.difference) > LEAF_DEVIATION_THRESHOLD_MM / 10)
    # convert the number of deviations to binary based on whether number was > deviation threshold per day
    for idx, num_deviations in leaf_deviations.items():
        if num_deviations > LEAF_DEVIATION_NUMBER_PER_DAY:
            leaf_over_threshold[idx] = 1
    return leaf_over_threshold


# get deviations by analyzing logs day-by-day
today = datetime.today()
deviations_by_date = []
for shift in range(1, ANALYSIS_WINDOW_DAYS):
    date_of_interest = today - timedelta(days=shift)
    log_files_of_interest = get_logs_from_date(date=date_of_interest)
    deviations_by_date.append(get_total_deviations_by_leaf_per_day(log_files_of_interest))

# see if the deviations were above threshold for X deviations in Y days
leaves_flagged = LeafCounter()
for leaf in range(120):
    leaves_flagged[leaf] = sum(date[leaf] for date in deviations_by_date) >= DAYS_WITH_DEVIATIONS_WITHIN_WINDOW

# send email if leaves were flagged
if any(leaves_flagged.values()):
    with yagmail.SMTP(GMAIL_UN, GMAIL_PW) as y:
        subject = f'MLCAlert flagged leaves that may need a motor change on {MACHINE_NAME}'
        contents = [leaf_ids[idx] for idx, leaf in leaves_flagged.items() if leaf]
        y.send(RECIPIENTS, subject=subject, contents=contents)

