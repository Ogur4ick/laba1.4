import csv
import sys
import numpy as np
import os.path
import statistics
import os
import psutil


class Statistics:
    def __init__(self):
        print("Computing statistical metrics")
        self.csv_path = ''
        self.columns = []  # заголовок
        self.csv_data = []  # строка с регионом
        self.column_data = []  # выбранная колонка (данные)
        self.chosen_region = ''  # выбранный регион
        self.all_regions = set()  # все регионы

        max_memory_usage = 2 * 1024 * 1024 * 1024
        pid = os.getpid()  # API о системных ресурсах
        self.process = psutil.Process(pid)  # информация об используемой оперативной памяти
        self.mem_limit = int(max_memory_usage * 0.5)

    def compute(self):
        self.__get_path()
        self.__select_region()
        self.__read_data()
        self.__get_column_idx()
        self.__calculate_metrics()

    # ------------------------------------------------------------------------------------------------------------------

    def __get_path(self):
        print("Path to file")
        print('The best variant -> /Users/Public/laba1.4/russian_demography.csv')
        self.csv_path = input("Enter path to file: ")
        while not (os.path.exists(self.csv_path)):
            print("There is no such file")
            self.csv_path = input("Enter path to file: ")
        while self.csv_path.find('.csv') == -1:
            print("It is not a csv file")
            self.csv_path = input("Enter file path: ")

    # ------------------------------------------------------------------------------------------------------------------

    def __select_region(self):
        self.__list_all_regions()
        self.chosen_region = input("Enter name of region:")
        while self.chosen_region not in self.all_regions:
            print("There is no region with this name")
            self.chosen_region = input("Enter name of region:")

    def __list_all_regions(self):
        print("Regions:")
        with open(self.csv_path, newline='') as file:
            csv_reader = csv.reader(file, delimiter=",")
            next(csv_reader)
            for row in csv_reader:
                mem_usage = self.process.memory_info().rss  # реальное использование оперативной памяти
                if mem_usage >= self.mem_limit:
                    raise MemoryError("Troubles with memory")
                self.all_regions.add(row[1])
        self.all_regions = sorted(self.all_regions)
        for ind, region in enumerate(self.all_regions, start=1):
            if ind == 22:
                print("22. Khanty–Mansi Autonomous Okrug – Yugra")
            else:
                print(f'{ind}. {region}')

    # ------------------------------------------------------------------------------------------------------------------
    def __read_data(self):
        print("Chosen region")
        with open(self.csv_path, newline='') as file:
            csv_reader = csv.reader(file, delimiter=",")
            try:
                self.columns = next(csv_reader)
                print(*self.columns)
                for row in csv_reader:
                    mem_usage = self.process.memory_info().rss
                    if mem_usage >= self.mem_limit:
                        raise MemoryError("Troubles with memory")
                    if row[1] == self.chosen_region:
                        self.csv_data.append(row)
                        print(*self.csv_data[-1])
            except csv.Error as error:
                sys.exit(f' path: {self.csv_path}, number of row: {csv_reader.line_num}: error: {error}')

    # ------------------------------------------------------------------------------------------------------------------

    def __get_column_idx(self):
        print('\nNumber of column\n')
        print(*self.columns[2:])
        print(' 1      2          3       4       5')
        print('Choose a metric from 1 to ', len(self.columns) - 2)
        column_idx = input("Enter column number: ")
        while not column_idx.isdigit() or not 0 < int(column_idx) < len(self.columns)-2:
            print(f'Please insert number between 1 and {len(self.columns) - 2}')
            column_idx = input("Enter column number: ")
        column_idx = int(column_idx) + 1
        for row in self.csv_data:
            self.column_data.append(float(row[column_idx]))

    # ------------------------------------------------------------------------------------------------------------------

    def __calculate_metrics(self):
        print(f'Maximum: {max(self.column_data)}')
        print(f'Minimum: {min(self.column_data)}')
        print(f'Median: {statistics.median(self.column_data):.3f}')
        self.display_percentiles()

    def display_percentiles(self):
        for i in range(0, 101, 5):
            percentile_val = np.percentile(self.column_data, i)
            print(f"{i}%: {percentile_val:.2f}", end=" | ")
