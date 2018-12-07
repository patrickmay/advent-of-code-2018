#!/usr/bin/env python3

import sys
from collections import defaultdict

# Solution to part 2 of the day 7 puzzle from Advent of Code 2018.
# https://adventofcode.com/2018/day/7

def parse_steps(filename):
    """
    Read each line of FILENAME and return a dict where the key is the
    step and the value is a list of prerequisite steps.
    """
    steps = defaultdict(lambda: list())
    all_steps = set()
    with open(filename) as f:
        for line in f:
            words = line.split(' ')
            steps[words[7]].append(words[1])
            all_steps.add(words[1])

    # Add steps with no prerequisites.
    for step in all_steps:
        if step not in steps:
            steps[step] = []

    return steps


def available_steps(steps):
    """ Return a list of steps in STEPS with no prerequisites. """
    return {step for step in steps if len(steps[step]) == 0}


class Worker:
    def __init__(self):
        self.current_job = None
        self.job_completion = None

    def jobDone(self,seconds):
        return seconds >= self.job_completion

    def assignJob(self,job,eta):
        self.current_job = job
        self.job_completion = eta

    def reset(self):
        self.current_job = None
        self.job_completion = None
        

def remove_prerequisite(steps,prerequisite):
    """
    Return a copy of STEPS with PREREQUISITE removed from both the keys
    and lists of values.
    """
    next_steps = defaultdict(lambda: list())
    for step in steps:
        if step != prerequisite:
            next_steps[step] = [prereq for prereq in steps[step]
                                if prereq != prerequisite]

    return next_steps

    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        steps = parse_steps(sys.argv[1])
        completed = ''
        jobs_in_progress = set()
        jobs_pending = available_steps(steps)
        workers = [Worker() for i in range(5)]
        time = 0
        while jobs_in_progress or jobs_pending:
            #print(jobs_in_progress)
            #print(jobs_pending)
            for worker in workers:
                if worker.current_job is not None and worker.jobDone(time):
                    jobs_in_progress.remove(worker.current_job)
                    steps = remove_prerequisite(steps,worker.current_job)
                    completed += worker.current_job
                    jobs_pending = available_steps(steps) - jobs_in_progress
                    worker.reset()

            for worker in workers:
                if worker.current_job is None and jobs_pending:
                    next_job = min(jobs_pending)
                    duration = 60 + ord(next_job) - ord('A') + 1
                    jobs_pending.remove(next_job)
                    worker.assignJob(next_job,time + duration)
                    jobs_in_progress.add(next_job)
                    print("Assigned job " + next_job + " at time " + str(time))

            time += 1

        print("Completed in " + str(time) + " seconds.")
        print(completed)
    else:
        print("Usage:  " + sys.argv[0] + " <data-file>")
