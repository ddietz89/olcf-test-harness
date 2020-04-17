#! /usr/bin/env python3
import string
import os
import configparser

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

    def __init__(self,inputfilename="rgt.input", configfilename="master.ini", runmodecmd=None):
        self.__tests = []
        self.__harness_task = []
        self.__path_to_tests = ""
        self.__inputFileName = inputfilename
        self.__configFileName = configfilename

        # Read the master config file
        self.__read_config()

        # Read the input file.
        self.__read_file()

        # If a CLI task was input use that instead
        if runmodecmd != None:
            print("Overriding tasks in inputfile since CLI mode was provided")
            print("runmodecmd = ", runmodecmd)
            modetasklist = runmodecmd.split(",")
            print("modetasklist = ", modetasklist)
            self.__harness_task = []
            for modetask in modetasklist:
                if modetask == "checkout":
                    runmodetask = ["check_out_tests",None,None]
                elif modetask == "start":
                    runmodetask = ["start_tests",None,None]
                elif modetask == "stop":
                    runmodetask = ["stop_tests",None,None]
                elif modetask == "status":
                    runmodetask = ["display_tests",None,None]
                else:
                    runmodetask = None
                    print("Found invalid task in the command line: ", modetask)

                # Append task to this harness instance
                if runmodetask != None:
                    self.__harness_task.append(runmodetask)
                    print("self.__harness_task: ", self.__harness_task)
                
                # Clear mode to avoid duplicate
                runmodetask = None

        if self.__harness_task == []:
            print("ERROR: No valid tasks found in the inputfile or the CLI")

    def __read_config(self):
        if os.path.isfile(self.__configFileName):
            print("reading master config")
            master_cfg = configparser.ConfigParser()
            master_cfg.read(self.__configFileName)

            machine_vars = master_cfg['MachineDetails']
            repo_vars = master_cfg['RepoDetails']
            testshot_vars = master_cfg['TestshotDefaults']

            self.set_rgt_env_vars(machine_vars)
            self.set_rgt_env_vars(repo_vars)
            self.set_rgt_env_vars(testshot_vars)

            #print(os.environ.get("RGT_MACHINE_NAME"))
            #print(os.environ.get("RGT_ACCT_ID"))
        

    def __read_file(self):
        ifile_obj = open(self.__inputFileName,"r")
        lines = ifile_obj.readlines()
        ifile_obj.close()
        
        for tmpline in lines:

            #If this is a comment line, the continue to next line.
            if self.__is_comment_line(tmpline):
                continue

            words = str.split(tmpline)

            #If there are no words, then continue to next line.
            if len(words) == 0:
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
                if len(words) == 5:
                    nm_iters = int(words[4])
                elif len(words) > 5:
                    log_message = "Invalid number of words in test line: " + tmpline
                    print(log_message)
                self.__tests.append([app,subtest,nm_iters])
                    
            elif firstword == rgt_input_file.path_to_test_entry:
                if (len(words) == 3):
                    self.__path_to_tests = words[2]
                elif len(words) > 3:
                    log_message = "Invalid number of words in path line: " + tmpline
                    print(log_message)

            elif firstword == rgt_input_file.harness_task_entry:
                if (len(words) == 3):
                    self.__harness_task.append([words[2],None,None])
                elif (len(words) == 5):
                    self.__harness_task.append([words[2],words[3],words[4]])
                else:
                    log_message = "Invalid number of words in task line: " + tmpline
                    print(log_message)
            else:
                log_message = "Invalid line: " + tmpline
                print(log_message)

    def __is_comment_line(self,word):
        if word[0] == rgt_input_file.comment_line_entry:
            return True
        else:
            return False

    def set_rgt_env_vars(self,env_vars):
        for k in env_vars:
            envk = "RGT_" + str.upper(k)
            v = env_vars[k]

            if envk in os.environ:
                print(envk + " is already set. Skipping.")
            else:
                os.environ[envk] = v

    def get_harness_tasks(self):
            return self.__harness_task

    def get_tests(self):
            return self.__tests

    def get_local_path_to_tests(self):
            return self.__path_to_tests
