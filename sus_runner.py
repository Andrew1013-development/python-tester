import os
import time
import file_generator
import file_copier
import file_seeker
import file_sorter
import file_remover
import file_sorter_2
import file_remover_2

__version__ = "1.1.0"

def runner(directory1, directory2, dates, debug_short, debug_full):
    if debug_short or debug_full:
        print("----------INFORMATION----------")
        print(f"testing directory 1 (test set 1): {directory1}")
        print(f"testing directory 2 (test set 2): {directory2}")    
        print(f"short debug flag: {debug_short}")
        print(f"full debug flag: {debug_full}")
        print(f"folders count: {dates}")
        print()

    #generate 2 test folders
    if debug_short or debug_full:
        print("----------GENERATOR RUNNING----------")
    generator_time,num_files = file_generator.generator(directory1,debug_short,dates,debug_full)
    if debug_short or debug_full:
        print("----------COPIER RUNNING----------")
    copier_time = file_copier.copier(directory1,directory2,debug_short,debug_full)

    #main code for old modules
    start_old = time.time()
    if debug_short or debug_full:
        print("----------OLD SORTER RUNNING----------")
    sorter_time = file_sorter.sorter(directory1,debug_short,debug_full)
    if debug_short or debug_full:
        print("----------OLD REMOVER RUNNING----------")
    remover_time = file_remover.reporter(directory1,debug_short,debug_full)
    end_old = time.time()

    execution_time_old = end_old - start_old 
    delta_time_old = execution_time_old - (sorter_time + remover_time)

    #main code for new modules
    start_new = time.time()
    if debug_short or debug_full:
        print("----------SEEKER RUNNING----------")
    seeker_time, filepath_list = file_seeker.seeker(directory2,debug_short,debug_full)
    if debug_short or debug_full:
        print("----------NEW SORTER RUNNING----------")
    sorter_time_2, filepath_list_sorted = file_sorter_2.sorter(filepath_list, directory2, debug_short,debug_full)
    if debug_short or debug_full:
        print("----------NEW REMOVER RUNNING----------")
    remover_time_2 = file_remover_2.remover(filepath_list_sorted, directory2, debug_short,debug_full)
    end_new = time.time()

    execution_time_new = end_new - start_new 
    delta_time_new = execution_time_new - (sorter_time_2 + remover_time_2 + seeker_time)

    print("----------------------------EXECUTION INFORMATION (OLD MODULES)---------------------------")
    print(f"Total time to execute all 2 functions (runner time): {round(execution_time_old,3)} seconds")
    print(f"Individual time of each segment (individual function time):")
    print(f"\tSorter: {round(sorter_time,3)} seconds ({round(sorter_time / (execution_time_old) * 100,3)}% of runtime)")
    print(f"\tRemover: {round(remover_time,3)} seconds ({round(remover_time / (execution_time_old) * 100,3)}% of runtime)")
    print(f"Time dilation (delta): {round(delta_time_old,3)} seconds ({round(delta_time_old / execution_time_old * 100,3)}% of runtime)")

    print("----------------------------EXECUTION INFORMATION (NEW MODULES)---------------------------")
    print(f"Total time to execute all 3 functions (runner time): {round(execution_time_new,3)} seconds")
    print(f"Individual time of each segment (individual function time):")
    print(f"\tSeeker: {round(seeker_time,3)} seconds ({round(seeker_time / execution_time_new * 100,3)}% of runtime)")
    print(f"\tSorter: {round(sorter_time_2,3)} seconds ({round(sorter_time_2 / execution_time_new * 100,3)}% of runtime)")
    print(f"\tRemover: {round(remover_time_2,3)} seconds ({round(remover_time / execution_time_new * 100,3)}% of runtime)")
    print(f"Time dilation (delta): {round(delta_time_new,3)} seconds ({round(delta_time_new / execution_time_new * 100,3)}% of runtime)")

try:
    n = int(input("How many times to run: "))
    for i in range(1,n+1):
        runner(directory1=r"Z:\test-simulator\test1",directory2=r"Z:\test-simulator\test2",dates=i,debug_short=False,debug_full=False)
        print()
except KeyboardInterrupt:
    file_remover.remover(r"Z:\test-simulator\test1",False,False)
    file_remover.remover(r"Z:\test-simulator\test2",False,False)