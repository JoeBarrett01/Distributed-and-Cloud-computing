"""Find Vroots with more than 400 visits.
This program will take a CSV data file and output tab-seperated lines of
    Vroot -> number of visits
To run:
    python top_pages_solution.py anonymous-msweb.data
To store output:
    python top_pages_solution.py anonymous-msweb.data > top_pages.out
"""

from mrjob.job import MRJob
import csv


class TopPages(MRJob):

    def mapper(self, line_no, line):
        """Extracts the Vroot that was visited"""
        cell = line.split(",")
        if cell[0] == 'V':
            yield cell[1], ('V',1)
        elif cell[0] == 'A':
            cell[1], ('A', cell[3]) 
        

    def reducer(self, vroot, visit_counts):
        """Sumarizes the visit counts by adding them together.  If total visits
        is more than 400, yield the results"""
        total = 0
        title = ''

        for value in visit_counts_and_title:
            if value[0] == 'V':
                total += value[1]
            elif value[0] == 'A':
                title = value[1]

            yield title, total
        
TopPages.run()