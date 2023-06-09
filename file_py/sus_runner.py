import platform
import sys
import time
import subprocess
import file_generator
import file_copier
import file_seeker
import file_sorter
import file_remover
import file_sorter_2
import file_remover_2

platform_flag = platform.platform().split("-")[0]
__version__ = "3.0.0-WIP6"
if platform_flag == "Windows":
    executable_name = "sus_runner_cpp.exe"
else:
    executable_name = "./sus_runner_cpp.out"

def sus_runner(directory1, directory2, directory3, debug_short, debug_full, dates):
    print("----------INFORMATION----------")
    print(f"testing directory 1 (test set 1): {directory1}")
    print(f"testing directory 2 (test set 2): {directory2}")
    print(f"testing directory 3 (test set 3): {directory3}")    
    print(f"short debug flag: {debug_short}")
    print(f"full debug flag: {debug_full}")
    print(f"folders count: {dates}")
    print()

    #generate 2 test folders
    print("----------GENERATOR RUNNING----------")
    generator_time,num_files = file_generator.generator(directory1,debug_short,dates,debug_full)
    print("----------COPIER RUNNING----------")
    file_copier.copier(directory1,directory2,debug_short,debug_full)
    file_copier.copier(directory1,directory3,debug_short,debug_full)

    #main code for old modules
    start_old = time.time()
    print("----------OLD SORTER RUNNING----------")
    sorter_time = file_sorter.sorter(directory1,debug_short,debug_full)
    print("----------OLD REMOVER RUNNING----------")
    remover_time = file_remover.reporter(directory1,debug_short,debug_full)
    end_old = time.time()

    execution_time_old = end_old - start_old 
    delta_time_old = execution_time_old - (sorter_time + remover_time)

    #main code for new modules
    start_new = time.time()
    print("----------SEEKER RUNNING----------")
    seeker_time, filepath_list = file_seeker.seeker(directory2,debug_short,debug_full)
    print("----------NEW SORTER RUNNING----------")
    sorter_time_2, filepath_list_sorted = file_sorter_2.sorter(filepath_list, directory2, debug_short,debug_full)
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
    print(f"Files sorted: {num_files}")
    print()

    print("----------------------------EXECUTION INFORMATION (NEW MODULES)---------------------------")
    print(f"Total time to execute all 3 functions (runner time): {round(execution_time_new,3)} seconds")
    print(f"Individual time of each segment (individual function time):")
    print(f"\tSeeker: {round(seeker_time,3)} seconds ({round(seeker_time / execution_time_new * 100,3)}% of runtime)")
    print(f"\tSorter: {round(sorter_time_2,3)} seconds ({round(sorter_time_2 / execution_time_new * 100,3)}% of runtime)")
    print(f"\tRemover: {round(remover_time_2,3)} seconds ({round(remover_time / execution_time_new * 100,3)}% of runtime)")
    print(f"Time dilation (delta): {round(delta_time_new,3)} seconds ({round(delta_time_new / execution_time_new * 100,3)}% of runtime)")
    print(f"Files sorted: {num_files}")
    print()
    
    if debug_short:
        debug_short_converted = "-debug"
    else: 
        debug_short_converted = "-nodebug"
    if debug_full:
        debug_full_converted = "-fulldebug"
    else:
        debug_full_converted = "-nofulldebug"
    
    cpp_process = subprocess.Popen([executable_name,dir3,debug_short_converted,debug_full_converted,str(dates)],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    cpp_process_out = cpp_process.communicate()
    lines = cpp_process_out[0].strip().splitlines()
    for line in lines:
        print(line.decode("utf-8"))

if __name__ == "__main__" :
    dbg_flag = False
    fulldbg_flag = False

    if len(sys.argv) == 7:
        dir1 = sys.argv[1]
        dir2 = sys.argv[2]
        dir3 = sys.argv[3]
        if sys.argv[4] == "-debug":
            dbg_flag = True
        elif sys.argv[4] == "-nodebug":
            dgb_flag = False
        else :
            print("oh you gay for debug flag")
        if sys.argv[5] == "-fulldebug":
            fulldbg_flag = True
        elif sys.argv[5] == "-nofulldebug":
            fulldbg_flag = False
        else:
            print("oh another gay")
        n_dates = int(sys.argv[6])
        sus_runner(dir1, dir2, dir3, dbg_flag, fulldbg_flag, n_dates)