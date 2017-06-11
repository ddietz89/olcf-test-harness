#! /usr/bin/env python3
import string

#
# Author: Arnold Tharrington (arnoldt@ornl.gov)
# National Center for Computational Sciences, Scientific Computing Group.
# Oak Ridge National Laboratory
#

class rgt_input_file:

    #These are the entries in the input file.
    test_entry = "test"
    path_to_test_entry = "path_to_tests"
    comment_line_entry = "#"
    harness_task_entry = "harness_task"

    def __init__(self,inputfilename="rgt.input"):
        self.__tests = []
        self.__path_to_tests = ""
        self.__harness_task = []
        self.__inputFileName = inputfilename


        #
        # Read the input file.
        #
        self.__read_file()

    def __read_file(self):
        ifile_obj = open(self.__inputFileName,"r")
        lines = ifile_obj.readlines()
        ifile_obj.close()
        
        for tmpline in lines:

            words = str.split(tmpline)

            #If there are no words, then continue to next line.
            if len(words) == 0:
                continue

            #If this is a comment line, the continue to next line.
            if self.__is_comment_line(words[0]):
                continue

            #Convert the first word to lower case.
            firstword = str.lower(words[0])

            # Parse the line,depending upon what type of entry it is.
            if firstword == rgt_input_file.test_entry:
                # Determine the number of words. If the number of words is 3
                # The we run an indefinite number of times. If the number
                # of words is 4, the we run a definite number of times dictated
                # by the third word.
                app = words[2]
                subtest = words[3]
                nm_iters = -1
                if (len(words) == 4):
                    nm_iters = -1
                elif len(words) == 5:
                    nm_iters = int(words[4])
                self.__tests = self.__tests + [[app,subtest,nm_iters]]
                    
            elif firstword == rgt_input_file.path_to_test_entry:
                self.__path_to_tests = words[2]

            elif firstword == rgt_input_file.harness_task_entry:
                if (len(words) == 3):
                    self.__harness_task = self.__harness_task + [[words[2],None,None]]
                elif (len(words) == 5):
                    self.__harness_task = self.__harness_task + [[words[2],words[3],words[4]]]
            else:
                log_message = "Undefined entry:  " + tmpline
                print(log_message)

    def __is_comment_line(self,word):
        if word[0] == rgt_input_file.comment_line_entry:
            return True
        else:
            return False

    def get_harness_tasks(self):
            return self.__harness_task

    def get_tests(self):
            return self.__tests

    def get_local_path_to_tests(self):
            return self.__path_to_tests